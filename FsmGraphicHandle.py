from PyQt4 import QtCore, QtGui

class FsmGraphicHandle(QtGui.QGraphicsRectItem):
    def __init__(self, parent=None, scene=None):
        self.SIDE=4.
        super(FsmGraphicHandle, self).__init__(0, 0,
                                               self.SIDE, self.SIDE, parent)
        self.setFlags(QtGui.QGraphicsItem.ItemIsMovable |
                       QtGui.QGraphicsItem.ItemIsSelectable )
                      
                      

    def shape(self):
        pp = QtGui.QPainterPath()
        pp.addRect(-self.SIDE/2-1, -self.SIDE/2-1,
                   self.SIDE+2, self.SIDE+2)
        return pp
    
    def boundingRect(self):
        return self.shape().boundingRect()
    
    def paint(self, painter, option, widget=None):
        #display shape for debug
        #painter.fillPath(self.shape(), QtCore.Qt.cyan)
        painter.setPen(QtCore.Qt.black)
        if self.isSelected():
            painter.setBrush(QtCore.Qt.yellow)
        else:
            painter.setBrush(QtCore.Qt.white)
        painter.drawRect(-self.SIDE/2, -self.SIDE/2,
                         self.SIDE, self.SIDE)

    def mouseMoveEvent(self, event):
        self.parentItem().updatePosition()
        super(FsmGraphicHandle, self).mouseMoveEvent(event)
