from PyQt4 import QtCore, QtGui

class FsmGraphicHandle(QtGui.QGraphicsRectItem):
    def __init__(self, parent=None, scene=None):
        self.SIDE=4.
        super(FsmGraphicHandle, self).__init__(0, 0,
                                               self.SIDE, self.SIDE, parent)


    def paint(self, painter, option, widget=None):
            painter.drawRect(-self.SIDE/2, -self.SIDE/2,
                             self.SIDE, self.SIDE)
