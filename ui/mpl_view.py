import matplotlib
import numpy as np
from scipy import interpolate
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
     
    def plot(self, thing_to_plot, ticks=None, labels=None):
        self.clear()
        
        cmap = None
        norm = None
        if ticks: #if we specified ticks, produce a discrete maping
            cmap = self.cmap_discretize(matplotlib.cm.jet,len(ticks)+1)
            norm = matplotlib.colors.BoundaryNorm(sum([ticks[:],[ticks[-1]+1]],[]), cmap.N)

        #plot
        h=self.axes.imshow(thing_to_plot,cmap=cmap,norm=norm)
        #align the cbar with the plot
        divider = make_axes_locatable(self.axes)
        cax = divider.append_axes("right", size="5%", pad=0.05)   
        
        if ticks:
            self.curr_cb=self.fig.colorbar(h,cax=cax,ticks=ticks)
        else:
            self.curr_cb=self.fig.colorbar(h,cax=cax) #even thought colorbar(...) has ticks=None as default arg, if we call it with ticks=None no ticks are shown.
        
        if labels:
            self.curr_cb.ax.set_yticklabels(labels)        
       
        
        self.canvas.draw()
    
    #http://www.scipy.org/Cookbook/Matplotlib/ColormapTransformations
    def cmap_discretize(self,cmap, N):
        """Return a discrete colormap from the continuous colormap cmap.
        
            cmap: colormap instance, eg. cm.jet. 
            N: Number of colors.
        
        Example
            x = resize(arange(100), (5,100))
            djet = cmap_discretize(cm.jet, 5)
            imshow(x, cmap=djet)
        """
    
        cdict = cmap._segmentdata.copy()
        # N colors
        colors_i = np.linspace(0,1.,N)
        # N+1 indices
        indices = np.linspace(0,1.,N+1)
        for key in ('red','green','blue'):
            # Find the N colors
            D = np.array(cdict[key])
            I = interpolate.interp1d(D[:,0], D[:,1])
            colors = I(colors_i)
            # Place these colors at the correct indices.
            A = np.zeros((N+1,3), float)
            A[:,0] = indices
            A[1:,1] = colors
            A[:-1,2] = colors
            # Create a tuple for the dictionary.
            L = []
            for l in A:
                L.append(tuple(l))
            cdict[key] = tuple(L)
        # Return colormap object.
        return matplotlib.colors.LinearSegmentedColormap('colormap',cdict,1024)        