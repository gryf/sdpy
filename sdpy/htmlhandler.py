import re
from itertools import pairwise


OPENTAG = re.compile(r'<([a-zA-Z]+)\s*[a-zA-Z0-9=\-:"#]*>', re.IGNORECASE)


def _remove_html_tags(text):
    """
    Simply remove html tags
    """
    text = text.replace('<br>', '\n')
    text = text.replace('<BR>', '\n')
    index = 0

    while True:
        s = OPENTAG.search(text, index)
        if not s:
            break
        s_start, s_end = s.span()
        tag = s.groups()[0].lower()

        endtagfind = re.compile(r'</\s*%s\s*>' % tag, re.IGNORECASE)
        e = endtagfind.search(text, s_end)
        e_start, e_end = e.span()

        index = s_start
        # get rid of the tag
        t = text[:s_start] + text[s_end:e_start] + text[e_end:]
        text = t

    return text


def parse(text, parsetype='plain'):
    t = text.lower()
    if '<font' in t or '<b' in t or '<i' in t or '<span' in t or '<div' in t:
        if parsetype == 'plain':
            return _remove_html_tags(text)
        if parsetype == 'dummy':
            return text
    return text
