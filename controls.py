from PyQt5 import QtCore, QtWidgets


class Controls(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        horizontalLayout = QtWidgets.QHBoxLayout(self)
        verticalLayout = QtWidgets.QVBoxLayout()

        #Details showing label
        self.datashow = QtWidgets.QLabel(self)
        self.changeDetails(100)

        #Iteration slider
        self.iterations = QtWidgets.QSlider(self)
        self.iterations.setMinimum(100)
        self.iterations.setMaximum(1000)
        self.iterations.setOrientation(QtCore.Qt.Horizontal)
        self.iterations.setValue(100)
        self.iterations.valueChanged.connect(self.changeDetails)

        #Image size input field
        self.imageSize = QtWidgets.QLineEdit(self)
        self.imageSize.setText("1024")
        self.imageSize.setPlaceholderText("Image Size")

        verticalLayout.addWidget(self.iterations)
        verticalLayout.addWidget(self.imageSize)
        horizontalLayout.addLayout(verticalLayout)
        horizontalLayout.addWidget(self.datashow)

    def changeDetails(self, val):
        self.datashow.setText("Iterations: " + str(val))