from typing import List, Tuple, Set, Dict

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from features import build_syllable_vocabulary, cap_vocabulary, \
    extract_features, is_long_syllable, DEFAULT_FEATURES
from preprocess import read_syllabified_words, PREPROCESSED_DATA_PATH


def build_vocabulary(syllabified_words: List[List[str]]) -> List[str]:
    vocab_dict = build_syllable_vocabulary(syllabified_words)
    vocab_size = len(vocab_dict)
    print(f'Vocabulary size: {vocab_size}')
    vocabulary = cap_vocabulary(vocab_dict, 10000)

    return vocabulary


def assemble_data(syllabified_words: List[List[str]], vocabulary: List[str],
                  use_features: Set[str]) \
        -> Tuple[List[Dict[str, float]], List[bool], List[str]]:
    featurized_syllables = []
    label_list = []

    print(f'Using features: {list(use_features)}')
    features = set()
    for word in syllabified_words:
        word_syllable_features = extract_features(word, vocabulary,
                                                  use_features)
        featurized_syllables.extend(word_syllable_features)
        label_list.extend([is_long_syllable(syllable) for syllable in word])
        features.update(key for syllable_features in word_syllable_features
                        for key in syllable_features.keys())

    feature_count = len(features)
    print(f'Extracted {feature_count} features '
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
             classifier, features: List[str]):
    predicted_labels = classifier.predict(test_data)
    label_names = ['short', 'long']
    print(classification_report(test_labels, predicted_labels,
                                target_names=label_names))

    if isinstance(classifier, LogisticRegression):
        # log_reg_importances(classifier, features)
        importances = abs(classifier.coef_[0])
    elif isinstance(classifier, RandomForestClassifier) or \
            isinstance(classifier, DecisionTreeClassifier):
        # forest_feature_importances(classifier, features)
        importances = classifier.feature_importances_
    else:
        return

    importances = 100.0 * (importances / importances.max())
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print("Feature ranking:")
    for f in range(min(25, len(features))):
        print(f'{f + 1}. feature {features[indices[f]]} '
              f'({importances[indices[f]]:.3})')


def log_reg_importances(classifier, features):
    importances = abs(classifier.coef_[0])
    # importances = 100.0 * (importances / importances.max())
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print("Feature ranking:")
    for f in range(min(25, len(features))):
        print(f'{f + 1}. feature {features[indices[f]]} '
              f'({importances[indices[f]]})')


def forest_feature_importances(classifier, features):
    importances = classifier.feature_importances_
    indices = np.argsort(importances)[::-1]
    # Print the feature ranking
    print("Feature ranking:")
    for f in range(min(25, len(features))):
        print(f'{f + 1}. feature {features[indices[f]]} '
              f'({importances[indices[f]]})')


if __name__ == '__main__':
    syllabified_words = read_syllabified_words(PREPROCESSED_DATA_PATH)
    vocabulary = build_vocabulary(syllabified_words)
    syl_features, label_list, features = assemble_data(syllabified_words, vocabulary,
                                                       DEFAULT_FEATURES)

    print(f'Hyperparameters: min_samples_split=5, n_estimators=50')
    classifier = RandomForestClassifier(min_samples_split=5, n_estimators=50)

    data, labels = numpyify_data(syl_features, label_list, features)

    train_data, test_data, train_labels, test_labels = \
        train_test_split(data, labels, test_size=0.2)

    classifier.fit(train_data, train_labels)

    evaluate(test_data, test_labels, classifier, features)
