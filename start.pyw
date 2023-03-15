from PyQt6 import QtWidgets, QtGui
import sys
from modules.mainwindow import MainWindow



app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon(r"modules/images/svd.png"))
window = MainWindow()
window.show()
sys.exit(app.exec())