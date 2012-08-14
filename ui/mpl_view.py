import matplotlib

## Added for PySide
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable

#Container for the matplotlib plot
class mpl_widget(object):
    def __init__(self, parent):
        self.fig = Figure() #(6.0, 4.0)
        self.axes = self.fig.add_subplot(111)     
        
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(parent)
        self.fig.set_facecolor('white')

        self.curr_cb = None # holds current colorbar
   
    
    def clear(self):
        self.axes.clear()  
                       
        #remove the old colorbar
        if self.curr_cb:
                self.fig.delaxes(self.fig.axes[1])
                self.fig.subplots_adjust(right=0.90) 
                self.curr_cb=None
        self.canvas.draw()              
     
    def plot(self, thing_to_plot):
        self.clear()
        h=self.axes.imshow(thing_to_plot)
        
        divider = make_axes_locatable(self.axes)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        
        self.curr_cb=self.fig.colorbar(h,cax=cax) 
        
        
        self.canvas.draw()
        
       
    #set colourbar ticks
    def set_cb_ticks(self,tick_range):
        self.curr_cb.set_ticks(tick_range)
        
    #set colourbar tick labels
    def set_cb_ticklabels(self,tick_labels):
        self.curr_cb.set_ticklabels(tick_labels)