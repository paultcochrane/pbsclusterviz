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
This is a program to visualize the load status of a cluster 
using the output of pbsnodes
"""

import sys, getopt, logging, os
from pbsclusterviz import NodeGrid, NodeGridDisplay, ClustervizConfig, \
        TextLog, GuiButtons
from vtk import vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor, \
        vtkInteractorStyleTrackballCamera

class MyInteractorStyle(vtkInteractorStyleTrackballCamera):
    def __init__(self,parent=None):
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.AddObserver("MouseMoveEvent", self.MouseMoveEvent)
        self.AddObserver("LeftButtonReleaseEvent", self.LeftButtonReleaseEvent)
        self.MouseMotion = 0

    def leftButtonPressEvent(self, obj, ev):
        self.MouseMotion = 0
        self.OnLeftButtonDown()
        return
 
    def MouseMoveEvent(self, obj, ev):
        self.MouseMotion = 1
        self.OnMouseMove()
        return

    def LeftButtonReleaseEvent(self, obj, ev):
        if self.MouseMotion == 0:
            logging.debug("Klick detected.")
        else:
            logging.debug("Drag detected.")
        self.OnLeftButtonUp()
        return

def PostResetCamera(obj, event):
    active_camera = obj.GetActiveCamera()
    active_camera.Zoom(1.3)

### The interaction callback routines ################################
def key_input(obj, event, node_grid, node_grid_display, clusterviz_config, render_window, text_log):
    key_pressed = obj.GetKeySym()

    if key_pressed == 'j':
        # switch to job visualisation
        clusterviz_config.set_display_mode('job')
        logging.debug("switching to job display...")
    elif key_pressed == 'l':
        # switch to load visualisation
        clusterviz_config.set_display_mode('load')
        logging.debug("switching to load display...")
    elif key_pressed == 'u':
        # update the view to the current pbsnodes output
        logging.debug("updating...")
    else:
        return
    update_display(node_grid, node_grid_display, clusterviz_config, render_window, text_log)

def update_display(node_grid, node_grid_display, clusterviz_config, render_window, text_log):

    # system call to update the xml
    syscall(clusterviz_config)

    text_log.add_to_log("Updating ...")
    display_mode = clusterviz_config.get_display_mode()
    xml_file = clusterviz_config.get_xml_file()
    node_grid.update(xml_file, display_mode, node_grid_display)

    # update the scalar bar
    scalar_bar = node_grid_display.get_scalar_bar()
    scalar_bar.SetLookupTable(node_grid_display.get_lookup_table(display_mode))
    scalar_bar.SetTitle(node_grid_display.get_scalar_bar_title(display_mode))

    # update the utilisation text
    utilisation_text = \
            node_grid_display.get_utilisation_text(display_mode, node_grid)
    utilisation_actor = node_grid_display.get_utilisation_actor()
    utilisation_actor.SetInput(utilisation_text)

    # update the title text
    title_text = \
            node_grid_display.get_title_text(clusterviz_config)
    title_actor = node_grid_display.get_title_actor()
    title_actor.SetInput(title_text)

    # update the text log
    text_log.synch()

    # update window dimensions if needed
    size = render_window.GetSize()
    window_width = clusterviz_config.get_window_width()
    window_height = clusterviz_config.get_window_height()
    if (size[0] != window_width or size[1] != window_height):
        render_window.SetSize(window_width, window_height)

    render_window.Render()
    return

### The main program
def main():

    # set up a log output for critical errors
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)

    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    logger.addHandler(ch)

    # Read in the configuration
    clusterviz_config = ClustervizConfig()
    clusterviz_config.find_config_files()

    # parse the command line options
    handle_options(sys.argv[1:], clusterviz_config)

    clusterviz_config.read_config()

    # System call to update the xml
    syscall(clusterviz_config)

    # set up the renderer to create the images
    renderer = vtkRenderer()
    render_window = vtkRenderWindow()
    render_window.AddRenderer(renderer)
    window_width = clusterviz_config.get_window_width()
    window_height = clusterviz_config.get_window_height()
    render_window.SetSize(window_width, window_height)
    renderer.SetBackground(0, 0, 0)

    # get the current visualization mode
    display_mode = clusterviz_config.get_display_mode()
    logging.debug("Display mode = %s" % display_mode)

    # Create text log
    text_log = TextLog(clusterviz_config)

    # read in the nodes list
    node_grid = NodeGrid(text_log)
    node_grid.read_nodes_file(clusterviz_config.get_nodes_file(), text_log)

    # Collect the actors of the visualized loads from the nodes
    box_list = node_grid.init_boxes()

    # initialise the visualisation of the grid
    label_list = node_grid.init_labels()
    for label in label_list:
        renderer.AddActor(label)

    # get the title ready
    node_grid_display = NodeGridDisplay()
    node_grid_display.set_title_actor(clusterviz_config)
    renderer.AddActor(node_grid_display.get_title_actor())

    # read in the output of pbsnodes -x
    xml_file = clusterviz_config.get_xml_file()
    node_grid.update(xml_file, display_mode, node_grid_display)

    # now that we now more about them, we can choose boxes to show
    for box in box_list:
        if box.get_num_processors() is None:
            logging.error("Node " + box.get_name() + " not initialised correctly.")
        else:
            renderer.AddActor(box.init_box())

    # boxes now have heights and are no longer on one plane
    node_grid.flatten()

    # shows overall utilisation as text
    node_grid_display.set_utilisation_actor(display_mode, node_grid)
    renderer.AddActor(node_grid_display.get_utilisation_actor())

    # displays approximately corresponding colors to numerical values
    node_grid_display.set_scalar_bar(display_mode)
    renderer.AddActor(node_grid_display.get_scalar_bar())

    # set up the camera properly
    renderer.ResetCamera()
    active_camera = renderer.GetActiveCamera()
    active_camera.Elevation(-90)
    active_camera.SetViewUp(0, 0, 1)
    active_camera.Azimuth(-30)
    active_camera.Elevation(35)
    renderer.ResetCameraClippingRange()
    active_camera.Zoom(1.3)

    # add text log
    text_log.synch()
    renderer.AddActor(text_log.get_log_actor())

    if clusterviz_config.is_interactive():

        config_parser = clusterviz_config.get_config_parser()

        # set up the interactive render window stuff
        iren = vtkRenderWindowInteractor()
        iren.SetInteractorStyle(MyInteractorStyle())
        iren.SetRenderWindow(render_window)
        iren.AddObserver("KeyPressEvent", lambda obj, event:
            key_input(obj, event, node_grid, node_grid_display, clusterviz_config, render_window, text_log))

        # When the user presses 'r' zoom is set to 1. With this we set it to 1.3 again.
        renderer.AddObserver("ResetCameraEvent", PostResetCamera)

        if config_parser.has_option("main", "enable_gui_buttons"):
            if config_parser.getboolean("main", "enable_gui_buttons"):
                gui_buttons = GuiButtons(clusterviz_config)
                button_renderer = gui_buttons.get_renderer()
                # The screen is splitted to hold 2 renderes: Visualisation and GUI Buttons.
                renderer.SetViewport(0,0,1,0.96)
                button_renderer.SetViewport(0,0.96,1,1)
                render_window.AddRenderer(button_renderer)

        # we now have balloons on the nodes telling us what jobs are running where
        balloon_widget = node_grid.init_balloons()
        balloon_widget.SetInteractor(iren)

        # Render the scene and start interaction.
        iren.Initialize()

        if config_parser.has_option("main", "enable_balloons"):
            if config_parser.getboolean("main", "enable_balloons"):
                balloon_widget.On()
        else:
            balloon_widget.On()

        # Adding a timer to autonmously update the display
        if clusterviz_config.is_updating():
            if config_parser.has_option("main", "update_rate"):
                iren.CreateRepeatingTimer(config_parser.getint("main", "update_rate"))
            else:
                iren.CreateRepeatingTimer(10000)

            iren.AddObserver("TimerEvent", lambda o, e:
                update_display(node_grid, node_grid_display, clusterviz_config, render_window, text_log))

        render_window.Render()
        iren.Start()
    else:
        # write the displayed window to file
        node_grid_display.save_render_window(render_window, \
                clusterviz_config, display_mode)

# system call to update the xml
def syscall(clusterviz_config):
    if clusterviz_config.is_syscalling():
        config_parser = clusterviz_config.get_config_parser()
        if config_parser.has_option("main", "syscall"):
            syscall = config_parser.get("main", "syscall")
            os.system(syscall)
        else:
            logging.error("No system call specified in the config file.")

def usage():
    """
    Prints the usage information
    """
    print """Usage:
    cluster_status [options]
    
    options:
    [-h/--help]                  Print usage information and exit
    [-V/--version]               Print version information and exit
    [-d/--debug]                 Turn on debugging output
    [-l/--logfile=<filename>]    Specify an alternative log file name
    [-i/--interactive]           Turn on interactive behaviour (default on)
    [-N/--non_interactive]       Turn off interactive behaviour
    [-x/--xmlfile]               Specify an input pbsnodes xml file
    [-s/--syscall]               Issue system call at update to renew xml file
    [-o/--outfile=<filename>]    Specify an output image file
    [-c/--configfile=<filename>] Specify an input configuration file
    [-n/--nodesfile=<filename>]  Specify an alternate nodes file
    [-m/--display_mode=<mode>]   Specify either 'job' or 'load' display mode
    """

def version():
    """
    Prints version information
    """
    print """cluster_status version 0.7a"""

def handle_options(args, clusterviz_config):
    logger = logging.getLogger("")
    # handle the command line options
    try:
        options_list, args_list = getopt.getopt(
                args, "hVdiNsl:x:o:c:n:m:",
                ["help", "version", "debug", 
                    "interactive", "non_interactive", 
                    "syscall", "logfile=",
                    "xmlfile=", "outfile=", 
                    "configfile=", "nodesfile=", 
                    "debug", 'display_mode='])
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)

    # parse the command line options
    for option, arg in options_list:
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        elif option in ("-V", "--version"):
            version()
            sys.exit()
        elif option in ("-d", "--debug"):
            logger = logging.getLogger("")
            #create console handler
            ch = logging.StreamHandler()
            logger.addHandler(ch)
            logger.debug("Debugging switched on")
        elif option in ("-i", "--interactive"):
            clusterviz_config.set_interactive_mode(True)
        elif option in ("-N", "--non_interactive"):
            clusterviz_config.set_interactive_mode(False)
        elif option in ("-s", "--syscall"):
            clusterviz_config.set_syscalling(True)
        elif option in ("-l", "--logfile"):
            logger = logging.getLogger("")
            #create file handler
            filehandler = logging.FileHandler(arg)
            logger.addHandler(filehandler)
            logger.debug("Logfile " + arg + " created.")
            clusterviz_config.set_log_file(arg)
        elif option in ("-x", "--xmlfile"):
            clusterviz_config.set_xml_file(arg)
        elif option in ("-o", "--outfile"):
            clusterviz_config.output_file_chosen = True
            clusterviz_config.set_output_file(arg)
        elif option in ("-c", "--configfile"):
            clusterviz_config.set_config_file(arg)
        elif option in ("-n", "--nodesfile"):
            clusterviz_config.set_nodes_file(arg)
        elif option in ("-m", "--display_mode"):
            clusterviz_config.set_display_mode(arg)
        else:
            logger.critical("Unknown option %s" % option)
            sys.exit(2)

    if len(args_list) > 2:
        logger.critical("Too many arguments")
        usage()
        sys.exit(2)

### run the main program #############################################
main()

# vim: expandtab shiftwidth=4:
