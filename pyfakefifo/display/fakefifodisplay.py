#thanks taritree

import os,sys,copy
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

from ..pyfakefifo import PyFakeFifo

class FakeFifoDisplay(QtGui.QWidget) :
    def __init__(self,infiles):
        super(FakeFifoDisplay,self).__init__()
        self.resize( 1200, 700 )

        # Mother canvas for plots
        self.graphics = pg.GraphicsLayoutWidget()

        # 1) waveform plotting region
        self.wfplot = pg.PlotItem(name="Readout Plot")
        self.wf_time_range = pg.LinearRegionItem(values=[0,1500], orientation=pg.LinearRegionItem.Vertical)
        self.wfplot.addItem( self.wf_time_range )

        self.lastevent = None
        self.newevent = True

        # Main Layout
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget( self.graphics, 0, 0, 1, 10 )
        self.graphics.addItem( self.wfplot, 3, 0, rowspan=3 )
        self.setLayout(self.layout)

        # -------------
        # Input Widgets
        # -------------
        
        # Layouts
        self.lay_inputs = QtGui.QGridLayout()
        self.layout.addLayout( self.lay_inputs, 1, 0 )
        
        # Navigation
        self.event = QtGui.QLineEdit("%d"%(126))     # event number
        self.channel = QtGui.QLineEdit("%d"%(10))     # slot number
        self.chosen_file = QtGui.QLineEdit("aho")     # slot number
        self.prev_event = QtGui.QPushButton("Previous")
        self.next_event = QtGui.QPushButton("Next")

        # List of input files
        self.file_list = QtGui.QListWidget(self)
        self.file_list.addItems(infiles)

        # Fifo type
        self.nu_type = QtGui.QRadioButton("Trig")
        self.sn_type = QtGui.QRadioButton("SN")
        
        
        # add to layout
        self.lay_inputs.addWidget( QtGui.QLabel("File List"), 0, 0 )
        self.lay_inputs.addWidget( self.file_list, 1, 0, -1, 1)

        self.lay_inputs.addWidget( QtGui.QLabel("Chosen File"), 0, 1 )
        self.lay_inputs.addWidget( self.chosen_file, 1, 1 )

        self.lay_inputs.addWidget( QtGui.QLabel("Event"), 2, 1 )
        self.lay_inputs.addWidget( self.event, 3, 1 )

        self.lay_inputs.addWidget( QtGui.QLabel("Channel"), 4, 1 )
        self.lay_inputs.addWidget( self.channel, 5, 1 )

        self.lay_inputs.addWidget( self.sn_type,0,2)
        self.lay_inputs.addWidget( self.nu_type,1,2)

        # axis options
        self.set_xaxis = QtGui.QPushButton("Plot")
        self.lay_inputs.addWidget( self.set_xaxis, 0, 6 )

        def on_item_changed(curr, prev):
            self.chosen_file.setText(curr.text())
            
        self.file_list.currentItemChanged.connect(on_item_changed)

        self.set_xaxis.clicked.connect( self.plotData )


        # Data factory
        self.pyff = PyFakeFifo()
        
        
    def plotData(self):
        rfile = str(self.chosen_file.text())
        event = int(self.event.text())
        channel = int(self.channel.text())
        
        stream= None;
        
        if self.nu_type.isChecked():
            stream = 'trig'
        if self.sn_type.isChecked():
            stream = 'sn'

        assert stream is not None, "you have to choose"
        print stream,rfile
        
        thisfifo = self.pyff[(stream,rfile)]

        theevent = thisfifo.get_event(event)
        theslice = theevent["ch%d"%channel]
        print theslice
        self.wfplot.plot(x=theslice[:,0], y=theslice[:,1], symbol='o',pen=(0,2))  
