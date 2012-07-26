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
import numpy as np
import matplotlib.pyplot as plt
gdal.UseExceptions() #enable exception handling

class landclass:
    """Defines the base characteristics of a land"""

    def __init__(self):
        """Constructor"""
        self._raster = None
        self._is_open = False
        self._classified = None
        self._classes = []
        self._name = ''
        self._file = ''
    
    def show(self,figure_handle,classified=True):
        
        if not classified:
            r = self._raster
        else:
            r = self._classified
        
        h=figure_handle.imshow(r)
        #cb=figure_handle.colorbar()
        
        #if classified:
            #cb.set_ticks( list(range(1,self.get_nclasses()+1)))
            #cb.set_ticklabels(self.get_classes_str())
            
        #figure_handle.draw()
        
    def open(self,fname,name):
        self._raw = gdal.Open(fname)
        self._raster = np.array(self._raw.GetRasterBand(1).ReadAsArray())        
        self._name = name
        self._is_open = True
        self._fname = fname
        
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
        
    def get_classraster(self):
        """Returns the classified raster"""
        return self._classified
    
    def get_raster(self):
        return self._raster
    
    def get_gdalraster(self):
        return self._raw

    def name(self):
        return self._name
    def get_file_name(self):
        return self._fname
    
    def get_classes(self):
        return self._classes
    
    def get_classes_str(self):
        y=np.array(["%.0f" % w for w in self.get_classes().reshape(self.get_classes().size)])
        y=y.reshape(self.get_classes().shape)
        x=[]
        for i in range(self._nclass):
            x.append(str(y[i,0]) + '--' + str(y[i,1]))
        return x
    
    def get_nclasses(self):
        return self._nclass
    
    def classify(self, nclass=2):
        #inspired by http://svn.osgeo.org/gdal/trunk/gdal/swig/python/samples/classify.py
        
        if not self._is_open:
            raise Exception('Raster not open')
        if nclass <=0:
            raise Exception('Number of classes must be >0')
    
        self._nclass = nclass
        #create the bins 
        hist, edges = np.histogram(self._raster, bins=nclass)
        classes= np.zeros([nclass,2])
        output = np.zeros([self.ysize(),self.xsize()])
        
        #create a 2*n matrix to hold the edges for use in np
        for i in range(0,nclass):
            classes[i,:] = [edges[i],edges[i+1]]    
            
            c_value = np.ones([self.ysize(),self.xsize()]) * (i+1)
            c_start = edges[i]
            c_end   = edges[i+1]
            src = self._raster
            mask = np.bitwise_and(
                               np.greater_equal(src,c_start),
                               np.less_equal(src,c_end))
                       
            output = np.choose( mask, (output, c_value) )               
            
        self._classified = output
        self._classes = classes
        
    def save_to_file(self,fname):
        pass
    
    