import sys

from PyQt6 import QtCore, QtWidgets, QtGui
from modules.mylabel import MyLabel


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # по умолчанию  в QWidget наведение фокуса отключено
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

        vBoxMain = QtWidgets.QVBoxLayout()

        # рамка под основным полем
        frame1 = QtWidgets.QFrame()
        frame1.setStyleSheet("background-color: #9AA6A7; border:1px solid #9AA6A7;")

        # сетка для клеток
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(0)

        # массив id клеток светло-серого цвета
        idColor = (3, 4, 5, 12, 13, 14, 21, 22, 23, 27, 28, 29, 36, 37, 38, 45, 46, 47,
                   33, 34, 35, 42, 43, 44, 51, 52, 53, 57, 58, 59, 66, 67, 68, 75, 76, 77)

        # создаем клетки разного цвета
        self.cells = [MyLabel(i, MyLabel.colorGray if i in idColor else MyLabel.colorOrange) for i in range(0, 81)]

        # фокус на первой клетке
        self.cells[0].setCellFocus()

        # создаем атрибут класса, помещаем в него первую клетку
        self.idCellInFocus = 0

        # помещаем все созданные ячейки в сетку

        i = 0
        for j in range(0, 9):
            for k in range(0, 9):
                grid.addWidget(self.cells[i], j, k)
                i += 1

        # у всех ячеек задаем пока еще не созданный обработчик(onChangeCellFocus) сигнала changeCellFocus
        for cell in self.cells:
            cell.changeCellFocus.connect(self.onChangeCellFocus)

        # Помещаем сетку в панель с рамкой
        frame1.setLayout(grid)
        vBoxMain.addWidget(frame1, QtCore.Qt.AlignmentFlag.AlignHCenter)

        # создаем контейнер frame для кнопок управления, устанавливаем размеры

        frame2 = QtWidgets.QFrame()
        frame2.setFixedSize(300, 36)

        # лэйаут для кнопок

        hbox = QtWidgets.QHBoxLayout()
        hbox.setSpacing(1)

        btns = []
        for i in range(1, 10):
            btn = QtWidgets.QPushButton(str(i))
            btn.setFixedSize(27, 27)
            btn.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
            btns.append(btn)

        btn = QtWidgets.QPushButton("X")
        btn.setFixedSize(27, 27)
        btns.append(btn)

        for btn in btns:
            hbox.addWidget(btn)

        btns[0].clicked.connect(self.onBtn1Clicked)
        btns[1].clicked.connect(self.onBtn2Clicked)
        btns[2].clicked.connect(self.onBtn3Clicked)
        btns[3].clicked.connect(self.onBtn4Clicked)
        btns[4].clicked.connect(self.onBtn5Clicked)
        btns[5].clicked.connect(self.onBtn6Clicked)
        btns[6].clicked.connect(self.onBtn7Clicked)
        btns[7].clicked.connect(self.onBtn8Clicked)
        btns[8].clicked.connect(self.onBtn9Clicked)
        btns[9].clicked.connect(self.onBtnXClicked)

        frame2.setLayout(hbox)
        vBoxMain.addWidget(frame2, QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(vBoxMain)

    def onChangeCellFocus(self, id):
        if self.idCellInFocus != id and not (id < 0 or id > 80):
            self.cells[self.idCellInFocus].clearCellFocus()
            self.idCellInFocus = id
            self.cells[id].setCellFocus()

    def keyPressEvent(self, evt: QtGui.QKeyEvent) -> None:
        key = evt.key()
        if key == QtCore.Qt.Key.Key_Up:
            tid = self.idCellInFocus - 9
            if tid < 0:
                tid += 81
            self.onChangeCellFocus(tid)
        elif key == QtCore.Qt.Key.Key_Right:
            tid = self.idCellInFocus + 1
            if tid > 80:
                tid -= 81
            self.onChangeCellFocus(tid)
        elif key == QtCore.Qt.Key.Key_Down:
            tid = self.idCellInFocus + 9
            if tid > 80:
                tid -= 81
            self.onChangeCellFocus(tid)
        elif key == QtCore.Qt.Key.Key_Left:
            tid = self.idCellInFocus - 1
            if tid < 0:
                tid += 81
            self.onChangeCellFocus(tid)
        elif key >= QtCore.Qt.Key.Key_1 and key <= QtCore.Qt.Key.Key_9:
            self.cells[self.idCellInFocus].setNewText(chr(key))
        elif key == QtCore.Qt.Key.Key_Backspace or \
                key == QtCore.Qt.Key.Key_Delete or \
                key == QtCore.Qt.Key.Key_Space:
            self.cells[self.idCellInFocus].setNewText("")
        QtWidgets.QWidget.keyPressEvent(self, evt)

    def onBtn1Clicked(self):
        self.cells[self.idCellInFocus].setNewText("1")

    def onBtn2Clicked(self):
        self.cells[self.idCellInFocus].setNewText("2")

    def onBtn3Clicked(self):
        self.cells[self.idCellInFocus].setNewText("3")

    def onBtn4Clicked(self):
        self.cells[self.idCellInFocus].setNewText("4")

    def onBtn5Clicked(self):
        self.cells[self.idCellInFocus].setNewText("5")

    def onBtn6Clicked(self):
        self.cells[self.idCellInFocus].setNewText("6")

    def onBtn7Clicked(self):
        self.cells[self.idCellInFocus].setNewText("7")

    def onBtn8Clicked(self):
        self.cells[self.idCellInFocus].setNewText("8")

    def onBtn9Clicked(self):
        self.cells[self.idCellInFocus].setNewText("9")

    def onBtnXClicked(self):
        self.cells[self.idCellInFocus].setNewText("")

    def onClearAllCells(self):
        for cell in self.cells:
            cell.setNewText("")
            cell.clearCellBlock()

    def onBlockCell(self):
        cell = self.cells[self.idCellInFocus]
        if cell.text() != "":
            if cell.isCellChanged:
                cell.setCellBlock()

    def onBlockCells(self):
        for cell in self.cells:
            if cell.text() and cell.isCellChanged:
                cell.setCellBlock()

    def onClearBlockCell(self):
        cell = self.cells[self.idCellInFocus]
        if not cell.isCellChanged:
            cell.clearCellBlock()

    def onClearBlockCells(self):
        for cell in self.cells:
            if not cell.isCellChanged:
                cell.clearCellBlock()

    # сохранение данных

    def getDataAllCells(self):
        listAllData = []
        for cell in self.cells:
            listAllData.append("0" if cell.isCellChanged else "1")
            s = cell.text()
            listAllData.append(s if len(s) == 1 else "0")
        return "".join(listAllData)

    def getDataAllCellsMini(self):
        listAllData = []
        for cell in self.cells:
            s = cell.text()
            listAllData.append(s if len(s) == 1 else "0")
        return "".join(listAllData)

    def getDataCellsExcel(self):
        numbers = (9, 18, 27, 36, 45, 54, 63, 72)
        listAllData = [self.cells[0].text()]
        for i in range(1, 81):
            listAllData.append("\r\n" if i in numbers else "\t")
            listAllData.append(self.cells[i].text())
        listAllData.append("\r\n")
        return "".join(listAllData)

    def setDataAllCells(self, data):
        l = len(data)
        if l == 81:
            for i in range(0, 81):
                if data[i] == "0":
                    self.cells[i].setText("")
                    self.cells[i].clearCellBlock()
                else:
                    self.cells[i].setText(data[i])
                    self.cells[i].clearCellBlock()
            self.onChangeCellFocus(0)
        if l == 162:
            for i in range(0, 162, 2):
                if data[i] == "0":
                    self.cells[i // 2].clearCellBlock()
                else:
                    self.cells[i // 2].setCellBlock()
                self.cells[i // 2].setText("" if data[i + 1] == "0" else data[i + 1])
            self.onChangeCellFocus(0)

    def print(self, printer):
        penText = QtGui.QPen(QtGui.QColor(MyLabel.colorBlack), 1)
        penBorder = QtGui.QPen(QtGui.QColor(QtCore.Qt.GlobalColor.darkGray), 1)
        brushOrange = QtGui.QBrush(QtGui.QColor(MyLabel.colorOrange))
        brushGray = QtGui.QBrush(QtGui.QColor(MyLabel.colorGray))

        painter = QtGui.QPainter()
        painter.begin(printer)

        painter.setFont(QtGui.QFont("Veranda", pointSize=14))

        i = 0
        for j in range(0, 9):
            for k in range(0, 9):
                x = k * 30
                y = j * 30

                painter.setPen(penBorder)
                painter.setBrush(brushGray if self.cells[i].bgColorDefault == MyLabel.colorGray else brushOrange)
                painter.drawRect(x, y, 30, 30)
                painter.setPen(penText)
                painter.drawText(x, y, 30, 30, QtCore.Qt.AlignmentFlag.AlignCenter, self.cells[i].text())
                i += 1

        painter.end()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = Widget()
    win.show()
    sys.exit(app.exec())