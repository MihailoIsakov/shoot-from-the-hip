# -*- coding: utf-8 -*-
cyrillic = set(u"АаБбВвГгДдЂђЕеЖжЗзИиЈјКкЛлЉљМмНнЊњОоПпРрСсТтЋћУуФфХхЦцЧчЏџШш")


def remove_cyrillic_comments(comments, labels, print_perc=True):
    clean_coms = []
    clean_labels = []

    for comment, label in zip(comments, labels):
        if not bool(set(comment.decode('utf8')).intersection(cyrillic)):
            clean_coms.append(comment)
            clean_labels.append(label)

    return clean_coms, clean_labels


def remove_serbian_accents(comments):
    bald = []
    for comment in comments:
        bald_comment = (comment.decode('utf8')) \
            .replace(u"ć", u"c") \
            .replace(u"č", u"c") \
            .replace(u"š", u"s") \
            .replace(u"đ", u"dj") \
            .replace(u"ž", u"z")

        bald.append(bald_comment)

    return bald


def remove_cyrillic_and_accents(comments, labels=None, remove_accents=True):
    if labels is None:
        _labels = range(len(comments))
    else:
        _labels = labels

    comments, _labels = remove_cyrillic_comments(comments, _labels)
    if remove_accents:
        comments = remove_serbian_accents(comments)

    if labels:
        return comments, _labels
    else:
        return comments
