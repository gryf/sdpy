import asyncio

import urwid

from sdpy import htmlhandler
from sdpy import dicthandler
from sdpy import scroll


class ListItem(urwid.WidgetWrap):
    def __init__(self, item):
        self.content = item
        t = urwid.AttrWrap(urwid.Text(item), "item", "item_selected")
        urwid.WidgetWrap.__init__(self, t)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


class ListView(urwid.WidgetWrap):
    def __init__(self):
        urwid.register_signal(self.__class__, ['show_details'])
        self.walker = urwid.SimpleFocusListWalker([])
        self.lb = urwid.ListBox(self.walker)
        urwid.WidgetWrap.__init__(self, self.lb)

    def modified(self):
        walker_focus = self.walker.get_focus()
        if walker_focus:
            focus_w, _ = walker_focus
            if focus_w:
                urwid.emit_signal(self, 'show_details', focus_w.content)

    def set_data(self, items):
        words_widgets = [ListItem(c) for c in items]
        urwid.disconnect_signal(self.walker, 'modified', self.modified)

        while len(self.walker) > 0:
            self.walker.pop()

        self.walker.extend(words_widgets)
        urwid.connect_signal(self.walker, "modified", self.modified)

    def selectable(self):
        return True

    def set_focus(self):
        try:
            self._w.set_focus(0)
        except IndexError:
            return False


class DetailView(urwid.WidgetWrap):
    def __init__(self):
        t = urwid.Text("")
        urwid.WidgetWrap.__init__(self, t)

    def show_item(self, c):
        self._w.set_text(c)

    def selectable(self):
        return True

    def set_focus(self):
        return True

    def keypress(self, size, key):
        return key


class SearchBox(urwid.WidgetWrap):
    def __init__(self):
        self.t = urwid.Edit(caption="Search: ")
        urwid.WidgetWrap.__init__(self, self.t)

    def selectable(self):
        return True


class App(object):

    def unhandled_input(self, key):
        if key in ('esc',):
            raise urwid.ExitMainLoop()
        if key in ('down',):
            if self.frame.focus.base_widget == self.search_box:
                self.frame.focus_position = 'body'
                self.columns.focus_position = 0
                self.list_view.set_focus()
        if key in ('tab',):
            if self.frame.focus.base_widget == self.search_box:
                # move focus in frame from header to the body and select
                # listview
                self.frame.focus_position = 'body'
                self.columns.focus_position = 0
                self.list_view.set_focus()
            elif (self.frame.focus.base_widget.focus
                  .base_widget == self.list_view):
                self.detail_view.set_focus()
                self.columns.focus_position = 1
            else:
                self.frame.focus_position = 'header'
        if key in ('shift tab',):
            if self.frame.focus.base_widget == self.search_box:
                self.frame.focus_position = 'body'
                self.columns.focus_position = 1
                self.detail_view.set_focus()
            elif (self.frame.focus.base_widget.focus
                  .base_widget == self.list_view):
                self.frame.focus_position = 'header'
            else:
                self.frame.focus_position = 'body'
                self.columns.focus_position = 0
                self.list_view.set_focus()

    def show_details(self, item):
        definitions = self.dhandler.get_definition(item)
        if not definitions:
            return
        text = []
        for name in definitions:
            if text:
                text.append(('blue', f'\n\n--- {name} ---\n\n'))
            else:
                text.append(('blue', f'--- {name} ---\n\n'))
            definition = htmlhandler.parse(definitions[name]
                                           .replace('\t', '    '))
            text.append(definition)
        self.detail_view.show_item(text)

    def search_words(self, item, item2):
        words = self.dhandler.match_words(item.get_edit_text())
        self.update_data(words)
        if words:
            self.list_view.set_focus()

    def __init__(self):

        self._focus = 0

        self.palette = {("item_selected", "white", "dark blue"),
                        ("footer", "white, bold", "dark gray"),
                        ("italic", "light gray, italics", "black"),
                        ("bolditalic", "light gray, italics, bold", "black"),
                        ("red", "light red", "black"),
                        ("blueitalic", "light blue, italics", "black"),
                        ("blue", "light blue", "black"),
                        ("green", "light green", "black"),
                        ("cyan", "light cyan", "black")}

        self.list_view = ListView()
        self.detail_view = DetailView()
        self.search_box = SearchBox()

        self.focusable = [self.search_box, self.list_view, self.detail_view]

        urwid.connect_signal(self.list_view, 'show_details', self.show_details)
        urwid.connect_signal(self.search_box.t, 'postchange',
                             self.search_words)

        footer = urwid.AttrWrap(urwid.Text(" ESC to exit"), "footer")

        col_rows = urwid.raw_display.Screen().get_cols_rows()
        h = col_rows[0] - 2

        f1 = urwid.Filler(self.list_view, valign='top', height=h)
        f2 = scroll.ScrollBar(scroll.Scrollable(self.detail_view))

        self.search = urwid.LineBox(self.search_box, title_align="left")
        self.c_list = urwid.LineBox(f1, title="Keywords")

        c_details = urwid.LineBox(f2, title="Definition")

        self.columns = urwid.Columns([('weight', 30, self.c_list),
                                      ('weight', 70, c_details)])

        self.frame = urwid.Frame(body=self.columns, footer=footer,
                                 header=self.search,
                                 focus_part="header")

        evl = urwid.AsyncioEventLoop(loop=asyncio.get_event_loop())
        self.loop = urwid.MainLoop(self.frame, self.palette, event_loop=evl,
                                   unhandled_input=self.unhandled_input)

        self.dhandler = dicthandler.DictHandler()

    def update_data(self, data):
        self.list_view.set_data(data)

    def start(self):
        self.update_data(self.dhandler.keys()[:100])
        self.loop.run()


def main():
    app = App()
    app.start()


if __name__ == '__main__':
    main()
