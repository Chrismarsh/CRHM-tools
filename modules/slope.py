import numpy as np
import crhmtools as ct
from ui.module_base import  *
from PySide import QtGui, QtCore,QtUiTools 




class mod_slope(module_base):
    def __init__(self,imported_files,generated_lc):
        
        #load the ui file
        super(mod_slope,self).__init__(imported_files,generated_lc,'./modules/slope_ui.ui')

        self.name = 'Slope'
        self.version = '1.0'
        self.description = 'Creates a slope.'
        self.author = 'Chris Marsh'
        self.category = 'Terrain'

        #set a validator to the linedit so it only accepts integers
        v=QtGui.QIntValidator(1,999,self.window.radiusLineEdit)
        self.window.radiusLineEdit.setValidator(v)   
    def init_run(self):
    
        try:
            #get the name from the edit widget
            name = self.window.edit_name.text()
            if name == '':
                raise ValueError()

            window = self.window.radiusLineEdit.text()
            kwargs={}
            kwargs['name']=name
            kwargs['window']=window
            return kwargs 
        except ValueError:
            self.mbox_error('Invalid field. Perhaps a field is empty?')            
        
        return None   
    
    #This is what can be called from the command line if wanted
    def exec_module(self,**kwargs):
        r = self.selected_file.copy()
        r._name = kwargs['name']
        r.set_creator(self.name)
        window = int(kwargs['window'])
        p,q = np.gradient(r.get_raster(),window,window)
        
        
        r._raster = np.arctan(np.sqrt(p**2 + q**2)) * 180.0/np.pi
        return r

    


 
 