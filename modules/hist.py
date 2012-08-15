import numpy as np
import crhmtools as ct
from ui.module_base import  *
from PySide import QtGui, QtCore,QtUiTools 

    
class mod_hist(module_base):
    def __init__(self,imported_files):
        
        #load the ui file
        super(mod_hist,self).__init__(imported_files,'./modules/hist_ui.ui')

        self.name = 'Histogram partioning'
        self.version = '1.0'
        self.description = 'Creates a landscape class by partitioning the histogram in to n partitions.'
        self.author = 'Chris Marsh'
        self.category = 'Statistics'

    def run(self):
        #set a validator to the linedit so it only accepts integers
        v=QtGui.QIntValidator(1,999,self.window.lineEdit)
        self.window.lineEdit.setValidator(v)        
        #show the ui
        self.show_ui()
        
        #if we cleanly exited
        if self.ok_exit == True:
            
            #get the number of classes from the line edit widget
            nclasses=int(self.window.lineEdit.text())
            #get the name from the edit widget
            name = self.window.edit_name.text()
           
            #call our main handler
            return self.exec_module(file=self.selected_file, nbin=nclasses, name=name)
        
        
        return None
    
    #This is what can be called from the command line if wanted
    def exec_module(self,**kwargs):
        #create a new landclass
        r = ct.terrain.landclass()
        r.set_creator(self.name)
        #open the file
        r.open(kwargs['file'])
        
        #create the bins based on a histogram
        hist, edges = np.histogram(r.get_raster(), bins=kwargs['nbin'])               

        return ct.gis.classify(r,kwargs['nbin'],edges,kwargs['name'])
    
    


 
 