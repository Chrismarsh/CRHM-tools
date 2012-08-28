import numpy as np
import crhmtools as ct
from ui.module_base import  *
from PySide import QtGui, QtCore,QtUiTools 

    
class mod_slope(module_base):
    def __init__(self,imported_files):
        
        #load the ui file
        super(mod_slope,self).__init__(imported_files,'./modules/slope_ui.ui')

        self.name = 'Slope'
        self.version = '1.0'
        self.description = 'Creates a slope.'
        self.author = 'Chris Marsh'
        self.category = 'Terrain'

    def run(self):
    
        try:
            #get the name from the edit widget
            name = self.window.edit_name.text()
            if name == '':
                raise ValueError()
            #call our main handler
            return self.exec_module(file=self.selected_file, name=name)
        except ValueError:
            self.mbox_error('Invalid field. Perhaps a field is empty?')
        
        return None
    
    #This is what can be called from the command line if wanted
    def exec_module(self,**kwargs):
        #create a new landclass
        r = ct.terrain.landclass()
        r.set_creator(self.name)
        r._name = kwargs['name']
        #open the file
        r.open(kwargs['file'])
        
        p,q = np.gradient(r.get_raster(),1,1)
        
        
        r._raster = np.arctan(np.sqrt(p**2 + q**2)) * 180.0/np.pi
        return r
    
    


 
 