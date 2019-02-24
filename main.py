import cv2
import pyzbar.pyzbar as pyzbar
import re
import math
import os
import csv
import sys
from collections import defaultdict

# Measure Time
# import time

# start_time = time.time()

class QRCode:
    def __init__(self, decodedObject):
        xSum = 0
        ySum = 0
        for point in decodedObject.polygon:
            xSum += point.x
            ySum += point.y

        self.code = decodedObject.data.decode("utf-8")
        self.x = xSum/4
        self.y = ySum/4
        
    def __str__(self):
        return str({'code': self.code, 'x': self.x, 'y': self.y})
    
class Location(QRCode):
    def __init__(self, decodedObject):
        QRCode.__init__(self, decodedObject)
        
class Carton(QRCode):
    def __init__(self, decodedObject):
        QRCode.__init__(self, decodedObject)
        
locationREStr = '[A-Z]{2}\d{6}'
locationRE = re.compile(locationREStr)

# cartonREStr = '\d{6}'
# cartonRE = re.compile(locationREStr)


def isLocation(obj):
    match = locationRE.findall(obj.data.decode("utf-8"))
    if len(match) > 0:
        return True
    else:
        return False

def isCarton(obj):
    match = cartonRE.findall(obj.data.decode("utf-8"))
    if len(match) > 0:
        return True
    else:
        return False
    

directory = './images/'

locationIDs = set()
data = list()

for filename in os.listdir(directory):
    if filename.endswith(".JPG"):        
        frame = cv2.imread(os.path.join(directory, filename))
        
#         print("--- (A) %s seconds ---" % (time.time() - start_time))
#         start_time = time.time()

        locations = list()
        cartons = list()
        decodedObjects = pyzbar.decode(frame, symbols=[pyzbar.ZBarSymbol.QRCODE])
        
#         print("--- (B) %s seconds ---" % (time.time() - start_time))
#         start_time = time.time()

        for obj in decodedObjects:
            if isLocation(obj):
                locations.append(Location(obj))
            else:
                cartons.append(Carton(obj))
                
#         print("--- (C) %s seconds ---" % (time.time() - start_time))
#         start_time = time.time()

        for location in locations:
            locationIDs.add(location.code)
            
#         print("--- (D) %s seconds ---" % (time.time() - start_time))
#         start_time = time.time()

        if len(locations) > 0:
            inFrameData = list()
            for carton in cartons:
                shortestDistance = sys.maxsize
                closestLocation = None
                for location in locations:
                    distance = math.sqrt(math.pow(carton.x - location.x, 2) + math.pow(carton.y - location.y, 2))
                    if distance < shortestDistance:
                        shortestDistance = distance
                        closestLocation = location

                pair = {'filename': filename, 'carton': carton.code, 'loc': closestLocation.code, 'distance': shortestDistance}

                sameLocPairs = [x for x in inFrameData if x['loc'] == pair['loc']]
                if len(sameLocPairs) > 0:
                    if sameLocPairs[0]['distance'] > pair['distance']:
                        inFrameData.remove(sameLocPairs[0])
                        inFrameData.append(pair)
                else:
                    inFrameData.append(pair)
            data.extend(inFrameData)
        
#         print("--- (E) %s seconds ---" % (time.time() - start_time))


finalResult = list()

for locationID in locationIDs:
    dataSubset = [x for x in data if x['loc'] == locationID]
    shortestDistance = sys.maxsize
    closestCarton = None
    if len(dataSubset) > 0:
        for pair in dataSubset:
            if pair['distance'] < shortestDistance:
                closestCarton = pair['carton']
                shortestDistance = pair['distance']
        resultPair = {'loc': locationID, 'carton': closestCarton, 'distance': shortestDistance}
        sameCartonPairs = [x for x in finalResult if x['carton'] == resultPair['carton']]
        if len(sameCartonPairs) > 0:
            if sameCartonPairs[0]['distance'] > resultPair['distance']:
                finalResult.remove(sameCartonPairs[0])
                finalResult.append(resultPair)
        else:
            finalResult.append(resultPair)

finalResultDict = defaultdict(str)
for x in finalResult:
    finalResultDict[x['loc']] = x['carton']

    
with open('hack2019-5.csv', mode='w') as fOut:
    writer = csv.writer(fOut, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    for locationID in locationIDs:
        writer.writerow([locationID, finalResultDict[locationID]])
        
# print("--- (A) %s seconds ---" % (time.time() - start_time))