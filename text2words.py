# -*- coding: utf-8 -*-


def load_text_as_unicode(fpath):
    import codecs
    f = codecs.open(fpath, 'r', 'utf-8')
    return f.read()


def balden2file(text, fname):
    """
    Remove cyrillic comments and balden accents
    """
    text = text.lower()
    text = remove_symbols(text)
    comments = text.split('\n')
    comments = remove_cyrillic_and_accents(comments)

    import codecs
    with codecs.open(fname, 'w', 'utf-8') as f:
        for comment in comments:
            f.write(comment + u"\n")


def remove_symbols(text):
    bad_chars = ['\t', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', '-', '/', ':', ';', '<', '=', '>', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    punctuation = ['.', ',', '?', '!']

    for char in bad_chars:
        print "Processing {}".format(char)
        text = text.replace(char, ' ')

    for char in punctuation:
        print "Processing {}".format(char)
        text = text.replace(char, ' ' + char + ' ')

    return text 


def remove_cyrillic_and_accents(comments, labels=None, remove_accents=True):
    """
    Removes any comment containing any cyrillic letter.
    If labels are provided, removes the coresponding labels.
    If remove_accents is true, removes accents from letter (ć -> c, ž -> z ...)
    """

    def remove_cyrillic_comments(comments, labels, print_perc=True):
        clean_coms = []
        clean_labels = []
        cyrillic = set(u"АаБбВвГгДдЂђЕеЖжЗзИиЈјКкЛлЉљМмНнЊњОоПпРрСсТтЋћУуФфХхЦцЧчЏџШш")
    
        for comment, label in zip(comments, labels):
            if not bool(set(comment).intersection(cyrillic)):
                clean_coms.append(comment)
                clean_labels.append(label)
    
        return clean_coms, clean_labels

    def remove_serbian_accents(comments):
        bald = []
        for comment in comments:
            bald_comment = (comment) \
                .replace(u"ć", u"c") \
                .replace(u"č", u"c") \
                .replace(u"š", u"s") \
                .replace(u"đ", u"dj") \
                .replace(u"ž", u"z")
    
            bald.append(bald_comment)
    
        return bald

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

