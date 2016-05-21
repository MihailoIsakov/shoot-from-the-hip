# -*-coding:utf-8-*-
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix


class CommentDataset(object):

    def __init__(self, comments_train, labels_train, comments_test, labels_test):
        """
        Setup training and test sets.
        Should check if labels are numpy arrays, and cast them if needed.
        """
        self._comments_train = comments_train
        self._comments_test = comments_test
        self.X_train = None
        self.X_test = None

        self.y_train = labels_train
        self.y_test = labels_test

        if not isinstance(self.y_train, np.ndarray):
            self.y_train = np.array(labels_train)
        if not isinstance(self.y_test, np.ndarray):
            self.y_test = np.array(labels_test)

    def test_prediction(self, y_pred, set="test", print_options=["accuracy", "precision", "recall"]):
        # round the y predictions if they are probabilites and not classes
        y_pred = np.round(y_pred).astype(np.int)
        y_true = self.y_test if set=="test" else self.y_train

        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        confusion = confusion_matrix(y_true, y_pred)
        values = [accuracy, precision, recall, confusion]

        if "accuracy" in print_options:
            print "\tAccuracy on {} set: {}".format(set, accuracy)
        if "precision" in print_options:
            print "\tPrecision on {} set: {}".format(set, precision)
        if "recall" in print_options:
            print "\tRecall on {} set: {}".format(set, recall)
        if "confusion" in print_options:
            print "\tConfusion matrix on {} set: {}".format(set, confusion)

        return values

    def test_prediction_above(self, y_pred, threshold, set="test", print_options=["accuracy", "precision", "recall"]):
        indices = np.argwhere(np.logical_or(y_pred < 1 - threshold, y_pred > threshold))
        if len(indices) == 0:
            return [np.NaN, np.NaN, np.NaN, [[0, 0], [0, 0]]]

        y_pred = y_pred[indices]
        y_pred = np.round(y_pred).astype(np.int)

        y_true = self.y_test if set=="test" else self.y_train
        y_true = y_true[indices]

        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        confusion = confusion_matrix(y_true, y_pred)
        values = [accuracy, precision, recall, confusion]

        if "accuracy" in print_options:
            print "\tAccuracy on {} set: {}".format(set, accuracy)
        if "precision" in print_options:
            print "\tPrecision on {} set: {}".format(set, precision)
        if "recall" in print_options:
            print "\tRecall on {} set: {}".format(set, recall)
        if "confusion" in print_options:
            print "\tConfusion matrix on {} set: {}".format(set, confusion)

        return values


class UnlabeledDataset(object):
    """
    Dataset containing the scraped comments, their TF-IDF sparse matrix,
    and classified bot comments from the dataset.
    """

    def __init__(self, comments):
        """
        A dataset containing only unlabeled comments, and their vectors.
        Relies on an outside vectorizer to create vectors.
        Contains 
        """
        self.comments = tuple(comments)
        self.bots = None
        self.X = None


class CombinedDataset(object):
    """
    Dataset containing the original comments, scraped comments,
    and comments tagged as not-bots, along with their labels.
    NB classified comments and manually tagged comments have lower weights.
    """

    def __init__(self, lns_comments, lns_labels, bots, nots, weight=0.1):  
        """
        Creates the dataset with the original comments and labels from the training set.
        Adds the bots and nots to the comments, and labels bots with 1s, and nots with 0s.
        """
        self._lns_comments = lns_comments
        self._lns_labels = lns_labels
        self._bots = bots  
        self._nots = nots  

        self._comments = self._lns_comments + bots + nots
        self._labels = list(self._lns_labels) + list(np.ones(len(bots))) + list(np.zeros(len(nots)))
        self._labels = np.array(self.labels)

        self._weights = np.ones(len(self._comments))
        self._weights[len(lns_comments):] = weight

    @property
    def comments(self):
        return self._comments

    @property
    def labels(self):
        return self._labels

    @property
    def weights(self):
        return self._weights
