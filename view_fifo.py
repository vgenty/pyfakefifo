#!/usr/bin python
#thanks taritree

import os,sys
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
from pyfakefifo.display import fakefifodisplay as ffd

infiles = sys.argv[1:]

app = QtGui.QApplication([])
ffdisplay = ffd.FakeFifoDisplay(infiles)
ffdisplay.show()

if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    print "exec called ..."
    ffdisplay.show()
    QtGui.QApplication.instance().exec_()

