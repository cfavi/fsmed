from PyQt4 import QtGui, QtCore

#from FsmState import FsmState
#from FsmTransition import FsmTransition
from VHDLHighlighter import VHDLHighlighter

class FsmStateAction(QtGui.QGraphicsRectItem):
    def __init__(self, text="", parent=None,scene=None):
        super(FsmStateAction, self).__init__(parent,scene)

        self.textItem = QtGui.QGraphicsTextItem(text, parent=self);
        self.textItem.setTextWidth(150)
        self.textItem.setTextWidth(150)
        #self.textItem.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.highlighter = VHDLHighlighter(self.textItem.document())

        self.setPos(QtCore.QPoint(50, -50))
        self.setRect(self.textItem.boundingRect())

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges, True)




