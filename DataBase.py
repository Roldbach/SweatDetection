from datetime import datetime, timedelta

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
        self.saveConfiguration()

    def saveConfiguration(self, name="Configuration"):
        with open(self.directory+"/"+name+".txt", "w") as file:
            storageLine="maximum storage:"+str(self.maximumStorage)+"\n"
            file.write(storageLine)

    def saveData(self, dataset, name):
        '''
            Save time-value pair separated by ","
        '''
        with open(self.directory+"/"+name+".txt", "w") as file:
            for pair in dataset.items():
                line=pair[0]+","+str(pair[1])+"\n"
                file.write(line)

    def load(self):
        self.loadConfiguration("Configuration")
        self.loadData("Na")
        self.loadData("K")
        self.loadData("Glucose")
        self.loadData("CRP")
        self.loadData("ILBeta")

    def loadData(self, name):
        '''
            Load concentration data and store them as time-value pair in a dictionary
        '''
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

    def loadConfiguration(self, name):
        try:
            with open(self.directory+"/"+name+".txt","r") as file:
                lines=file.readlines()
            for line in lines:
                index=line.index(":")
                if "maximum storage" in line:
                    self.maximumStorage=int(line[index+1:].strip("\n"))
        except FileNotFoundError:
            print("Fail to load "+name+".txt file. Please try again.")

    def sort(self):
        self.Na=self.sortData(self.Na)
        self.K=self.sortData(self.K)
        self.Glucose=self.sortData(self.Glucose)
        self.CRP=self.sortData(self.CRP)
        self.ILBeta=self.sortData(self.ILBeta)

    def sortData(self, dataset):
        '''
            Sort the given dictionary ordered from earliest time to latest time
        '''
        result={}
        timeLine=list(dataset.keys())
        timeLine.sort()
        for time in timeLine:
            result[time]=dataset[time]
        return result

    def update(self):
        self.sort()
        self.updateData(self.Na)
        self.updateData(self.K)
        self.updateData(self.Glucose)
        self.updateData(self.CRP)
        self.updateData(self.ILBeta)

    def updateData(self, dataset):
        '''
            Update the dataset so that it only stores data within the maximum storage
        '''
        timeLine=list(dataset.keys())
        latestTime=timeLine[-1]
        for time in timeLine:
            if self.checkTimeDifference(time, latestTime):
                dataset.pop(time)
            else:
                return

    def getCurrentTime(self):
        '''
            Get the formatted current time

            By default, the time should be in the format: yyyy/mm/dd hh:mm:ss
        
        Return:
            result: String, the formatted current time
        '''
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
    def checkTimeDifference(self, oldTime, newTime):
        '''
            Check whether the time difference between 2 given time
        exceeds the maximum storage

            By default, the time should be in the format: yyyy/mm/dd hh:mm:ss

        Return:
            result: Boolean, true if it exceeds the maximum storage, false otherwise
        '''
        oldTime=datetime.strptime(oldTime, "%Y/%m/%d %H:%M:%S")
        newTime=datetime.strptime(newTime, "%Y/%m/%d %H:%M:%S")
        maxTimeDifference=timedelta(hours=24*self.maximumStorage)
        return (newTime-oldTime>maxTimeDifference)