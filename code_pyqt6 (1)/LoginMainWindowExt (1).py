import traceback

from PyQt6.QtWidgets import QMainWindow

from Final.code_pyqt6.LoginMainWindow import Ui_MainWindow
from Final.code_pyqt6.MainWindowExt import MainWindowEx


class LoginMainWindowExt(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButtonlogin.clicked.connect(self.xuly_dangnhap)

    def xuly_dangnhap(self):
        try:
            self.MainWindow.hide()
            self.mainwindow = QMainWindow()
            self.myui = MainWindowEx()
            self.myui.setupUi(self.mainwindow)
            self.myui.show()
        except:
            traceback.print_exc()
