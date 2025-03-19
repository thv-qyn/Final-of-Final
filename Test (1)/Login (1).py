from PyQt6.QtWidgets import QApplication, QMainWindow

from Final.code_pyqt6.LoginMainWindowExt import LoginMainWindowExt

app=QApplication([])
mainwindow=QMainWindow()
myui=LoginMainWindowExt()
myui.setupUi(mainwindow)
myui.showWindow()
app.exec()