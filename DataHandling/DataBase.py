class DataBase():
    def __init__(self, directory="./Data"):
        '''
            Construct the database and load the stored data provided by
        the directory

            If the file can't be successfully loaded, empty database would
        be constructed

            By default, the unit of maximum storage is in days

        input:
            directory: String, the directory that stores data
        '''
        self.directory=directory
        self.Na=self.loadData("Na")
        self.K=self.loadData("K")
        self.Glucose=self.loadData("Glucose")
        self.CRP=self.loadData("CRP")
        self.ILBeta=self.loadData("ILBeta")
        self.maximumStorage=31

    def getNa(self):
        return self.Na
    
    def getK(self):
        return self.K
    
    def getGlucose(self):
        return self.Glucose
    
    def getCRP(self):
        return self.CRP
    
    def getILBeta(self):
        return self.ILBeta

    def addNa(self, time, value):
        self.Na[time]=value

    def addK(self, time ,value):
        self.K[time]=value
    
    def addGlucose(self, time, value):
        self.Glucose[time]=value
    
    def addCRP(self, time , value):
        self.CRP[time]=value
    
    def addILBeta(self, time, value):
        self.ILBeta[time]=value

    def setMaximumStorage(self, value):
        self.maximumStorage=value
    
    def save(self):
        self.saveData(self.Na, "Na")
        self.saveData(self.K, "K")
        self.saveData(self.Glucose, "Glucose")
        self.saveData(self.CRP, "CRP")
        self.saveData(self.ILBeta, "ILBeta")

    def saveConfiguration(self, name="Configuration"):
        with open(self.directory+"/"+name+".txt", "w") as file:
            file.write(str(self.maximumStorage))

    def saveData(self, dataset, name):
        with open(self.directory+"/"+name+".txt", "w") as file:
            for pair in dataset.items():
                line=pair[0]+","+str(pair[1])+"\n"
                file.write(line)

    def loadData(self, name):
        result=dict()
        try:
            with open(self.directory+"/"+name+".txt", "r") as file:
                lines=file.readlines()
            for line in lines:
                index=line.index(",")
                result[line[:index]]=line[index+1:].strip("\n")
        except FileNotFoundError:
            print("Fail to load "+name+".txt file. Please try again.")
        finally:
            return result
