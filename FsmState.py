from PyQt4 import QtGui, QtCore

class FsmState(QtGui.QGraphicsEllipseItem):
#class FsmState(QtGui.QGraphicsItem):
    
    def __init__(self, contextMenu, parent=None, scene=None):
        super(FsmState, self).__init__(parent, scene)

        self.stateName = "S0"
        self.diameter = 50
        self.setRect(self.diameter//-2,self.diameter//-2,self.diameter,self.diameter)
        self.arrows = []
        self.contextMenu = contextMenu

        #self.setPolygon(self.myPolygon)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges, True)
                
    def paint(self, painter, option, widget=None):
        if self.isSelected():
            painter.setBrush(QtCore.Qt.yellow)
        else:
            painter.setBrush(QtCore.Qt.cyan)
        painter.drawEllipse(-self.diameter/2, -self.diameter/2, self.diameter, self.diameter)
 #       super(FsmState, self).paint(painter, option, widget)
        painter.drawText(self.boundingRect(), QtCore.Qt.AlignCenter, self.stateName)

    def removeArrow(self, arrow):
        try:
            self.arrows.remove(arrow)
        except ValueError:
            pass

    def removeArrows(self):
        for arrow in self.arrows[:]:
            arrow.startItem().removeArrow(arrow)
            arrow.endItem().removeArrow(arrow)
            self.scene().removeItem(arrow)

    def addArrow(self, arrow):
        self.arrows.append(arrow)

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
            for arrow in self.arrows:
                arrow.updatePosition()
        
        return super(FsmState, self).itemChange(change,value)


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
    QTest.mouseClick(mainWindow.linePointerButton, Qt.LeftButton)
    QTest.mousePress(mainWindow.view.viewport(), Qt.LeftButton, Qt.NoModifier, QtCore.QPoint(400,200))
    QTest.mouseMove(mainWindow.view.viewport(), QtCore.QPoint(100,250))
    QTest.mouseRelease(mainWindow.view.viewport(), Qt.LeftButton, Qt.NoModifier, QtCore.QPoint(100,250))
        
    sys.exit(app.exec_()) 