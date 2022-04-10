import pyCompare
import matplotlib.pyplot as plt
import numpy as np

from scipy import stats
from sklearn.linear_model import LinearRegression

class DataLoader:
    '''
        The class to load calibration data and perform
    related calculations
    '''
    def __init__(self, name=["glucose 5", "glucose 4"], path="./ExperimentalData/glucose (5,4) calibration.txt"):
        self.channel=name
        self.timeLine=[]
        self.dataset={}
        data=[{} for i in range(len(name))]

        with open(path, "r") as file:
            lines=file.readlines()
        
        for line in lines:
            result=line.strip("\n").split("\t")
            for i in range(len(data)):
                data[i][float(result[0])]=float(result[i+1])
                self.timeLine.append(float(result[0]))

        for i in range(len(name)):
            self.dataset[name[i]]=data[i]
    
    def calibrate(self, path="./ExperimentalData/24 point calibration instruction.txt"):
        '''
            Calibrate the sensor according to the instruction
        '''
        result={}
        for channel in self.channel:
            result[channel]={}
        
        instruction=self.loadInstruction(path)
        for key, value in instruction.items():
            truncateDataset=self.truncate(value[0], value[1])
            for channel in self.channel:
                truncateData=list(truncateDataset[channel].values())
                result[channel][key]=self.getTrimmedMean(truncateData, value[2])
        
        return result
            
    def getTrimmedMean(self, data, gain, level=0.2):
        return stats.trim_mean(data, level)*gain

    def truncate(self, start, end):
        '''
            Return data only within the range for all channels

            Assume the input start is earlier than the input end
        '''
        result={}
        for channel in self.channel:
            result[channel]={}
        
        for time in self.timeLine:
            if time<start:
                pass
            elif start<=time<=end:
                for key in result.keys():
                    result[key][time]=self.dataset[key][time]
            else:
                return result

    def loadInstruction(self, path="./ExperimentalData/24 point calibration instruction.txt"):
        '''
            Use the listed timeline to get calibration results
        '''
        result={}
        
        with open(path, "r") as file:
            lines=file.readlines()
        
        for line in lines:
            content=line.strip("\n").split(",")
            result[float(content[0])]=(self.convertTimeToSecond(content[1]), self.convertTimeToSecond(content[2]), float(content[3]))
        
        return result
    
    def convertTimeToSecond(self, time):
        timeSplit=time.split(":")
        if len(timeSplit)==2:
            return float(timeSplit[0])*60+float(timeSplit[1])
        elif len(timeSplit)==3:
            return float(timeSplit[0])*3600+float(timeSplit[1])*60+float(timeSplit[2])
        else:
            return float(timeSplit[0])

    def PearsonCorrelationTest(self, path="./ExperimentalData/24 point calibration instruction.txt"):
        result={}
        calibration=self.calibrate(path="./ExperimentalData/24 point calibration instruction.txt")
        for channel in self.channel:
            result[channel], _=stats.pearsonr(list(calibration[channel].keys()), list(calibration[channel].values()))
        print(result)

    def StudentTTest(self, extra="./ExperimentalData/12 point spike and recovery.txt"):
        calibration=self.calibrate("./ExperimentalData/12 point calibration instruction.txt")
        reference=self.calibrate("./ExperimentalData/12 point spike and recovery.txt")

        for channel in self.channel:
            model=LinearRegression()

            calibration_y=np.array(list(calibration[channel].keys())).reshape(-1,1)
            calibration_x=np.array(list(calibration[channel].values())).reshape(-1,1)
            reference_y=np.array(list(reference[channel].keys())).reshape(-1,1)
            reference_x=np.array(list(reference[channel].values())).reshape(-1,1)

            regression=model.fit(calibration_x, calibration_y)
            prediction=regression.predict(reference_x)

            print(f"This is channel {channel}")
            print(stats.ttest_ind(prediction, reference_y))

    def plotResponse(self, startTime="51:30", endTime="1:06:00"):
        data=self.truncate(self.convertTimeToSecond(startTime), self.convertTimeToSecond(endTime))

        for channel in self.channel:
            time=list(data[channel].keys())
            response=list(data[channel].values())

            plt.plot(time, response, color="r", linewidth=0.1)
            plt.xlabel("Time (s)")
            plt.ylabel("Current (nA)")
            plt.show()
            print(f"This is channel {channel}")
    
    def plotCalibration(self):
        calibration=self.calibrate("./ExperimentalData/24 point calibration instruction.txt")
        for channel in self.channel:
            model=LinearRegression()

            calibration_x_value=list(calibration[channel].keys())[:10]
            calibration_y_value=list(calibration[channel].values())[:10]
            
            calibration_x=np.array(calibration_x_value).reshape(-1,1)
            calibration_y=np.array(calibration_y_value).reshape(-1,1)

            regression=model.fit(calibration_x, calibration_y)

            theta=np.polyfit(calibration_x_value, calibration_y_value, deg=1)
            y_line=theta[1]+theta[0]*np.array(calibration_x_value)

            print(f"This is channel {channel}")
            print(regression.coef_)
            plt.scatter(calibration_x_value, calibration_y_value, marker="x", color="r", linewidths=1)
            plt.plot(calibration_x_value, y_line, linewidth=1, color="r", linestyle="--", alpha=0.5)
            plt.xlabel("Glucose Concentration (mM)")
            plt.ylabel("Current (nA)")
            plt.show()
    
    def plotBlandAltman(self):
        calibration=self.calibrate("./ExperimentalData/24 point calibration instruction.txt")

        for channel in self.channel:
            calibration_y_value=list(calibration[channel].keys())[:7]
            calibration_x_value=list(calibration[channel].values())[:7]

            reference_y_value=list(calibration[channel].keys())[8:13]
            reference_x_value=list(calibration[channel].values())[8:13]

            theta=np.polyfit(calibration_x_value, calibration_y_value, deg=1)
            prediction=theta[1]+theta[0]*np.array(reference_x_value)
            prediction=prediction.tolist()

            pyCompare.blandAltman(prediction, reference_y_value, dpi=300, savePath=f"./ExperimentalData/BA {channel}.png")
        
