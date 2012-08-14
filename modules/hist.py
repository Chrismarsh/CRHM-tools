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
        
        #show the ui
        self.show_ui()
        
        #if we cleanly exited
        if self.ok_exit == True:
            
            #get the number of classes from the line edit widget
            nclasses=int(self.window.lineEdit.text())
            #get the name from the edit widget
            name = self.window.edit_name.text()

            #check number of classies/bins
            if nclasses  <= 0:
                mbox =QtGui.QMessageBox()
                mbox.setText("Cannot have <=0 bins.")
                mbox.exec_()
                return
            
            #create a new landclass
            lc = ct.terrain.landclass()
            #open the file
            lc.open(self.selected_file)
            #create the bins based on a histogram
            hist, edges = np.histogram(lc._raster, bins=nclasses)        
            
            #call our main handler
            return self.exec_module(landclass=lc, nbin=nclasses, edges=edges, name=name)
        
        return None
    
    #This is what can be called from the command line if wanted
    def exec_module(self,**kwargs):
        return ct.gis.classify(kwargs['landclass'],kwargs['nbin'],kwargs['edges'],kwargs['name'])
    
    


 
 