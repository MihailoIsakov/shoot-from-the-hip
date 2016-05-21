# -*-coding:utf-8-*-
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix


class CommentDataset(object):

    def __init__(self, comments_train, labels_train, comments_test, labels_test):
        """
        Setup training and test sets.
        Should check if labels are numpy arrays, and cast them if needed.
        """
        self.vectorizer = None

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

    def vectorize_fit(self, min_count=2, ngram_range=2):
        """
        Fit the vectorizer to the training set,
        transform the test set
        """
        croatian_stop_words = set([u"a",u"ako",u"ali",u"bi",u"bih",u"bila",u"bili",u"bilo",u"bio",u"bismo",u"biste",u"biti",u"bumo",u"da",u"do",u"duž",u"ga",u"hoće",u"hoćemo",u"hoćete",u"hoćeš",u"hoću",u"i",u"iako",u"ih",u"ili",u"iz",u"ja",u"je",u"jedna",u"jedne",u"jedno",u"jer",u"jesam",u"jesi",u"jesmo",u"jest",u"jeste",u"jesu",u"jim",u"joj",u"još",u"ju",u"kada",u"kako",u"kao",u"koja",u"koje",u"koji",u"kojima",u"koju",u"kroz",u"li",u"me",u"mene",u"meni",u"mi",u"mimo",u"moj",u"moja",u"moje",u"mu",u"na",u"nad",u"nakon",u"nam",u"nama",u"nas",u"naš",u"naša",u"naše",u"našeg",u"ne",u"nego",u"neka",u"neki",u"nekog",u"neku",u"nema",u"netko",u"neće",u"nećemo",u"nećete",u"nećeš",u"neću",u"nešto",u"ni",u"nije",u"nikoga",u"nikoje",u"nikoju",u"nisam",u"nisi",u"nismo",u"niste",u"nisu",u"njega",u"njegov",u"njegova",u"njegovo",u"njemu",u"njezin",u"njezina",u"njezino",u"njih",u"njihov",u"njihova",u"njihovo",u"njim",u"njima",u"njoj",u"nju",u"no",u"o",u"od",u"odmah",u"on",u"ona",u"oni",u"ono",u"ova",u"pa",u"pak",u"po",u"pod",u"pored",u"prije",u"s",u"sa",u"sam",u"samo",u"se",u"sebe",u"sebi",u"si",u"smo",u"ste",u"su",u"sve",u"svi",u"svog",u"svoj",u"svoja",u"svoje",u"svom",u"ta",u"tada",u"taj",u"tako",u"te",u"tebe",u"tebi",u"ti",u"to",u"toj",u"tome",u"tu",u"tvoj",u"tvoja",u"tvoje",u"u",u"uz",u"vam",u"vama",u"vas",u"vaš",u"vaša",u"vaše",u"već",u"vi",u"vrlo",u"za",u"zar",u"će",u"ćemo",u"ćete",u"ćeš",u"ću",u"što"])

        # build tf-idf vectorizer which uses unigrams and bigrams.
        # uses words with 2+ occurances as features
        self.vectorizer = TfidfVectorizer(
            strip_accents="unicode",
            lowercase=True,
            ngram_range=(1, ngram_range),
            min_df=min_count,
            norm='l2',
            smooth_idf=True,
            use_idf=True,
            stop_words=croatian_stop_words)

        # vectorize the text, convert to dense matrix
        self.X_train = self.vectorizer.fit_transform(self._comments_train)
        self.X_test = self.vectorizer.transform(self._comments_test)

    def vectorize_transform(self, comments):
        """
        Vectorize the comments with the fitted vectorizer
        """
        return self.vectorizer.transform(comments)

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

    def __init__(self, comments):
        """
        A dataset containing only unlabeled comments, and their vectors.
        Relies on an outside vectorizer to create vectors.
        Contains 
        """
        self._comments = comments
        self.X = None

    def vectorize_transform(self, vectorizer):
        self.X = vectorizer.transform(self._comments)
        return self.X
