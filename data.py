from PyQt5 import uic

from page_handler import PageWindow


class Data(PageWindow):
    def __init__(self):
        super(Data, self).__init__()
        self.layout = None
        self.central_widget = None
        uic.loadUi('data.ui', self)

        self.dashboard.mousePressEvent = lambda event: self.goto_page('dashboard')
        # self.liveBtn.clicked.connect(self.scan_host)

    def goto_page(self, event):
        self.goto(event)
