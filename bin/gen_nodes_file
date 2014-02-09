#!/usr/bin/env python

# Copyright (C) 2009-2011 Paul Cochrane
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
Automatically generate a nodes file
"""

import pbsclusterviz
from pbsclusterviz.node_grid import NodeGrid
from pbsclusterviz.node_grid_xml_handler import NodeGridXMLHandler
import xml.sax
import getopt
import sys, re, os
import logging, tempfile


def usage():
    print """Usage:
    gen_nodes_file [options]

    options:
    [-h/--help]                     Print usage information and exit
    [-V/--version]                  Print version information and exit
    [-x/--xmlfile=<filename>]       Specify an input pbsnodes xml file
    [-o/--nodesfile=<filename>]     Specify an output nodes file
    [-n/--section_name=<name>]      Specify a name for the node section
    [-p/--node_prefix=<prefix>]     Specify a nodename prefix
    [-w/--table_width=<width>]      Number of nodes across a section
    [-a/--append]                   Append to existing nodes file?
    """

def version():
    print """gen_nodes_file version 0.2a"""

#---------------------------------------------------------------------
# Handle options
#---------------------------------------------------------------------

try:
    options_list, args_list = getopt.getopt(sys.argv[1:], "hVax:o:n:p:w:d",
            ["help", "version", "xmlfile=", "nodesfile=", 
		"section_name=", "node_prefix=", "table_width=",
		"append", "debug"])
except getopt.GetoptError:
    # print help information and exit:
    usage()
    sys.exit(2)

xml_file = None
nodes_file = "nodes.gen"
section_name = None
node_prefix = None
table_width = 10
append_to_nodes_file = False
for option, arg in options_list:
    if option in ("-h", "--help"):
        usage()
        sys.exit()
    if option in ("-V", "--version"):
        version()
        sys.exit()
    elif option in ("-d", "--debug"):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Debugging switched on")
    elif option in ("-x", "--xmlfile"):
        xml_file = arg
    elif option in ("-o", "--outfile"):
        nodes_file = arg
    elif option in ("-n", "--section_name"):
	section_name = arg
    elif option in ("-p", "--node_prefix"):
	node_prefix = arg
    elif option in ("-w", "--table_width"):
	table_width = int(arg)
    elif option in ("-a", "--append"):
        append_to_nodes_file = True
    else:
        print "Unknown option %s" % option
        sys.exit(2)

if len(args_list) > 2:
    print "Too many arguments"
    usage()
    sys.exit()

if section_name is None:
    print "You need to specify a section name (-n <name>)"
    sys.exit(2)

if node_prefix is None:
    print "You need to specify a node prefix (-p <prefix>)"
    sys.exit(2)

screen_log = ""
node_grid = NodeGrid(screen_log)
handler = NodeGridXMLHandler(node_grid)
parser = xml.sax.make_parser()
parser.setContentHandler(handler)

if xml_file is not None:
    if not os.path.exists(xml_file):
        print "PBSNodes XML file: '%s' does not exist!" % xml_file
        sys.exit(1)
    parser.parse(xml_file)
else:
    xml_file = tempfile.NamedTemporaryFile(dir='/tmp')
    pbsnodes_cmd = "pbsnodes -x"
    error = os.system("%s > %s" % (pbsnodes_cmd, xml_file.name) )
    if error:
        print "Unable to run '%s'.  Exiting." % pbsnodes_cmd
        sys.exit(1)
    parser.parse(xml_file)

# the section prefix is used to filter the different kinds of nodes on a
# multi-cluster system
prefix_regex = re.compile(r"^%s" % node_prefix)

x_grid_pos = 0
y_grid_pos = 0

# automatically determine the current y grid position from a previous nodes
# file.  Only necessary if the "append" option is used.
if append_to_nodes_file and os.path.exists(nodes_file):
    fp = open(nodes_file, "r")
    lines = fp.readlines()
    fp.close()
    
    # get the last line but ignore leading hashes and lines with only return
    # characters in them
    hash_regex = re.compile(r'^#')
    return_regex = re.compile(r'\n')
    last_line = None
    for line in lines:
	if hash_regex.match(line) or return_regex.match(line):
	    pass
	else:
	    last_line = line
    
    y_grid_pos = int(last_line.split(' ')[-1]) + 1

# write the nodes info to file
fp = None
node_gen_message = ""
if append_to_nodes_file:
    fp = open(nodes_file, "a")
    node_gen_message += "Appending "
else:
    fp = open(nodes_file, "w")
    node_gen_message += "Writing "

node_gen_message += \
        "node information for the '%s' cluster to the nodes file: %s" %\
        (section_name, nodes_file)
print node_gen_message

fp.write("# section: %s\n" % section_name)
# need to get the node list from the xml, *not* from the nodes file...
for node in node_grid.get_node_list():
    node_name = node.get_name()
    if prefix_regex.match(node_name):
        fp.write("%s %i %i\n" % (node_name, x_grid_pos, y_grid_pos))
	# if we're at the side of the table, reset x and increment y
	if x_grid_pos >= table_width-1:
	    x_grid_pos = 0
	    y_grid_pos += 1
	else:
	    x_grid_pos += 1

fp.close()

print "Done!"

# vim: expandtab shiftwidth=4:
