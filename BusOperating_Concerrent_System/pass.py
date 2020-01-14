import rticonnextdds_connector as rti
import time
import sys

connector = rti.Connector("MyParticipantLibrary::Zero", "position.xml")
positionSubscription = connector.getInput("Subscriber::P2464_EECS_Bumjin_Park_POS")
accidentSubscription = connector.getInput("Subscriber::P2464_EECS_Bumjin_Park_ACC")

#print("MessageType {: >12}{: >6}{: >10}{: >3}{: >15}{: >20}{: >10}{: >15}".format("Route", "Vehicle", "Traffic", "Stop#", "#Stops", "TimeBetweenStops", "Fill%", "Timestamp"))
print("Waiting for the bus...")



expressName=sys.argv[1]
startStop=int(sys.argv[2])
endStop=int(sys.argv[3])

print(expressName)
print(startStop)
print(endStop)
foundName="null"
switch = 0
stopper=0
howManyLeft=0
getOnSwitch=0
timeTem="null"
trafficTem="null"
storedname="null"

leftstops=0

if __name__=='__main__':


    

    while(True):
        accidentSubscription.take()
        accNum = accidentSubscription.samples.getLength()
        positionSubscription.take()
        posNum = positionSubscription.samples.getLength()
        #print("accNum == : ",accNum)
        
       
        if accNum>0:
            
            routeA = accidentSubscription.samples.getString(0, "route")
            vehicleA = accidentSubscription.samples.getString(0, "vehicle")
            stopNumA = accidentSubscription.samples.getNumber(0, "stopNumber")
            timestampA = accidentSubscription.samples.getString(0, "timestamp")
            
            for i in range(0,posNum):
                vehicleP = positionSubscription.samples.getString(i, "vehicle")
                if vehicleA==vehicleP and expressName==routeA:
                    trafficP = positionSubscription.samples.getString(i,"trafficConditions") 
                    stopNumP = positionSubscription.samples.getString(i, "stopNumber")
                    numStopsA=positionSubscription.samples.getNumber(i,"numStops")

            #print("Position {: >12}{: >15}{: >10}{: >3}{: >8}{: >12}{: >21}{: >14}".format(routeP, vehicleP, trafficP, int(stopNumP), int(numStopsP), timeBetweenStopsP, int(fillInRatioP), timestampP))
            #print("Position     "+routeP+"       "+vehicleP+"    "+trafficP+"       "+stopNumP+"   "+str(numStopsP)+"     "+str(timeBetweenStopsP)+"        "+str(fillInRatioP)+"     "+timestampP)
            #print(str(num)+"\r")
            #print("Accident {: >12}{: >15}{: >13}{: >55}".format(routeA, vehicleA, int(stopNumA), timestampA))    
            #print("["+str(0)+"] Accident     "+routeA+"       "+vehicleA+"                   "+str(stopNumA)+"                        "+timestampA)    


            if int(stopNumA)==startStop and getOnSwitch==0 and routeA==expressName:
                storedname=vehicleA
                getOnSwitch=1
                if endStop>startStop:
                    howManyLeft= endStop-startStop
                elif startStop>endStop:
                        howManyLeft= numStopsA-startStop
                        howManyLeft+=endStop
                print("Geting on "+storedname+" at "+ timestampA+", "+trafficP+", accident, "+ str(int(howManyLeft))+" stops left ")

            elif storedname==vehicleA and getOnSwitch!=0:

                howManyLeft-=1
                print("Arriving at stop #"+str(stopNumA)+", at "+timestampA+", "+trafficP+", accident, "+str(int(howManyLeft))+" stops left")           
            
                if howManyLeft==0:
                    exit()



            """
            if int(stopNumA)==startStop and getOnSwitch==0:
                storedname=vehicleA
                print("Acc get on bus "+storedname)
                getOnSwitch=1    
            elif storedname==vehicleA and getOnSwitch!=0:
                print("Acc arrived "+storedname)
            """
            #got storedname ( vehicle number)
   

        else:
            for num in range(0,posNum):
                routeP = positionSubscription.samples.getString(num, "route")
                vehicleP = positionSubscription.samples.getString(num, "vehicle")
                trafficP = positionSubscription.samples.getString(num,"trafficConditions")  
                stopNumP = positionSubscription.samples.getString(num, "stopNumber")
                numStopsP=positionSubscription.samples.getNumber(num,"numStops")
                timeBetweenStopsP=positionSubscription.samples.getNumber(num,"timeBetweenStops")
                fillInRatioP=positionSubscription.samples.getNumber(num,"fillInRatio")
                timestampP = positionSubscription.samples.getString(num, "timestamp")
                #print("Position {: >12}{: >15}{: >10}{: >3}{: >8}{: >12}{: >21}{: >14}".format(routeP, vehicleP, trafficP, int(stopNumP), int(numStopsP), timeBetweenStopsP, int(fillInRatioP), timestampP))
                #print("Position     "+routeP+"       "+vehicleP+"    "+trafficP+"       "+stopNumP+"   "+str(numStopsP)+"     "+str(timeBetweenStopsP)+"        "+str(fillInRatioP)+"     "+timestampP)
                
                if int(stopNumP)==startStop and getOnSwitch==0 and routeP==expressName:
                    storedname=vehicleP
                    
                    getOnSwitch=1      
                    if endStop>startStop:
                        howManyLeft= endStop-startStop
                    elif startStop>=endStop:
                        howManyLeft= numStopsP-startStop
                        howManyLeft+=endStop
                    print("Getting on "+storedname+" at "+timestampP+", "+trafficP+", "+ str(int(howManyLeft)) + " stop left")    
                        
                elif storedname==vehicleP and getOnSwitch!=0:

                    howManyLeft-=1
                    print("Arriving at stop #"+str(stopNumP)+", at "+timestampP+", "+trafficP+" "+str(int(howManyLeft))+" stops left")           

                    if howManyLeft==0:
                        exit()
        time.sleep(1)


    print(foundName)