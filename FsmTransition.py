# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 18:36:41 2014

@author: favi
"""

from PyQt4 import QtCore, QtGui
from FsmGraphicHandle import FsmGraphicHandle

class FsmTransition(QtGui.QGraphicsPathItem):
#class FsmTransition(QtGui.QGraphicsLineItem):
    def __init__(self, startItem, endItem, parent=None, scene=None):
        super(FsmTransition, self).__init__(parent, scene)

        self.arrowHead = QtGui.QPainterPath()
        #self.path = QtGui.QPainterPath()
        
        self.myStartItem = startItem
        self.myEndItem = endItem
        self.intermediatePoints = []
        self.updatePosition()
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        #self.myColor = QtCore.Qt.black
        #self.setPen(QtGui.QPen(self.myColor, 1, QtCore.Qt.SolidLine,
        #                       QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))

    def toStore(self):
        return "FsmTransition(startItemName='{0}', endItemName='{1}', scene=self)\n".format(self.startItem().stateName, self.endItem().stateName)

    def setColor(self, color):
        self.myColor = color

    def startItem(self):
        return self.myStartItem

    def endItem(self):
        return self.myEndItem

    def addIntermediatePoint(self, point):
        #print "addIntermediatePoint @({},{})".format(point.x(), point.y())
        
        p = FsmGraphicHandle(parent=self, scene=self.scene())
        p.setPos(point) #using setPos instead of constructor position
                        #because it didn't get the right coordinates

        self.intermediatePoints.append(p)
        self.updatePosition()
        
    def popIntermediatePoint(self):
        if len(self.intermediatePoints):
            p = self.intermediatePoints.pop()
            p.setParentItem(None)
            self.scene().removeItem(p)
            self.updatePosition()

    def addEndItem(self, endItem):
        self.myEndItem = endItem
        self.updatePosition()

    def shape(self):
        ps = QtGui.QPainterPathStroker()
        ps.setWidth(5)
        path = self.path()
        path.addPath(self.arrowHead)
        shapepath = ps.createStroke(path)

        return shapepath

    def boundingRect(self):
        return self.shape().boundingRect()

    def updatePosition(self):
        def computeControlPoints(K):
            '''compute cubicTo control points according to
            https://www.particleincell.com/2012/bezier-splines/ 

            input K should be a list of x(or y) coordinates of the
            knots 

            returns two lists of control point x(or y) coordinates of
            length=(len(K)-1 )

            '''
            n=len(K)
            #this is the tridiagonal matrix A 
            a = [1]*(n-3) + [2]
            b = [2] + [4]*(n-3) + [7]
            c = [1]*(n-2)

            #this is rhs
            d = [K[0]+2*K[1]]
            d +=[4*K[i]+2*K[i+1] for i in range(1, n-2)] 
            d +=[8*K[n-2]+K[n-1]]
            
            #solve Ax=d with the Thomas algorithm
            #TODO optimize it with np
            def TDMAsolve(a,b,c,d):
                n = len(d)
                for i in xrange(n-1):
                    d[i+1] -= 1. * d[i] * a[i] / b[i]
                    b[i+1] -= 1. * c[i] * a[i] / b[i]
                for i in reversed(xrange(n-1)):
                    d[i] -= d[i+1] * c[i] / b[i+1]
                return [d[i] / b[i] for i in xrange(n)]

            p1 = TDMAsolve(a,b,c,d)
            p2 = [2*K[i+1]-p1[i+1] for i in range(n-2)] + \
                 [0.5*(K[n-1]+p1[n-2])]
            return (p1,p2)

        #start the path
        path = QtGui.QPainterPath(self.myStartItem.pos())

        #if the path is at it beginning or it is a straight line to another state...
        if len(self.intermediatePoints)<2 or \
           not self.myEndItem and len(self.intermediatePoints)==0:            
            if self.myEndItem:                     
                path.lineTo(self.myEndItem.pos())
            elif self.intermediatePoints:
                path.lineTo(self.intermediatePoints[0].pos())
            self.lastSubPath = path
        else:
            itemList = [self.myStartItem]
            itemList += self.intermediatePoints
            if self.myEndItem:                     
                itemList += [self.myEndItem]

            k = [p.scenePos() for p in itemList]
            
            kx = [p.x() for p in k]
            ky = [p.y() for p in k]
            c1x,c2x = computeControlPoints(kx)
            c1y,c2y = computeControlPoints(ky)
            c1 = tuple(QtCore.QPointF(x,y) for x,y in zip(c1x,c1y))
            c2 = tuple(QtCore.QPointF(x,y) for x,y in zip(c2x,c2y))

            for cc1,cc2,kk in zip(c1,c2,k[1:]):       
                path.cubicTo(cc1,cc2,kk)
            # for cc1 in k[1:-1]: #temporary showing knot points -> moved to FsmGraphicHandle
            #     path.addEllipse(cc1, 2,2)
            self.lastSubPath = QtGui.QPainterPath(k[-2])
            self.lastSubPath.cubicTo(c1[-1],c2[-1],k[-1])

        self.setPath(path)

        self.update(self.boundingRect())

    def paint(self, painter, option, widget=None):
        #display shape for debug
        #painter.fillPath(self.shape(), QtCore.Qt.cyan)        
        
        
        if self.isSelected():
            c = QtGui.QColor() #TODO: highligh color should be taken from preference
            c.setHsv(30, 255, 255)
        else:
            c = QtCore.Qt.black

        painter.setPen(c)
        painter.setBrush(QtCore.Qt.NoBrush)
        
        
        path = self.path()        
        painter.drawPath(path)

        #draw arrow
        painter.setBrush(c)
        #arrow computation should be moved elsewhere
        arrowSize = 20
        arrowAperture = 20 #degrees
        angle = self.lastSubPath.angleAtPercent(1.)+180
        if self.myEndItem:
            arrowTip = QtCore.QLineF.fromPolar(self.myEndItem.diameter/2, angle).translated(self.myEndItem.pos()).p2()
        else:
            arrowTip = self.intermediatePoints[-1].pos()
        arrowP1 = QtCore.QLineF.fromPolar(arrowSize,angle+arrowAperture).translated(arrowTip).p2()             
        arrowC1 = QtCore.QLineF.fromPolar(arrowSize/2,angle).translated(arrowTip).p2()        
        arrowP2 = QtCore.QLineF.fromPolar(arrowSize,angle-arrowAperture).translated(arrowTip).p2()

        self.arrowHead = QtGui.QPainterPath()
        self.arrowHead.moveTo(arrowTip)
        for point in (arrowP1, arrowC1, arrowP2):
            self.arrowHead.lineTo(point)
        self.arrowHead.closeSubpath()
        painter.drawPath(self.arrowHead)
        

        
        
            
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
