# -*- coding: utf-8 -*-
__rev_id__ = """$Id: lotto_gui1.py,v 0.1 2010/11/2 Markus Hackspacher cc by-sa $"""
import sys 
from PyQt4 import QtGui, QtCore 
from lotto_dialog import Ui_Dialog as Dlg

#zeichenzahl=[0,0,0,0,0,0]

class MeinDialog(QtGui.QDialog, Dlg): 
    def __init__(self): 
        QtGui.QDialog.__init__(self) 
        self.setupUi(self)
        painter = QtGui.QPainter(self) 
        #self.pen = QtGui.QPen(QtGui.QColor(0,0,0)) 
        #self.pen.setWidth(3) 
        #self.brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        
        # Slots einrichten 

    def paintEvent(self, event): 
        painter = QtGui.QPainter(self) 
        painter.setPen(self.pen) 
        painter.setBrush(self.brush) 
        painter.drawRect(420, 20, 210, 350)
	#self.plainTextEdit.appendPlainText(str(zeichenzahl))
        if 1!=1:
            painter.drawLine(50, 350-zeichenzahl[0]*6, 480, 350-zeichenzahl[1]*6)
            #painter.drawLine(80, 350-zeichenzahl[1]*6, 510, 350-zeichenzahl[2]*6)
            #painter.drawLine(110, 350-zeichenzahl[2]*6, 540, 350-zeichenzahl[3]*6)
            #painter.drawLine(240, 350-zeichenzahl[3]*6, 570, 350-zeichenzahl[4]*6)
            #painter.drawLine(270, 350-zeichenzahl[4]*6, 600, 350-zeichenzahl[5]*6)
            a=1
        

    def Zeichnen(self): 
       	self.update()

def gui_show():
  #app = QtGui.QApplication(sys.argv) 
  dialog = MeinDialog() 
  while 1:
    dialog.show() 

        
def gui():
  app = QtGui.QApplication(sys.argv) 
  dialog = MeinDialog() 
  dialog.show() 
  sys.exit(app.exec_())
  
if __name__ == "__main__":
  gui()
