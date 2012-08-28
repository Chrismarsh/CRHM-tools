import numpy as np
import crhmtools as ct
from ui.module_base import  *
from PySide import QtGui, QtCore,QtUiTools 

    
class mod_fetchR(module_base):
    def __init__(self,imported_files):
        
        #load the ui file
        super(mod_fetchR,self).__init__(imported_files,'./modules/fetchr_ui.ui')

        self.name = 'FetchR'
        self.version = '1.0'
        self.description = 'Creates a raster of Fetches.'
        self.author = 'Chris Marsh'
        self.category = 'Process'

        #set a validator to the linedit so it only accepts integers
        v=QtGui.QIntValidator(1,999,self.window.lineEdit)
        self.window.lineEdit.setValidator(v)    
    def run(self):
    
    #try:
       #height of obstructing terrain
        height=int(self.window.lineEdit.text())
        #get the name from the edit widget
        name = self.window.edit_name.text()
        if name == '':
            raise ValueError()
        direction = self.window.cb_direction.currentText()
        #call our main handler
        return self.exec_module(file=self.selected_file, height=height, name=name,wind_dir=direction)
    #except ValueError:
        #self.mbox_error('Invalid field. Perhaps a field is empty?')
    
        return None
    
    #This is what can be called from the command line if wanted
    def exec_module(self,**kwargs):
        #create a new landclass
        r = ct.terrain.landclass()
        r.set_creator(self.name)
        r._name = kwargs['name']
        #open the file
        r.open(kwargs['file'])
        fetch = np.zeros(r.xsize()*r.ysize()).reshape(r.ysize(),r.xsize())
        #hard-coded direction, fixup later
        direction = kwargs['wind_dir']
        elev = kwargs['height']

        for i in range(0,r.ysize()):
            for j in range(0,r.xsize()):
                try: 
                    if direction == 'N': #for NORTH
                        s = r._raster[:i,j] #north
                        idx =  np.roll(s,1) >= r._raster[i,j]+elev #the roll is because we are looking north
                        ncells=0
                        for k in range(0,idx.size):
                            if idx[0] == True:
                                if idx[k]==True:
                                    ncells = ncells+1
                                else:
                                    break
                        fetch[i,j] = ncells * r.get_resolution()[0]                        
                        #idx = np.where( np.roll(s,1) >= r._raster[i,j]+elev)[0][0] #the roll is because we are looking north
                        #fetch[i,j] = r._raster[i-idx:i,j].size * r.get_resolution()[0]
                    elif direction == 'S': #SOUTH
                        s = r._raster[i:,j]  #south direction
                        idx = np.where( s >= r._raster[i,j]+elev)[0][0]
                        fetch[i,j] = r._raster[i:i+idx,j].size * r.get_resolution()[0]          
                    elif direction == 'E':#east
                        s = r._raster[i,j:] 
                        idx = np.where( s >= r._raster[i,j]+elev)[0][0]
                        fetch[i,j] = r._raster[i,j:j+idx].size * r.get_resolution()[0]         
                    elif direction == 'W':#west
                        s = r._raster[i,:j] 
                        idx = np.where( np.roll(s,1) >= r._raster[i,j]+elev)[0][0]
                        fetch[i,j] = r._raster[i,j-idx:j].size * r.get_resolution()[0]                        
                except: #catch s == [] or np.where == []
                    pass
        
        r._raster = fetch
        return r
        #return ct.gis.classify(r,kwargs['nbin'],edges,kwargs['name'])
    
    


 
 