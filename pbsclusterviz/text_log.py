from vtk import vtkTextProperty, vtkTextActor
import time

class TextLog(object):
    def __init__(self, clusterviz_config):
        #First log entry
        self.time = [time.strftime("%H:%M:%S")]
        self.log = ["Initialisation"]
        self.config_parser = clusterviz_config.get_config_parser()
        if self.config_parser.has_section("log"):
            if self.config_parser.has_option("log", "log_pos_h"):
                self.log_pos_h = self.config_parser.getfloat("log", "log_pos_h")
            else:
                self.log_pos_h = 0.99
            if self.config_parser.has_option("log", "log_pos_v"):
                self.log_pos_v = self.config_parser.getfloat("log", "log_pos_v")
            else:
                self.log_pos_v = 0.01
            if self.config_parser.has_option("log", "max_log_lines"):
                self.max_log_lines = self.config_parser.getint("log", "max_log_lines")
            else:
                self.max_log_lines = 12
        else:
            self.log_pos_h = 0.99
            self.log_pos_v = 0.01
            self.max_log_lines = 12

        txt = self.get_log_txt()
        self.log_actor = vtkTextActor()
        self.log_actor.SetInput(txt)
        text_prop = self.log_actor.GetTextProperty()
        text_prop.SetJustification(2)
        log_position = self.log_actor.GetPositionCoordinate()
        log_position.SetCoordinateSystemToNormalizedDisplay()
        log_position.SetValue(self.log_pos_h, self.log_pos_v)

    def get_log(self):
        return self

    def add_to_log(self, log_message):
        #Updating... only needs to appear once but with correct Timestamp.
        if log_message== "Updating ...":
            log_line_index = 0
            for log_line in self.log:
                if log_line == "Updating ...":
                    self.time[log_line_index] = time.strftime("%H:%M:%S")
                log_line_index += 1

        #For everything else we want to see the time of the first appearance.
        for log_line in self.log:
            if log_message == log_line:
                return
        self.time.append(time.strftime("%H:%M:%S"))
        self.log.append(log_message)

    def get_log_actor(self):
        return self.log_actor

    def get_log_txt(self):
        if self.config_parser.has_option("log", "show_overloaded"):
            show_overloaded = self.config_parser.getboolean("log", "show_overloaded")
        else:
            show_overloaded = True
        if self.config_parser.has_option("log", "show_imbalance"):
            show_imbalance = self.config_parser.getboolean("log", "show_imbalance")
        else:
            show_imbalance = True
        log_to_print = []
        log_line_index = len(self.log)-1
        for log_line in reversed(self.log):
            if ("overloaded" in log_line and show_overloaded) or \
                ("imbalance" in log_line and show_imbalance) or \
                "Updating" in log_line or "Initialisation" in log_line:
                log_to_print.append(log_line + " - " + self.time[log_line_index] + "\n")
            log_line_index -= 1
        txt = "".join(sorted(log_to_print[0:self.max_log_lines]))
        return txt

    def synch(self):
        self.log_actor.SetInput(self.get_log_txt())

# vim: expandtab shiftwidth=4:
