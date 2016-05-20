#! /usr/bin/env python

"""
svipdagr is a systray-based program for knowing how late it is
Original idea of code copypasted from http://rowinggolfer.blogspot.se/2011/06/pyqt-qsystrayicon-example.html
"""
import sys, json
from PyQt4 import QtGui, QtCore


class SysTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None, config_data):
        super().__init__()
        self.config_data = config_data
        self.icon = self.init_icon()
        self.gui = GUI(self.config_data)

        #self.setIcon(QtGui.QIcon.fromTheme("exit24.png"))
        self.setIcon(self.icon)
        self.update_icon()
        self.setToolTip('This is a tooltip for the icon')
        self.activated.connect(self.click_trap)

        self.right_menu = RightClickMenu()
        #self.setContextMenu(self.right_menu) #TODO see issue #4
    
    def init_icon(self):
        #TODO Figure out the right color
        color = 'blue'
        pixmap = QtGui.QPixmap(100, 100)
        pixmap.fill(QtGui.QColor(color))
#        color = QtGui.QColor()
#        pixmap = QtGui.QPixmap("icon.png")
#        painter = QtGui.QPainter(pixmap)
#        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
#        painter.setBrush(color)
#        painter.setPen(color)
#        painter.drawRect(pixmap.rect())
        return QtGui.QIcon(pixmap)

    def click_trap(self, value):
        if value == self.Trigger: #left click!
            if self.gui.isVisible():
                self.gui.hide()
            else:
                self.gui.show()

    def update_icon(self):
        #TODO figure out icon color
        #TODO repaint pixmap?
        pass

    def show(self):
        QtGui.QSystemTrayIcon.show(self)
        #QtCore.QTimer.singleShot(100, self.welcome)


class GUI(QtGui.QWidget):
    #TODO Read everything from some decent config in Dropbox for good appiness
    def __init__(self, config_data):
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
        tformat_lbl = QtGui.QLabel('Tidsformat, visning:')

        apply_btn = QtGui.QButton('Verkställ')
        apply_btn.clicked.connect(self.update)

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
        grid.addWidget(apply_btn, 5, 1)

        self.setLayout(grid)

        self.setWindowTitle('Svipdagr')
        #self.show()

    def update(self):
        # see the textEdited() signal for automating this
        reveille_str = reveille_edit.text()
        optimum_str = optimum_edit.text()
        minute_format = minute_rbtn.isChecked()
        # TODO clean data
        reveille = reveille_str.strip()
        optimum_sleep = optimum_str.strip()
        color_early = [100, 100, 100]
        color_late = [255, 255, 255]
        config_data = {"reveille": reveille, 
                       "optimum_sleep": optimum_sleep,
                       "minute_format": minute_format,
                       "color_early": color_early,
                       "color_late": color_late}
        config_file = os.path.join('~/.config/svipdagr', 'config.json')
        write_config(config_file, config_data)

        self.hide()

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
        


class RightClickMenu(QtGui.QMenu): #NOTE Inactive right now
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


def read_config():
    config_file = '~/.config/svipdagr/config'
    if not os.path.exists(config_file):
        config_file = 'default_config.json'
    with open(config_file) as json_file:
        config_data = json.load(json_file)
        return config_data

def write_config(config_file, config_data):
    with open(config_file, 'w') as outfile:
        json.dump(config_data, outfile)


def main():
    app = QtGui.QApplication(sys.argv)
    config_data = read_config()
    tray = SysTrayIcon(config_data)
    tray.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
