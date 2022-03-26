import sys

from BluetoothServe import BluetoothServe
from Configuration import pageConfiguration
from DataBase import DataBase
from PyQt5.QtWidgets import*
from PyQt5.QtCore import QTimer
from UI.MainPage import MainPage
from UI.PlotPage import PlotPage
from UI.SettingPage import SettingPage
from UI.Window import Window
from UI.StartPage import StartPage

class UIController:
    def __init__(self):
        self.dataBase=DataBase()
        self.bluetooth=BluetoothServe()
        self.application=QApplication([])
        self.window=Window()
        self.timer=QTimer(self.window)
        self.startPage=StartPage()
        self.mainPage=MainPage()
        self.plotPage=PlotPage()
        self.settingPage=SettingPage()
        
        self.setStartPage()
        self.setMainPage()
        self.setPlotPage()
        self.setSettingPage()

    def getWindow(self):
        return self.window
    
    def setStartPage(self):
        '''
            Within the start page:
            (1) The start button should start the communication
                between arduino and PC via bluetooth
            (1) The start button should allow user to jump
                to the main page (only if the bluetooth connection
                is good)
        '''
        self.startPage.startButton.clicked.connect(self.connectBluetooth)
        self.startPage.startButton.clicked.connect(self.switchMainPage)
        self.window.addPage(self.startPage)

    def setMainPage(self):
        '''
            Within the main page:
            (1) The plot button should allow user to jump
                to the plot page
            (2) The setting button should allow user to jump
                to the setting page
        '''
        self.mainPage.plotButton.clicked.connect(self.switchPlotPage)
        self.mainPage.settingButton.clicked.connect(self.switchSettingPage)
        self.mainPage.quitButton.clicked.connect(self.quit)
        self.window.addPage(self.mainPage)

    def setPlotPage(self):
        '''
            Within the plot page:
            (1) Each radio button could change the scale
                of the plot
            (2) The back button should allow user to jump back
                to the main page
        '''
        self.plotPage.optionButton_1.clicked.connect(self.switchPlotPage)
        self.plotPage.optionButton_2.clicked.connect(self.switchPlotPage)
        self.plotPage.optionButton_3.clicked.connect(self.switchPlotPage)
        self.plotPage.backButton.clicked.connect(self.switchMainPage)
        self.window.addPage(self.plotPage)

    def setSettingPage(self):
        '''
            Within the setting page:
            (1) Each change button should allow user to change
                the corresponding setting by entering the value
            (2) The back button should allow user to jump back
                to the main page
        '''
        self.settingPage.changeMaximumStorageButton.clicked.connect(lambda:self.getMaximumStorage("Maximum Storage", "Please enter a new value:", "Please enter a valid integer."))
        self.settingPage.backButton.clicked.connect(self.switchMainPage)
        self.window.addPage(self.settingPage)

    def connectBluetooth(self):
        '''
            Connect to the arduino via bluetooth

            If successfully connecting to the sensor,
        start collecting data, otherwise report error
        to the user 
        '''
        self.bluetooth.connect()
        if self.bluetooth.status==True:
            self.timer.timeout.connect(self.updateMainPage)
            self.timer.start(1000)
        else:
            self.showError("Can't connect to the sensor. Please try again.")

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
            text, pressed=QInputDialog.getText(self.window, title, description, QLineEdit.Normal, "")
            try:
                if pressed is not True:
                    return
                else:
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
            Only switch to the main page when the bluetooth
        connection is good, otherwise force the user to stay
        at the start page and try again

            Before displaying the main page:
            (1) Update all labels using the latest data
                in the database
        '''
        if self.bluetooth.status==True:
            self.window.switchPage(1)
        else:
            self.showError("Can't connect to the sensor. Please try again.")
            self.window.switchPage(0)

    def switchPlotPage(self):
        self.plotPage.plot(self.getTruncatedData())
        self.window.switchPage(2)
    
    def switchSettingPage(self):
        self.settingPage.updateMaximumStorage(self.dataBase.getMaximumStorage())
        self.window.switchPage(3)

    def getTruncatedData(self):
        '''
            Return the truncated data as a dictionary,
        which could be directly used for plotting
        '''
        difference=self.plotPage.deformatChoice(self.plotPage.currentChoice)
        result={}
        result["Na"]=self.dataBase.truncateData(self.dataBase.getNa(), difference)
        result["K"]=self.dataBase.truncateData(self.dataBase.getK(), difference)
        result["Glucose"]=self.dataBase.truncateData(self.dataBase.getGlucose(), difference)
        result["CRP"]=self.dataBase.truncateData(self.dataBase.getCRP(), difference)
        result["ILBeta"]=self.dataBase.truncateData(self.dataBase.getILBeta(), difference)
        result["Temperature"]=self.dataBase.truncateData(self.dataBase.getTemperature(), difference)
        return result

    def updateMainPage(self):
        self.collect()
        self.mainPage.update(self.getLatestData())

    def collect(self):
        '''
            Collect the data from the arduino and 
        add it to the database after formatting
        '''
        if self.bluetooth.status==True:
            result=self.bluetooth.read()
            self.addData(result)
    
    def addData(self, text):
        '''
            Format the data from the arduino and add to the database
        '''
        index=text.index(",")
        flag=text[:index]
        value=float(text[index+1:])

        if flag=="Na":
            self.dataBase.addNa(self.dataBase.getCurrentTime(), value)
        elif flag=="K":
            self.dataBase.addK(self.dataBase.getCurrentTime(), value)
        elif flag=="Glucose":
            self.dataBase.addGlucose(self.dataBase.getCurrentTime(), value)
        elif flag=="CRP":
            self.dataBase.addCRP(self.dataBase.getCurrentTime(), value)
        elif flag=="ILBeta":
            self.dataBase.addILBeta(self.dataBase.getCurrentTime(), value)
        else:
            self.dataBase.addTemperature(self.dataBase.getCurrentTime(), value)

    def getLatestData(self):
        '''
            Return the latest data as a dictionary
        '''
        result=self.dataBase.getLatest()
        result["Time"]=self.dataBase.getCurrentTime()[-8:-3]
        return result

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

    def quit(self):
        self.dataBase.save()
        sys.exit()
    
    