from PyQt6 import QtCore, QtGui, QtWidgets, QtPrintSupport
from modules.widget import Widget
from modules.previewdialog import PreviewDialog
import re


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent,
                                       QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle("Sudoku 1.0.0")

        self.setStyleSheet("QFrame QPushButton{font-size:10pt;font-family:Veranda;color:black;font-weight:bold;}"
                           "MyLabel {font-size:14pt;font-family:Veranda;border:1px solid #9AA6A7}")

        self.settings = QtCore.QSettings("Кравецкий", "Судоку")
        self.printer = QtPrintSupport.QPrinter()

        self.sudoky = Widget()
        self.setCentralWidget(self.sudoky)

        menuBar = self.menuBar()
        toolBar = QtWidgets.QToolBar()

        myMenuFile = menuBar.addMenu("&Файл")

        action = myMenuFile.addAction(QtGui.QIcon(r"images/new.png"), "&Новый", QtGui.QKeySequence("Ctrl+N"),
                                      self.sudoky.onClearAllCells)

        toolBar.addAction(action)
        action.setStatusTip("Создание новой, пустой головоломки")

        action = myMenuFile.addAction(QtGui.QIcon(r"images/open.png"), "&Открыть...", QtGui.QKeySequence("Ctrl+O"), self.onOpenFile)
        toolBar.addAction(action)
        action.setStatusTip("Загрузка головоломки из файла")

        action = myMenuFile.addAction(QtGui.QIcon(r"images/save.png"), "Со&хранить...", QtGui.QKeySequence("Ctrl+S"), self.onSave)
        toolBar.addAction(action)
        action.setStatusTip("Сохранение головоломки в файле")

        action = myMenuFile.addAction(QtGui.QIcon(r"images/save.png"), "Со&хранить компактно...", QtGui.QKeySequence("Ctrl+L"), self.onSaveMini)
        action.setStatusTip("Сохранение головоломки в компактном формате")

        myMenuFile.addSeparator()
        toolBar.addSeparator()

        action = myMenuFile.addAction(QtGui.QIcon(r"images/print.png"), "&Печать...", QtGui.QKeySequence("Ctrl+P"), self.onPrint)
        toolBar.addAction(action)
        action.setStatusTip("Печать головоломки")

        action = myMenuFile.addAction(QtGui.QIcon(r"images/preview.png"), "П&редварительный просмотр...", self.onPreview)
        toolBar.addAction(action)
        action.setStatusTip("Предварительный просмотр головоломки")

        action = myMenuFile.addAction("&Параметры страницы...", self.onPageSetup)
        action.setStatusTip("Задание параметров страницы")


        myMenuFile.addSeparator()
        toolBar.addSeparator()

        action = myMenuFile.addAction(QtGui.QIcon(r"images/logout.png"), "&Выход", QtGui.QKeySequence("Ctrl+Q"),
                                      QtWidgets.QApplication.instance().quit)
        action.setStatusTip("Завершение работы программы")

        myMenuEdit = menuBar.addMenu("&Правка")

        #----------------------------------------------------------------------------------------------------

        action = myMenuEdit.addAction(QtGui.QIcon(r"images/copy.png"), "К&опировать", QtGui.QKeySequence("Ctrl+C"), self.onCopyData)
        toolBar.addAction(action)
        action.setStatusTip("Копирование головоломки в буфер обмена")

        action = myMenuEdit.addAction(QtGui.QIcon(r"images/copy.png"), "&Копировать компактно", QtGui.QKeySequence("Ctrl+M"), self.onCopyDataMini)
        action.setStatusTip("Копирование в компактном формате")

        action = myMenuEdit.addAction("Копировать &для Excel", self.onCopyDataExcel)
        action.setStatusTip("Копирование в формате MS Excel")

        action = myMenuEdit.addAction(QtGui.QIcon(r"images/paste.png"), "&Вставить", QtGui.QKeySequence("Ctrl+V"), self.onPasteData)
        toolBar.addAction(action)
        action.setStatusTip("Вставка головоломки из буфера обмена")

        action = myMenuEdit.addAction(QtGui.QIcon(r"images/paste.png"),"Вставить &из Excell", QtGui.QKeySequence("Ctrl+X"), self.onPasteDataExcel)
        action.setStatusTip("Вставка головоломки из MS Excell")

        myMenuEdit.addSeparator()
        toolBar.addSeparator()

        # ------------------------------------------------------------------------------------------------------

        action = myMenuEdit.addAction(QtGui.QIcon(r"images/lock.png"), "&Блокировать", QtCore.Qt.Key.Key_F2,
                                      self.sudoky.onBlockCell)
        action.setStatusTip("Блокирование активной ячейки")

        action = myMenuEdit.addAction(QtGui.QIcon(r"images/lockall.png"), "Б&локировать все", QtCore.Qt.Key.Key_F3,
                                      self.sudoky.onBlockCells)
        toolBar.addAction(action)
        action.setStatusTip("Блокирование всех ячеек")

        action = myMenuEdit.addAction(QtGui.QIcon(r"images/unlock.png"), "&Разблокировать", QtCore.Qt.Key.Key_F4,
                                      self.sudoky.onClearBlockCell)
        action.setStatusTip("Разблокирование активной ячейки")

        action = myMenuEdit.addAction(QtGui.QIcon(r"images/unlockall.png"), "Р&азблокировать все", QtCore.Qt.Key.Key_F5,
                                      self.sudoky.onClearBlockCells)
        toolBar.addAction(action)
        action.setStatusTip("Разблокирование всех ячеек")

        myMenuAbout = menuBar.addMenu("&Справка")

        action = myMenuAbout.addAction("О &программе...", self.aboutProgram)
        action.setStatusTip("Получение сведений о программе")

        action = myMenuAbout.addAction("О &Qt...", self.aboutQt)
        action.setStatusTip("Получение сведений о фреймворке Qt")

        toolBar.setMovable(False)
        toolBar.setFloatable(False)
        self.addToolBar(toolBar)

        statusBar = self.statusBar()
        statusBar.setSizeGripEnabled(False)
        statusBar.showMessage("\"Судоку\" приветствует вас")

        if self.settings.contains("X") and self.settings.contains("Y"):
            self.move(self.settings.value("X"), self.settings.value("Y"))

    def closeEvent(self, evt):
        g = self.geometry()
        self.settings.setValue("X", g.left())
        self.settings.setValue("Y", g.top())

    def aboutProgram(self):
        QtWidgets.QMessageBox.about(self, "О программе", "<center>\"Судоку\" v1.0.0<br><br>"
                                                         "Программа для просмотра и редактирования судоку<br><br>"
                                                         "(c) Кравецкий Д.Б., Акатова Е.С. 2023 г.")

    def aboutQt(self):
        QtWidgets.QMessageBox.aboutQt(self, title="О фреймворке Qt")



    def onCopyData(self):
        QtWidgets.QApplication.clipboard().setText(self.sudoky.getDataAllCells())

    def onCopyDataMini(self):
        QtWidgets.QApplication.clipboard().setText(self.sudoky.getDataAllCellsMini())

    def onCopyDataExcel(self):
        QtWidgets.QApplication.clipboard().setText(self.sudoky.getDataCellsExcel())


    def onPasteData(self):
        data = QtWidgets.QApplication.clipboard().text()
        if data:
            if len(data) == 81 or len(data) == 162:
                r = re.compile(r"[^0-9]")
                if not r.match(data):
                    self.sudoky.setDataAllCells(data)
                    return
        self.dataErrorMsg()

    def onPasteDataExcel(self):
        data = QtWidgets.QApplication.clipboard().text()
        if data:
            data = data.replace("\r", "")
            r = re.compile(r"([0-9]?[\t\n]){81}")
            if r.match(data):
                result = []
                if data[-1] == "\n":
                    data = data[:-1]
                dl = data.split("\n")
                for sl in dl:
                    dli = sl.split("\t")
                    for sli in dli:
                        if len(sli) == 0:
                            result.append("00")
                        else:
                            result.append("0" + sli[0])
                data = "".join(result)
                self.sudoky.setDataAllCells(data)
                return
        self.dataErrorMsg()

    def dataErrorMsg(self):
        QtWidgets.QMessageBox.information(self, "Судоку", "Данные имеют неправильный формат")


    def onOpenFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл", QtCore.QDir.homePath(), "Судоку (*.svd; *.txt)")[0]
        if filename:
            try:
                with open(filename, newline="") as f:
                    data = f.read()
            except:
                QtWidgets.QMessageBox.information(self, "Судоку", "Не удалось открыть файл")
                return
            if len(data) > 2:
                if data[-1] == "\n":
                    data = data[:-1]
                if len(data) == 81 or len(data) == 162:
                    r = re.compile(r"[^0-9]")
                    if not r.match(data):
                        self.sudoky.setDataAllCells(data)
                        return
            self.dataErrorMsg()

    def onSave(self):
        self.saveSVDFile(self.sudoky.getDataAllCells())

    def onSaveMini(self):
        self.saveSVDFile(self.sudoky.getDataAllCellsMini())

    def saveSVDFile(self, data):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, "Выберите файл", QtCore.QDir.homePath(), "Судоку (*.svd; *.txt)")[0]
        if filename:
            try:
                with open(filename, mode="w", newline="") as f:
                    f.write(data)
                self.statusBar().showMessage("Файл сохранен", 10000)
            except:
                QtWidgets.QMessageBox.information(self, "Судоку", "Не удалось сохранить файл")

    def onPrint(self):
        pd = QtPrintSupport.QPrintDialog(self.printer, parent=self)
        pd.setOptions(QtPrintSupport.QPrintDialog.PrintDialogOption.PrintToFile |
                      QtPrintSupport.QPrintDialog.PrintDialogOption.PrintSelection)

        if pd.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.sudoky.print(self.printer)

    def onPreview(self):
        print("Проверка превью")
        pd = PreviewDialog(self)
        pd.exec()

    def onPageSetup(self):
        pd = QtPrintSupport.QPageSetupDialog(self.printer, parent=self)
        pd.exec()











