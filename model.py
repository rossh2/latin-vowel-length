import logging
import sys
from datetime import datetime
from typing import List, Tuple, Set, Dict

import numpy as np
from seqlearn.evaluation import SequenceKFold
from seqlearn.perceptron import StructuredPerceptron
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from features import build_syllable_vocabulary, cap_vocabulary, \
    extract_features, is_long_syllable, VOCAB_FEATURE, \
    UNK_VOCABULARY, ALL_FEATURES
from preprocess import read_syllabified_words, PREPROCESSED_UNIQUE_DATA_PATH


def build_vocabulary(syllabified_words: List[List[str]], cap_size=10000) \
        -> List[str]:
    vocab_dict = build_syllable_vocabulary(syllabified_words)
    vocab_size = len(vocab_dict)
    logging.info(f'Full vocabulary size: {vocab_size}')
    if cap_size < vocab_size:
        logging.info(f'Capping vocabulary to {cap_size} words (+ unknown)')

    # This converts the vocabulary to a list even if it doesn't need capping
    vocabulary = cap_vocabulary(vocab_dict, cap_size)

    return vocabulary


def assemble_data(syllabified_words: List[List[str]], vocabulary: List[str],
                  use_features: Set[str]) \
        -> Tuple[List[Dict[str, float]], List[bool], List[str]]:
    featurized_syllables = []
    label_list = []

    features = set()
    for word in syllabified_words:
        word_syllable_features = extract_features(word, vocabulary,
                                                  use_features)
        featurized_syllables.extend(word_syllable_features)
        label_list.extend([is_long_syllable(syllable) for syllable in word])
        features.update(key for syllable_features in word_syllable_features
                        for key in syllable_features.keys())

    feature_count = len(features)
    logging.info(f'Extracted {feature_count} features '
                 f'for {len(vocabulary)} syllables in vocabulary')

    return featurized_syllables, label_list, list(features)


def numpyify_data(featurized_syllables: List[Dict[str, float]],
                  label_list: List[bool], features: List[str]) \
        -> Tuple[np.ndarray, np.ndarray]:
    feature_count = len(features)
    feature_arrays = []
    for syllable_features in featurized_syllables:
        feature_array = np.zeros((feature_count,))
        for i, feature in enumerate(features):
            if feature in syllable_features:
                feature_array[i] = syllable_features[feature]
        feature_arrays.append(feature_array)

    data = np.stack(feature_arrays)
    labels = np.array(label_list, dtype=np.int)

    assert len(data) == len(labels)

    return data, labels


def evaluate(test_data: np.ndarray, test_labels: np.ndarray,
             classifier, test_lengths=None):
    if isinstance(classifier, StructuredPerceptron):
        predicted_labels = classifier.predict(test_data, test_lengths)
    else:
        predicted_labels = classifier.predict(test_data)
    label_names = ['short', 'long']
    logging.info(classification_report(test_labels, predicted_labels,
                                       target_names=label_names))


def log_feature_importances(classifier, features: List[str]):
    if hasattr(classifier, 'feature_importances_'):
        importances = classifier.feature_importances_
    elif hasattr(classifier, 'coef_'):
        importances = abs(classifier.coef_[0])
    else:
        logging.warning('Unsupported classifier for feature ranking')
        return

    importances = 100.0 * (importances / importances.max())
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    logging.info("Feature ranking:")
    for f in range(min(25, len(features))):
        logging.info(f'{f + 1}. feature {features[indices[f]]} '
                     f'({importances[indices[f]]:.3f})')
    for f in range(25, min(75, len(features))):
        logging.debug(f'{f + 1}. feature {features[indices[f]]} '
                      f'({importances[indices[f]]:.3f})')


def initialize_logging():
    date = datetime.today().strftime('%Y-%m-%d-%H%M%S')
    logging.basicConfig(filename=f'experiments/{date}.log', filemode='w',
                        format='%(message)s',
                        level=logging.DEBUG)

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)


def prepare_data(use_features: Set[str], data_path: str) \
        -> Tuple[np.ndarray, np.ndarray, List[int], List[str]]:
    logging.info(f'Reading data from path: {data_path}')
    syllabified_words = read_syllabified_words(data_path)
    logging.info(f'Total number of words (train+test): '
                 f'{len(syllabified_words)}')

    feature_string = ', '.join(sorted(use_features))
    logging.info(f'Using features: {feature_string}')
    if VOCAB_FEATURE in use_features:
        vocabulary = build_vocabulary(syllabified_words)
    else:
        vocabulary = UNK_VOCABULARY

    word_lengths = [len(word) for word in syllabified_words]
    # assemble_data flattens all the words into a long list of syllables
    syl_features, label_list, features = assemble_data(syllabified_words,
                                                       vocabulary,
                                                       use_features)
    data, labels = numpyify_data(syl_features, label_list, features)

    # Don't hold two copies of the features, explicitly free up memory
    del syllabified_words
    del vocabulary
    del syl_features
    del label_list

    return data, labels, word_lengths, features


def kfold_train_evaluate(classifier, data: np.ndarray, labels: np.ndarray,
                         word_lengths: List[int], features: List[str],
                         fold_count: int, evaluate_folds: int):
    logging.info(f'K-fold cross-validation with {fold_count} folds, '
                 f'evaluate on {evaluate_folds} of them')

    folds = list(
        SequenceKFold(word_lengths, n_folds=fold_count, shuffle=True)
    )[:evaluate_folds]

    for i, (train_index, train_lengths, test_index, test_lengths) \
            in enumerate(folds):
        logging.info(f'Fold # {i + 1}')

        train_data, test_data = data[train_index], data[test_index]
        train_labels, test_labels = labels[train_index], labels[test_index]

        if isinstance(classifier, StructuredPerceptron):
            classifier.fit(train_data, train_labels, train_lengths)
        else:
            classifier.fit(train_data, train_labels)

        logging.info('Training set performance:')
        evaluate(train_data, train_labels, classifier, train_lengths)

        logging.info('Test set performance:')
        evaluate(test_data, test_labels, classifier, test_lengths)

    logging.info('Feature importances for most recent train/test split')
    log_feature_importances(classifier, features)


if __name__ == '__main__':
    initialize_logging()

    # PREPROCESSED_DATA_PATH or PREPROCESSED_UNIQUE_DATA_PATH
    data_path = PREPROCESSED_UNIQUE_DATA_PATH
    use_features = ALL_FEATURES
    data, labels, word_lengths, features = prepare_data(use_features,
                                                        data_path)

    classifier = RandomForestClassifier(min_samples_split=5, max_features=5,
                                        n_estimators=75)
    logging.info(f'Classifier type: {classifier.__class__.__name__}')
    logging.info(f'Hyperparameters: min_samples_split=5, max_features=5, '
                 f'n_estimators=75')

    # 5 folds: 80-20 train/test split
    fold_count = 5
    # Only actually train and evaluate on some of them
    # (saves time when dataset sufficiently large and all folds are similar)
    evaluate_folds = 3
    kfold_train_evaluate(classifier, data, labels, word_lengths, features,
                         fold_count, evaluate_folds)
