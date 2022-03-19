#Helper functions when constructing different windows
from PyQt5.QtGui import*
from PyQt5.QtWidgets import*

def constructLabel(text, font="New Times Roman", size=16):
    label=QLabel(text)
    label.setFont(QFont(font, size))
    return label

