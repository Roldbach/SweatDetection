from Configuration import pageConfiguration
from PyQt5.QtWidgets import*

from UI.WindowHelper import constructButton, constructLabel

class SettingPage(QWidget):
    '''
        The setting page to display settings and allow user to
    modify them

        If the change button is pressed, there would be a dialog box poping
    which allows the user to change the corresponding value
    '''
    def __init__(self):
        super().__init__()
        self.resize(pageConfiguration["width"], pageConfiguration["height"])

        self.maximumStorageLabel=constructLabel("Maximum Storage: 31 days")
        self.changeMaximumStorageButton=constructButton("Change")
        self.backButton=constructButton("Back")

        maximumStorageLayout=QHBoxLayout()
        maximumStorageLayout.addWidget(self.maximumStorageLabel)
        maximumStorageLayout.addStretch(2)
        maximumStorageLayout.addWidget(self.changeMaximumStorageButton)

        lowerLayout=QHBoxLayout()
        lowerLayout.addWidget(QLabel(""))
        lowerLayout.addWidget(self.backButton)
        lowerLayout.addWidget(QLabel(""))

        layout=QGridLayout()
        layout.addWidget(QLabel(""), 0, 0)
        layout.addWidget(QLabel(""), 1, 0)
        layout.addWidget(QLabel(""), 2, 0)
        layout.addWidget(QLabel(""), 3, 0)
        layout.addLayout(maximumStorageLayout, 4, 0)
        layout.addWidget(QLabel(""), 5, 0)
        layout.addWidget(QLabel(""), 6, 0)
        layout.addWidget(QLabel(""), 7, 0)
        layout.addWidget(QLabel(""), 8, 0)
        layout.addLayout(lowerLayout, 9, 0)
        self.setLayout(layout)
    
    def updateMaximumStorage(self, maximumStorage):
        if maximumStorage>1:
            self.maximumStorageLabel.setText(f"Maximum Storage: {maximumStorage} days")
        else:
            self.maximumStorageLabel.setText(f"Maximum Storage: {maximumStorage} day")
