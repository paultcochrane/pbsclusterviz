#!/usr/bin/env python

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

"""
The main file for the cluster_job_status application
"""

import pbsclusterviz
from pbsclusterviz.pbs.pbsnodes import PBSNodes, Node
from pbsclusterviz.pbs.xml_handler import PBSNodesXMLHandler
from pbsclusterviz.compute_node import ComputeNode
import xml.sax
import getopt
import sys, re, os
import ConfigParser


def usage():
    print """Usage:
    cluster_job_status [options]

    options:
    [-h/--help]                  Print usage information and exit
    [-V/--version]               Print version information and exit
    [-l/--logfile=<filename>]    Specify an alternative log file name
    [-i/--interactive]           Turn on interactive behaviour (default off)
    [-x/--xmlfile=<filename>]    Specify an input pbsnodes xml file
    [-o/--outfile=<filename>]    Specify an output image file
    [-c/--configfile=<filename>] Specify an input configuration file
    [-n/--nodesfile=<filename>]  Specify an alternate nodes file
    """

def version():
    print """cluster_job_status version 0.1a"""

#---------------------------------------------------------------------
# Handle options
#---------------------------------------------------------------------

try:
    options_list, args_list = getopt.getopt(sys.argv[1:], "hVil:x:o:c:n:d",
            ["help", "version", "interactive", "logfile=", "xmlfile=",
                "outfile=", "configfile=", "nodesfile=", "debug"])
except getopt.GetoptError:
    # print help information and exit:
    usage()
    sys.exit(2)

interactive = False
xml_file = None
output_file = "cluster_job_status.png"

pbsclusterviz.pbs.__debug = False

# parse the command line options
for option, arg in options_list:
    if option in ("-h", "--help"):
        usage()
        sys.exit()
    if option in ("-V", "--version"):
        version()
        sys.exit()
    if option in ("-i", "--interactive"):
        interactive = True
    elif option in ("-l", "--logfile"):
        print "Not yet implemented"
        sys.exit()
        log_file = arg
    elif option in ("-x", "--xmlfile"):
        xml_file = arg
    elif option in ("-o", "--outfile"):
        output_file = arg
    elif option in ("-c", "--configfile"):
        config_file = arg
    elif option in ("-n", "--nodesfile"):
        nodes_file = arg
    elif option in ("-d", "--debug"):
        pbsclusterviz.pbs.__debug = True
    else:
        print "Unknown option %s" % option
        sys.exit(2)

if len(args_list) > 2:
    print "Too many arguments"
    usage()
    sys.exit()

# work out where the config files are from the PYTHONPATH environment variable
pythonpath = os.environ.get('PYTHONPATH')
pythonpath_elements = []
config_path = "/etc/pbsclusterviz.d"
if pythonpath is not None:
    # split the PYTHONPATH on ':' and search for the pbsclusterviz.d directory
    pythonpath_elements = pythonpath.split(':')
    for path in pythonpath_elements:
        # trim off the path to the python site-packages to get the base path
        site_packages_regexp = re.compile(r'lib\d{0,2}/python\d\.\d/site-packages')
        path = site_packages_regexp.sub('', path)
        test_path = "%s/etc/pbsclusterviz.d" % path
        if os.path.exists(test_path):
            config_path = test_path

        if pbsclusterviz.pbs.__debug:
            print "path = %s" % path
            print "test_path = %s" % test_path
            print "config_path = %s" % config_path

config_file = "%s/clusterviz.conf" % config_path
nodes_file = "%s/nodes" % config_path

# make sure one can find the config file and the nodes file
if not os.path.exists(config_file):
    print "Unable to find pbsclusterviz configuration file: %s" % config_file
    print "Your PYTHONPATH variable should include the location of the"
    print ".../etc/pbsclusterviz.d directory"
    sys.exit(1)

if not os.path.exists(nodes_file):
    print "Unable to find pbsclusterviz nodes file: %s" % nodes_file
    print "Your PYTHONPATH variable should include the location of the"
    print ".../etc/pbsclusterviz.d directory"
    sys.exit(1)

# Now collect the data from the pbsnodes-generated XML file
pbsnodes = PBSNodes()
parser = xml.sax.make_parser()
handler = PBSNodesXMLHandler(pbsnodes)
parser.setContentHandler(handler)

if xml_file is not None:
    if not os.path.exists(xml_file):
        print "PBSNodes XML file: '%s' does not exist!" % xml_file
        sys.exit(1)
    parser.parse(xml_file)
else:
    xml_file = '/tmp/pbsnodes.xml'
    pbsnodes_cmd = "pbsnodes -x"
    error = os.system("%s > %s" % (pbsnodes_cmd, xml_file) )
    if error:
        print "Unable to run '%s'.  Exiting." % pbsnodes_cmd
        sys.exit(1)
    parser.parse(xml_file)

max_num_jobs = 0
for node in pbsnodes.get_node_list():
    #print "%s %i" % (node.get_name(), node.get_num_jobs())
    max_num_jobs += node.get_num_processors()
node_table = pbsnodes.get_node_table()

# read in the node list
fp = open(nodes_file, "r")
lines = fp.readlines()
fp.close()

node_list = []
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

    if node_table.has_key(node_name):
        node = ComputeNode(display_mode = "jobs", three_d_view = True)
        node.set_hostname(node_name)
        node.set_max_jobs(node_table[node_name].get_num_processors())
        node.set_num_jobs(node_table[node_name].get_num_jobs())
        node.set_grid_xy_pos(x_pos, y_pos)
        node_list.append(node)

# read in the configuration file
config = ConfigParser.RawConfigParser()
config.read(config_file)
title_text = config.get('job viewer', 'title')

# work out the output file name's base name (the bit without .png)
base_regex = re.compile(r'(.*?)\.\w+$')
basename_search_result = base_regex.search(output_file)
if basename_search_result.group(1) is None:
    print "Unable to determine the base image output file name"
    sys.exit(0)

output_file_basename = basename_search_result.group(1)

import vtk

# Create the usual rendering stuff.
renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(1024, 768)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(render_window)

renderer.SetBackground(0, 0, 0)

# set up the text properties for nice text
font_size = 10
text_prop = vtk.vtkTextProperty()
text_prop.SetFontSize(font_size)
text_prop.SetFontFamilyToArial()
text_prop.BoldOff()
text_prop.ItalicOff()
text_prop.ShadowOff()

# add a title to the image
import time
now = time.ctime()

title_text = "%s: %s" % (title_text, now)

title = vtk.vtkTextMapper()
title.SetInput(title_text)

title_prop = title.GetTextProperty()
title_prop.ShallowCopy(text_prop)
title_prop.SetJustificationToCentered()
title_prop.SetVerticalJustificationToTop()
title_prop.SetFontSize(20)
title_prop.SetColor(1,1,1)
title_prop.BoldOn()

title_actor = vtk.vtkTextActor()
title_actor.SetMapper(title)
title_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
title_actor.GetPositionCoordinate().SetValue(0.5,0.95)

renderer.AddActor(title_actor)

# make a lookup table for the colour map and invert it (colours look
# better when it's inverted)
lut = vtk.vtkLookupTable()
refLut = vtk.vtkLookupTable()
lut.Build()
refLut.Build()
for j in range(256):
    lut.SetTableValue(j, refLut.GetTableValue(255-j))

# get the colours, assign a colour to each host and get the current total
# number of jobs
current_num_jobs = 0
rgb = [0.0, 0.0, 0.0]
for node in node_list:
    hostname = node.get_hostname()
    node_num_jobs = node.get_num_jobs()
    node_max_jobs = node.get_max_jobs()
    current_num_jobs += node_num_jobs

    lut.GetColor(float(node_num_jobs)/float(node_max_jobs), rgb)
    node.set_rgb(rgb)

# how well is the cluster system being used?
utilisation_value = current_num_jobs*100.0/max_num_jobs

# add the utilisation text to the image
utilisation_text = "System utilisation: %0.2f %%" % utilisation_value

utilisation = vtk.vtkTextMapper()
utilisation.SetInput(utilisation_text)

utilisation_prop = utilisation.GetTextProperty()
utilisation_prop.ShallowCopy(text_prop)
utilisation_prop.SetJustificationToCentered()
utilisation_prop.SetVerticalJustificationToTop()
utilisation_prop.SetFontSize(16)
utilisation_prop.SetColor(1,1,1)
utilisation_prop.BoldOn()

utilisation_actor = vtk.vtkTextActor()
utilisation_actor.SetMapper(utilisation)
utilisation_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
utilisation_actor.GetPositionCoordinate().SetValue(0.5,0.92)

renderer.AddActor(utilisation_actor)

# set up the scalar bar
scalar_bar = vtk.vtkScalarBarActor()
scalar_bar.SetLookupTable(lut)
scalar_bar.SetTitle("Scaled Job Count")
scalar_bar.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
scalar_bar.GetPositionCoordinate().SetValue(0.1, 0.8)
scalar_bar.SetOrientationToHorizontal()
scalar_bar.SetWidth(0.8)
scalar_bar.SetHeight(0.1)

scalar_bar_title_prop = scalar_bar.GetTitleTextProperty()
scalar_bar_title_prop.SetFontFamilyToCourier()
scalar_bar_title_prop.SetFontSize(6)
scalar_bar_title_prop.ItalicOff()

scalar_bar_label_prop = scalar_bar.GetLabelTextProperty()
scalar_bar_label_prop.SetFontFamilyToCourier()
scalar_bar_label_prop.SetFontSize(4)
scalar_bar_label_prop.ItalicOff()

renderer.AddActor(scalar_bar)

### generate the node matrix
for node in node_list:
    node.add_box(renderer)
    node.add_label(renderer)

# set up the camera properly
renderer.ResetCamera()
renderer.ResetCameraClippingRange()
renderer.GetActiveCamera().Azimuth(140)
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Zoom(1.3)

#interactive = 0
if interactive:
    # Render the scene and start interaction.
    iren.Initialize()
    render_window.Render()
    iren.Start()
else:
    # make sure we're using the mesa classes when saving to file
    fact_graphics = vtk.vtkGraphicsFactory()
    fact_graphics.SetUseMesaClasses(1)
    fact_graphics.SetOffScreenOnlyMode(1)
    fact_image = vtk.vtkImagingFactory()
    fact_image.SetUseMesaClasses(1)

    render_window.OffScreenRenderingOn()
    # to save the file to png, need to pass the render window through a filter
    # to an image object
    win2img_filter = vtk.vtkWindowToImageFilter()
    win2img_filter.SetInput(render_window)

    out_writer = vtk.vtkPNGWriter()
    out_writer.SetInput(win2img_filter.GetOutput())
    out_writer.SetFileName("%s.png" % output_file_basename)

    # render the window to save it to file
    render_window.Render()
    out_writer.Write()

    # and write out a file with the current date on it
    from datetime import datetime
    date = datetime.now()
    date_str = date.strftime("%Y%m%d_%H%M")
    fname_str = "%s_%s.png" % (output_file_basename, date_str)
    out_writer.SetFileName(fname_str)

    # save it to file
    out_writer.Write()

# vim: expandtab shiftwidth=4:
