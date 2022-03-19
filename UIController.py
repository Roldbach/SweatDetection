
from DataBase import DataBase
from PyQt5.QtWidgets import*
from UI.MainPage import MainPage
from UI.SettingPage import SettingPage
from UI.Window import Window
from UI.StartPage import StartPage

class UIController:
    def __init__(self):
        self.dataBase=DataBase()
        self.application=QApplication([])
        self.window=Window()
        self.startPage=StartPage()
        self.mainPage=MainPage()
        self.settingPage=SettingPage()
        
        self.setStartPage()
        self.setMainPage()
        self.setSettingPage()
        self.window.addPage(self.settingPage)

    def getWindow(self):
        return self.window
    
    def setStartPage(self):
        '''
            Within the start page:
            (1) The start button should allow user to jump
                to the main page
        '''
        self.startPage.startButton.clicked.connect(lambda:self.window.switchPage(1))
        self.window.addPage(self.startPage)

    def setMainPage(self):
        '''
            Within the main page:
            (1) The plot button should allow user to jump
                to the plot page
            (2) The setting button should allow user to jump
                to the setting page
        '''
        self.mainPage.settingButton.clicked.connect(lambda:self.window.switchPage(2))
        self.window.addPage(self.mainPage)
    
    def setSettingPage(self):
        '''
            Within the setting page:
            (1) Each change button should allow user to change
                the corresponding setting by entering the value
            (2) The back button should allow user to jump back
                to the main page
        '''
        self.settingPage.changeMaximumStorageButton.clicked.connect(lambda:self.getMaximumStorage("Maximum Storage", "Please enter a new value:", "Please enter a valid integer."))

    def getMaximumStorage(self, title, description, error):
        '''
            Ask the user to input a valid integer by showing a dialog box
        If the input is valid, update the corresponding label and database,
        otherwise display error message and repeat

        input:
            title: String, the title displayed at the top
            description: String, describes the necessary information to the user
            error: String, the error message displayed to the user if not a valid input
        '''
        while True:
            text, _=QInputDialog.getText(self.window, title, description, QLineEdit.Normal, "")
            try:
                result=self.checkInteger(text)
                self.dataBase.setMaximumStorage(result)
                self.settingPage.updateMaximumStorage(result)
                return
            except:
                self.showError(error)
    
    def checkInteger(self, text):
        '''
            Check whether the given text is a valid non-negative integer
        and return it, otherwise raise exception

        input:
            text: String, the text given by the user
        '''
        try:
            result=int(text.strip(""))
        except:
            raise ValueError
        
        if result>0:
            return result
        else:
            raise ValueError

    def switchMainPage(self):
        '''
            Before displaying the main page:
            (1) Update all labels using the latest data
                in the database
        '''

    def getLatestData(self):
        '''
            Return the latest data as a dictionary
        '''
        result=self.dataBase.getLatest()
        
    def showError(self, text):
        '''
            Show an error message box to the user using the given text
        '''
        message=QMessageBox()
        message.setIcon(QMessageBox.Critical)
        message.setWindowTitle("Error")
        message.setStandardButtons(QMessageBox.Ok)
        message.setText(text)
        message.exec_()


    
    