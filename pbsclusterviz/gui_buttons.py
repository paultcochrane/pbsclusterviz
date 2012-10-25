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

from vtk import vtkRectangularButtonSource, vtkTextActor, \
                vtkRenderer

class GuiButtons(object):
    """
    Holds sources and actors for all buttons.
    """
    def __init__(self, clusterviz_config, iren):
        txt="Refresh"
        self.refresh=vtkTextActor()
        self.refresh.SetInput(txt)
        self.refresh.GetTextProperty().SetFontSize(15)
        self.refresh.GetPositionCoordinate().SetValue(3, 4)
        txt="Reset Camera"
        self.reset=vtkTextActor()
        self.reset.SetInput(txt)
        self.reset.GetTextProperty().SetFontSize(15)
        self.reset.GetPositionCoordinate().SetValue(80, 3)
        self.load_job=vtkTextActor()
        self.load_job.GetTextProperty().SetFontSize(15)
        self.load_job.GetPositionCoordinate().SetValue(209, 3)
        if clusterviz_config.get_display_mode() == "job":
            txt="Load View"
            self.load_job.SetInput(txt)
        elif clusterviz_config.get_display_mode() == "load":
            txt="Job View"
            self.load_job.SetInput(txt)
        txt="Quit"
        self.quit=vtkTextActor()
        self.quit.SetInput(txt)
        self.quit.GetTextProperty().SetFontSize(15)
        self.quit.GetPositionCoordinate().SetValue(309, -1)

        self.renderer = vtkRenderer()
        self.renderer.AddActor(self.refresh)
        self.renderer.AddActor(self.reset)
        self.renderer.AddActor(self.load_job)
        self.renderer.AddActor(self.quit)

        self.clusterviz_config = clusterviz_config
        self.iren = iren

    def get_renderer(self):
        return self.renderer

    def click(self, clickpos):
        h = self.clusterviz_config.get_window_height()
        if clickpos[1] > h-20:
            if clickpos[0] < 60:
                print "refresh"
            elif 190 > clickpos[0] > 70:
                print "reset"
            elif 290 > clickpos[0] > 206:
                print "load/view switch"
            elif 425 > clickpos[0] > 307:
                self.iren.GetRenderWindow().Finalize()
                self.iren.TerminateApp()
        else:
            print clickpos[0]
            print clickpos[1]

# vim: expandtab shiftwidth=4:
