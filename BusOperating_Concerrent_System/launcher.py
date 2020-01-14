import rticonnextdds_connector as rti
import random
import threading
import configparser
import datetime
import time
import numpy as np # random number with probabiliry generator
from functools import partial
from itertools import chain


#connector = rti.Connector("MyParticipantLibrary::Zero","./accident.xml"); 

class TreadingBuses(object):
    
    def __init__(self):
        self.vehiclelist=[]
    
    def appendVehicle(self, vehicleInput):
        self.vehiclelist.append(vehicleInput)

    def doThreading(self):
        threads = []
        for bus in self.vehiclelist:
            #print("aaa")
            threadTem = threading.Thread(target=bus.operateBus)  # testing
            threads.append(threadTem)
            print("Thread {} initialized".format(bus.vehicleName))

        time.sleep(2) #sleep
        print("All thread has started \n")
        for t in threads:
            t.start()


class Bus(object):
    
    def __init__(self, rn, vn, ns, tbs):
        self.routeName=rn
        self.vehicleName=vn
        self.numStops=ns
        self.timeBetweenStops=tbs
        self.stopNum=1
        self.savedTimeBetweenStops=tbs
        
        self.accStat=0
        
        self.connector = rti.Connector("MyParticipantLibrary::Zero", "./position.xml")
        self.writePOS = self.connector.getOutput("Publisher::P2464_EECS_Bumjin_Park_POS")
        self.writeACC = self.connector.getOutput("Publisher::P2464_EECS_Bumjin_Park_ACC")

        self.total_stops = self.numStops*3 #18
        self.heavyNums= int(self.total_stops/10) #1
        self.lightNums= int(self.total_stops/4)  #4
        self.normalNums= self.total_stops-self.heavyNums-self.lightNums # 13

    def setTBS(self,saved,times):
        self.timeBetweenStops=saved*times

    def traffic(self):
        #light = 0.25 * timeBetweenStops    # for simplicity, use total_stops instead of timeBetweenStops.
        #heavy = 1.5 * timeBetweenStops
        #normal = 1 * timeBetweenStops
        # total number of stops = numStops*3
        ##np.random.choice(np.arange(0, 3), p=[0.25, 0.1, 0.65])
        
        while (1):
            #randomNum=random.randint(1,3)  #1~3
            randomNum=np.random.choice(np.arange(0, 3), p=[0.1, 0.25, 0.65])       ##note. this is just a random number generator based on probability ### 
            if(randomNum==0 and self.heavyNums!=0):                               ## condition on rightside is the # of heavys based on total stop_num
                self.heavyNums -= 1
                #tem = self.savedTimeBetweenStops*1.5
                #self.timeBetweenStops=self.savedTimeBetweenStops*50.0/100.0 # increases speed by 50%
                self.setTBS(self.savedTimeBetweenStops,1.5)
                return "Heavy "
            if(randomNum==1 and self.lightNums!=0):
                self.lightNums -= 1
                #tem = self.savedTimeBetweenStops*0.75
                #self.timeBetweenStops = self.savedTimeBetweenStops*75.0 / 100.0 # decreases speed by 25%
                self.setTBS(self.savedTimeBetweenStops,0.75)

                return "Light "
            if(randomNum==2 and self.normalNums!=0):
                self.normalNums -=1
                #self.timeBetweenStops=self.savedTimeBetweenStops
                self.setTBS(self.savedTimeBetweenStops,1.0)

                return "Normal"
            



    def writePosition(self, acc): #publish position
        
        #self.timeBetweenStops+=10
        self.writePOS.instance.setString("route",self.routeName)
        self.writePOS.instance.setString("vehicle",self.vehicleName)
        self.writePOS.instance.setNumber("numStops",self.numStops)
        
        self.writePOS.instance.setNumber("fillInRatio",random.randint(1,100))
        self.writePOS.instance.setNumber("stopNumber",self.stopNum)
        trafficCon=self.traffic()


        if acc==1:
            self.timeBetweenStops+=10.0
        #if self.accStat==0:
        #    self.timeBetweenStops=self.savedTimeBetweenStops
        self.writePOS.instance.setNumber("timeBetweenStops",self.timeBetweenStops)
        self.writePOS.instance.setString("trafficConditions",trafficCon)


        self.timeStamp = str(datetime.datetime.now().time().strftime("%H:%M:%S"))
        self.writePOS.instance.setString("timestamp",self.timeStamp)
        self.writePOS.write()
        #self.timeStamp = datetime.datetime.now()
        
        return "{} published a position message at stop #{} on route {} at {} {}".format(self.vehicleName, self.stopNum, self.routeName, self.timeStamp,trafficCon)
    
    def writeAccident(self): # publish accident
        

        self.writeACC.instance.setString("route",self.routeName)
        self.writeACC.instance.setString("vehicle",self.vehicleName)
        self.writeACC.instance.setNumber("stopNumber",self.stopNum)
        
        self.timeStamp = str(datetime.datetime.now().time().strftime("%H:%M:%S"))
        self.writeACC.instance.setString("timestamp",self.timeStamp) 
        self.writeACC.write()
        

        return "{} published a accidnet message at stop #{} on route {} at {} ".format(self.vehicleName, self.stopNum, self.routeName, self.timeStamp)
    

    def operateBus(self):
        print("operateBus called")
        for i in range(3):# 3rounds
            for j in range(self.numStops):

                randomNum=np.random.choice(np.arange(0, 2), p=[0.1, 0.9]) # accident probabilty
                #accis=0
                if randomNum==0: #accident
                    #self.accStat=1
                    #accis=1
                    accidentTem = self.writeAccident()
                    
                    positionTem = self.writePosition(1)
                    #accidentTem = self.writeAccident()
                    print(accidentTem)
                    print(positionTem)
                    time.sleep(0.5)
                    #time.sleep(10) # delays 10 seconds.
                    #self.savedTimeBetweenStops+=10
                #else:
                #    self.accStat=0
                else:
                    positionTem = self.writePosition(0)
                    #accidentTem = self.writeAccident()
                    print(positionTem)
                    #print(accidentTem)
                #if self.accStat==1:
                #    self.accStat=0

                if self.numStops == self.stopNum:
                    self.stopNum=0
                self.stopNum+=1

                time.sleep(self.timeBetweenStops)







if __name__== "__main__":

    f = open("pub.properties","r")

    v1=[]
    v2=[]
    info1=[]
    info2=[]
    str1 =""

    f1 = f.readlines()
    for x in f1:
        if x!='\n':
            str1 +=x

    lines=str1.split("\n")
    lines.pop() #removing last \n
    for i in lines:
        tem = (i.split('='))
        if tem[0] == "numRoutes":
            numRoutes=tem[1]
        if tem[0] == "numVehicles":
            numVehicles = tem [1]
        if tem[0][5]== '1':
            info1.append(tem[1])
        if tem[0][5]== '2':
            info2.append(tem[1])
TreadingBuses=TreadingBuses()


for i in range(0,6):
    #Bus(info1[0],info1[3+i],info1[1],info1[2])
    
    if(i <3):
        TreadingBuses.appendVehicle(Bus(info1[0],info1[3+i],int(info1[1]),float(info1[2])))
    else:
        TreadingBuses.appendVehicle(Bus(info2[0],info2[i],int(info2[1]),float(info2[2])))

    #print("-----------------------")
TreadingBuses.doThreading()
    