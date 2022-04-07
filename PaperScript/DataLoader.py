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


    

        
