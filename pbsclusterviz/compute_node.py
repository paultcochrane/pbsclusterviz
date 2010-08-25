#!/usr/bin/env python

"""
File containing the ComputeNode class
"""

import vtk
import sys

class ComputeNode(object):
    """
    The ComputeNode class

    ComputeNodes contain information about a node's load, maximum possible
    number of jobs, current number of jobs and where it is to be displayed
    on the node load and job spread matrices.
    """
    def __init__(self,
            hostname = "",
            max_load = 0.0,
            max_jobs = 0,
            num_jobs = 0,
            xy_pos = (0, 0),
            three_d_view = None,
            display_mode = "load",   # by default return the load
            ):
        self.hostname = hostname
        self.max_load = max_load
        self.max_jobs = max_jobs
        self.num_jobs = num_jobs
        self.load_avg = 0.0
        self.up_state = True  # assume the node is up
        self.grid_x_pos = float(xy_pos[0])
        self.grid_y_pos = float(xy_pos[1])
        self.rgb = [ 0.0, 0.0, 0.0 ]
        self.grid_scale = 6.0
        self.box_scale = 4.0
        self.three_d_view = three_d_view
        self.display_mode = display_mode

    def get_display_mode(self):
        """
        Return the current display mode.  Can be either "load" or "jobs"
        """
        return self.display_mode

    def set_display_mode(self, display_mode):
        """
        Set the current display mode.  Can be either "load" or "jobs"

        @param display_mode: the display mode to set
        @type display_mode: string
        """
        self.display_mode = display_mode

    def get_hostname(self):
        """
        Return the node's hostname
        """
        return self.hostname

    def set_hostname(self, hostname):
        """
        Set the node's hostname

        @param hostname: the hostname to set
        @type hostname: string
        """
        self.hostname = hostname

    def get_max_load(self):
        """
        Return the node's maximum load
        """
        return self.max_load

    def set_max_load(self, max_load):
        """
        Set the node's maximum load

        @param max_load: the load to set
        @type max_load: float
        """
        self.max_load = max_load

    def get_max_jobs(self):
        """
        Return the maximum number of jobs the node can run
        """
        return self.max_jobs

    def set_max_jobs(self, max_jobs):
        """
        Set the node's maximum number of jobs

        @param max_jobs: the maximum number of jobs
        @type max_jobs: integer
        """
        self.max_jobs = max_jobs

    def get_num_jobs(self):
        """
        Return the current number of jobs running on the node
        """
        return self.num_jobs

    def set_num_jobs(self, num_jobs):
        """
        Set the number of jobs currently running on the nodes

        @param num_jobs: the currently running number of jobs
        @type num_jobs: integer
        """
        self.num_jobs = num_jobs

    def get_load_avg(self):
        """
        Return the node's current load average
        """
        return self.load_avg

    def set_load_avg(self, load_avg):
        """
        Set the node's current load average

        @param load_avg: the current load average
        @type load_avg: float
        """
        self.load_avg = float(load_avg)

    def is_down(self):
        """
        Returns true if the node is down
        """
        return not self.up_state

    def set_node_down(self):
        """
        Set the node to be in the 'down' state
        """
        self.up_state = False

    def get_rgb(self):
        """
        Return the rgb colour value currently assigned to the node as a list
        """
        return self.rgb

    def set_rgb(self, rgb):
        """
        Set the rgb colour value list for the node.

        The list is organised as follows: [red, green, blue] (but you
        probably guessed that)

        @param rgb: the list of rgb values
        @type rgb: list of floats
        """
        self.rgb[0] = rgb[0]
        self.rgb[1] = rgb[1]
        self.rgb[2] = rgb[2]

    def get_box_height(self):
        """
        Return the height of the box representing the node in the load
        matrix.
        """
        if self.get_display_mode() == "load":
            if self.three_d_view:
                return self.box_scale*self.load_avg/self.max_load
            else:
                return 0.0
        elif self.get_display_mode() == "jobs":
            return self.box_scale*float(self.get_num_jobs())/float(self.get_max_jobs())
        else:
            print "Unknown display mode %s" % self.get_display_mode()
            sys.exit(1)

    def get_box_width(self):
        """
        Return the width of the box representing the node in the load or job
        matrix.
        """
        return self.box_scale

    def get_grid_x_pos(self):
        """
        Return the x position of the node box within the grid
        """
        return self.grid_x_pos

    def set_grid_x_pos(self, grid_x_pos):
        """
        Set the x position of the node box within the grid

        @param grid_x_pos: the grid x position
        @type grid_x_pos: integer
        """
        self.grid_x_pos = float(grid_x_pos)

    def get_grid_y_pos(self):
        """
        Return the y position of the node box within the grid
        """
        return self.grid_y_pos

    def set_grid_y_pos(self, grid_y_pos):
        """
        Set the y position of the node box within the grid

        @param grid_y_pos: the grid y position
        @type grid_y_pos: integer
        """
        self.grid_y_pos = float(grid_y_pos)

    def set_grid_xy_pos(self, grid_x_pos, grid_y_pos):
        """
        Set the x-y position of the node box within the grid

        @param grid_x_pos: the grid x position
        @type grid_x_pos: integer
        @param grid_y_pos: the grid y position
        @type grid_y_pos: integer
        """
        self.set_grid_x_pos(grid_x_pos)
        self.set_grid_y_pos(grid_y_pos)

    def add_box(self, renderer):
        """
        Add a box to the given renderer object

        @param renderer: the vtk renderer
        @type renderer: vtk renderer object
        """
        # set up the box to display
        voxel_points = vtk.vtkPoints()
        voxel_points.SetNumberOfPoints(8)
        box_height = self.get_box_height() # z-axis
        box_width = self.get_box_width()

        x_pos_1 = -self.grid_scale*self.get_grid_x_pos()
        y_pos_1 = -self.grid_scale*self.get_grid_y_pos()
        x_pos_2 = -(self.grid_scale*self.get_grid_x_pos()+box_width)
        y_pos_2 = -(self.grid_scale*self.get_grid_y_pos()+box_width)

        voxel_points.InsertPoint(0, x_pos_1, 0, y_pos_1)
        voxel_points.InsertPoint(1, x_pos_2, 0, y_pos_1)
        voxel_points.InsertPoint(2, x_pos_1, 0, y_pos_2)
        voxel_points.InsertPoint(3, x_pos_2, 0, y_pos_2)
        voxel_points.InsertPoint(4, x_pos_1, box_height, y_pos_1)
        voxel_points.InsertPoint(5, x_pos_2, box_height, y_pos_1)
        voxel_points.InsertPoint(6, x_pos_1, box_height, y_pos_2)
        voxel_points.InsertPoint(7, x_pos_2, box_height, y_pos_2)

        voxel = vtk.vtkVoxel()
        voxel.GetPointIds().SetId(0, 0)
        voxel.GetPointIds().SetId(1, 1)
        voxel.GetPointIds().SetId(2, 2)
        voxel.GetPointIds().SetId(3, 3)
        voxel.GetPointIds().SetId(4, 4)
        voxel.GetPointIds().SetId(5, 5)
        voxel.GetPointIds().SetId(6, 6)
        voxel.GetPointIds().SetId(7, 7)

        voxel_grid = vtk.vtkUnstructuredGrid()
        voxel_grid.Allocate(1, 1)
        voxel_grid.InsertNextCell(voxel.GetCellType(), voxel.GetPointIds())
        voxel_grid.SetPoints(voxel_points)

        voxel_mapper = vtk.vtkDataSetMapper()
        voxel_mapper.SetInput(voxel_grid)

        # if the node is down make the colour white
        if self.is_down():
            [r, g, b] = [1.0, 1.0, 1.0]
        else:
            [r, g, b] = self.get_rgb()
        voxel_actor = vtk.vtkActor()
        voxel_actor.SetMapper(voxel_mapper)
        voxel_actor.GetProperty().SetDiffuseColor(r, g, b)
        renderer.AddActor(voxel_actor)

    def add_label(self, renderer):
        """
        Add a label to the given renderer.  This actually adds a label to
        the box within the load or job matrix

        @param renderer: the vtk renderer to add the label to
        @type renderer: vtk renderer object
        """
        # make a label for the box
        node_label = vtk.vtkTextMapper()
        node_label.SetInput(self.get_hostname())

        # use the relevant text properties
        node_label_prop = node_label.GetTextProperty()
        node_label_prop.ShallowCopy(node_label_prop)
        node_label_prop.SetJustificationToCentered()
        node_label_prop.SetVerticalJustificationToTop()
        node_label_prop.SetFontSize(8)
        node_label_prop.BoldOn()
        node_label_prop.SetFontFamilyToCourier()
        node_label_prop.SetOpacity(1.0)

        # make the actor for the label
        box_width = self.get_box_width()
        x_pos = -self.grid_scale*self.get_grid_x_pos()
        y_pos = -self.grid_scale*self.get_grid_y_pos()-box_width*1.2
        z_pos = self.get_box_height()

        node_label_actor = vtk.vtkTextActor3D()
        node_label_actor.SetPosition(x_pos, z_pos, y_pos)
        node_label_actor.SetInput(self.get_hostname())
        node_label_actor.SetScale(0.1, 0.1, 0.1)
        node_label_actor.SetTextProperty(node_label_prop)
        if self.three_d_view:
            node_label_actor.SetOrientation(30, 180, 0)
        else:
            node_label_actor.SetOrientation(90, 180, 0)

        renderer.AddActor(node_label_actor)

        # if we're down, add a label to say as much
        if self.is_down():
            # make a label for the box
            down_label = vtk.vtkTextMapper()
            down_label.SetInput(self.get_hostname())

            # use the relevant text properties
            down_label_prop = down_label.GetTextProperty()
            down_label_prop.ShallowCopy(down_label_prop)
            down_label_prop.SetJustificationToCentered()
            down_label_prop.SetVerticalJustificationToTop()
            down_label_prop.SetFontSize(8)
            down_label_prop.BoldOn()
            down_label_prop.SetFontFamilyToCourier()
            down_label_prop.SetOpacity(1.0)

            # make the actor for the label
            box_width = self.get_box_width()
            x_pos = -self.grid_scale*self.get_grid_x_pos()-box_width*0.25
            y_pos = -self.grid_scale*self.get_grid_y_pos()-box_width*0.5
            z_pos = self.get_box_height()

            down_label_actor = vtk.vtkTextActor3D()
            down_label_actor.SetPosition(x_pos, z_pos, y_pos)
            down_label_actor.SetInput("down")
            down_label_actor.SetScale(0.1, 0.1, 0.1)
            down_label_actor.SetTextProperty(down_label_prop)
            if self.three_d_view:
                down_label_actor.SetOrientation(30, 180, 0)
            else:
                down_label_actor.SetOrientation(90, 180, 0)

            renderer.AddActor(down_label_actor)

# vim: expandtab shiftwidth=4:
