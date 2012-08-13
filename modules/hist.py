import numpy as np
import crhmtools as ct
from ui.module_base import  *
from PySide import QtGui, QtCore,QtUiTools 

    
class mod_hist(module_base):
    def __init__(self,imported_files):
        super(mod_hist,self).__init__(imported_files,'./modules/hist_ui.ui')
        
        
        self.name = 'Histogram partioning'
        self.version = '1.0'
        self.description = 'Creates a landscape class by partitioning the histogram in to n partitions.'
        self.author = 'Chris Marsh'
        self.category = 'Statistics'

    def run(self):
        self.show_ui()
        
        if self.ok_exit == True:
            nclasses=int(self.window.lineEdit.text())
            name = self.window.edit_name.text()

            #check number of classies/bins
            if nclasses  <= 0:
                mbox =QtGui.QMessageBox()
                mbox.setText("Cannot have <=0 bins.")
                mbox.exec_()
                return
            
            return self.exec_module(file=self.selected_file, nbin=nclasses, name=name)
        
        return None
    
    def exec_module(self,**kwargs):
        return ct.gis.classify(kwargs['file'],kwargs['nbin'],kwargs['name'])
    
    


 
 