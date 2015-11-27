from PyQt4 import QtGui, QtCore

class FsmState(QtGui.QGraphicsEllipseItem):
#class FsmState(QtGui.QGraphicsItem):
    
    def __init__(self, contextMenu, stateName='S0', pos=None, parent=None, scene=None):
        super(FsmState, self).__init__(parent, scene)

        self.stateNameTextItem = QtGui.QGraphicsTextItem(parent=self, scene=scene)
        self.stateNameTextItem.setPlainText(stateName)
        self.stateNameTextItem.setTextInteractionFlags(QtCore.Qt.TextEditable)
        brc = self.stateNameTextItem.boundingRect()
        self.stateNameTextItem.setPos(- brc.width()/2, - brc.height()/2)
        self.stateName = stateName
        self.diameter = 50
        self.setRect(self.diameter//-2,self.diameter//-2,self.diameter,self.diameter)
        self.outboundTransitions = []
        self.inboundTransitions = []
        self.contextMenu = contextMenu

        if pos:
            self.setPos(pos)

        #self.setPolygon(self.myPolygon)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges, True)

    def toStore(self):
        return "FsmState(contextMenu=None, stateName='{0}', pos={1})\n".format(self.stateName, self.pos())
                
    def paint(self, painter, option, widget=None):
        if self.isSelected():
            painter.setBrush(QtCore.Qt.yellow)
        else:
            painter.setBrush(QtCore.Qt.cyan)
        painter.drawEllipse(-self.diameter/2, -self.diameter/2, self.diameter, self.diameter)
 #       super(FsmState, self).paint(painter, option, widget)
 #painter.drawText(self.boundingRect(), QtCore.Qt.AlignCenter, self.stateName)

    def keyPressEvent(self, keyEvent):
        pass

    def removeTransition(self, x):
        if x in self.inboundTransitions:
            self.inboundTransitions.remove(x)
        if x in self.outboundTransitions:
            self.outboundTransitions.remove(x)

    def removeTransitions(self):
        for x in self.inboundTransitions[:] + self.outboundTransitions[:]:
            x.startItem().removeArrow(x)
            x.endItem().removeArrow(x)
            self.scene().removeItem(x)

    def addInboundTransition(self, x):
        self.inboundTransitions.append(x)

    def addOutboundTransition(self, x):
        self.outboundTransitions.append(x)



    def image(self):
        pixmap = QtGui.QPixmap(250, 250)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 8))
        painter.translate(125, 125)
        painter.drawEllipse(-100, -100, 100, 100)
        return pixmap

    def contextMenuEvent(self, event):
        self.scene().clearSelection()
        self.setSelected(True)
        self.contextMenu.exec_(event.screenPos())

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionHasChanged:
            for x in self.inboundTransitions + self.outboundTransitions:
                x.updatePosition()
        
        return super(FsmState, self).itemChange(change,value)

    # def mouseDoubleClickEvent(self, event):        
    #     pass
if __name__ == '__main__':
    import sys
    from MainWindow import MainWindow
    from PyQt4.QtTest import QTest
    from PyQt4.QtCore import Qt
    
    app = QtGui.QApplication(sys.argv)


    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 800, 500)
    mainWindow.show()

    QTest.mouseClick(mainWindow.addStateButton, Qt.LeftButton)
    QTest.mouseClick(mainWindow.view.viewport(), Qt.LeftButton, Qt.NoModifier, QtCore.QPoint(400,200))
    QTest.mouseClick(mainWindow.view.viewport(), Qt.LeftButton, Qt.NoModifier, QtCore.QPoint(100,250))
    QTest.mouseClick(mainWindow.addTransitionButton, Qt.LeftButton)
    QTest.mousePress(mainWindow.view.viewport(), Qt.LeftButton, Qt.NoModifier, QtCore.QPoint(400,200))
    QTest.mouseMove(mainWindow.view.viewport(), QtCore.QPoint(100,250))
    QTest.mouseRelease(mainWindow.view.viewport(), Qt.LeftButton, Qt.NoModifier, QtCore.QPoint(100,250))
        
    sys.exit(app.exec_()) 
