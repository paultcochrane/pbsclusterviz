#!/usr/bin/env python

# $Id: cluster_status.py 28 2009-04-24 15:27:36Z cochrane $

import vtk

class ComputeHost(object):
    def __init__(self,
            hostname = "",
            max_load = 0.0,
            xy_pos = (0, 0),
            three_d_view = None,
            ):
        self.hostname = hostname
        self.max_load = max_load
        self.load_avg = 0.0
        self.up_state = True  # assume the host is up
        self.grid_x_pos = float(xy_pos[0])
        self.grid_y_pos = float(xy_pos[1])
        self.rgb = [ 0.0, 0.0, 0.0 ]
        self.grid_scale = 6.0
        self.box_scale = 4.0
        self.three_d_view = three_d_view

    def get_hostname(self):
        return self.hostname

    def set_hostname(self, hostname):
        self.hostname = hostname

    def get_max_load(self):
        return self.max_load

    def set_max_load(self, max_load):
        self.max_load = max_load

    def get_load_avg(self):
        return self.load_avg

    def set_load_avg(self, load_avg):
        self.load_avg = load_avg

    def is_down(self):
        return not self.up_state

    def set_host_down(self):
        self.up_state = False

    def get_rgb(self):
        return self.rgb

    def set_rgb(self, rgb):
        self.rgb[0] = rgb[0]
        self.rgb[1] = rgb[1]
        self.rgb[2] = rgb[2]

    def get_box_height(self):
        if self.three_d_view:
            return self.box_scale*self.load_avg/self.max_load
        else:
            return 0.0

    def get_box_width(self):
        return self.box_scale

    def get_grid_x_pos(self):
        return self.grid_x_pos

    def set_grid_x_pos(self, grid_x_pos):
        self.grid_x_pos = float(grid_x_pos)

    def get_grid_y_pos(self):
        return self.grid_y_pos

    def set_grid_y_pos(self, grid_y_pos):
        self.grid_y_pos = float(grid_y_pos)

    def set_grid_xy_pos(self, grid_x_pos, grid_y_pos):
        self.set_grid_x_pos(grid_x_pos)
        self.set_grid_y_pos(grid_y_pos)

    def add_box(self, renderer):
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

        # if the host is down make the colour white
        if self.is_down():
            [r, g, b] = [1.0, 1.0, 1.0]
        else:
            [r, g, b] = self.get_rgb()
        voxel_actor = vtk.vtkActor()
        voxel_actor.SetMapper(voxel_mapper)
        voxel_actor.GetProperty().SetDiffuseColor(r, g, b)
        renderer.AddActor(voxel_actor)

    def add_label(self, renderer):
        # make a label for the box
        host_label = vtk.vtkTextMapper()
        host_label.SetInput(self.get_hostname())

        # use the relevant text properties
        host_label_prop = host_label.GetTextProperty()
        host_label_prop.ShallowCopy(host_label_prop)
        host_label_prop.SetJustificationToCentered()
        host_label_prop.SetVerticalJustificationToTop()
        host_label_prop.SetFontSize(8)
        host_label_prop.BoldOn()
        host_label_prop.SetFontFamilyToCourier()
        host_label_prop.SetOpacity(1.0)

        # make the actor for the label
        box_width = self.get_box_width()
        x_pos = -self.grid_scale*self.get_grid_x_pos()
        y_pos = -self.grid_scale*self.get_grid_y_pos()-box_width*1.2
        z_pos = self.get_box_height()

        host_label_actor = vtk.vtkTextActor3D()
        host_label_actor.SetPosition(x_pos, z_pos, y_pos)
        host_label_actor.SetInput(self.get_hostname())
        host_label_actor.SetScale(0.1, 0.1, 0.1)
        host_label_actor.SetTextProperty(host_label_prop)
        if self.three_d_view:
            host_label_actor.SetOrientation(30, 180, 0)
        else:
            host_label_actor.SetOrientation(90, 180, 0)

        renderer.AddActor(host_label_actor)

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
                host_label_actor.SetOrientation(30, 180, 0)
            else:
                host_label_actor.SetOrientation(90, 180, 0)

            renderer.AddActor(down_label_actor)

# vim: expandtab shiftwidth=4:
