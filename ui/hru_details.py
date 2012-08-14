from PySide import QtGui, QtCore,QtUiTools 

class HRUDetails(QtGui.QMainWindow):
    def __init__(self,parent,HRUS):
        super(HRUDetails,self).__init__(parent=parent)
        
        #load the UI file
        file = QtCore.QFile('./ui/hru_details.ui')
        file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.window = loader.load(file,self)
        file.close() 
        
        #setup menubar
        self.window.actionClose.triggered.connect(self.window.close)
    def show(self):
        self.window.show()