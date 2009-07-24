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

# $Id$

"""
The main file for the cluster_job_status application
"""

import pbs
from pbs.pbsnodes import PBSNodes, Node
from pbs.xml_handler import PBSNodesXMLHandler
from compute_host import ComputeHost
import xml.sax
import getopt
import sys


def usage():
    print """Usage:
    python cluster_job_status.py [options]

    options:
    [-h/--help]                  Print usage information and exit
    [-V/--version]               Print version information and exit
    [-l/--logfile=<filename>]    Specify an alternative log file name
    [-i/--interactive]           Turn on interactive behaviour
    [-x/--xmlfile=<filename>]    Specify an input xml file
    """

def version():
    print """cluster_job_status version 0.1a"""

#---------------------------------------------------------------------
# Handle options
#---------------------------------------------------------------------

try:
    options_list, args_list = getopt.getopt(sys.argv[1:], "hVil:x:o:d",
            ["help", "version", "interactive", "logfile=", "xmlfile=", "outfile=", "debug"])
except getopt.GetoptError:
    # print help information and exit:
    usage()
    sys.exit(2)

interactive = False
xml_file = None
output_file = "cluster_job_status.png"
pbs.__debug = False
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
    elif option in ("-d", "--debug"):
        pbs.__debug = True

if len(args_list) > 2:
    print "Too many arguments"
    usage()
    sys.exit()

pbsnodes = PBSNodes()
parser = xml.sax.make_parser()
handler = PBSNodesXMLHandler(pbsnodes)
parser.setContentHandler(handler)

if xml_file is not None:
    # TODO: check that the file exists
    parser.parse(xml_file)
else:
    # TODO: implement a direct call to pbsnodes -x
    print "Direct call to pbsnodes not yet implemented"
    sys.exit()

for node in pbsnodes.get_node_list():
    print "%s %i" % (node.get_name(), node.get_num_jobs())
node_table = pbsnodes.get_node_table()

host_list = []

pozzo = ComputeHost()
pozzo.set_hostname('pozzo')
pozzo.set_max_jobs(16)
pozzo.set_num_jobs(node_table[pozzo.get_hostname()].get_num_jobs())
pozzo.set_grid_xy_pos(1, 0)
pozzo.set_display_mode("jobs")
host_list.append(pozzo)

paris01 = ComputeHost()
paris01.set_hostname('paris-n001')
paris01.set_max_jobs(8)
paris01.set_num_jobs(node_table[paris01.get_hostname()].get_num_jobs())
paris01.set_grid_xy_pos(0, 1)
paris01.set_display_mode("jobs")
host_list.append(paris01)

paris02 = ComputeHost()
paris02.set_hostname('paris-n002')
paris02.set_max_jobs(8)
paris02.set_num_jobs(node_table[paris02.get_hostname()].get_num_jobs())
paris02.set_grid_xy_pos(1, 1)
paris02.set_display_mode("jobs")
host_list.append(paris02)

paris03 = ComputeHost()
paris03.set_hostname('paris-n003')
paris03.set_max_jobs(8)
paris03.set_num_jobs(node_table[paris03.get_hostname()].get_num_jobs())
paris03.set_grid_xy_pos(2, 1)
paris03.set_display_mode("jobs")
host_list.append(paris03)

paris04 = ComputeHost()
paris04.set_hostname('paris-n004')
paris04.set_max_jobs(8)
paris04.set_num_jobs(node_table[paris04.get_hostname()].get_num_jobs())
paris04.set_grid_xy_pos(3, 1)
paris04.set_display_mode("jobs")
host_list.append(paris04)

paris05 = ComputeHost()
paris05.set_hostname('paris-n005')
paris05.set_max_jobs(8)
paris05.set_num_jobs(node_table[paris05.get_hostname()].get_num_jobs())
paris05.set_grid_xy_pos(4, 1)
paris05.set_display_mode("jobs")
host_list.append(paris05)

paris06 = ComputeHost()
paris06.set_hostname('paris-n006')
paris06.set_max_jobs(8)
paris06.set_num_jobs(node_table[paris06.get_hostname()].get_num_jobs())
paris06.set_grid_xy_pos(5, 1)
paris06.set_display_mode("jobs")
host_list.append(paris06)

paris07 = ComputeHost()
paris07.set_hostname('paris-n007')
paris07.set_max_jobs(8)
paris07.set_num_jobs(node_table[paris07.get_hostname()].get_num_jobs())
paris07.set_grid_xy_pos(0, 2)
paris07.set_display_mode("jobs")
host_list.append(paris07)

paris08 = ComputeHost()
paris08.set_hostname('paris-n008')
paris08.set_max_jobs(8)
paris08.set_num_jobs(node_table[paris08.get_hostname()].get_num_jobs())
paris08.set_grid_xy_pos(1, 2)
paris08.set_display_mode("jobs")
host_list.append(paris08)

paris09 = ComputeHost()
paris09.set_hostname('paris-n009')
paris09.set_max_jobs(8)
paris09.set_num_jobs(node_table[paris09.get_hostname()].get_num_jobs())
paris09.set_grid_xy_pos(2, 2)
paris09.set_display_mode("jobs")
host_list.append(paris09)

paris10 = ComputeHost()
paris10.set_hostname('paris-n010')
paris10.set_max_jobs(8)
paris10.set_num_jobs(node_table[paris10.get_hostname()].get_num_jobs())
paris10.set_grid_xy_pos(3, 2)
paris10.set_display_mode("jobs")
host_list.append(paris10)

paris11 = ComputeHost()
paris11.set_hostname('paris-n011')
paris11.set_max_jobs(8)
paris11.set_num_jobs(node_table[paris11.get_hostname()].get_num_jobs())
paris11.set_grid_xy_pos(4, 2)
paris11.set_display_mode("jobs")
host_list.append(paris11)

tcn01 = ComputeHost()
tcn01.set_hostname('tcn01')
tcn01.set_max_jobs(2)
tcn01.set_num_jobs(node_table[tcn01.get_hostname()].get_num_jobs())
tcn01.set_grid_xy_pos(0, 3)
tcn01.set_display_mode("jobs")
host_list.append(tcn01)

tcn02 = ComputeHost()
tcn02.set_hostname('tcn02')
tcn02.set_max_jobs(2)
tcn02.set_num_jobs(node_table[tcn02.get_hostname()].get_num_jobs())
tcn02.set_grid_xy_pos(1, 3)
tcn02.set_display_mode("jobs")
host_list.append(tcn02)

tcn03 = ComputeHost()
tcn03.set_hostname('tcn03')
tcn03.set_max_jobs(2)
tcn03.set_num_jobs(node_table[tcn03.get_hostname()].get_num_jobs())
tcn03.set_grid_xy_pos(2, 3)
tcn03.set_display_mode("jobs")
host_list.append(tcn03)

tcn04 = ComputeHost()
tcn04.set_hostname('tcn04')
tcn04.set_max_jobs(2)
tcn04.set_num_jobs(node_table[tcn04.get_hostname()].get_num_jobs())
tcn04.set_grid_xy_pos(3, 3)
tcn04.set_display_mode("jobs")
host_list.append(tcn04)

tcn05 = ComputeHost()
tcn05.set_hostname('tcn05')
tcn05.set_max_jobs(2)
tcn05.set_num_jobs(node_table[tcn05.get_hostname()].get_num_jobs())
tcn05.set_grid_xy_pos(4, 3)
tcn05.set_display_mode("jobs")
host_list.append(tcn05)

tcn06 = ComputeHost()
tcn06.set_hostname('tcn06')
tcn06.set_max_jobs(2)
tcn06.set_num_jobs(node_table[tcn06.get_hostname()].get_num_jobs())
tcn06.set_grid_xy_pos(5, 3)
tcn06.set_display_mode("jobs")
host_list.append(tcn06)

tcn07 = ComputeHost()
tcn07.set_hostname('tcn07')
tcn07.set_max_jobs(2)
tcn07.set_num_jobs(node_table[tcn07.get_hostname()].get_num_jobs())
tcn07.set_grid_xy_pos(0, 4)
tcn07.set_display_mode("jobs")
host_list.append(tcn07)

tcn08 = ComputeHost()
tcn08.set_hostname('tcn08')
tcn08.set_max_jobs(2)
tcn08.set_num_jobs(node_table[tcn08.get_hostname()].get_num_jobs())
tcn08.set_grid_xy_pos(1, 4)
tcn08.set_display_mode("jobs")
host_list.append(tcn08)

tcn09 = ComputeHost()
tcn09.set_hostname('tcn09')
tcn09.set_max_jobs(2)
tcn09.set_num_jobs(node_table[tcn09.get_hostname()].get_num_jobs())
tcn09.set_grid_xy_pos(2, 4)
tcn09.set_display_mode("jobs")
host_list.append(tcn09)

tcn10 = ComputeHost()
tcn10.set_hostname('tcn10')
tcn10.set_max_jobs(2)
tcn10.set_num_jobs(node_table[tcn10.get_hostname()].get_num_jobs())
tcn10.set_grid_xy_pos(3, 4)
tcn10.set_display_mode("jobs")
host_list.append(tcn10)

tcn11 = ComputeHost()
tcn11.set_hostname('tcn11')
tcn11.set_max_jobs(2)
tcn11.set_num_jobs(node_table[tcn11.get_hostname()].get_num_jobs())
tcn11.set_grid_xy_pos(4, 4)
tcn11.set_display_mode("jobs")
host_list.append(tcn11)

tcn12 = ComputeHost()
tcn12.set_hostname('tcn12')
tcn12.set_max_jobs(2)
tcn12.set_num_jobs(node_table[tcn12.get_hostname()].get_num_jobs())
tcn12.set_grid_xy_pos(5, 4)
tcn12.set_display_mode("jobs")
host_list.append(tcn12)

lcn01 = ComputeHost()
lcn01.set_hostname('lcn01')
lcn01.set_max_jobs(4)
lcn01.set_num_jobs(node_table[lcn01.get_hostname()].get_num_jobs())
lcn01.set_grid_xy_pos(0, 5)
lcn01.set_display_mode("jobs")
host_list.append(lcn01)

lcn02 = ComputeHost()
lcn02.set_hostname('lcn02')
lcn02.set_max_jobs(4)
lcn02.set_num_jobs(node_table[lcn02.get_hostname()].get_num_jobs())
lcn02.set_grid_xy_pos(1, 5)
lcn02.set_display_mode("jobs")
host_list.append(lcn02)

lcn03 = ComputeHost()
lcn03.set_hostname('lcn03')
lcn03.set_max_jobs(4)
lcn03.set_num_jobs(node_table[lcn03.get_hostname()].get_num_jobs())
lcn03.set_grid_xy_pos(2, 5)
lcn03.set_display_mode("jobs")
host_list.append(lcn03)

lcn04 = ComputeHost()
lcn04.set_hostname('lcn04')
lcn04.set_max_jobs(4)
lcn04.set_num_jobs(node_table[lcn04.get_hostname()].get_num_jobs())
lcn04.set_grid_xy_pos(3, 5)
lcn04.set_display_mode("jobs")
host_list.append(lcn04)

lcn05 = ComputeHost()
lcn05.set_hostname('lcn05')
lcn05.set_max_jobs(4)
lcn05.set_num_jobs(node_table[lcn05.get_hostname()].get_num_jobs())
lcn05.set_grid_xy_pos(4, 5)
lcn05.set_display_mode("jobs")
host_list.append(lcn05)

lcn06 = ComputeHost()
lcn06.set_hostname('lcn06')
lcn06.set_max_jobs(4)
lcn06.set_num_jobs(node_table[lcn06.get_hostname()].get_num_jobs())
lcn06.set_grid_xy_pos(5, 5)
lcn06.set_display_mode("jobs")
host_list.append(lcn06)

lcn07 = ComputeHost()
lcn07.set_hostname('lcn07')
lcn07.set_max_jobs(4)
lcn07.set_num_jobs(node_table[lcn07.get_hostname()].get_num_jobs())
lcn07.set_grid_xy_pos(6, 5)
lcn07.set_display_mode("jobs")
host_list.append(lcn07)

lcn08 = ComputeHost()
lcn08.set_hostname('lcn08')
lcn08.set_max_jobs(4)
lcn08.set_num_jobs(node_table[lcn08.get_hostname()].get_num_jobs())
lcn08.set_grid_xy_pos(7, 5)
lcn08.set_display_mode("jobs")
host_list.append(lcn08)

lcn09 = ComputeHost()
lcn09.set_hostname('lcn09')
lcn09.set_max_jobs(4)
lcn09.set_num_jobs(node_table[lcn09.get_hostname()].get_num_jobs())
lcn09.set_grid_xy_pos(0, 6)
lcn09.set_display_mode("jobs")
host_list.append(lcn09)

lcn10 = ComputeHost()
lcn10.set_hostname('lcn10')
lcn10.set_max_jobs(4)
lcn10.set_num_jobs(node_table[lcn10.get_hostname()].get_num_jobs())
lcn10.set_grid_xy_pos(1, 6)
lcn10.set_display_mode("jobs")
host_list.append(lcn10)

lcn11 = ComputeHost()
lcn11.set_hostname('lcn11')
lcn11.set_max_jobs(4)
lcn11.set_num_jobs(node_table[lcn11.get_hostname()].get_num_jobs())
lcn11.set_grid_xy_pos(2, 6)
lcn11.set_display_mode("jobs")
host_list.append(lcn11)

lcn12 = ComputeHost()
lcn12.set_hostname('lcn12')
lcn12.set_max_jobs(4)
lcn12.set_num_jobs(node_table[lcn12.get_hostname()].get_num_jobs())
lcn12.set_grid_xy_pos(3, 6)
lcn12.set_display_mode("jobs")
host_list.append(lcn12)

lcn13 = ComputeHost()
lcn13.set_hostname('lcn13')
lcn13.set_max_jobs(4)
lcn13.set_num_jobs(node_table[lcn13.get_hostname()].get_num_jobs())
lcn13.set_grid_xy_pos(4, 6)
lcn13.set_display_mode("jobs")
host_list.append(lcn13)

lcn14 = ComputeHost()
lcn14.set_hostname('lcn14')
lcn14.set_max_jobs(4)
lcn14.set_num_jobs(node_table[lcn14.get_hostname()].get_num_jobs())
lcn14.set_grid_xy_pos(5, 6)
lcn14.set_display_mode("jobs")
host_list.append(lcn14)

lcn15 = ComputeHost()
lcn15.set_hostname('lcn15')
lcn15.set_max_jobs(4)
lcn15.set_num_jobs(node_table[lcn15.get_hostname()].get_num_jobs())
lcn15.set_grid_xy_pos(6, 6)
lcn15.set_display_mode("jobs")
host_list.append(lcn15)

lcn16 = ComputeHost()
lcn16.set_hostname('lcn16')
lcn16.set_max_jobs(4)
lcn16.set_num_jobs(node_table[lcn16.get_hostname()].get_num_jobs())
lcn16.set_grid_xy_pos(7, 6)
lcn16.set_display_mode("jobs")
host_list.append(lcn16)

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

title_text = "RRZN Cluster Job Status: %s" % now

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

# get the colours
rgb = [0.0, 0.0, 0.0]
for host in host_list:
    hostname = host.get_hostname()
    host_num_jobs = host.get_num_jobs()
    max_host_jobs = host.get_max_jobs()
    lut.GetColor(float(host_num_jobs)/float(max_host_jobs), rgb)
    host.set_rgb(rgb)

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

### generate the host matrix
for host in host_list:
    host.add_box(renderer)
    host.add_label(renderer)

# set up the camera properly
renderer.ResetCamera()
renderer.ResetCameraClippingRange()
renderer.GetActiveCamera().Azimuth(140)
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Zoom(1.3)

interactive = 0
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
    out_writer.SetFileName("cluster_job_status.png")

    # render the window to save it to file
    render_window.Render()
    out_writer.Write()

    # and write out a file with the current date on it
    from datetime import datetime
    date = datetime.now()
    date_str = date.strftime("%Y%m%d_%H%M")
    fname_str = "cluster_job_status_%s.png" % (date_str)
    out_writer.SetFileName(fname_str)

    # save it to file
    out_writer.Write()

# vim: expandtab shiftwidth=4:
