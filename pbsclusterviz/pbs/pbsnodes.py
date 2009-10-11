# Copyright (C) 2009 Paul Cochrane
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

# $Id$

"""
File containing the PBSNodes and Node classes
"""

import re

class PBSNodes:
    """
    The PBSNodes class
    """

    def __init__(self):
	"""
	Initialise the PBSNodes class
	"""

        self.node_list = []

    def get_node_list(self):
        """
        Return a list of Node objects
        """
        return self.node_list

    def add_node(self, node):
        """
        Add a node to the list of Node objects
        
        @param node: the Node object to add to the node list
        @type node: Node object
        """
        self.node_list.append(node)

    def get_node_table(self):
        """
        Return a hash table of Node objects indexed by node name
        """
        node_list = self.get_node_list()
        node_table = {}
        for node in node_list:
            node_name = node.get_name()
            node_table[node_name] = node

        return node_table

    def reset(self):
        """
        Reset the object to contain no data.  This is useful when reading in
        more than one xml file.
        """
        self.node_list = []


class Node:
    """
    The class holding information for a given node
    """

    def __init__(self):
        """
        Initialise the Node class
        """
        self.name = None
        self.state = None
        self.num_processors = None
        self.properties = None   # usually the queue name
        self.jobs_string = None  # a string of jobs currently running
        #self.status = "" # maybe can extract useful info out of here someday

    def set_name(self, node_name):
        """
        Set the node's name

        @param node_name: the node name
        @type node_name: string
        """
        self.name = node_name

    def get_name(self):
        """
        Return the node's name
        """
        return self.name

    def set_state(self, node_state):
        """
        Set the node's state (e.g. busy, free, job-exclusive)

        @param node_state: the state to set
        @type node_state: string
        """
        self.state = node_state

    def get_state(self):
        """
        Return the node's state
        """
        return self.state

    def set_num_processors(self, num_processors):
        """
        Set the number of processors on a given node

        @param num_processors: the number of processors on the node
        @type num_processors: integer
        """
        self.num_processors = num_processors

    def get_num_processors(self):
        """
        Return the number of processors on the node
        """
        return self.num_processors

    def set_properties(self, node_properties):
        """
        Set the node's properties (usually something like a queue name)

        @param node_properties: the node properties
        @type node_properties: string
        """
        self.properties = node_properties

    def get_properties(self):
        """
        Return the node's properties
        """
        return self.properties

    def set_jobs_string(self, jobs_string):
        """
        Set the string of jobs currently running on the node

        @param jobs_string: the string of jobs currently running on the node
        @type jobs_string: string
        """
        self.jobs_string = jobs_string

    def get_jobs_string(self):
        """
        Return the string of jobs
        """
        return self.jobs_string

    def get_num_jobs(self):
        """
        Return the number of jobs currently running on the node
        """
        jobs_string = self.get_jobs_string()
        if jobs_string is None:
            return 0
        else:
            jobs = re.split(',', jobs_string)
            num_jobs = len(jobs)
            return num_jobs

# vim: expandtab shiftwidth=4:
