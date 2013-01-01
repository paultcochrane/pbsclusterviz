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
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307,
# USA.

"""
File containing the NodeGrid class
"""

from vtk import vtkBalloonWidget, vtkBalloonRepresentation
import sys, re, os, logging
import xml.sax
from pbsclusterviz.node import Node
from pbsclusterviz.node_grid_xml_handler import NodeGridXMLHandler
import tempfile

class NodeGrid(object):
    """
    The NodeGrid class

    :param screen_log: Holds messages to be logged to the screen
    :type screen_log: string
    """
    def __init__(self, screen_log):
        # initialize the class variables:
        self.box_list = []
        self.label_list = []
        self.balloon_widget = vtkBalloonWidget()
        self.node_table = {}
        self.screen_log = screen_log
        self.logger = logging.getLogger("")
   
    def read_nodes_file(self, nodes_file, screen_log):
        """
        Read the nodes file and populate the node grid with Node objects
        """
        fp_node_file = open(nodes_file, "r")
        lines = fp_node_file.readlines()
        fp_node_file.close()
        
        hash_regex = re.compile(r'^#')
        return_regex = re.compile(r'\n')
        for line in lines:
            node_name = ""
            x_pos = 0
            y_pos = 0
            if hash_regex.match(line) or return_regex.match(line):
                pass
            else:
                node_info = line.split(' ', 3)
                node_name = node_info[0]
                x_pos = node_info[1]
                y_pos = node_info[2]
                y_pos = y_pos.replace('\n', '')
        
                node = Node(screen_log)
                node.set_name(node_name)
                node.set_grid_location(x_pos, y_pos)
                self.node_table[node_name] = node

    def get_node_by_name(self, name):
        """
        Returns an instance of Node with the name 'name'
        if it is in the list
        """
        if name in self.node_table.keys():
            return self.node_table[ name ]
        else:
            return None

    def add_new_node(self, node_name):
        """
        Creates an empty Node object with the given name and
        adds it to the node list
        """
        node = Node(self.screen_log)
        node.set_name(node_name)
        self.node_table[node_name] = node

    def get_node_list(self):
        """
        Return the list of nodes currently in the node grid
        """
        self.logger.debug("Getting node list")
        return self.node_table.values()

    def init_boxes(self):
        """
        Initialises each box in the node list and returns the box list
        """
        for node in self.get_node_list():
            self.box_list.append(node)
        return self.box_list

    def init_labels(self):
        """
        Initialises all box labels for nodes in the node list and returns
        the label list
        """
        for node in self.get_node_list():
            label = node.init_label()
            self.label_list.append(label)
        return self.label_list

    def init_balloons(self):
        """
        Initialise the balloon widget with text for each node and return the
        balloon widget
        """
        # prepare the global balloon maintainance for the grid
        balloon_rep = vtkBalloonRepresentation()
        balloon_rep.SetBalloonLayoutToImageRight()
        self.balloon_widget.SetRepresentation(balloon_rep)

        for node in self.get_node_list():
            self.balloon_widget.AddBalloon(node.get_box_actor(), 
                    node.get_balloon_text())
        return self.balloon_widget
    
    def update(self, xml_file, display_mode, node_grid_display):
        """
        The main update routine for the visualization

        :param xml_file:        filename of the output of pbsnodes -x
        :type xml_file:         string

        :param display_mode:    specifies what to visualize (load or job)
        :type display_mode:     string
        """
        # Now collect the data from the pbsnodes-generated XML file
        parser = xml.sax.make_parser()
        handler = NodeGridXMLHandler(self)
        parser.setContentHandler(handler)
        
        if xml_file is not None:
            if not os.path.exists(xml_file):
                self.logger.critical("PBSNodes XML file: '%s' does not exist!" % xml_file)
                sys.exit(1)
            parser.parse(xml_file)
        else:
            self.logger.debug("No xml file given. Trying to get one.")
            xml_file = tempfile.NamedTemporaryFile(dir='/tmp')
            pbsnodes_cmd = "pbsnodes -x"
            error = os.system("%s > %s" % (pbsnodes_cmd, xml_file.name) )
            if error:
                self.logger.critical("Unable to run '%s'.  Exiting." % pbsnodes_cmd)
                sys.exit(1)
            parser.parse(xml_file)

        for node in self.get_node_list():
            node.update_box(display_mode, node_grid_display)
            node.update_label()
            self.balloon_widget.RemoveBalloon(node.get_box_actor())
            self.balloon_widget.AddBalloon(node.get_box_actor(), node.get_balloon_text())
        return

    # restore coplanarity after modifying box height
    def flatten(self):
        """
        Restore coplanarity after modifying box height
        """
        for node in self.get_node_list():
            node.flat()

    def get_job_utilisation(self):
        """
        Return the system utilisation in the job display mode
        """
        total_num_processors = 0
        total_num_jobs = 0
        for node in self.get_node_list():
            # TODO the nodes in the configured node list should be compared
            # with the nodes in the xml output well before reaching here.
            # If this is done, then the following if statement can disappear
            if node.num_processors is None:
                continue
            total_num_processors += int(node.num_processors)
            total_num_jobs += len(node.jobs)
        return float(total_num_jobs) / float(total_num_processors)

    def get_load_utilisation(self):
        """
        Return the system utilisation in the load display mode
        """
        loadavg = 0.0
        total_num_processors = 0
        for node in self.get_node_list():
            if 'loadave' in node.status.keys():
                loadavg += float(node.status['loadave'])
            total_num_processors += node.max_load
        return float(loadavg) / float(total_num_processors)

# vim: expandtab shiftwidth=4:
