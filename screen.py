from PyQt5 import QtCore, QtWidgets, QtGui
from fractal import Fractal

class Screen(QtWidgets.QGraphicsView):
    def __init__(self, frac: Fractal, parent=None):
        super().__init__(parent)
        
        #Disable scrollbars
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        #Scene
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)

        self.cords = [ [None, None], None]
        self.drawing = 0            #{'0':'not drawing', '1':'drawing', '-1':'drawing complete'}

        self.update_m(frac)
    
    def update_m(self, frac: Fractal):
        self.fractal = frac
        self.loadedSet = self.fractal.config

    def loadImage(self, img):
        self.scene.clear()
        self.qimg = QtGui.QPixmap(QtGui.QImage(img.tobytes(), img.shape[1], img.shape[0], 3*img.shape[1], QtGui.QImage.Format.Format_RGB888))
        self.scene.addPixmap(self.qimg)
        size = self.loadedSet['IMAGE_SIZE']
        self.scene.setSceneRect(0,0,size,size)
        
        self.ensureVisible(self.scene.sceneRect())
        self.fitInView(self.scene.sceneRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        
        #self.reset

    def update_box_set(self):
       #Mapping image cords to set cords
        x = self.mapval(self.cords[0][0], 0, self.loadedSet['IMAGE_SIZE'], self.loadedSet['SET_X'], self.loadedSet['SET_X']+self.loadedSet['SET_SIZE'])
        y = self.mapval(self.cords[0][1] + self.cords[1], 0, self.loadedSet['IMAGE_SIZE'], self.loadedSet['SET_Y']+self.loadedSet['SET_SIZE'], self.loadedSet['SET_Y'])

        s = (self.loadedSet['SET_SIZE']/self.loadedSet['IMAGE_SIZE']) * self.cords[1]

        self.nextSet = {
            'SET_X':x,
            'SET_Y':y,
            'SET_SIZE':s
        }

        print("Selected Box:", self.nextSet)

    def mapval(self, val, olow, ohigh, nlow, nhigh):
        return nlow + (val - olow)*((nhigh-nlow)/(ohigh-olow))
    

    # Event Handling
    def wheelEvent(self, event: QtGui.QWheelEvent):
        '''
        Zoom in and out event
        '''
        scaleFactor = 1.1

        pos = event.pos()
        posf = self.mapToScene(pos)

        if (event.angleDelta().y()>0):
            self.scale(scaleFactor, scaleFactor)
        else:
            self.scale(1/scaleFactor, 1/scaleFactor)

        w = self.viewport().width()
        h = self.viewport().height()
        wf = self.mapToScene(w-1,0).x() - self.mapToScene(0,0).x()
        hf = self.mapToScene(0, h-1).y() - self.mapToScene(0,0).y()

        lf = posf.x() - pos.x() * wf/w
        tf = posf.y() - pos.y() * hf/h

        self.ensureVisible(lf, tf, wf, hf, 0, 0)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if (event.button() == 2):
            #Reset the box if right mouse button clicked
            self.scene.clear()
            self.scene.addPixmap(self.qimg)
            self.drawing = 0
            self.nextSet = None
        elif (not self.drawing and event.button() == 1):
            clicked_cords = self.mapToScene( event.pos() )
            x = clicked_cords.x()
            y = clicked_cords.y()

            if((x<self.loadedSet['IMAGE_SIZE'] and x>0) and (y<self.loadedSet['IMAGE_SIZE'] and y>0)):#Inside scene?
                self.drawing = 1
                self.cords[0] = [ x, y ]

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        '''
        Draw the selcting box
        '''
        if(self.drawing == 1):
            current_cord = self.mapToScene( event.pos() )
            cx = current_cord.x()
            cy = current_cord.y()
            
            if ((cx<self.loadedSet['IMAGE_SIZE'] and cx>0) and (cy<self.loadedSet['IMAGE_SIZE'] and cy>0)):
                x = self.cords[0][0]
                y = self.cords[0][1]

                w = cx - x
                h = cy - y

                s = min(w, h)
                
                self.cords[1] = s

                self.scene.clear()
                self.scene.addPixmap(self.qimg)
                self.scene.addRect(x, y, s, s)
        
    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        curr = self.mapToScene(event.pos())
        curr = [curr.x(), curr.y()]
        if (event.button() == 1 and curr != self.cords[0]):
            self.drawing = -1
            self.update_box_set()