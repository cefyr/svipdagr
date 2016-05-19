#! /usr/bin/env python

"""
svipdagr is a systray-based program for knowing how late it is
Original idea of code copypasted from http://rowinggolfer.blogspot.se/2011/06/pyqt-qsystrayicon-example.html
"""
import sys
from PyQt4 import QtGui, QtCore

class RightClickMenu(QtGui.QMenu):
    def __init__(self, parent=None):
        QtGui.QMenu.__init__(self, "Svipdagr", parent)

        quit_action = QtGui.QAction("&Quit", self)
        self.addAction(quit_action)
        quit_action.triggered.connect(QtGui.qApp.quit)

    def closeEvent(self, event):
        # 1st string is titlebar, 2nd is message, last param is default btn
        # Note that reply is a varaible that stores the return value!
        reply = QtGui.QMessageBox.question(self, 'Message',
                "Are you sure you want to quit?", QtGui.QMessageBox.Yes |
                QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    
class SysTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__()
        self.gui = GUI()

        self.setIcon(QtGui.QIcon.fromTheme("exit24.png"))
        self.setToolTip('This is a tooltip for the icon')
        self.activated.connect(self.click_trap)

        self.right_menu = RightClickMenu()
        self.setContextMenu(self.right_menu)
    

    def click_trap(self, value):
        if value == self.Trigger: #left click!
            if self.gui.isVisible():
                self.gui.hide()
            else:
                self.gui.show()

    def welcome(self):
        self.showMessage("Hello", "I should be aware of both buttons")
        
    def show(self):
        QtGui.QSystemTrayIcon.show(self)
        #QtCore.QTimer.singleShot(100, self.welcome)


class GUI(QtGui.QWidget):
    #TODO Read everything from some decent config in Dropbox for good appiness
    def __init__(self):
        super().__init__()

        # Night config widgets
        reveille_lbl = QtGui.QLabel('Revelj [HH:MM]:')
        reveille_edit = QtGui.QLineEdit()
        optimum_lbl = QtGui.QLabel('Sovtid [timmar]:')
        optimum_edit = QtGui.QLineEdit()

        # Time format widgets
        #tformat_group = QtGui.QGroupBox('Tidsformat')
        minute_rbtn = QtGui.QRadioButton('HH:MM')
        fraction_rbtn = QtGui.QRadioButton('HH,H')
        minute_rbtn.setChecked(True)
        # Time format layout
        #tformat_vbox = QtGui.QVBoxLayout()
        #tformat_vbox.addWidget(minute_rbtn)
        #tformat_vbox.addWidget(fraction_rbtn)
        #tformat_group.setLayout(tformat_vbox)
        tformat_lbl = QtGui.QLabel('Tidsformat:')

        # Grid layout for everything
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(reveille_lbl, 1, 0)
        grid.addWidget(reveille_edit, 1, 1)

        grid.addWidget(optimum_lbl, 2, 0)
        grid.addWidget(optimum_edit, 2, 1)

        #grid.addLayout(tformat_vbox, 3, 0, 2, 2)
        grid.addWidget(tformat_lbl, 3, 0)
        grid.addWidget(minute_rbtn, 3, 1)
        grid.addWidget(fraction_rbtn, 4, 1)

        self.setLayout(grid)

        self.setWindowTitle('Svipdagr')
        #self.show()

    def closeEvent(self, event):
        # 1st string is titlebar, 2nd is message, last param is default btn
        # Note that reply is a varaible that stores the return value!
        reply = QtGui.QMessageBox.question(self, 'Message',
                "Are you sure you want to quit?", QtGui.QMessageBox.Yes |
                QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        
def main():

    app = QtGui.QApplication(sys.argv)
    tray = SysTrayIcon()
    tray.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
