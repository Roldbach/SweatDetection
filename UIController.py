
from DataBase import DataBase
from PyQt5.QtWidgets import QApplication
from UI.Window import Window
from UI.StartPage import StartPage

class UIController:
    '''
        The class to set up pages properly and connect labels and buttons to
    functions

        This class contains following attributes:
        (1) dataBase: DataBase
        (2) application: QApplication
        (3) window: Window, the main window in the application
        (4) startPage: StartPage
    '''

    def __init__(self):
        self.dataBase=DataBase()
        self.application=QApplication([])
        self.window=Window()
        self.startPage=StartPage()

        self.window.addPage(self.startPage)
        self.window.switchPage(0)

    def getWindow(self):
        return self.window
