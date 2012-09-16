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
File containing the Node class
"""

from vtk import vtkCubeSource, vtkActor, vtkTextActor3D, \
        vtkPolyDataMapper, vtkTextMapper
import re, logging

class Node(object):
    """
    The Node class.
    Every node contains information about its name, capabilities,
    status and position in the grid.
    This information can be updated and visualized.
    """
    def __init__(self, text_log):
        self.name = ""
        self.x_pos = 0
        self.y_pos = 0
        self.height = 0.0
        self.max_load = 1
        self.max_jobs = 1
        self.up_state = True
        self.rgb = [ 0.0, 0.0, 0.0 ]
        self.grid_scale = 6.0
        self.box_scale = 4.0
        self.box_actor = vtkActor()
        self.label_actor = vtkTextActor3D()
        self.state = None
        self.num_processors = None
        self.properties = None
        self.jobs = []
        self.status = {}
        self.box = vtkCubeSource()
        self.norm_jobs = 0.0
        self.norm_load = 0.0
        self.text_log = text_log
        self.logger = logging.getLogger("")

    def get_name(self):
        """
        Return the name of the node
        """
        return self.name

    def set_name(self, node_name):
        """
        Set the name of the node
        """
        debug_msg = "Node name: %s" % node_name
        self.logger.debug(debug_msg)
        self.name = node_name

    def get_grid_location(self):
        """
        Return the node's x,y position in the grid
        """
        return (self.x_pos, self.y_pos)

    def set_grid_location(self, x_pos, y_pos):
        """
        Set the node's x,y position in the grid
        """
        debug_msg = "Node location: (%s, %s)" % (x_pos, y_pos)
        self.logger.debug(debug_msg)
        self.x_pos = x_pos
        self.y_pos = y_pos

    def get_num_processors(self):
        """
        Return the number of processors in the given node
        """
        return self.num_processors

    def init_box(self):
        """
        Routine to create an actor, which visualizes the load or the
        job status.
        """
        self.box.SetXLength(0.8)
        self.box.SetYLength(0.8)
        self.box.SetCenter((float(self.x_pos), float(self.y_pos), 0.0))
        box_mapper = vtkPolyDataMapper()
        box_mapper.SetInput(self.box.GetOutput())
        self.box_actor.SetMapper(box_mapper)

        return(self.box_actor)

    def update_box(self, display_mode, node_grid_display):
        """
        Updates the box describing the load/job status of a node
        """

        if self.state is not None and "down" in self.state:
            self.text_log.add_to_log(self.name + " down.")
            return self.get_grey_square()
        if self.state is not None and "offline" in self.state:
            self.text_log.add_to_log(self.name + " offline.")

        color = [ 0.0, 0.0, 0.0 ]
        lut = node_grid_display.get_lookup_table(display_mode)
        self.norm_load = self.get_load_avg()/float(self.max_load)
        if self.num_processors is not None:
            self.norm_jobs = float(len(self.jobs))/float(self.num_processors)
        if display_mode == 'load':
            # select color and height of the box according to the
            # current load
            lut.GetColor(self.norm_load, color)
            self.height = 0.6 * self.norm_load
        elif display_mode == 'job':
            lut.GetColor(self.norm_jobs, color)
            self.height = 0.6 * self.norm_jobs
        else:
            self.logger.error("Unknown display mode: ", display_mode)

        #Complain about job/load imbalance
        if abs(self.norm_load-self.norm_jobs) >= 0.2:
            self.text_log.add_to_log("Job/load imbalance on " + self.name)

        #Complain about overload
        if self.num_processors is not None:
            load_threshold = float(self.num_processors)*1.2
            if self.get_load_avg() > load_threshold:
                node_load_info = "node: %s, load = %f, threshold = %f" % \
                        (self.name, self.get_load_avg(), load_threshold)
                self.logger.debug(node_load_info)
                self.text_log.add_to_log(self.name + " overloaded.")

        self.box.SetZLength(self.height)
        self.box.SetCenter((float(self.x_pos), float(self.y_pos), self.height/2))
        self.box_actor.GetProperty().SetDiffuseColor(color)
        return self.box_actor

    def flat(self):
        """
        Utility function to help restore coplanarity of node boxes in display
        """
        self.box.SetCenter((float(self.x_pos), float(self.y_pos), self.height/2))

    def get_grey_square(self):
        """
        Creates and returns a grey square in order to denote "down" nodes
        """
        color = [ 0.5, 0.5, 0.5 ]
        self.box.SetZLength(0.0)
        self.box_actor.GetProperty().SetDiffuseColor(color)
        return self.box_actor

    def init_label(self):
        """
        Initialises the label for a box
        """
        # make a label for the box
        node_label = vtkTextMapper()
        node_label.SetInput(self.get_name())
        
        # use the relevant text properties
        node_label_prop = node_label.GetTextProperty()
        #node_label_prop.ShallowCopy(node_label_prop)
        node_label_prop.SetJustificationToCentered()
        node_label_prop.SetVerticalJustificationToTop()
        node_label_prop.SetFontSize(8)
        node_label_prop.BoldOn()
        node_label_prop.SetFontFamilyToCourier()
        node_label_prop.SetOpacity(1.0)

        # make the actor for the label
        self.label_actor.SetScale(0.02, 0.02, 0.02)
        self.label_actor.SetTextProperty(node_label_prop)
        self.label_actor.SetOrientation(30, 0, 0)

        self.update_label()
        return self.label_actor

    def update_label(self):
        """
        Updates the label of a box
        """
        self.label_actor.SetInput(self.get_name())
        self.label_actor.SetPosition(
                float(self.x_pos)-0.4, 
                float(self.y_pos)-0.4,
                float(self.height) + 0.1)
        return self.label_actor

    def get_balloon_text(self):
        """
        Generate and return the text used in the node's balloon
        """
        # Create a ballon which lists the name 
        # of the node and the currently running jobs
        load_avg = self.get_load_avg()
        percent_load = int(100 * load_avg/float(self.max_load))
        text = '%s: %d cores, %s%%\n' % \
                (self.get_name(), self.max_load, percent_load)
        if len(self.jobs) != 0:
            jobdict = {}
            for job in self.jobs: 
                matcher = re.match('.*/(\d*)\..*', job)
                if matcher:
                    jobname = matcher.group(1)
                    if jobname in jobdict.keys():
                        jobdict[ jobname ] += 1
                    else:
                        jobdict[ jobname ] = 1
                else:
                    self.logger.debug("Job not matched in regexp: " + job)

            for key in jobdict.keys():
                text += " %s - \t%s cores\n" % (str(key), str(jobdict[key]))
        else:
            text += 'no jobs'
        return text

    def get_load_avg(self):
        """
        Return a node's load average
        """
        if 'loadave' in self.status.keys():
            load_avg = float(self.status['loadave'])
        else:
            load_avg = 0
        return load_avg

    def get_box_actor(self):
        """
        Returns the actor (for display) of a box
        """
        return self.box_actor

# vim: expandtab shiftwidth=4:
