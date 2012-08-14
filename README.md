CRHM-tools
==========

Python/QT front-end for the [Cold Regions Hydrologic Model (CRHM)](http://www.usask.ca/hydrology/CRHM.php) to generate HRUs from specified terrain classes.

<img src="https://raw.github.com/Chrismarsh/CRHM-tools/master/Screenshot_1.png" width="95%">


Depends
==========
- Requires Python < 3 
- PySide & QT
- Matplotlib
- GDAL

A python distribution such as [Enthought Python](http://www.enthought.com/products/epd.php) installs all the prerequisits. 

Only tested with x64 python, but should work with x86. 

Tested on Win7x64 and OSX 10.7

Usage
==========
- Load 'Primary Landclasses' via file menu or right-clicking the treeview
- Use the tool menu to generate the final set of HRUs
- Right-click treeview items to toggle plotting views

Features
=========
- Extensible plugin and UI to allow for additional functions

Limitations
==========
This is still very alpha, so many features are missing such as exporting the HRU information, &c. 
