import html
import re


HTML_TAGS = ("<a", "<abbr", "<acronym", "<address", "<area", "<article",
             "<aside", "<audio", "<b", "<base", "<bdi", "<bdo", "<big",
             "<blockquote", "<body", "<br", "<button", "<canvas", "<caption",
             "<center", "<cite", "<code", "<col", "<colgroup", "<data",
             "<datalist", "<dd", "<del", "<details", "<dfn", "<dialog",
             "<dir", "<div", "<dl", "<dt", "<em", "<embed", "<fieldset",
             "<figcaption", "<figure", "<font", "<footer", "<form", "<frame",
             "<frameset", "<h1", "<head", "<header", "<hgroup", "<hr",
             "<html", "<i", "<iframe", "<image", "<img", "<input", "<ins",
             "<kbd", "<label", "<legend", "<li", "<link", "<main", "<map",
             "<mark", "<marquee", "<menu", "<menuitem", "<meta", "<meter",
             "<nav", "<nobr", "<noembed", "<noframes", "<noscript", "<object",
             "<ol", "<optgroup", "<option", "<output", "<p", "<param",
             "<picture", "<plaintext", "<portal", "<pre", "<progress", "<q",
             "<rb", "<rp", "<rt", "<rtc", "<ruby", "<s", "<samp", "<script",
             "<section", "<select", "<slot", "<small", "<source", "<span",
             "<strike", "<strong", "<style", "<sub", "<summary", "<sup",
             "<table", "<tbody", "<td", "<template", "<textarea", "<tfoot",
             "<th", "<thead", "<time", "<title", "<tr", "<track", "<tt", "<u",
             "<ul", "<var", "<video", "<wbr", "<xmp")
OPENTAG = re.compile(r'<([a-zA-Z]+)\s*[^>]*>', re.IGNORECASE)
HR = re.compile(r'<hr>', re.IGNORECASE)
BR = re.compile(r'<br>', re.IGNORECASE)


def _remove_html_tags(text):
    """
    Simply remove html tags
    """
    text = HR.sub('\n', text)
    text = BR.sub('\n' + 40 * '-' + '\n', text)
    index = 0

    while True:
        s = OPENTAG.search(text, index)
        if not s:
            break
        s_start, s_end = s.span()
        tag = s.groups()[0].lower()
        t = text[:s_start] + text[s_end:]
        text = t
        index = s_start

        endtagfind = re.compile(r'</\s*%s\s*>' % tag, re.IGNORECASE)
        e = endtagfind.search(text, s_start)
        if not e:
            continue

        e_start, e_end = e.span()
        t = text[:e_start] + text[e_end:]
        text = t

    return html.unescape(text)


def parse(text, parsetype='plain'):
    t = text.lower()
    html = False
    for tag in HTML_TAGS:
        if tag in t:
            html = True
            break
    if html:
        if parsetype == 'plain':
            return _remove_html_tags(text)
        if parsetype == 'dummy':
            return text
    return text
