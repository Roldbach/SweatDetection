from Configuration import pageConfiguration
from PyQt5.QtWidgets import*

class Window(QWidget):
    '''
        The main window which could control different pages

        The index of each sub window is shown below:
        (0) Start Page
        (1) Main Page
        (2) Plot Page
        (3) Setting Page
    '''
    def __init__(self):
        super().__init__()
        self.resize(pageConfiguration["width"], pageConfiguration["height"])
        self.stack=QStackedLayout()
        self.setLayout(self.stack)
    
    def addPage(self, page):
        self.stack.addWidget(page)
    
    def switchPage(self, index):
        self.stack.setCurrentIndex(index)