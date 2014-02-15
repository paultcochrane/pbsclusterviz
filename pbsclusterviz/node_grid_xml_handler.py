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
The handler for the output of ``pbsnodes -x``.
The parsed file is in XML-Format.
"""

from xml.sax.handler import ContentHandler
import re, logging

# This class extends the ContentHandler class from xml.sax.handler.
# When a xml.sax-Parser parses a xml-file, at each xml-element 
# this handler is invoked. 
# For example a segment like
#    <tag1>
#        property1, property2
#    </tag1>
# will lead to the following calls of the handler:
#    ContentHandler.startElement("tag1")
#    ContentHandler.characters("property1, property2")
#    ContentHandler.endElement("tag1")
# According to the output of 'pbsnodes -x' the call of 
# startElement only marks the type of the current element.
# Then the content is read and stored to the corresponding 
# variable. Calling endElement unsets the current type,
# stores the result in the nodelist 'pbsnodes' and
# resets the handler for the next element.
#
# The hierarchy of the output of 'pbsnodes -x' is flat,
# i.e. there is only the <Node>-tag and then a list
# of properties, which contain no further sub-properties:
# <Node>
#    <name>Pozzo</name>
#    ...
#    <status>blubb</status>
# </Node>
# Further nesting could lead to problems as the hierarchy
# of the tags is not stored in the implementation of this 
# handler.

class NodeGridXMLHandler(ContentHandler):
    """
    The XML handler class for processing pbsnodes XML output
    """

    def __init__(self, node_grid):
        """
        Initialise the handler class
        """

        ContentHandler.__init__(self)

        self.node_grid = node_grid
        self.current_node = None
        self.property_dict = {}
        self.keyword = ""
        self.content = ""
        self.logger = logging.getLogger("")

    def startElement(self, name, attrs):
        """
        Method to call at the beginning of an XML element
        
        :param name: the element name
        :type name: string

        :param attrs: the attribute name
        :type attrs: string
        """

        # if the block of a new Node start, reset the data
        if name == "Node":
            self.current_node = None
            self.property_dict = {}
        self.keyword = name

    def endElement(self, name):
        """
        Method to call at the end of an XML element

        :param name: the element name
        :type name: string
        """
        if name == "Node":
            # first check whether the node was found in the grid
            if self.current_node == None:
                if 'name' in self.property_dict.keys():
                    self.logger.error("Node " + self.property_dict['name'] + \
                            " not found in nodes file!")
                else:
                    self.logger.error('No name defined for current node')
                return

            self.save_node_data(self.property_dict)
        else:
            self.property_dict[ self.keyword ] = self.content
            self.keyword = ""
            self.content = ""
        return

    def characters(self, content):
        """
        Process the characters in the XML data

        :param content: the current character(s) (i.e. content) to be processed
        :type content: string
        """
        if self.keyword == "name":
            node_name = content
            debug_msg = "%s: Node name = %s" % (__name__, node_name)
            self.logger.debug(debug_msg)
            self.current_node = self.node_grid.get_node_by_name(node_name)
            if self.current_node == None:
                # create a new, empty node if no node known by that name
                self.node_grid.add_new_node(node_name)
                self.current_node = self.node_grid.get_node_by_name(node_name)
        self.content = content

    def save_node_data(self, property_dict):
        """
        Collects the data in the property dictionary and stores it in the
        node
        """
        for prop in property_dict.keys():
            if prop == "state":
                self.current_node.state = property_dict[ prop ]
            elif prop == "np":
                self.current_node.num_processors = property_dict[ prop ]
                self.current_node.max_load = \
                        float(self.current_node.num_processors)
            elif prop == "properties":
                self.current_node.properties = property_dict[ prop ]
            elif prop == "jobs":
                self.current_node.jobs = re.split(',', property_dict[prop])
            elif prop == "status":
                # create a dictionary from the status string
                self.current_node.status = {}
                status_info_list = re.split(',', property_dict[prop])
                for item in status_info_list:
                    if not re.match('.*=.*', item):
                        debug_message = "<status> tag item not parseable"
                        self.logger.debug(debug_message)
                    else:
                        (tag, value) = re.split('=', item)
                        self.current_node.status[tag] = value

# vim: expandtab shiftwidth=4:
