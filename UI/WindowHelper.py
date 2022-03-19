#Helper functions when constructing different windows
from Configuration import widgetConfiguration, borderConfiguration
from PyQt5.QtCore import*
from PyQt5.QtGui import*
from PyQt5.QtWidgets import*

def constructLabel(text, font=widgetConfiguration["font"], size=widgetConfiguration["size"], bold=widgetConfiguration["bold"], border=widgetConfiguration["border"]):
    label=QLabel(text)
    font=QFont(font, size)
    font.setBold(bold)
    label.setFont(font)
    if border:
        label.setStyleSheet("border: "+borderConfiguration["size"]+"px "+borderConfiguration["type"]+" "+borderConfiguration["color"]+";")
    label.setAlignment(Qt.AlignCenter)
    return label

def constructButton(text, font=widgetConfiguration["font"], size=widgetConfiguration["size"]):
    button=QPushButton(text)
    button.setFont(QFont(font, size))
    return button

