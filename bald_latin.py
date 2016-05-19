# -*- coding: utf-8 -*-
cyrillic = set(u"АаБбВвГгДдЂђЕеЖжЗзИиЈјКкЛлЉљМмНнЊњОоПпРрСсТтЋћУуФфХхЦцЧчЏџШш")


def remove_cyrillic_comments(comments, labels, print_perc=True):
    cyrillic_count = 0.0

    clean_coms = []
    clean_labels = []

    for comment, label in zip(comments, labels):
        if not bool(set(comment.decode('utf8')).intersection(cyrillic)):
            clean_coms.append(comment)
            clean_labels.append(label)
        else:
            cyrillic_count += 1

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
        labels = range(len(comments))

    comments, labels = remove_cyrillic_comments(comments, labels)
    if remove_accents:
        comments = remove_serbian_accents(comments)

    return comments, labels
