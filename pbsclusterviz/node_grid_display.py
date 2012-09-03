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
The NodeGridDisplay class

Controls various display aspects of a node grid
"""

from vtk import vtkLookupTable, vtkScalarBarActor, vtkTextProperty, \
        vtkTextActor, vtkGraphicsFactory, vtkWindowToImageFilter, \
        vtkPNGWriter, vtkRenderWindow
import re, sys, os, datetime, time

class NodeGridDisplay(object):
    """
    The NodeGridDisplay class
    """
    def __init__(self):
        # initialize the class variables:
        self.scalar_bar = vtkScalarBarActor()
        self.utilisation_actor = vtkTextActor()
        self.title_actor = vtkTextActor()
    
    def get_lookup_table(self, display_mode):
        """
        Sets up and returns the lookup table depending upon the display mode
        """
        lut = vtkLookupTable()
        ref_lut = vtkLookupTable()
        num_colours = 256
        lut.SetNumberOfColors(num_colours)
        ref_lut.SetNumberOfColors(num_colours)

        if (display_mode == 'load'):
            lut.SetTableRange(0.0, 1.75)
            ref_lut.SetTableRange(0.0, 1.75)
        else:
            lut.SetTableRange(0.0, 1.0)
            ref_lut.SetTableRange(0.0, 1.0)

        lut.Build()
        ref_lut.Build()

        # invert the colours: we want red to be at the high end
        for j in range(num_colours):
            lut.SetTableValue(j, ref_lut.GetTableValue(num_colours-1-j))

        return lut

    def set_scalar_bar(self, display_mode):
        """
        Sets up the scalar bar display actor
        """
        scalar_bar_position = self.scalar_bar.GetPositionCoordinate()
        scalar_bar_position.SetCoordinateSystemToNormalizedDisplay()
        self.scalar_bar.SetLookupTable(self.get_lookup_table(display_mode))

        self.scalar_bar.SetTitle(self.get_scalar_bar_title(display_mode))

        self.scalar_bar.GetPositionCoordinate().SetValue(0.1, 0.8)
        self.scalar_bar.SetOrientationToHorizontal()
        self.scalar_bar.SetWidth(0.8)
        self.scalar_bar.SetHeight(0.1)

        scalar_bar_title_prop = self.scalar_bar.GetTitleTextProperty()
        scalar_bar_title_prop.SetFontFamilyToCourier()
        scalar_bar_title_prop.SetFontSize(6)
        scalar_bar_title_prop.ItalicOff()

        scalar_bar_label_prop = self.scalar_bar.GetLabelTextProperty()
        scalar_bar_label_prop.SetFontFamilyToCourier()
        scalar_bar_label_prop.SetFontSize(4)
        scalar_bar_label_prop.ItalicOff()

    def get_scalar_bar(self):
        return self.scalar_bar

    def get_scalar_bar_title(self, display_mode):
        """
        Returns the scalar bar's title dependent upon the display mode
        """
        if display_mode == 'job':
            scalar_bar_title = "Job Fill Level"
        else:
            scalar_bar_title = "Scaled Load"

        return scalar_bar_title

    def get_default_text_prop(self):
        """
        Sets up and returns the default text properties for text display
        """
        # set up the default text properties for nice text
        font_size = 10
        text_prop = vtkTextProperty()
        text_prop.SetFontSize(font_size)
        text_prop.SetFontFamilyToArial()
        text_prop.BoldOff()
        text_prop.ItalicOff()
        text_prop.ShadowOff()

        return text_prop

    def set_utilisation_actor(self, display_mode, node_grid):
        """
        Sets up and returns the display actor for the utilisation text
        """
        # add the utilisation text to the image
        if display_mode == 'load':
            utilisation_value = node_grid.get_load_utilisation() * 100
        else:
            utilisation_value = node_grid.get_job_utilisation() * 100
        utilisation_text = "System utilisation: %0.2f %%" % utilisation_value

        self.utilisation_actor.SetInput(utilisation_text)
        utilisation_actor_position = self.utilisation_actor.GetPositionCoordinate()
        utilisation_actor_position.SetCoordinateSystemToNormalizedDisplay()
        utilisation_actor_position.SetValue(0.5, 0.92)

        utilisation_prop = self.utilisation_actor.GetTextProperty()
        utilisation_prop.ShallowCopy(self.get_default_text_prop())
        utilisation_prop.SetJustificationToCentered()
        utilisation_prop.SetVerticalJustificationToTop()
        utilisation_prop.SetFontSize(16)
        utilisation_prop.SetColor(1, 1, 1)
        utilisation_prop.BoldOn()

    def get_utilisation_actor(self):
        return self.utilisation_actor

    def get_utilisation_text(self, display_mode, node_grid):
        """
        Return the utilisation text depending upon display mode
        """
        utilisation_value = 0.0
        if display_mode == 'load':
            utilisation_value = node_grid.get_load_utilisation() * 100
        else:
            utilisation_value = node_grid.get_job_utilisation() * 100 
        utilisation_text = "System utilisation: %0.2f %%" % utilisation_value

        return utilisation_text

    def set_title_actor(self, clusterviz_config):
        """
        Sets up and returns the display actor for the title text
        """
        # add a title to the image
        self.title_actor.SetInput(self.get_title_text(clusterviz_config))
        title_actor_position = self.title_actor.GetPositionCoordinate()
        title_actor_position.SetCoordinateSystemToNormalizedDisplay()
        title_actor_position.SetValue(0.5, 0.95)

        title_prop = self.title_actor.GetTextProperty()
        title_prop.ShallowCopy(self.get_default_text_prop())
        title_prop.SetJustificationToCentered()
        title_prop.SetVerticalJustificationToTop()
        title_prop.SetFontSize(20)
        title_prop.SetColor(1, 1, 1)
        title_prop.BoldOn()

    def get_title_actor(self):
        return self.title_actor

    def get_title_text(self, clusterviz_config):
        """
        Returns the title text depending upon display mode
        """
        xml = clusterviz_config.get_xml_file()
        if xml is not None and os.path.isfile(xml):
            mtime = time.localtime(os.path.getmtime(xml))
            mtime = time.strftime("%d.%m.%Y um %H:%M:%S Uhr", mtime) 
        else:
            mtime = "N.a."

        config_parser = clusterviz_config.get_config_parser()
        config_segment = clusterviz_config.get_display_mode() + " viewer"
        if config_parser.has_option(config_segment, 'title' ):
            title_text = config_parser.get(config_segment, 'title' )
        else:
            title_text = "pbsclusterviz"
        title_text = "%s: %s" % (title_text, mtime)

        return title_text

    def save_render_window(self, render_window, clusterviz_config, \
            display_mode):
        """
        Save the current render window to file
        """
        # make sure we're using the mesa classes when saving to file
        fact_graphics = vtkGraphicsFactory()
        fact_graphics.SetUseMesaClasses(1)
        fact_graphics.SetOffScreenOnlyMode(1)

        render_window.OffScreenRenderingOn()
        # to save the file to png, need to pass the render window
        # through a filter to an image object
        win2img_filter = vtkWindowToImageFilter()
        win2img_filter.SetInput(render_window)

        output_file = clusterviz_config.get_output_file(display_mode)

        # work out the output file name's base name (the bit without .png)
        base_regex = re.compile(r'(.*?)\.\w+$')
        basename_search_result = base_regex.search(output_file)
        if basename_search_result.group(1) is None:
            self.logger.critical("Unable to determine the base image output file name.")
            sys.exit(1)

        output_file_basename = basename_search_result.group(1)

        out_writer = vtkPNGWriter()
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
