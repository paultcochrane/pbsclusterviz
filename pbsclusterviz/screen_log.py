# Copyright (C) 2009-2012 Paul Cochrane, Matthias Zach and Marco Reps
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.

"""
An object of this class stores various messages from other
modules and shows them according to configuration.
"""

from vtk import vtkTextActor
import time

class ScreenLog(object):
    """
    Holds data and functions for the text log.
    """
    def __init__(self, clusterviz_config):
        """
        Initialises with a first message, configuration or default values
        and create the first vtk actor.
        """
        # first log entry
        self.time = [time.strftime("%H:%M:%S")]
        self.log = ["Initialisation"]
        self.last_seen = [time.time()]

        # read config file section
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

        # initialise the vtk actor
        txt = self.get_log_txt()
        self.log_actor = vtkTextActor()
        self.log_actor.SetInput(txt)
        text_prop = self.log_actor.GetTextProperty()
        # this seems to be documented nowhere: 2 means right-aligned
        text_prop.SetJustification(2)
        log_position = self.log_actor.GetPositionCoordinate()
        log_position.SetCoordinateSystemToNormalizedDisplay()
        log_position.SetValue(self.log_pos_h, self.log_pos_v)

    def add_to_log(self, log_message):
        """
        Takes all messages from other modules and decides which timestamp
        to show.
        :param log_message: new message to add
        :type fname: string
        """
        log_line_index = 0
        # Updating... only needs to appear once but with correct Timestamp.
        if log_message == "Updating ...":
            for log_line in self.log:
                if log_line == "Updating ...":
                    self.time[log_line_index] = time.strftime("%H:%M:%S")
                    self.last_seen[log_line_index] = time.time()
                    return
                log_line_index += 1
            self.time.append(time.strftime("%H:%M:%S"))
            self.log.append(log_message)
            self.last_seen.append(time.time())
            return
        # For everything else we want to see the time of the first appearance.
        else:
            for log_line in self.log:
                if log_message == log_line:
                    self.last_seen[log_line_index] = time.time()
                    return
                log_line_index += 1
        self.time.append(time.strftime("%H:%M:%S"))
        self.log.append(log_message)
        self.last_seen.append(time.time())

    def get_log_actor(self):
        """
        Provides the log actor for the main program to display.
        Be aware that this might not be the latest version.
        """
        return self.log_actor

    def get_log_txt(self):
        """
        This function returnes a well formatted text log as one string.
        """
        # parsing config options
        if self.config_parser.has_option("log", "show_overloaded"):
            show_overloaded = self.config_parser.getboolean("log", "show_overloaded")
        else:
            show_overloaded = True
        if self.config_parser.has_option("log", "show_imbalance"):
            show_imbalance = self.config_parser.getboolean("log", "show_imbalance")
        else:
            show_imbalance = True
        if self.config_parser.has_option("log", "show_down"):
            show_down = self.config_parser.getboolean("log", "show_down")
        else:
            show_down = True
        if self.config_parser.has_option("main", "update_rate"):
            update_rate = self.config_parser.getfloat("main", "update_rate")
        else:
            update_rate = 60000.0
        # preparing array of log messages
        log_to_print = []
        log_line_index = len(self.log)-1
        for log_line in reversed(self.log):
            # if the message has been sent within one update interval, it is relevant.
            if(time.time() - self.last_seen[log_line_index] < update_rate/1000):
                # filtering messages according to configuration
                if ("overloaded" in log_line and show_overloaded) or \
                    ("imbalance" in log_line and show_imbalance) or \
                    ("down" in log_line and show_down) or \
                    "Updating" in log_line or "Initialisation" in log_line:
                    # merging message, timestamp and new line symbol
                    log_to_print.append(log_line + " - " + self.time[log_line_index] + "\n")
            log_line_index -= 1
        # merging the sorted log array to string
        txt = "".join(sorted(log_to_print[0:self.max_log_lines]))
        # informing user about hidden messages
        if len(log_to_print) > self.max_log_lines:
            txt += "Some messages hidden."
        return txt

    def synch(self):
        """
        Refreshes the vtk actor with latest text output.
        """
        self.log_actor.SetInput(self.get_log_txt())

# vim: expandtab shiftwidth=4:
