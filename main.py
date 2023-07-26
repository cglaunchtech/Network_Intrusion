import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from dashboard import Dashboard
from data import Data
from page_handler import PageWindow


class Home(QtWidgets.QMainWindow):
    def __init__(self):
        super(Home, self).__init__()

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.pages = {}

        self.home_page(Dashboard(self), 'dashboard')
        self.home_page(Data(), 'data')
        self.goto('dashboard')

    def home_page(self, page, name):
        self.pages[name] = page
        self.stacked_widget.addWidget(page)

        if isinstance(page, PageWindow):
            page.gotoSignal.connect(self.goto)

    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.pages:
            self.stacked_widget.setCurrentWidget(self.pages[name])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    home = Home()
    home.showMaximized()
    sys.exit(app.exec_())
