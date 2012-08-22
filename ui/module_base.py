
from PySide import QtGui, QtCore,QtUiTools 

#Base class for GUI modules that abstracts away some of the setup
class module_base(QtGui.QDialog):
    #Imported_files list of the files that have been inported
    #ui_file the pyside .ui file to build the GUI for the module
    def __init__(self,imported_files,ui_file):
        super(module_base,self).__init__()
        self.files = imported_files
    
        #load the UI file
        file = QtCore.QFile(ui_file)
        file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.window = loader.load(file,self)
        
        file.close()
      
        self.window.btnCncl.clicked.connect(self.window.close)
        self.window.btnOk.clicked.connect(self._Ok_pressed)
        
        self.selected_file=''

        self.lc = None
    
    def mbox_error(self, string):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(string)
        msgBox.setWindowTitle('Error')
        msgBox.setIcon(QtGui.QMessageBox.Critical) 
        msgBox.exec_()        
    #return the selected file before handing off to the 'user' function
    def _Ok_pressed(self):

        file = self.window.filelist.currentText()
        file = file[file.find('[')+1:-1]   
        self.selected_file = file
        
        self.lc =  self.run()
        
        if self.lc:
            self.window.close()
    
    #setup the ui and then show it
    def show_ui(self):
        #setup the file list
        self.window.filelist.clear()
        for f in self.files:
            self.window.filelist.addItem( f + '  [' + self.files[f].get_path()+']' )      
        self.window.setWindowTitle(self.name + ' - ' + str(self.version))
        #show the window
        self.window.exec_()
        return self.lc
