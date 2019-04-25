import urwid
import time
import sys
from random import randint

class View():

    def __init__(self):
        self.view = self.setup_view(self.default_widgets())
    
    def keyboard(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        return key

    def setup_view(self, widgets):
        return urwid.ListBox(urwid.SimpleFocusListWalker(widgets))

    def default_widgets(self):
        body = urwid.Text(u'INIT', align='center')
        return [body]

    def mount_widgets(self):
        header = urwid.Text(u'TEXT', align='center')
        _timer_text = urwid.BigText(str(randint(1,50)), urwid.Thin3x3Font())
        body = urwid.Padding(_timer_text, width='clip', align='center')
        footer = urwid.Text(u'TEXT', align='center')
        return [header, body, footer]

    def refresh(self, loop, param):
        self.view = self.setup_view(self.mount_widgets())
        loop.widget = self.view
        loop.set_alarm_in(1, self.refresh)


screen = View()
loop = urwid.MainLoop(screen.view, unhandled_input=screen.keyboard)
loop.set_alarm_in(1, screen.refresh, user_data=None)
loop.run()