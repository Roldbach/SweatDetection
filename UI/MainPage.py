from Configuration import pageConfiguration
from PyQt5.QtWidgets import*

from UI.WindowHelper import constructButton, constructLabel

class MainPage(QWidget):
    '''
        The main page to display different results and allow the user to
    jump to other pages

        If bluetooth is implemented, it will display the connection status
    and the temperature reading

        The following results will be displayed to the user:
        (1) latest Na concentration reading
        (2) latest K concentration reading
        (3) latest Glucose concentration reading
        (4) latest CRP concentration reading
        (5) latest ILBeta concentration reading
        (6) latest temperature reading
        (7) current time
    
        The following pages could be reached:
        (1) Plot page
        (2) Setting page
    '''

    def __init__(self):
        super().__init__()
        self.resize(pageConfiguration["width"], pageConfiguration["height"])
        self.NaConcentrationLabel=constructLabel(size=32, border=True)
        self.NaLabel=constructLabel("Sodium (Na)", border=True)
        self.KConcentrationLabel=constructLabel(size=32, border=True)
        self.KLabel=constructLabel("Potassium (K)", border=True)
        self.GlucoseConcentrationLabel=constructLabel(size=32, border=True)
        self.GlucoseLabel=constructLabel("Glucose", border=True)
        self.CRPConcentrationLabel=constructLabel(size=32, border=True)
        self.CRPLabel=constructLabel("CRP", border=True)
        self.ILBetaConcentrationLabel=constructLabel(size=32, border=True)
        self.ILBetaLabel=constructLabel("IL-Beta", border=True)
        self.temperatureValueLabel=constructLabel(size=32, border=True)
        self.temperatureLabel=constructLabel("Temperature", border=True)
        self.timeValueLabel=constructLabel(size=32, border=True)
        self.timeLabel=constructLabel("Time", border=True)

        self.plotButton=constructButton("Plot")
        self.settingButton=constructButton("Setting")
        self.quitButton=constructButton("Quit")

        NaLayout=self.constructLayout(self.NaConcentrationLabel, self.NaLabel)
        KLayout=self.constructLayout(self.KConcentrationLabel, self.KLabel)
        GlucoseLayout=self.constructLayout(self.GlucoseConcentrationLabel, self.GlucoseLabel)
        CRPLayout=self.constructLayout(self.CRPConcentrationLabel, self.CRPLabel)
        ILBetaLayout=self.constructLayout(self.ILBetaConcentrationLabel, self.ILBetaLabel)
        temperatrueLayout=self.constructLayout(self.temperatureValueLabel, self.temperatureLabel)
        timeLayout=self.constructLayout(self.timeValueLabel, self.timeLabel)

        upperLayout=QGridLayout()
        upperLayout.setHorizontalSpacing(25)
        upperLayout.addLayout(NaLayout, 0, 0)
        upperLayout.addLayout(CRPLayout, 0, 1)
        upperLayout.addLayout(KLayout, 1, 0)
        upperLayout.addLayout(ILBetaLayout, 1,1)

        lowerLayout=QGridLayout()
        lowerLayout.setHorizontalSpacing(25)
        lowerLayout.addLayout(temperatrueLayout, 0, 0)
        lowerLayout.addLayout(GlucoseLayout, 0, 1)
        lowerLayout.addLayout(timeLayout, 0, 2)
        
        lowerLayout.addWidget(self.plotButton, 2, 0)
        lowerLayout.addWidget(self.settingButton, 2, 1)
        lowerLayout.addWidget(self.quitButton, 2, 2)

        layout=QVBoxLayout()
        layout.addLayout(upperLayout)
        layout.addLayout(lowerLayout)
        self.setLayout(layout)

    def constructLayout(self, concentrationLabel, nameLabel):
        '''
            Return a layout that vertically stacks the concentration label
        and the name label with border
        '''
        layout=QGridLayout()
        layout.setHorizontalSpacing(100)
        layout.addWidget(concentrationLabel)
        layout.setSpacing(0)
        layout.addWidget(nameLabel)
        layout.addWidget(QLabel(""))
        return layout
    
    def update(self, result):
        '''
            Update the main page using the given dataset for every label
        '''
        self.updateLabel(self.NaConcentrationLabel, result["Na"], "mM")
        self.updateLabel(self.KConcentrationLabel, result["K"], "mM")
        self.updateLabel(self.GlucoseConcentrationLabel, result["Glucose"], "??M")
        self.updateLabel(self.CRPConcentrationLabel, result["CRP"], "pg/mL")
        self.updateLabel(self.ILBetaConcentrationLabel, result["ILBeta"], "ng/mL")
        self.updateLabel(self.temperatureValueLabel, result["Temperature"], "??C")
        self.updateLabel(self.timeValueLabel, result["Time"])

    def updateLabel(self, label, value, unit=""):
        '''
            Update the given label with the given value and
        corresponding unit

        input:
            label: QLabel, the label displaying the value to the user
            value: float, the latest value stored in the dataset
            unit: String, the unit for the value
        '''
        if value!="None":
            label.setText(str(value)+unit)
        else:
            label.setText("NaN")