# -*- coding: utf-8 -*-


def balden2file(finput, foutput):
    """
    Remove cyrillic comments and balden accents
    """
    def load_text_as_unicode(fpath):
        import codecs
        f = codecs.open(fpath, 'r', 'utf-8')
        return f.read()

    text = load_text_as_unicode(finput)
    text = text.lower()
    text = _remove_symbols(text)
    comments = text.split('\n')
    comments = _remove_cyrillic_and_accents(comments)

    import codecs
    with codecs.open(foutput, 'w', 'utf-8') as f:
        for comment in comments:
            f.write(comment + u"\n")


def _remove_symbols(text):
    bad_chars = ['\t', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', '-', '/', ':', ';', '<', '=', '>', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    punctuation = ['.', ',', '?', '!']

    print("Processing: "),
    for char in bad_chars:
        print(char)
        text = text.replace(char, ' ')

    print("\nProcessing: "),
    for char in punctuation:
        print(char)
        text = text.replace(char, ' ' + char + ' ')

    return text 


def _remove_cyrillic_and_accents(comments, labels=None, remove_accents=True):
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


if __name__=="__main__":
    import sys
    finput = sys.argv[1]
    foutput = sys.argv[2]

    balden2file(finput, foutput)
