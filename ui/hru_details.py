from PySide import QtGui, QtCore,QtUiTools 
import crhmtools as ct
import numpy as np

class HRUDetails(QtGui.QMainWindow):
    def __init__(self, parent, basin, secondary_lc, imported_files):
        super(HRUDetails,self).__init__(parent=parent)

        #load the UI file
        file = QtCore.QFile('./ui/hru_details.ui')
        file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.window = loader.load(file,self)
        file.close() 

        self.basin = basin
        self.slc = secondary_lc
        self.imported_files = imported_files
        
        self.window.setWindowTitle('HRU details - CRHM Tools')
        #setup menubar
        self.window.actionClose.triggered.connect(self.window.close)
    def show(self):
        #setup the grid
        nhru = self.basin.get_num_hrus()
        self.window.tableWidget.setColumnCount(nhru)
        self.window.tableWidget.setRowCount(len(self.slc))
        
        for i in range(0,nhru):
            header = QtGui.QTableWidgetItem('HRU ' + str(i+1))
            self.window.tableWidget.setHorizontalHeaderItem(i,header)

        
        for i in range(0,len(self.slc)):
            header = QtGui.QTableWidgetItem('Mean of ' + self.slc[i])
            self.window.tableWidget.setVerticalHeaderItem(i,header)   
        
        for i in range(0,nhru):
            for j in range(0,len(self.slc)):
                mean = np.mean(self.imported_files[self.slc[j]].get_raster()[self.basin._hrus  == i+1])
                item = QtGui.QTableWidgetItem('{0:.2f}'.format(mean))
                self.window.tableWidget.setItem(j,i,item) #intentional i,j flip here

        self.window.show()