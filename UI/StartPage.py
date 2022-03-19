from Configuration import pageConfiguration
from PyQt5.QtWidgets import*
from UI.WindowHelper import constructLabel

class StartPage(QWidget):
    '''
        The start page to display the title of the application
    and allow the user to use the application by pressing the button

        If bluetooth is implemented, it will start connecting when pressing
    the button and would show error message if the bluetooth connection is
    failed
    '''
    def __init__(self):
        super().__init__()
        self.resize(pageConfiguration["width"], pageConfiguration["height"])
        
        titleLabel=constructLabel("Sweat Monitoring App")
        layout=QVBoxLayout()
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel(""))
        layout.addWidget(titleLabel)
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel(""))
        self.setLayout(layout)

