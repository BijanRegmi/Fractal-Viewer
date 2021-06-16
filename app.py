from fractalloader import FractalLoader
from controls import Controls
from buttons import Buttons

from mandelbrot import mandelbrot

from PyQt5 import QtWidgets, QtCore

class APP(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        verticalLayout = QtWidgets.QVBoxLayout(self)

        self.m = mandelbrot()

        self.controlpanel = Controls(self)
        self.buttons = Buttons(self)
        self.display = FractalLoader(self.m, parent)

        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.addWidget(self.controlpanel)
        horizontalLayout.addWidget(self.buttons)

        verticalLayout.addWidget(self.display)
        verticalLayout.addLayout(horizontalLayout)

        self.display.display.loadImage(self.m.genImage())

        self.buttons.btn_generate.clicked.connect(self.generateclicked)
        self.buttons.btn_saveimage.clicked.connect(self.saveimageclicked)
        self.buttons.btn_reset.clicked.connect(self.resetclicked)

    def resetclicked(self, *args):
        self.m = mandelbrot()
        self.display.display.update_m(self.m)
        self.display.display.loadImage(self.m.genImage())
        print("Done resetting")
    
    def generateclicked(self, *args):
        try:
            new_P = self.display.display.nextSet
            im_size = int(self.controlpanel.imageSize.text())
            itter = self.controlpanel.iterations.value()
            new_P['ITERS'] = itter
            new_P['IMAGE_SIZE'] = im_size
            self.m.updateparams(**new_P)
            self.display.display.update_m(self.m)
            self.display.display.loadImage(self.m.genImage())
            print("Done generating image")
        except:
            print("Draw a box first")

        pass

    def saveimageclicked(self, *args):
        print(args)
        self.m.saveimage("mandelbrot.png")
        pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    
    ui = APP(None)

    
    ui.show()
    sys.exit(app.exec_())
