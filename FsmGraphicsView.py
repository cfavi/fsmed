# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 00:41:46 2014
taken from http://stackoverflow.com/questions/15034627/qgraphicsview-double-click-events-and-scrollhanddrag-mode-item-issue

@author: favi
"""

from PyQt4 import QtGui, QtCore
Qt=QtCore.Qt

class FsmGraphicsView(QtGui.QGraphicsView):
    def __init__(self):
        super(FsmGraphicsView, self).__init__()
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self._isPanning = False
        self._mousePressed = False
        self.setMouseTracking(True)

    def mousePressEvent(self,  event):
        if event.button() == Qt.LeftButton:
            self._mousePressed = True
            if self._isPanning:
                self.setCursor(Qt.ClosedHandCursor)
                self._dragPos = event.pos()
                event.accept()
            else:
                super(FsmGraphicsView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._mousePressed and self._isPanning:
            newPos = event.pos()
            diff = newPos - self._dragPos
            self._dragPos = newPos
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - diff.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - diff.y())
            event.accept()
        else:
            super(FsmGraphicsView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.modifiers() & Qt.ControlModifier:
                self.setCursor(Qt.OpenHandCursor)
            else:
                self._isPanning = False
                self.setCursor(Qt.ArrowCursor)
            self._mousePressed = False
        super(FsmGraphicsView, self).mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event): pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control and not self._mousePressed:
            self._isPanning = True
            self.setCursor(Qt.OpenHandCursor)
        else:
            super(FsmGraphicsView, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            if not self._mousePressed:
                self._isPanning = False
                self.setCursor(Qt.ArrowCursor)
        else:
            super(FsmGraphicsView, self).keyPressEvent(event)


    def wheelEvent(self,  event):
        if QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            factor = 1.2;
            if event.delta() < 0:
                factor = 1.0 / factor
            self.scale(factor, factor)
        else:
            super(FsmGraphicsView,self).wheelEvent(event)