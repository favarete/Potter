import urwid

def show_or_exit(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    return key

counter = urwid.BigText(('banner', "4"), urwid.Thin3x3Font())

view = urwid.ListBox(urwid.SimpleFocusListWalker([
    urwid.Text(u'TEXT', align='center'),
    urwid.Padding(counter, width='clip', align='center'),
    urwid.Text(u'TEXT', align='center')
]))

loop = urwid.MainLoop(view, unhandled_input=show_or_exit)
loop.run()