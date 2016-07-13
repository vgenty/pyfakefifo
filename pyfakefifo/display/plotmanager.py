from . import QtGui, QtCore

class PlotManager(object) :

    def __init__(self,name,plottable,viewbox):
        self.name = name;
        self.directory = {}
        self.plottable = plottable
        self.clicked = None
        self.viewbox = viewbox
        
    def register(self,stream,event,rfile,channel,plotitem) :
        self.directory[ (str(stream),str(event),str(rfile),str(channel)) ] = plotitem
        
    def remove(self):
        row=self.clicked.row()
        cstream  = str(self.plottable.item(row,0).text())
        cevent   = str(self.plottable.item(row,1).text())
        cchannel = str(self.plottable.item(row,3).text())
        crfile   = str(self.plottable.item(row,4).text())

        cplot = self.directory[(cstream,cevent,crfile,cchannel)]

        self.viewbox.legend.removeItem("{} ch{}".format(cstream,cchannel))
        self.viewbox.removeItem(cplot)
        self.directory.pop((cstream,cevent,crfile,cchannel), None)
        self.plottable.removeRow(row)
        
    def update(self,stream,event,frame,channel,rfile):

        cur_row = self.plottable.rowCount()
        self.plottable.setRowCount(cur_row+1)

        self.plottable.setItem(cur_row,0,QtGui.QTableWidgetItem(str(stream)))
        self.plottable.setItem(cur_row,1,QtGui.QTableWidgetItem(str(event)))
        self.plottable.setItem(cur_row,2,QtGui.QTableWidgetItem(str(frame)))
        self.plottable.setItem(cur_row,3,QtGui.QTableWidgetItem(str(channel)))
        self.plottable.setItem(cur_row,4,QtGui.QTableWidgetItem(str(rfile)))
                                
    def set_clicked(self,clicked):
        self.clicked = clicked

    def cleartable(self):
        while self.plottable.rowCount() > 0:
            self.plottable.removeRow(0)
        
