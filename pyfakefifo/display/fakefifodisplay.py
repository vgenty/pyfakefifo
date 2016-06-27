#by vic (vgenty@nevis.columbia.edu)

#straight rip of from taritree (taritree@mit.edu)

import os,sys,copy
from . import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

from ..pyfakefifo import PyFakeFifo
import plotmanager

class FakeFifoDisplay(QtGui.QWidget) :
    def __init__(self,infiles):

        super(FakeFifoDisplay,self).__init__()

        self.resize( 1200, 700 )

        # Mother canvas for plots
        self.graphics = pg.GraphicsLayoutWidget()

        # 1) waveform plotting region
        self.wfplot = pg.PlotItem(name="Readout Plot")
        self.wfplot.addLegend()
        
        ax = self.wfplot.getAxis('bottom')
        xStyle = {'color':'#FFFFFF','font-size':'14pt'}
        ax.setLabel('2 MHz Tick',**xStyle)

        ax = self.wfplot.getAxis('left')
        yStyle = {'color':'#FFFFFF','font-size':'14pt'}
        ax.setLabel('ADC',**yStyle)
        
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
        self.event = QtGui.QLineEdit("%d"%(1))       # event number
        self.channel = QtGui.QLineEdit("%d"%(10))     # slot number
        self.chosen_file = QtGui.QLineEdit("aho")     # chosen_file

        self.prev_event = QtGui.QPushButton("Prev Event") # previous event
        self.next_event = QtGui.QPushButton("Next Event") # next event

        self.prev_chan = QtGui.QPushButton("Prev Chan")  # previous channel
        self.next_chan = QtGui.QPushButton("Next Chan") # next channel

        # List of input files
        self.file_list = QtGui.QListWidget(self)
        self.file_list.addItems(infiles)

        # Fifo type
        self.nu_type = QtGui.QRadioButton("Trig")
        self.sn_type = QtGui.QRadioButton("SN")

        # Plotted items
        self.plottable = QtGui.QTableWidget()
        self.plottable.setRowCount(0)
        self.plottable.setColumnCount(5)
        self.plottable.setHorizontalHeaderItem(0,QtGui.QTableWidgetItem("Stream"))
        self.plottable.setColumnWidth(0,45)
        self.plottable.setHorizontalHeaderItem(1,QtGui.QTableWidgetItem("Event"))
        self.plottable.setColumnWidth(1,45)
        self.plottable.setHorizontalHeaderItem(2,QtGui.QTableWidgetItem("Frame"))
        self.plottable.setColumnWidth(2,45)
        self.plottable.setHorizontalHeaderItem(3,QtGui.QTableWidgetItem("Channel"))
        self.plottable.setColumnWidth(3,55)
        self.plottable.setHorizontalHeaderItem(4,QtGui.QTableWidgetItem("File"))
        self.plottable.setColumnWidth(4,5*45)
        self.plottable.setSelectionBehavior(QtGui.QTableView.SelectRows);       
 
        # add to layout
        self.lay_inputs.addWidget( QtGui.QLabel("File List"), 0, 0 )
        self.lay_inputs.addWidget( self.file_list, 1, 0, -1, 1)

        self.lay_inputs.addWidget( QtGui.QLabel("File"), 0, 1 )
        self.lay_inputs.addWidget( self.chosen_file, 0, 2 )

        self.lay_inputs.addWidget( QtGui.QLabel("Event"), 1,1)
        self.lay_inputs.addWidget( self.event, 1, 2 )

        self.lay_inputs.addWidget( QtGui.QLabel("Channel"), 2, 1 )
        self.lay_inputs.addWidget( self.channel, 2, 2 )

        self.lay_inputs.addWidget( QtGui.QLabel("Stream"), 0, 3 )

        self.lay_inputs.addWidget( self.sn_type,1,3)
        self.lay_inputs.addWidget( self.nu_type,2,3)
        
        self.lay_inputs.addWidget( self.prev_event,2,4)
        self.lay_inputs.addWidget( self.next_event,2,5)
        self.lay_inputs.addWidget( self.prev_chan,3,4)
        self.lay_inputs.addWidget( self.next_chan,3,5) 
        
        # axis options
        self.axis_plot = QtGui.QPushButton("Plot!")
        self.lay_inputs.addWidget( self.axis_plot, 0, 4 )

        self.axis_clear = QtGui.QPushButton("Clear All")
        self.lay_inputs.addWidget( self.axis_clear, 0, 5 )

        self.axis_arange = QtGui.QPushButton("AutoRange")
        self.lay_inputs.addWidget( self.axis_arange, 0, 6 )

        self.axis_remove = QtGui.QPushButton("Remove")
        self.lay_inputs.addWidget( self.axis_remove, 0, 7 )

        self.lay_inputs.addWidget( self.plottable,3,1,1,3 )
                               
        def on_item_changed(curr, prev):
            self.chosen_file.setText(curr.text())
            
        self.file_list.currentItemChanged.connect(on_item_changed)

        self.axis_plot.clicked.connect( self.plotData )
        self.axis_clear.clicked.connect( self.clearData )
        self.axis_arange.clicked.connect( self.autoRange )
        self.axis_remove.clicked.connect( self.removeIt )

        self.plottable.clicked.connect(self.toRemove)

        self.prev_event.clicked.connect(self.prevEvent)
        self.next_event.clicked.connect(self.nextEvent)
        self.prev_chan.clicked.connect(self.prevChan)
        self.next_chan.clicked.connect(self.nextChan)
        
        # Data factory
        self.pyff = PyFakeFifo()
        
        # Plot manager
        self.pmanager = plotmanager.PlotManager("plotmanager",self.plottable,self.wfplot)
        
    def plotData(self):

        rfile   = str(self.chosen_file.text())
        event   = int(self.event.text())
        channel = int(self.channel.text())
        
        stream=None;
        
        if self.nu_type.isChecked():
            stream = 'trig'
        if self.sn_type.isChecked():
            stream = 'sn'

        assert stream is not None, "you have to choose"
        
        thisfifo = self.pyff[(stream,rfile)]

        theevent = thisfifo.get_event(event)
        theslice = theevent["ch%d"%channel]

        p = self.wfplot.plot(x=theslice[:,0],
                             y=theslice[:,1],
                             symbol='o',
                             pen=len(self.pmanager.directory),
                             name='{} ch{}'.format(stream,channel))

        self.pmanager.register(stream,event,rfile,channel,p)
        self.pmanager.update(stream,event,theevent.frame_number,channel,rfile)

    def clearData(self):
        self.wfplot.clear()
        self.wfplot.legend.scene().removeItem(self.wfplot.legend)
        self.pmanager.cleartable()
        
    def autoRange(self):
        self.wfplot.autoRange()
        
    def toRemove(self,clickedIndex):
        self.pmanager.set_clicked(clickedIndex)
       
    def removeIt(self):
        self.pmanager.remove()

    def prevEvent(self):

        #casting lame-o
        
        event   = int(self.event.text())
        event-=1
        if event < 0 : event = 0
        
        self.event.setText(str(event))

    
        self.plotData()
        

    def nextEvent(self):

        #casting lame-o
        
        event = int(self.event.text())
        event += 1

        self.event.setText(str(event))

        self.plotData()

    def prevChan(self):

        #casting lame-o
        
        ch = int(self.channel.text())
        ch -= 1

        if ch < 0 : ch = 0
        
        self.channel.setText(str(ch))

        self.plotData()
        
    def nextChan(self):

        #casting lame-o
        
        ch = int(self.channel.text())
        ch += 1

        self.channel.setText(str(ch))

        self.plotData()
