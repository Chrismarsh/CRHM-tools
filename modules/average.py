import numpy as np
import crhmtools as ct

from PySide import QtGui 

    
class mod_avg(object):
    def __init__(self,imported_files):
        self.name = 'Average partioning'
        self.version = '1.0'
        self.description = 'Creates a landscape class by partitioning the average in to n partitions.'
        self.author = 'Chris Marsh'
        self.category = 'Statistics'
        
    def run(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Hello world from mod_avg()")
        msgBox.exec_()        