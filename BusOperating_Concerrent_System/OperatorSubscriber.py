import rticonnextdds_connector as rti
import time

connector = rti.Connector("MyParticipantLibrary::Zero", "position.xml")
positionSubscription = connector.getInput("Subscriber::P2464_EECS_Bumjin_Park_POS")
accidentSubscription = connector.getInput("Subscriber::P2464_EECS_Bumjin_Park_ACC")

#print("MessageType {: >12}{: >6}{: >10}{: >3}{: >15}{: >20}{: >10}{: >15}".format("Route", "Vehicle", "Traffic", "Stop#", "#Stops", "TimeBetweenStops", "Fill%", "Timestamp"))
print("MessageType  Route             Vehicle  Traffic Stop#   #stop   TimeBetweenStops        Fill%   Timestamp")

while(True):
        accidentSubscription.take()
        accNum = accidentSubscription.samples.getLength()
        positionSubscription.take()
        posNum = positionSubscription.samples.getLength()
        ##print()
        
        if accNum!=0:
         
            routeA = accidentSubscription.samples.getString(0, "route")
            vehicleA = accidentSubscription.samples.getString(0, "vehicle")
            stopNumA = accidentSubscription.samples.getNumber(0, "stopNumber")
            timestampA = accidentSubscription.samples.getString(0, "timestamp")
            print("Accident {: >12}{: >15}{: >13}{: >55}".format(routeA, vehicleA, int(stopNumA), timestampA))
            #print("Accident     "+routeA+"       "+vehicleA+"                   "+str(stopNumA)+"                        "+timestampA)
            
            
        if posNum!=0:
            for num in range(0,posNum):
                routeP = positionSubscription.samples.getString(num, "route")
                vehicleP = positionSubscription.samples.getString(num, "vehicle")
                trafficP = positionSubscription.samples.getString(num,"trafficConditions")  
                stopNumP = positionSubscription.samples.getString(num, "stopNumber")
                numStopsP=positionSubscription.samples.getNumber(num,"numStops")
                timeBetweenStopsP=positionSubscription.samples.getNumber(num,"timeBetweenStops")
                fillInRatioP=positionSubscription.samples.getNumber(num,"fillInRatio")
                timestampP = positionSubscription.samples.getString(num, "timestamp")
                #print("["+str(num)+"]\r")
                print("Position {: >12}{: >15}{: >10}{: >3}{: >8}{: >12}{: >21}{: >14}".format(routeP, vehicleP, trafficP, int(stopNumP), int(numStopsP), timeBetweenStopsP, int(fillInRatioP), timestampP))
                #print("Position     "+routeP+"       "+vehicleP+"    "+trafficP+"       "+stopNumP+"   "+str(numStopsP)+"     "+str(timeBetweenStopsP)+"        "+str(fillInRatioP)+"     "+timestampP)
            
       
        time.sleep(1)
