from PyQt5 import QtCore, QtWidgets
from screen import Screen

class FractalLoader(QtWidgets.QWidget):
    def __init__(self, m, parent=None):
        super().__init__(parent)
        horizontalLayout = QtWidgets.QHBoxLayout(self)

        self.display = Screen(m, parent)

        #Spacers
        spacerItem = QtWidgets.QSpacerItem(150, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        spacerItem1 = QtWidgets.QSpacerItem(150, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        
        #Label to show the selected box x and y val
        self.boxdetails = QtWidgets.QLabel(self)

        #Details Show Layout
        verticalLayout = QtWidgets.QVBoxLayout()
        verticalLayout.addItem(spacerItem)
        verticalLayout.addWidget(self.boxdetails)
        verticalLayout.addItem(spacerItem1)
        
        horizontalLayout.addWidget(self.display)
        horizontalLayout.addLayout(verticalLayout)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.setText)
        self.timer.start(500) #trigger .5 seconds

    def setText(self):
        if(self.display.drawing == -1): #Drawing Completed
            box_set = self.display.nextSet
            box_cords = self.display.cords
            
            text = f"*SET_CORD*\nx: {box_set['SET_X']}\ny: {box_set['SET_Y']}\nw: {box_set['SET_SIZE']}\n\n"
            text += f"*IMG_CORD*\nx: {box_cords[0][0]}\ny: {box_cords[0][1]}\nw: {box_cords[1]}"
            self.boxdetails.setText(text)
            self.display.drawing = 0
