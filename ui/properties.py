from PySide import QtGui, QtCore,QtUiTools 

class Properties(QtGui.QDialog):
    def __init__(self,lc):
        super(Properties,self).__init__()
        #load the UI file
        file = QtCore.QFile('./ui/properties.ui')
        file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.window = loader.load(file,self)        
        
        self.window.name.setText(lc.get_name())
        self.window.location.setText(lc.get_path())
        res = lc.get_resolution()
        self.window.resolution.setText(str(abs(res[0]))+' x ' +str(abs(res[1])))
        self.window.classes.setText(str(lc.get_nclasses()))
        self.window.ysize.setText(str(lc.ysize()))
        self.window.xsize.setText(str(lc.xsize()))
        self.window.creator.setText(lc.get_creator())
        classes = lc.get_classes_str()
        
        for c in classes:
            self.window.plainTextEdit.appendPlainText('Class: '+c+'\n')
        
        self.window.tabWidget.setCurrentIndex(0)