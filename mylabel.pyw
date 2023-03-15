from PyQt6 import QtCore, QtWidgets


class MyLabel(QtWidgets.QLabel):
    colorYellow = "#FFFF90"
    colorOrange = "#F5D8C1"
    colorGray = "#E8E8E8"
    colorBlack = "#000000"
    colorRed = "#D77A38"

    changeCellFocus = QtCore.pyqtSignal(int)

    def __init__(self, id, bgColor, parent=None):
        QtWidgets.QLabel.__init__(self, parent)

        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(30, 30)
        self.setMargin(0)
        self.setText("")
        if id < 0 or id > 80:
            id = 0
        self.id = id
        self.isCellChanged = True
        self.fontColorCurent = self.colorBlack
        self.bgColorDefault = bgColor
        self.bgColorCurrent = bgColor
        self.showColorCurrent()

    def showColorCurrent(self):
        self.setStyleSheet("background-color:" + self.bgColorCurrent +
                           "; color:" + self.fontColorCurent + ";")

    def mousePressEvent(self, ev) -> None:
        self.changeCellFocus.emit(self.id)
        QtWidgets.QLabel.mousePressEvent(self, ev)

    def setCellFocus(self):
        self.bgColorCurrent = self.colorYellow
        self.showColorCurrent()

    def clearCellFocus(self):
        self.bgColorCurrent = self.bgColorDefault
        self.showColorCurrent()

    def setCellBlock(self):
        self.isCellChanged = False
        self.fontColorCurent = self.colorRed
        self.showColorCurrent()

    def clearCellBlock(self):
        self.isCellChanged = True
        self.fontColorCurent = self.colorBlack
        self.showColorCurrent()

    def setNewText(self, text):
        if self.isCellChanged:
            self.setText(text)


