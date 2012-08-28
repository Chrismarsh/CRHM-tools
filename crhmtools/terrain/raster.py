#Copyright (C) 2012  Chris Marsh

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import gdal
import matplotlib.pyplot as plt
gdal.UseExceptions() #enable exception handling

class raster(object):
    """Defines the base characteristics of a land"""

    def __init__(self):
        """Constructor"""
        self._raster = None
        self._is_open = False
        self._file = ''

    
    def show(self,figure_handle):
        
        r = self._raster

        h=figure_handle.imshow(r)
        
        
    def open(self,fname):
        self._raw = gdal.Open(fname)
        self._raster = np.array(self._raw.GetRasterBand(1).ReadAsArray())        
        self._is_open = True
        self._fname = fname
    def get_resolution(self):
        geotransform = self._raw.GetGeoTransform()
        return [geotransform[1],geotransform[5]]
    
    #Returns the x size
    def xsize(self):
        return self._raw.RasterXSize
    #Returns the y size
    def ysize(self):
        return self._raw.RasterYSize       
    def size(self):
        return [self._raw.RasterYSize, self._raw.RasterXSize]    
    #Returns True is a raster has been loaded
    def is_open(self):
        if self._raw is None:
            return False
        else:
            return True
      
    
    def get_raster(self):
        return self._raster
    
    def get_gdalraster(self):
        return self._raw

    def get_path(self):
        return self._fname
        
    def save_to_file(self,fname):
        pass
    
    def __call__(self,row,col):
        return self._raster[x,y]
    