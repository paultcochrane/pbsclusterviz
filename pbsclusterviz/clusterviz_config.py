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
This class reads in and stores all config data needed to visualize 
the clusters load or job status
"""

import re, ConfigParser, os, sys, logging

class ClustervizConfig(object):
    """
    Class to hold configuration data for the cluster visualisation
    """
    def __init__(self):
        # Set some variables to default values
        self.xml_file = 'pbsnodes.xml'
        self.interactive = True
        self.output_file = "cluster_job_status.png"
        self.output_file_chosen = False
        self.nodes_file = None
        self.config_file = None
        self.config_parser = ConfigParser.RawConfigParser()
        self.display_mode = 'job' # default: display cluster job status
        self.window_width = 1280
        self.window_height = 1024
        self.log_file = None
        # does the user want the visualisation to update itself?
        self.updating = True
        self.logger = logging.getLogger("")
        # does the user want to issue a system call at every update?
        self.syscalling = None

    def find_config_files(self):
        """
        Determines configuration file locations as well as base
        configuration directory and sets the relevant values
        in the ClustervizConfig object

        Configuration files: nodes, clusterviz.conf
        """
        self.logger.debug("Finding the configuration files")

        # find out where the config files are
        pythonpath_elements = []
        pythonpath = os.environ.get('PYTHONPATH')
        config_path = "/etc/pbsclusterviz.d"
        if pythonpath is not None:
            # split the PYTHONPATH on ':' and search for the
            # pbsclusterviz.d directory
            pythonpath_elements = pythonpath.split(':')
            for path in pythonpath_elements:
                # trim off the path to the python site-packages to get
                # the base path
                site_packages_regexp = \
                        re.compile(r'lib\d{0,2}/python\d\.\d/site-packages')
                path = site_packages_regexp.sub('', path)
                test_path = "%s/etc/pbsclusterviz.d" % path
                if os.path.exists(test_path):
                    config_path = test_path
        
                self.logger.debug("path = " + path)
                self.logger.debug("test_path = " + test_path)
                self.logger.debug("config_path = " + config_path)
        
        if self.get_config_file() is None:
            self.set_config_file("%s/clusterviz.conf" % config_path)
        if self.get_nodes_file() is None:
            self.set_nodes_file("%s/nodes" % config_path)
       
        # make sure one can find the config file and the nodes file
        config_file = self.get_config_file()
        if not os.path.exists(config_file):
            self.logger.critical("Unable to find pbsclusterviz configuration file: %s" % \
                    config_file)
            self.logger.critical("Your PYTHONPATH variable should include the location of the")
            self.logger.critical(".../etc/pbsclusterviz.d directory")
            sys.exit(1)
        
        nodes_file = self.get_nodes_file()
        if not os.path.exists(nodes_file):
            self.logger.critical("Unable to find pbsclusterviz nodes file: %s" % nodes_file)
            self.logger.critical("Your PYTHONPATH variable should include the location of the")
            self.logger.critical(".../etc/pbsclusterviz.d directory")
            sys.exit(1)
    
        self.logger.debug("Using nodes file: " + nodes_file)

    def read_config(self):
        """
        Reads the configuration file for pbsclusterviz and stores
        configuration information in the config object
        """
        self.logger.debug("Reading the clusterviz.conf file")
        self.config_parser.read(self.get_config_file())

    def get_xml_file(self):
        """
        Returns the name of the pbsnodes xml file
        """
        return self.xml_file

    def set_xml_file(self, fname):
        """
        Sets the name of the pbsnodes xml file to the given filename

        :param fname: pbsnodes xml filename
        :type fname: string
        """
        self.logger.debug("Setting xml file to: " + fname)
        if os.path.isfile(fname):
            self.xml_file = fname
        else:
            self.logger.critical("XML file invalid: " + fname)

    def is_interactive(self):
        """
        Returns true if interactive mode is set
        """
        return self.interactive

    def set_interactive_mode(self, mode):
        """
        Sets interactive mode on or off

        :param mode: mode for interactive display (either True or False)
        :type mode: boolean
        """
        if mode is True:
            self.interactive = True
            self.logger.debug("Interactive mode on")
        else:
            self.interactive = False
            self.logger.debug("Interactive mode off")

    def set_display_mode(self, display_mode):
        """
        Sets the display mode to the given value

        :param display_mode: the display mode; either 'job' or 'load'
        :type display_mode: string
        """
        self.logger.debug("Display mode set to: " + display_mode)
        self.display_mode = display_mode

    def get_display_mode(self):
        """
        Returns the current display mode setting
        """
        return self.display_mode

    def get_output_file(self, display_mode):
        """
        Returns the output file name depending upon the display mode
        """
        if self.output_file_chosen:
            return self.output_file
        else:
            return "cluster_%s_status.png" % display_mode

    def set_output_file(self, fname):
        """
        Sets the output file to the given filename

        :param fname: filename of the output image file
        :type fname: string
        """
        self.logger.debug("Setting output file to: " + fname)
        self.output_file = fname

    def get_config_parser(self):
        """
        Returns the configuration parser object
        """
        return self.config_parser

    def get_window_width(self):
        """
        Returns the currently configured render window width
        """
        viewer = self.display_mode + ' viewer'
        config_parser = self.get_config_parser()
        if self.config_parser.has_option(viewer, "window_width"):
            self.window_width = config_parser.getint(viewer, 'window_width' )
        else:
            self.window_width = 640
        return self.window_width

    def get_window_height(self):
        """
        Returns the currently configured render window height
        """
        viewer = self.display_mode + ' viewer'
        config_parser = self.get_config_parser()
        if self.config_parser.has_option(viewer, "window_height"):
            self.window_height = config_parser.getint(viewer, 'window_height' )
        else:
            self.window_height = 480
        return self.window_height

    def set_log_file(self, fname):
        """
        Sets the log file to the given filename

        :param fname: filename of the log file
        :type fname: string
        """
        self.log_file = fname

    def get_log_file(self):
        """
        Returns the current log filename
        """
        return self.log_file

    def set_config_file(self, fname):
        """
        Sets the config file to the given filename

        :param fname: filename of the config file
        :type fname: string
        """
        self.logger.debug("Setting config file to: " + fname)
        if os.path.isfile(fname):
            self.config_file = fname
        else:
            self.logger.critical("Config file invalid: " + fname)
        self.read_config()

    def get_config_file(self):
        """
        Returns the current config filename
        """
        return self.config_file

    def set_nodes_file(self, fname):
        """
        Sets the nodes file to the given filename

        :param fname: filename of the nodes file
        :type fname: string
        """
        self.logger.debug("Setting nodes file to: " + fname)
        if os.path.isfile(fname):
            self.nodes_file = fname
        else:
            self.logger.critical("Nodes file invalid: " + fname)

    def get_nodes_file(self):
        """
        Returns the filename of the current nodes file
        """
        return self.nodes_file

    def is_updating(self):
        """
        Return true when the display is updating
        """
        return self.updating

    def set_updating(self, updating):
        """
        Set the updating flag
        """
        self.updating = updating

    def is_syscalling(self):
        """
        Return true if a system call should be used for every update
        """
        return self.syscalling

    def set_syscalling(self, syscalling):
        """
        Set the syscalling flag
        """
        self.syscalling = syscalling

# vim: expandtab shiftwidth=4:
