CRHM-tools
==========

Python/QT front-end for the [Cold Regions Hydrologic Model (CRHM)](http://www.usask.ca/hydrology/CRHM.php) to generate HRUs from specified terrain classes.

<img src="https://raw.github.com/Chrismarsh/CRHM-tools/master/Screenshot_1.png" width="95%">


Depends
==========
- Python 2.7
- PySide
- Matplotlib
- Numpy and SciPy
- GDAL

A python distribution such as [Enthought Python](http://www.enthought.com/products/epd.php) installs all the prerequisits. 

Only tested with x64 python, but should work with x86. 

Tested on Win7x64 and OSX 10.7

Usage
==========
- Import raster files via file menu or right-clicking 'imported files'
- Create 'primary land classes' via the functions tab
	- Primary land classes are used to create the final HRUs
- Use the tools menu->generate HRUS to generate the final set of HRUs
	- These HRUs are essentially the intersection of each permutation of primary landclasses
- Drag and drog imported files to the 'secondary land classes' treeview item to create secondary land classes
	- These are used for generating HRU parameters for use in CRHM.
- Right-click treeview items to toggle plotting views
	- Primary land classes may either be displayed as 'classified' or as 'non-classified'. Classified shows the land classe output from running a function, while the non-classified shows the base data; exactly the same as if it was plotted from the imported files treeview.
- HRU parameters (for insertion into CRHM) are generated using the view->HRU details menu. This requires that one or more secondary land classes are selected. 

Features
=========
- Extensible plugin and UI to allow for additional functions to be easily added
- Quickly generates HRU from a range of existing functions

