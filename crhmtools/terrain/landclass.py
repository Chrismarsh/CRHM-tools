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
from raster import *

class landclass(raster):
    """Defines the base characteristics of a land"""

    def __init__(self):
        """Constructor"""
        super(landclass,self).__init__()
        self._classified = None
        self._classes = []
        self._name = ''
        self._creator='None'
        self._nclass=0

    
    def show(self,figure_handle,classified=True):
        
        if not classified:
            super(landclass,self).show(figure_handle)
        else:
            r = self._classified
            h=figure_handle.imshow(r)
    def get_creator(self):
        return self._creator
    def set_creator(self,name):
        self._creator = name
    def get_classraster(self):
        """Returns the classified raster"""
        return self._classified
    
    def get_name(self):
        return self._name
    
    def get_classes(self):
        return self._classes
    
    def get_classes_str(self):
        if self._nclass > 0:
            y=np.array(["%.0f" % w for w in self.get_classes().reshape(self.get_classes().size)])
            y=y.reshape(self.get_classes().shape)
            x=[]
            for i in range(self._nclass):
                x.append(str(y[i,0]) + '--' + str(y[i,1]))
            return x
        else:
            return ''
    
    def get_nclasses(self):
        return self._nclass
    
    def save_to_file(self,fname):
        pass
    
    