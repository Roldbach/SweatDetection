import copy

from datetime import datetime, timedelta

class DataBase():
    def __init__(self, directory="./Data"):
        '''
            Construct the database and load the stored data provided by
        the directory

            The code for CRP and ILBeta part is commented but could be used
        once the IBD sensor is finished

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
        self.temperature=self.loadData("Temperature")
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

    def getTemperature(self):
        return self.temperature

    def getMaximumStorage(self):
        return self.maximumStorage
    
    def getLatest(self):
        self.truncate()
        result={}
        result["Na"]=self.getLatestData(self.Na)
        result["K"]=self.getLatestData(self.K)
        result["Glucose"]=self.getLatestData(self.Glucose)
        result["CRP"]=self.getLatestData(self.CRP)
        result["ILBeta"]=self.getLatestData(self.ILBeta)
        result["Temperature"]=self.getLatestData(self.temperature)
        return result

    def getLatestData(self, dataset):
        '''
            Return the latest data stored in the dataset

            Return None if no data stored previously
        '''
        try:
            timeLine=list(dataset.keys())
            return dataset[timeLine[-1]]
        except:
            return "None"

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

    def addTemperature(self, time ,value):
        self.temperature[time]=value

    def setMaximumStorage(self, value):
        self.maximumStorage=value
    
    def save(self):
        self.saveData(self.Na, "Na")
        self.saveData(self.K, "K")
        self.saveData(self.Glucose, "Glucose")
        self.saveData(self.CRP, "CRP")
        self.saveData(self.ILBeta, "ILBeta")
        self.saveData(self.temperature, "Temperature")
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
        self.loadData("Temperature")

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
                result[line[:index]]=float(line[index+1:].strip("\n"))
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
        self.temperature=self.sortData(self.temperature)

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

    def truncate(self):
        self.sort()
        self.Na=self.truncateData(self.Na)
        self.K=self.truncateData(self.K)
        self.Glucose=self.truncateData(self.Glucose)
        self.CRP=self.truncateData(self.CRP)
        self.ILBeta=self.truncateData(self.ILBeta)
        self.temperature=self.truncateData(self.temperature)

    def truncateData(self, dataset, difference=None):
        '''
            Truncate the dataset using the given time difference
        '''
        try:
            timeLine=list(dataset.keys())
            latestTime=timeLine[-1]

            result=copy.deepcopy(dataset)
            for time in timeLine:
                if self.checkTimeDifference(time, latestTime, difference):
                    result.pop(time)
                else:
                    return result
        except:
            return

    def getCurrentTime(self):
        '''
            Get the formatted current time

            By default, the time should be in the format: yyyy/mm/dd hh:mm:ss
        
        Return:
            result: String, the formatted current time
        '''
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
    def checkTimeDifference(self, oldTime, newTime, difference=None):
        '''
            Check whether the time difference between 2 given time
        exceeds the given time difference

            By default, the time should be in the format: yyyy/mm/dd hh:mm:ss
        and the time difference should be in unit: day

        Return:
            result: Boolean, true if it exceeds the time difference, false otherwise
        '''
        oldTime=datetime.strptime(oldTime, "%Y/%m/%d %H:%M:%S")
        newTime=datetime.strptime(newTime, "%Y/%m/%d %H:%M:%S")
        if difference:
            maxTimeDifference=timedelta(hours=24*difference)
        else:
            maxTimeDifference=timedelta(hours=24*self.maximumStorage)
        return (newTime-oldTime>maxTimeDifference)