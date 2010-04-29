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
File containing the XML handler class for processing pbs-related XML output
"""

from xml.sax.handler import ContentHandler
from pbsclusterviz.pbs.pbsnodes import PBSNodes, Node

class PBSNodesXMLHandler(ContentHandler):
    """
    The XML handler class for processing pbsnodes XML output
    """

    def __init__(self, pbsnodes):
	"""
	Initialise the handler class
	"""

	ContentHandler.__init__(self)

        self.is_node_element = False
        self.is_name_element = False
        self.is_state_element = False
        self.is_num_processors_element = False
        self.is_properities_element = False
        self.is_jobs_element = False
        self.is_status_element = False

        self.node = Node()
        self.pbsnodes = pbsnodes
        self.name = ""
        self.state = ""
        self.num_processors = ""
        self.properties = ""
        self.jobs = ""
        self.status = ""

    def startElement(self, name, attrs):
	"""
	Method to call at the beginning of an XML element
	
	@param name: the element name
	@type name: string

	@param attrs: the attribute name
	@type attrs: string
	"""

        if name == "Node":
            self.is_node_element = True
            self.node = Node()
        elif name == "name":
            self.is_name_element = True
            self.name = ""
        elif name == "state":
            self.is_state_element = True
            self.state = ""
        elif name == "np":
            self.is_num_processors_element = True
            self.num_processors = ""
        elif name == "properties":
            self.is_properties_element = True
            self.properties = ""
        elif name == "jobs":
            self.is_jobs_element = True
            self.jobs = ""
        elif name == "status":
            self.is_status_element = True
            self.status = ""

    def endElement(self, name):
	"""
	Method to call at the end of an XML element

	@param name: the element name
	@type name: string
	"""
        if name == "Node":
            self.is_node_element = False
            self.pbsnodes.add_node(self.node)
        elif name == "name":
            self.is_name_element = False
            self.node.set_name(self.name)
        elif name == "state":
            self.is_state_element = False
            self.node.set_state(self.state)
        elif name == "np":
            self.is_num_processors_element = False
            self.node.set_num_processors(int(self.num_processors))
        elif name == "properties":
            self.is_properties_element = False
            self.node.set_properties(self.properties)
        elif name == "jobs":
            self.is_jobs_element = False
            self.node.set_jobs_string(self.jobs)
        elif name == "status":
            self.is_status_element = False
            self.node.set_status_string(self.status)

    def characters(self, content):
	"""
	Process the characters in the XML data

	@param content: the current character(s) (i.e. content) to be processed
	@type content: string
	"""

        if self.is_name_element:
            self.name += content
        elif self.is_state_element:
            self.state += content
        elif self.is_num_processors_element:
            self.num_processors += content
        elif self.is_properties_element:
            self.properties += content
        elif self.is_jobs_element:
            self.jobs += content
        elif self.is_status_element:
            self.status += content

# vim: expandtab shiftwidth=4:
