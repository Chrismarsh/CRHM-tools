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

        #set a validator to the linedit so it only accepts integers
        v=QtGui.QIntValidator(1,999,self.window.lineEdit)
        self.window.lineEdit.setValidator(v)    
    def init_run(self):
    
        try:
            #get the number of classes from the line edit widget
            nclasses=int(self.window.lineEdit.text())
            #get the name from the edit widget
            name = self.window.edit_name.text()
            if name == '':
                raise Exception()
            kwargs={}
            kwargs['file']=self.selected_file
            kwargs['nbin']=nclasses
            kwargs['name']=name
            #call our main handler
            return kwargs
        except:
            self.mbox_error('Invalid field. Perhaps a field is empty?')
        
       
    
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
    
    


 
 