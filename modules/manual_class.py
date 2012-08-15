import numpy as np
import crhmtools as ct
from ui.module_base import  *
from PySide import QtGui, QtCore,QtUiTools 

    
class mod_manclass(module_base):
    def __init__(self,imported_files):
        
        #load the ui file
        super(mod_manclass,self).__init__(imported_files,'./modules/manual_class.ui')

        self.name = 'Manual partioning'
        self.version = '1.0'
        self.description = 'Creates a landscape class by partitioning the domain in to n, user defined, partitions.'
        self.author = 'Chris Marsh'
        self.category = 'Statistics'
        
        self.nclasses = 0
        
    #this is called when we change the number of
    def update_tableview(self,arg):
        self.nclasses = int(arg) #we know this to be valid because of our validator
        self.window.tableWidget.setRowCount(self.nclasses)
        
    #this is called when a table cell is changed, so we can check if it has valid input   
    def validate_table(self,row,col):
        item = self.window.tableWidget.item(row,col) #get what was just changed
        v=QtGui.QDoubleValidator() #create a validator for doubles
        v.setRange(-99999,99999)
        if v.validate(item.text(),0)[0] == QtGui.QValidator.State.Invalid: #did our validator return an invalid vale?
            self.window.tableWidget.setItem(row,col,QtGui.QTableWidgetItem('0')) #just reset the cell to 0
            
    def run(self):
        
        #connect the lineedit text changed signal 
        self.window.lineEdit.textChanged.connect(self.update_tableview)     
        #connect the cell changed signal to the validator function
        self.window.tableWidget.cellChanged.connect(self.validate_table)
        
        #give the line editor a validator so it only takes integers
        v=QtGui.QIntValidator(1,999,self.window.lineEdit)
        self.window.lineEdit.setValidator(v)

        #show the ui
        self.show_ui()


        #if we cleanly exited
        if self.ok_exit == True:
            
            #get the number of classes from the line edit widget
            nclasses=int(self.window.lineEdit.text())
            #get the name from the edit widget
            name = self.window.edit_name.text()


            #call our main handler
            return self.exec_module( nbin=nclasses,  name=name)
        
        return None
    
    #This is what can be called from the command line if wanted
    def exec_module(self,**kwargs):
        
        #create a new landclass
        r = ct.terrain.landclass()
        #open the file
        r.open(self.selected_file)        
        r.set_creator(self.name)
        edges = []
        for i in range(0,self.window.tableWidget.rowCount()):
            start = self.window.tableWidget.item(i,0)
            end = self.window.tableWidget.item(i,1)
            
            #empty list, so just insert
            if len(edges) == 0:
                edges.append(int(start.text()))
                edges.append(int(end.text()))
            else:
            #However!! if we have something like 0-90, 90-360, we don't want to add the 90 twice
                prev = edges[-1]
                cstart = int(start.text()) 
                cend = int(end.text()) 
                if prev != cstart:
                    edges.append(cstart)
                edges.append(cend)

        return ct.gis.classify(r,kwargs['nbin'],edges,kwargs['name'])
    
    


 
 