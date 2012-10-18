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
This class is responsible for user interface buttons that may be shown
on top of the visualisation.
"""

from vtk import vtkRectangularButtonSource, vtkPolyDataMapper, \
                vtkActor, vtkTextActor, vtkRenderer

class GuiButtons(object):
    """
    Holds sources and actors for all buttons.
    """
    def __init__(self, clusterviz_config):
        self.common_button_source = vtkRectangularButtonSource()
        self.common_button_source.SetWidth(2)
        self.common_button_source.SetHeight(1)
        self.common_button_source.SetDepth(0.1)
        self.common_button_source.SetCenter(0.0, 0.0, 1.0)
        self.common_button_source.SetBoxRatio(1.2)
        self.button_mapper = vtkPolyDataMapper()
        self.button_mapper.SetInput(self.common_button_source.GetOutput())
        self.load_jobs_button_actor = vtkActor()
        self.refresh_button_actor = vtkActor()
        self.reset_camera_button_actor = vtkActor()
        self.toggle_balloons_button_actor = vtkActor()

        self.load_jobs_button_actor.AddObserver('LeftButtonPressEvent', self.DummyFunc1)
        self.load_jobs_button_actor.SetMapper(self.button_mapper)
        self.button_renderer = vtkRenderer()
        self.button_renderer.AddActor(self.load_jobs_button_actor)
        #self.button_renderer.AddActor(button_actor)
        #self.button_renderer.AddActor(button_actor)
        #self.button_renderer.AddActor(button_actor)
        #self.button_renderer.AddActor(button_actor)
        #render_window.AddRenderer(button_renderer)

    def get_renderer(self):
        return self.button_renderer

    def DummyFunc1(obj, ev):
        print "Before Event"

# vim: expandtab shiftwidth=4:
