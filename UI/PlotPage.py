from types import TracebackType
import numpy as np
import matplotlib.pyplot as plt

from Configuration import pageConfiguration, radioButtonConfiguration
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from UI.WindowHelper import*

class PlotPage(QWidget):
    '''
        The plot page to display various plots for each type of data
    and allow to user to choose the scale of plotting
        
        The following plots could be shown to the user:
        (1) Na concentration against time
        (2) K concentration against time
        (3) Glucose concentration against time
        (4) CRP concentration against time
        (5) ILBeta concentration against time
        (6) Temperature against time

        The following scales are provided:
        (1) Within one day
        (2) Within one week
        (3) All (Within one month by default)
    '''
    def __init__(self):
        super().__init__()
        self.resize(pageConfiguration["width"], pageConfiguration["height"])

        self.NaPlotLabel=constructLabel("Na")
        self.KPlotLabel=constructLabel("K")
        self.GlucosePlotLabel=constructLabel("Glu")
        self.CRPPlotLabel=constructLabel("CRP")
        self.ILBetaPlotLabel=constructLabel("Beta")
        self.temperaturePlotLabel=constructLabel("Temperature")
        
        self.backButton=constructButton("Back")

        self.optionButton_1=constructRadioButton(self.formatChoice(radioButtonConfiguration["option 1"]))
        self.optionButton_2=constructRadioButton(self.formatChoice(radioButtonConfiguration["option 2"]))
        self.optionButton_3=constructRadioButton(self.formatChoice(radioButtonConfiguration["option 3"]))
        self.optionButton_1.clicked.connect(lambda: self.chooseOption(self.optionButton_1))
        self.optionButton_2.clicked.connect(lambda: self.chooseOption(self.optionButton_2))
        self.optionButton_3.clicked.connect(lambda: self.chooseOption(self.optionButton_3))
        self.optionButton_1.setChecked(True)
        self.currentChoice=self.optionButton_1

        self.plotComboBox=QComboBox()
        self.plotComboBox.addItems(["Na","K", "Glucose", "CRP", "ILBeta", "Temperature"])
        self.plotComboBox.setFont(QFont(widgetConfiguration["font"], 16))
        self.plotComboBox.activated.connect(self.switchPage)

        self.plotStack=QStackedLayout()
        self.plotStack.addWidget(self.NaPlotLabel)
        self.plotStack.addWidget(self.KPlotLabel)
        self.plotStack.addWidget(self.GlucosePlotLabel)
        self.plotStack.addWidget(self.CRPPlotLabel)
        self.plotStack.addWidget(self.ILBetaPlotLabel)
        self.plotStack.addWidget(self.temperaturePlotLabel)

        middleLayout=QVBoxLayout()
        middleLayout.addWidget(self.plotComboBox)
        middleLayout.addLayout(self.plotStack)

        radioButtonLayout=QHBoxLayout()
        radioButtonLayout.addWidget(QLabel(""))
        radioButtonLayout.addWidget(self.optionButton_1)
        radioButtonLayout.addWidget(QLabel(""))
        radioButtonLayout.addWidget(self.optionButton_2)
        radioButtonLayout.addWidget(QLabel(""))
        radioButtonLayout.addWidget(self.optionButton_3)
        radioButtonLayout.addWidget(QLabel(""))

        lowerLayout=QHBoxLayout()
        lowerLayout.addWidget(QLabel(""))
        lowerLayout.addWidget(self.backButton)
        lowerLayout.addWidget(QLabel(""))

        layout=QGridLayout()
        layout.addWidget(QLabel(""), 0, 0)
        layout.addWidget(QLabel(""), 1, 0)
        layout.addLayout(middleLayout, 2, 0, 7, 0)
        layout.addWidget(QLabel(""), 8, 0)
        layout.addLayout(radioButtonLayout, 9, 0)
        layout.addWidget(QLabel(""), 10, 0)
        layout.addLayout(lowerLayout, 11, 0)
        self.setLayout(layout)

    def formatChoice(self, value, unit="day"):
        if value>1:
            return f"{value} "+unit+"s"
        else:
            return f"{value} "+unit
    
    def deformatChoice(self, radioButton):
        text=radioButton.text()
        index=text.index(" ")
        return int(text[:index])
        
    def switchPage(self):
        self.plotStack.setCurrentIndex(self.plotComboBox.currentIndex())
    
    def chooseOption(self, radioButton):
        '''
            Only allow the user to choose one option at a time
        '''
        self.currentChoice.setChecked(False)
        radioButton.setChecked(True)
        self.currentChoice=radioButton

    def plot(self, dataset):
        '''
            Plot graphs for each type of data and load them
        to the corresponding label
        '''
        self.plotGraph(dataset["Na"], "mM", self.currentChoice.text(), "Na")
        self.plotGraph(dataset["K"], "mM", self.currentChoice.text(), "K")
        self.plotGraph(dataset["Glucose"], "µM", self.currentChoice.text(), "Glucose")
        self.plotGraph(dataset["CRP"], "mM", self.currentChoice.text(), "CRP")
        self.plotGraph(dataset["ILBeta"], "mM", self.currentChoice.text(), "ILBeta")
        self.plotGraph(dataset["Temperature"], "°C", self.currentChoice.text(), "Temperature")
        self.setImage(self.NaPlotLabel, "Na")
        self.setImage(self.KPlotLabel, "K")
        self.setImage(self.GlucosePlotLabel, "Glucose")
        self.setImage(self.CRPPlotLabel, "CRP")
        self.setImage(self.ILBetaPlotLabel, "ILBeta")
        self.setImage(self.temperaturePlotLabel, "Temperature")

    def plotGraph(self, data, unit, scale, name, directory="./Plot/"):
        '''
            Plot the graph with the given data and store it using
        the given name

            There are axis labels at the 0, 25, 75, 100 percentile of the data
        
        input:
            data: dictionary, key=timestamp, value=concentration/temperature
            unit: String, the unit of the value
            scale: String, the range of displayed data
            name: String, the name of the plot
            directory: String, the position to save the plot
        '''
        timeLine=list(data.keys())
        value=list(data.values())

        timeLine=[time[5:-3] for time in timeLine]
        timeIndex=[i for i in range(len(timeLine))]
        percentile=np.percentile(timeIndex, [0, 25, 75, 100]).astype("uint8")
        timeTick=[timeLine[i] for i in percentile]

        figure, axis=plt.subplots(figsize=(3, 2), dpi=300)
        axis.plot(value, color="black", linewidth=0.5)
        axis.set_title(name+"("+unit+")"+" in "+scale)
        axis.set_xticks(percentile)
        axis.set_xticklabels(timeTick, fontsize=4)

        figure.savefig(directory+name+".png")

    def setImage(self, label, name, directory="./Plot/"):
        '''
            Set the target image to the label using the given name and scale the content
        
        input:
            label: QLabel, the label to display the image
            name: String, the name of the image to display 
        '''
        path=directory+name+".png"
        image=QPixmap(path)
        label.setPixmap(image)
        label.setScaledContents(True)