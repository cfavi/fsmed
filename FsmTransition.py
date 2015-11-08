# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 18:36:41 2014

@author: favi
"""

from PyQt4 import QtCore, QtGui

class FsmTransition(QtGui.QGraphicsPathItem):
#class FsmTransition(QtGui.QGraphicsLineItem):
    def __init__(self, startItem, endItem, parent=None, scene=None):
        super(FsmTransition, self).__init__(parent, scene)

        self.arrowHead = QtGui.QPolygonF()
        self.path = QtGui.QPainterPath()
        
        self.myStartItem = startItem
        self.myEndItem = endItem
        self.intermediatePoints = []
        self.updatePosition()
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.myColor = QtCore.Qt.black
        self.setPen(QtGui.QPen(self.myColor, 1, QtCore.Qt.SolidLine,
                               QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))

    def toStore(self):
        return "FsmTransition(startItemName='{0}', endItemName='{1}', scene=self)\n".format(self.startItem().stateName, self.endItem().stateName)

    def setColor(self, color):
        self.myColor = color

    def startItem(self):
        return self.myStartItem

    def endItem(self):
        return self.myEndItem

    def addIntermediatePoint(self, point):        
        self.intermediatePoints.append(point)
        self.updatePosition()
        
    def popIntermediatePoint(self):
        if len(self.intermediatePoints):
            self.intermediatePoints.pop()
            self.updatePosition()

    def addEndItem(self, endItem):
        self.myEndItem = endItem
        self.updatePosition()

    # def boundingRect(self):
    #     extra = (self.pen().width() + 20) / 2.0
    #     p1 = self.line().p1()
    #     p2 = self.line().p2()
    #     return QtCore.QRectF(p1, QtCore.QSizeF(p2.x() - p1.x(), p2.y() - p1.y())).normalized().adjusted(-extra, -extra, extra, extra)

    # def shape(self):
    #     path = super(FsmTransition, self).shape()
    #     path.addPolygon(self.arrowHead)
    #     return path

    

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
        #if the transition is closed we beautify it...
        if self.myEndItem:
            if len(self.intermediatePoints)==0:
                path.lineTo(self.myEndItem.pos())
            else:
                k = [self.myStartItem.pos()] + \
                    self.intermediatePoints + \
                    [self.myEndItem.pos()] 

                kx = [p.x() for p in k]
                ky = [p.y() for p in k]
                c1x,c2x = computeControlPoints(kx)
                c1y,c2y = computeControlPoints(ky)
                c1 = tuple(QtCore.QPointF(x,y) for x,y in zip(c1x,c1y))
                c2 = tuple(QtCore.QPointF(x,y) for x,y in zip(c2x,c2y))
                
                for cc1,cc2,kk in zip(c1,c2,k[1:]):       
                    path.cubicTo(cc1,cc2,kk)
                for cc1 in c1+c2+tuple(k[1:-1]):
                    path.addEllipse(cc1, 5,5)
        else:
            for p in self.intermediatePoints:
                path.lineTo(p)

                
        self.setPath(path)
        self.update(self.boundingRect())

#     def paint(self, painter, option, widget=None):
#         if (self.myStartItem.collidesWithItem(self.myEndItem)):
#             return

#         myStartItem = self.myStartItem
#         myEndItem = self.myEndItem
#         myColor = self.myColor
#         myPen = self.pen()
#         myPen.setColor(self.myColor)
#         arrowSize = 20.0
        
#         painter.setPen(myPen)
#         painter.setBrush(self.myColor)

#         centerLine = QtCore.QLineF(myStartItem.pos(), myEndItem.pos())
#         uv = centerLine.unitVector()        
#         endPos = myEndItem.pos()-QtCore.QPointF(uv.dx()*myEndItem.diameter/2, uv.dy()*myEndItem.diameter/2)
        
#         # endPolygon = myEndItem.polygon()
#         # p1 = endPolygon.first() + myEndItem.pos()

#         # intersectPoint = QtCore.QPointF()
#         # for i in endPolygon:
#         #     p2 = i + myEndItem.pos()
#         #     polyLine = QtCore.QLineF(p1, p2)
#         #     intersectType = polyLine.intersect(centerLine, intersectPoint)
#         #     if intersectType == QtCore.QLineF.BoundedIntersection:
#         #         break
#         #     p1 = p2
        
#         #self.setLine(QtCore.QLineF(intersectPoint, myStartItem.pos()))
#         self.setLine(QtCore.QLineF(endPos, myStartItem.pos()))
#         #self.setLine(centerLine)
#         line = self.line()
        
        
#         # 
# #        angle = math.acos(line.dx() / line.length())
# #        if line.dy() >= 0:
# #            angle = (math.pi * 2.0) - angle
# #        arrowAperture = math.pi/3.0 #angle 
# #        arrowP1 = line.p1() + QtCore.QPointF(math.sin(angle + arrowAperture) * arrowSize,
# #                                        math.cos(angle + arrowAperture) * arrowSize)
# #        arrowC1 = line.p1() -  QtCore.QPointF(uv.dx()*arrowSize/2, uv.dy()*arrowSize/2)                                
# #        arrowP2 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi - arrowAperture) * arrowSize,
# #                                        math.cos(angle + math.pi - arrowAperture) * arrowSize)
                                        
#         angle = line.angle() #in degrees
#         arrowAperture = 20 #degrees    
#         arrowP1 = QtCore.QLineF.fromPolar(arrowSize,angle+arrowAperture).translated(line.p1()).p2()                                 
#         arrowC1 = QtCore.QLineF.fromPolar(arrowSize/2,angle).translated(line.p1()).p2()        
#         arrowP2 = QtCore.QLineF.fromPolar(arrowSize,angle-arrowAperture).translated(line.p1()).p2()

#         self.arrowHead.clear()
#         for point in [line.p1(), arrowP1, arrowC1, arrowP2]:
#             self.arrowHead.append(point)

#         painter.drawLine(line)
#         painter.drawPolygon(self.arrowHead)
#         if self.isSelected():
#             painter.setPen(QtGui.QPen(myColor, 1, QtCore.Qt.DashLine))
#             myLine = QtCore.QLineF(line)
#             myLine.translate(0, 4.0)
#             painter.drawLine(myLine)
#             myLine.translate(0,-8.0)
#             painter.drawLine(myLine)
            
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
