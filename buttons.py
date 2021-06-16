from PyQt5 import QtWidgets


class Buttons(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        verticalLayout = QtWidgets.QVBoxLayout(self)

        self.btn_generate = QtWidgets.QPushButton(self)
        self.btn_saveimage = QtWidgets.QPushButton(self)
        self.btn_reset = QtWidgets.QPushButton(self)

        self.btn_generate.setText("Generate")
        self.btn_saveimage.setText("Save Image")
        self.btn_reset.setText("Reset")

        verticalLayout.addWidget(self.btn_generate)
        verticalLayout.addWidget(self.btn_reset)
        verticalLayout.addWidget(self.btn_saveimage)