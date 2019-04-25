import urwid
import time
from random import randint

palette = [
        ('body',         'black',      'light gray', 'standout'),
        ('header',       'white',      'dark red',   'bold'),
        ('pg normal',    'white',      'black', 'standout'),
        ('pg complete',  'white',      'dark magenta'),
]

class View():

    def __init__(self):
        self.view = self.setup_view(self.default_widgets())
        self.progress_bar = EmptyProgressBar('pg normal', 'pg complete', 0, 60)
    
    def keyboard(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        return key

    def setup_view(self, widgets):
        return urwid.ListBox(urwid.SimpleFocusListWalker(widgets))

    def default_widgets(self):
        body = urwid.Text(u'INIT', align='center')
        return [body]

    def widget_progress_bar(self, value):
        self.progress_bar.set_completion(value)
        return self.progress_bar

    def widget_timer_text(self, value):
        tt = urwid.BigText(str(value), urwid.Thin3x3Font())
        return tt

    def mount_widgets(self):
        header = urwid.Text(u'TEXT', align='center')
        _timer_text = urwid.BigText(str(randint(1,50)), urwid.Thin3x3Font())

        body_num = urwid.Padding(self.widget_timer_text(randint(1,50)), 
                                 width='clip', 
                                 align='center')

        body_bar = urwid.Padding(self.widget_progress_bar(randint(1,50)), 
                                 width=('relative', 70), 
                                 align='center')

        footer = urwid.Text(u'TEXT', align='center')
        return [header, urwid.Divider(), body_num, body_bar, urwid.Divider(), footer]

    def refresh(self, loop, user_data=None):
        self.view = self.setup_view(self.mount_widgets())
        loop.widget = self.view
        loop.set_alarm_in(1, self.refresh)

class EmptyProgressBar(urwid.ProgressBar):
    def get_text(self):
        return u''

class Timer():

    def __init__(self, timer_name="unamed",
                 set_size=4, 
                 pom_time=1500, 
                 short_rest=300, 
                 long_rest=1800):

        self.timer_name= timer_name
        self.set_size = set_size
        self.pom_time = pom_time
        self.short_rest = short_rest
        self.long_rest = long_rest

if __name__ == "__main__":
    app = View()
    main_view = app.view
    keyboard_callback = app.keyboard
    loop_callback = app.refresh
    initialization_time = 1

    loop = urwid.MainLoop(main_view, palette, unhandled_input=keyboard_callback)
    loop.set_alarm_in(initialization_time, loop_callback)
    loop.run()
