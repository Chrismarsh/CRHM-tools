
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui

class LCTreeViewModel(QtGui.QStandardItemModel):
    def __init(self):
        super(LCTreeViewModel,self).__init__()
    def mimeData(self, indexes):
        i = indexes[0]
        md = QtCore.QMimeData()
        md.setText(i.data())
        return md
        
    def mimeTypes(self):
        return ['text/plain']
    def dropMimeData(self, data, action, row, column, parent):
        
        item = QtGui.QStandardItem(data.text())
        p = self.itemFromIndex(parent) # get the real parent
        
        #findItem is not working, not sure why
        #but make sure we aren't dropping the same thing 
        for i in range(0,p.rowCount()):
            if p.child(i).text() == data.text():
                return False
        item.setDropEnabled(False)
        item.setDragEnabled(False)
        p.appendRow(item)
        return True
    
class LCTreeView(QtGui.QTreeView):
    def __init__(self,parent):
        super(LCTreeView,self).__init__(parent)
        
     
    def dropEvent(self, event):
        super(LCTreeView,self).dropEvent(event)
    
    def dragEnterEvent(self, event):
        event.accept()
    
    def dragmoveEvent(self,event):
        event.accept()
        
    