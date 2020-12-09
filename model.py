import logging
import sys
from datetime import datetime
from typing import List, Tuple, Set, Dict

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeClassifier

from features import build_syllable_vocabulary, cap_vocabulary, \
    extract_features, is_long_syllable, ALL_FEATURES
from preprocess import read_syllabified_words, PREPROCESSED_DATA_PATH


def build_vocabulary(syllabified_words: List[List[str]]) -> List[str]:
    vocab_dict = build_syllable_vocabulary(syllabified_words)
    vocab_size = len(vocab_dict)
    logging.info(f'Vocabulary size: {vocab_size}')
    vocabulary = cap_vocabulary(vocab_dict, 10000)

    return vocabulary


def assemble_data(syllabified_words: List[List[str]], vocabulary: List[str],
                  use_features: Set[str]) \
        -> Tuple[List[Dict[str, float]], List[bool], List[str]]:
    featurized_syllables = []
    label_list = []

    logging.info(f'Using features: {list(sorted(use_features))}')
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
                  label_list: List[bool], features: List[str]):
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
             classifier):
    predicted_labels = classifier.predict(test_data)
    label_names = ['short', 'long']
    logging.info(classification_report(test_labels, predicted_labels,
                                       target_names=label_names))


def log_feature_importances(classifier, features: List[str]):
    if isinstance(classifier, LogisticRegression):
        # log_reg_importances(classifier, features)
        importances = abs(classifier.coef_[0])
    elif isinstance(classifier, RandomForestClassifier) or \
            isinstance(classifier, DecisionTreeClassifier):
        # forest_feature_importances(classifier, features)
        importances = classifier.feature_importances_
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


if __name__ == '__main__':
    initialize_logging()

    syllabified_words = read_syllabified_words(PREPROCESSED_DATA_PATH)
    vocabulary = build_vocabulary(syllabified_words)
    syl_features, label_list, features = assemble_data(syllabified_words,
                                                       vocabulary,
                                                       ALL_FEATURES)

    classifier = RandomForestClassifier(min_samples_split=5, max_features=5,
                                        n_estimators=50)
    logging.info(f'Classifier type: {classifier.__class__.__name__}')
    logging.info(f'Hyperparameters: min_samples_split=5, max_features=5, '
                 f'n_estimators=50')

    data, labels = numpyify_data(syl_features, label_list, features)

    # Don't hold two copies of the features, free up memory
    del syl_features
    del label_list

    # 5 folds: 80-20 train/test split
    fold_count = 5
    # Only actually train and evaluate on 2 of them
    evaluate_folds = 2
    logging.info(f'K-fold cross-validation with {fold_count} folds, '
                 f'evaluate on {evaluate_folds} of them')
    kf = KFold(n_splits=fold_count, shuffle=True)

    folds = list(kf.split(data, labels))[:evaluate_folds]
    for train_index, test_index in folds:
        train_data, test_data = data[train_index], data[test_index]
        train_labels, test_labels = labels[train_index], labels[test_index]

        classifier.fit(train_data, train_labels)

        evaluate(test_data, test_labels, classifier)

    logging.info('Feature importances for most recent train/test split')
    log_feature_importances(classifier, features)
