
from PySide import QtGui, QtCore,QtUiTools 
class module_base(QtGui.QDialog):
    def __init__(self,imported_files,ui_file):
        super(module_base,self).__init__()
        self.files = imported_files
    
        file = QtCore.QFile(ui_file)
        file.open(QtCore.QFile.ReadOnly)

        
        loader = QtUiTools.QUiLoader()
        self.window = loader.load(file,self)
        
        file.close()
      
        self.window.btnCncl.clicked.connect(self.window.close)
        self.window.btnOk.clicked.connect(self._Ok_pressed)
        
        self.selected_file=''
        self.ok_exit = False
    
    def _Ok_pressed(self):
        self.ok_exit = True
        file = self.window.filelist.currentText()
        file = file[file.find('[')+1:-1]   
        self.selected_file = file
        self.window.close()
        
    def show_ui(self):
        #setup the file list
        self.window.filelist.clear()
        for f in self.files:
            self.window.filelist.addItem( f + '  [' + self.files[f].get_path()+']' )      
        
        #show the window
        self.window.exec_()
        
