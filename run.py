import urwid
import copy

palette = [
        ('body',         'black',      'light gray', 'standout'),
        ('header',       'white',      'dark blue',   'bold'),
        ('pg normal',    'white',      'light gray', 'standout'),
        ('pg complete',  'black',      'dark blue'),
]

UNIT = 60

class View():

    def __init__(self):
        self.view = self.setup_view(self.default_widgets())
        self.progress_bar = EmptyProgressBar('pg normal', 'pg complete', 0, 60)
        self.timer = Timer(timer_name="Working on Task",
                           set_size=3,
                           section_size=1,
                           pom_time=20, 
                           short_rest=3, 
                           long_rest=15)
    
    def keyboard(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        return key

    def setup_view(self, widgets):
        return urwid.ListBox(urwid.SimpleFocusListWalker(widgets))

    def default_widgets(self):
        body = urwid.Text(u'INIT', align='center')
        return [body]

    def end_widgets(self):
        body = urwid.Text(u'END', align='center')
        return [body]

    def widget_progress_bar(self, value):
        self.progress_bar.set_completion(value)
        return self.progress_bar

    def widget_timer_text(self, value):
        tt = urwid.BigText(("header", str(value)), urwid.Thin3x3Font())
        return tt

    def widget_info(self):

        def_sec = self.timer.default_value["section_size"]
        def_set = self.timer.default_value["set_size"]

        din_sec = self.timer.timer_data["actual_section"]
        din_set = self.timer.timer_data["actual_set"]

        fin_sec = "finished" if din_sec > def_sec else str(din_sec)
        fin_set = "finished" if din_set > def_set else str(din_set)

        if(fin_sec == "finished"):
            sections = "SECTION: " + fin_sec
        else:
            sections = "SECTION: " + fin_sec + "/" + str(def_sec)

        if(fin_set == "finished"):
            sets = "SET: " + fin_set
        else:
            sets = "SET: " + fin_set + "/" + str(def_set)
        
        return urwid.Text(sections + " - " + sets, align='center')

    def mount_widgets(self, time):

        header = urwid.Text(self.timer.timer_data["timer_name"], align='center')
        info = self.widget_info()
        body_num = urwid.Padding(self.widget_timer_text(time["min"]), 
                                 width='clip', 
                                 align='center')

        body_bar = urwid.Padding(self.widget_progress_bar(time["secs"]), 
                                 width=('relative', 70), 
                                 align='center')

        footer = urwid.Text(time["text"], align='center')
        return [urwid.Divider(), header, info, urwid.Divider(), body_num, body_bar, urwid.Divider(), footer]

    def refresh(self, loop, user_data=None):
        time = self.timer.run()

        if(time == False):
            self.view = self.setup_view(self.end_widgets())
            loop.widget = self.view
            loop.set_alarm_in(1, self.finish)
        else:
            self.view = self.setup_view(self.mount_widgets(time))
            loop.widget = self.view
            loop.set_alarm_in(1, self.refresh)
            
    def finish(self, loop, user_data=None):
        raise urwid.ExitMainLoop()

class EmptyProgressBar(urwid.ProgressBar):
    def get_text(self):
        return ''

class Timer():

    def __init__(self, timer_name="unamed",
                 set_size=3,
                 section_size=1, 
                 pom_time=20, 
                 short_rest=3, 
                 long_rest=20):

        self.timer_data = {
            "timer_name": timer_name,
            "set_size": set_size,
            "actual_set": 1,
            "section_size": section_size,
            "actual_section": 1,
            "pom_time": {
                "value": (pom_time * UNIT) - 1,
                "text": "Focus on the Task!",
                "min": -1,
                "secs": -1
            },
            
            "short_rest": {
                "value": (short_rest * UNIT) - 1,
                "text": "Short Break and Fixate Concepts",
                "min": -1,
                "secs": -1
            },

            "long_rest": {
                "value": (long_rest * UNIT) - 1,
                "text": "Congrats. Take a Long Break and do Something Nice",
                "min": -1,
                "secs": -1
            }
        }

        self.default_value = copy.deepcopy(self.timer_data)

    def set_time(self, step):
        mins, secs = divmod(self.timer_data[step]["value"], UNIT) 
        self.timer_data[step]["value"] -= 1
        self.timer_data[step]["min"] = mins + 1
        self.timer_data[step]["secs"] = secs + 1

    def run(self):
        if(self.timer_data["actual_section"] <= self.timer_data["section_size"]):
            if(self.timer_data["actual_set"] <= self.timer_data["set_size"]):
                if(self.timer_data["pom_time"]["value"] >= 0):
                    self.set_time("pom_time")
                    return self.timer_data["pom_time"]
                else:
                    if(self.timer_data["short_rest"]["value"] > 0):
                        self.set_time("short_rest")
                    else:
                        self.set_time("short_rest")
                        self.timer_data["actual_set"] += 1
                        self.timer_data["short_rest"]["value"] = self.default_value["short_rest"]["value"]
                        self.timer_data["pom_time"]["value"] = self.default_value["pom_time"]["value"]
                    return self.timer_data["short_rest"]
            else:
                if(self.timer_data["long_rest"]["value"] > 0):
                    self.set_time("long_rest")
                else:
                    self.set_time("long_rest")
                    self.timer_data["actual_section"] += 1
                    self.timer_data["actual_set"] = 1
                    self.timer_data["long_rest"]["value"] = self.default_value["long_rest"]["value"]
                return self.timer_data["long_rest"]
        else:
            return False

if __name__ == "__main__":
    app = View()
    main_view = app.view
    keyboard_callback = app.keyboard
    loop_callback = app.refresh
    initialization_time = 1

    loop = urwid.MainLoop(main_view, palette, unhandled_input=keyboard_callback)
    loop.set_alarm_in(initialization_time, loop_callback)
    loop.run()
