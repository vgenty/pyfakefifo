#!/usr/bin python
#thanks taritree

import os,sys
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
from pyfakefifo.display import fakefifodisplay as ffd

inputs = sys.argv
def usage() :
    print("\n\t" + '\033[91m' + " view_fifo.py [dir | root files]..." + '\033[0m' + "\n")

if len(inputs) < 2:
    usage()
    sys.exit(1)

inputs = sys.argv[1:]

infiles = [f for f in inputs if os.path.isfile(f)]
indirs  = [d for d in inputs if os.path.isdir(d) ]

for d in indirs:
    files = [ os.path.join(d,f) for f in os.listdir(d) if f.endswith(".root") ]
    infiles += files

app = QtGui.QApplication([])
ffdisplay = ffd.FakeFifoDisplay(infiles)
ffdisplay.show()

if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    print "exec called ..."
    ffdisplay.show()
    QtGui.QApplication.instance().exec_()
