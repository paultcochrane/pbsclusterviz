#!/usr/bin/env python

import os
import re
import sys
from compute_node import ComputeNode
import getopt

def usage():
    print """Usage:
    python cluster_load_status.py -t/--three_d_view
    """

try:
    options_list, args_list = getopt.getopt(sys.argv[1:], "t", ["three_d_view"])
except getopt.GetoptError:
    # print help information and exit:
    usage()
    sys.exit(2)

testing = True
three_d_view = False

for option, arg in options_list:
    if option in ("-t", "--three_d_view"):
        three_d_view = True
    else:
        print "Unknown option %s" % option
        sys.exit(2)

host_list = []

host_list.append(
    ComputeNode(
        hostname = 'orac',
        max_load = 4.0, xy_pos = (0, 0), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'pozzo',
        max_load = 16.0, xy_pos = (1, 0), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'paris',
        max_load = 8.0, xy_pos = (2, 0), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'paris-n001',
        max_load = 8.0, xy_pos = (0, 1), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'paris-n002',
        max_load = 8.0, xy_pos = (1, 1), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'paris-n003',
        max_load = 8.0, xy_pos = (2, 1), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'paris-n004',
        max_load = 8.0, xy_pos = (3, 1), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'paris-n005',
        max_load = 8.0, xy_pos = (4, 1), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'paris-n006',
        max_load = 8.0, xy_pos = (5, 1), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'paris-n007',
        max_load = 8.0, xy_pos = (0, 2), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'paris-n008',
        max_load = 8.0, xy_pos = (1, 2), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'paris-n009',
        max_load = 8.0, xy_pos = (2, 2), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'paris-n010',
        max_load = 8.0, xy_pos = (3, 2), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'paris-n011',
        max_load = 8.0, xy_pos = (4, 2), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'tclog',
        max_load = 2.0, xy_pos = (3, 0), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'tcn01',
        max_load = 2.0, xy_pos = (0, 3), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'tcn02',
        max_load = 2.0, xy_pos = (1, 3), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'tcn03',
        max_load = 2.0, xy_pos = (2, 3), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'tcn04',
        max_load = 2.0, xy_pos = (3, 3), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'tcn05',
        max_load = 2.0, xy_pos = (4, 3), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'tcn06',
        max_load = 2.0, xy_pos = (5, 3), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'tcn07',
        max_load = 2.0, xy_pos = (0, 4), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'tcn08',
        max_load = 2.0, xy_pos = (1, 4), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'tcn09',
        max_load = 2.0, xy_pos = (2, 4), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'tcn10',
        max_load = 2.0, xy_pos = (3, 4), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'tcn11',
        max_load = 2.0, xy_pos = (4, 4), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'tcn12',
        max_load = 2.0, xy_pos = (5, 4), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'cluhadm',
        max_load = 2.0, xy_pos = (4, 0), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'lcn01',
        max_load = 4.0, xy_pos = (0, 5), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'lcn02',
        max_load = 4.0, xy_pos = (1, 5), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'lcn03',
        max_load = 4.0, xy_pos = (2, 5), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'lcn04',
        max_load = 4.0, xy_pos = (3, 5), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'lcn05',
        max_load = 4.0, xy_pos = (4, 5), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'lcn06',
        max_load = 4.0, xy_pos = (5, 5), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'lcn07',
        max_load = 4.0, xy_pos = (6, 5), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'lcn08',
        max_load = 4.0, xy_pos = (7, 5), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'lcn09',
        max_load = 4.0, xy_pos = (0, 6), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'lcn10',
        max_load = 4.0, xy_pos = (1, 6), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'lcn11',
        max_load = 4.0, xy_pos = (2, 6), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'lcn12',
        max_load = 4.0, xy_pos = (3, 6), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'lcn13',
        max_load = 4.0, xy_pos = (4, 6), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'lcn14',
        max_load = 4.0, xy_pos = (5, 6), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'lcn15',
        max_load = 4.0, xy_pos = (6, 6), three_d_view = three_d_view,
    )
)

host_list.append(
    ComputeNode(
        hostname = 'lcn16',
        max_load = 4.0, xy_pos = (7, 6), three_d_view = three_d_view,
    )
)

# username to use for the ssh command
username = "zzzzcoch"

# TODO: need to ping each host to see if it is there and display that
load_avg = {}
load_avg['orac'] = 0.08
load_avg['pozzo'] = 0.06
load_avg['paris'] = 0.85

load_avg['paris-n001'] = 1.00
load_avg['paris-n002'] = 8.00
load_avg['paris-n003'] = 0.00
load_avg['paris-n004'] = 0.00
load_avg['paris-n005'] = 0.02
load_avg['paris-n006'] = 0.00
load_avg['paris-n007'] = 0.00
load_avg['paris-n008'] = 0.00
load_avg['paris-n009'] = 0.00
load_avg['paris-n010'] = 0.00
load_avg['paris-n011'] = 0.07

load_avg['tclog'] = 0.08
load_avg['tcn01'] = 0.00
load_avg['tcn02'] = 0.00
load_avg['tcn03'] = 0.00
load_avg['tcn04'] = 4.00
load_avg['tcn05'] = 0.00
load_avg['tcn06'] = 0.00
load_avg['tcn07'] = 0.00
load_avg['tcn08'] = 0.00
load_avg['tcn09'] = 0.00
load_avg['tcn10'] = 0.00
load_avg['tcn11'] = 0.00
load_avg['tcn12'] = 0.00

load_avg['cluhadm'] = 0.00
load_avg['lcn01'] = 0.00
load_avg['lcn02'] = 0.00
load_avg['lcn03'] = 0.00
load_avg['lcn04'] = 4.00
load_avg['lcn05'] = 0.00
load_avg['lcn06'] = 0.00
load_avg['lcn07'] = 2.00
load_avg['lcn08'] = 0.00
load_avg['lcn09'] = 0.00
load_avg['lcn10'] = 0.00
load_avg['lcn11'] = 0.00
load_avg['lcn12'] = 0.00
load_avg['lcn13'] = 0.00
load_avg['lcn14'] = 0.00
load_avg['lcn15'] = 0.00
load_avg['lcn16'] = 0.00

from subprocess import *
import time

# get the current uptime of each host
for host in host_list:
    hostname = host.get_hostname()
    one_min_avg = 0.0
    if not testing:
        # get the uptime from the host
        command = "ssh %s@%s uptime" % (username, hostname)
        subproc = Popen(command, shell=True, stdin=PIPE, stdout=PIPE)
        (child_stdin, child_stdout) = (subproc.stdin, subproc.stdout)
        child_pid = subproc.pid
        # check if the child has terminated
        sleep_counter = 0
        while sleep_counter < 30:
            poll_result = subproc.poll()
            if poll_result is not None:
                break
            else:
                time.sleep(1)
                sleep_counter += 1
                print "Waiting... %d s" % sleep_counter

        # if we've waited too long, kill the process
        if sleep_counter == 30:
            kill_cmd = "kill -15 %d" % child_pid
            killproc = Popen(kill_cmd, shell=True, stdin=PIPE, stdout=PIPE)
            if killproc.poll() is None:
                kill_cmd = "kill -9 %d" % child_pid
                killproc = Popen(kill_cmd, shell=True, stdin=PIPE, stdout=PIPE)

            #subproc.kill()  # only from python 2.6
            host.set_host_down()   # label the host as down
        else:
            cmd_output = child_stdout.read()

            # just get the 1 minute load average
            uptime_regex = re.compile("load average:\s+(\d+\.\d{2}),")
            if uptime_regex.search(cmd_output) is None:
                one_min_avg = 0.0
            else:
                one_min_avg = uptime_regex.search(cmd_output).group(1)
    else:
        one_min_avg = load_avg[hostname]

    host.set_load_avg(float(one_min_avg))
    print hostname, one_min_avg
    if host.is_down():
        print "Node marked as down:", hostname

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

title_text = "RRZN Cluster Load Status: %s" % now

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
num_colors = 256
lut.SetNumberOfColors(num_colors)
refLut.SetNumberOfColors(num_colors)
lut.SetTableRange(0.0, 1.75)
refLut.SetTableRange(0.0, 1.75)
lut.Build()
refLut.Build()
for j in range(num_colors):
    lut.SetTableValue(j, refLut.GetTableValue(num_colors-1-j))

# get the colours
rgb = [0.0, 0.0, 0.0]
for host in host_list:
    hostname = host.get_hostname()
    host_load = host.get_load_avg()
    max_host_load = host.get_max_load()
    lut.GetColor(host_load/max_host_load, rgb)
    host.set_rgb(rgb)

# set up the scalar bar
scalar_bar = vtk.vtkScalarBarActor()
scalar_bar.SetLookupTable(lut)
scalar_bar.SetTitle("Scaled Load")
scalar_bar.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
if three_d_view:
    scalar_bar.GetPositionCoordinate().SetValue(0.1, 0.8)
    scalar_bar.SetOrientationToHorizontal()
    scalar_bar.SetWidth(0.8)
    scalar_bar.SetHeight(0.1)
else:
    scalar_bar.GetPositionCoordinate().SetValue(0.9, 0.1)
    scalar_bar.SetOrientationToVertical()
    scalar_bar.SetWidth(0.1)
    scalar_bar.SetHeight(0.8)

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
if three_d_view:
    renderer.GetActiveCamera().Azimuth(140)
    renderer.GetActiveCamera().Elevation(30)
    renderer.GetActiveCamera().Zoom(1.3)
else:
    renderer.GetActiveCamera().Azimuth(180)
    renderer.GetActiveCamera().Elevation(90)
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
    if three_d_view:
        out_writer.SetFileName("cluster_load_status.png")
    else:
        out_writer.SetFileName("cluster_load_status_2d.png")

    # render the window to save it to file
    render_window.Render()
    out_writer.Write()

    # and write out a file with the current date on it
    from datetime import datetime
    date = datetime.now()
    date_str = date.strftime("%Y%m%d_%H%M")
    if three_d_view:
        fname_str = "cluster_load_status_%s.png" % (date_str)
    else:
        fname_str = "cluster_load_status_2d_%s.png" % (date_str)
    out_writer.SetFileName(fname_str)

    # save it to file
    out_writer.Write()

# vim: expandtab shiftwidth=4:
