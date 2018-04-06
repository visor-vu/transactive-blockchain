import datetime
import sys
import random
import logging
logging.basicConfig(level=logging.INFO)
from math import cos, asin, sqrt, floor
import pprint
import pymongo
import pandas as pd
from Prosumer import Prosumer
METERS_PER_KM = 1000

#class Carpooler(Prosumer.Prosumer):
#    def __init__(self, srclat, srclng, dstlat, dstlng, prosumer_id, ip, port):
class Carpooler(Prosumer):
    def __init__(self,srclat,srclng,dstlat,dstlng):
        self.geo_db = pymongo.MongoClient().geo
        self.quantity = {}
        self.value = {}
        self.seats = 0
        self.providing = 0
        self.earliest = 0
        self.latest = 0
        self.pud = 1000
        self.srclat = srclat
        self.srclng = srclng
        self.dstlat = dstlat
        self.dstlng = dstlng
        self.dst = str(dstlat) +","+str(dstlng)
        self.departure_times = []
        #self.randomSetup()
        super(Carpooler, self).__init__(prosumer_id, ip, port)

    def bidBuilder(self,pups):
        self.logger.info("num pickups : %s"%len(pups))
        if pups:
            for pup in pups:
                pup_lng, pup_lat = pup['location']['coordinates']
                pup_id = pup['location']['pupID']
                pup_dist = self.distance(float(self.srclat), float(self.srclng), pup_lat, pup_lng)
                self.logger.info("Distance to pickup point : %s" %pup_dist)
                dest_dist = self.distance(pup_lat, pup_lng, float(self.dstlat), float(self.dstlng))
                self.logger.info("Distance to destination from pup %s" %dest_dist)
                for time in self.departure_times[self.earliest:self.latest+1]:
                    #t = time.strftime("%d/%m/%Y %H:%M")
                    t = int(time.timestamp())
                    #src = str(pup_lat)+","+str(pup_lng)
                    #key = src+"_"+t+"_"+self.dst
                    # print(pup_id)
                    # print(t)
                    # print(time.strftime("%d/%m/%Y %H:%M"))
                    # print(self.dst_id)
                    key = int(str(pup_id)+str(t)+str(self.dst_id))
                    #print("Key : %s" %key)
                    self.quantity[key] = self.seats
                    self.value[key] = floor(pup_dist+dest_dist-self.directDist)
            #pprint.pprint(self.quantity)
            #pprint.pprint(self.value)
            bid = (self.providing, self.quantity, self.value)
        else:
            self.logger.info("no pickup in range")
            bid = ()
        return bid


    def randomSetup(self):
        #--Random number of seats--
        rnd = random.random()
        if rnd >=.5:
            self.seats = 1
        elif rnd >=.2 and rnd<.5:
            self.seats = 2
        else:
            self.seats = 3
        #--Randomly assign provider state
        rnd = random.random()
        if rnd <= .1:
            self.providing = True
        else:
            self.providing = False
        #--Randomly assign departure interval--
        today = datetime.datetime.combine(datetime.date.today(),datetime.time(hour=7))
        for i in range(9):
            self.departure_times.append(today + datetime.timedelta(minutes=15*i))
        #pprint.pprint(self.departure_times)
        earliest = random.choice(self.departure_times)
        self.logger.info("earliest time %s" %earliest)
        self.earliest = self.departure_times.index(earliest)
        self.logger.info("earliest index %s" %self.earliest)
        latest = random.choice(self.departure_times[self.earliest:])
        self.logger.info("latest time %s" %latest)
        self.latest = self.departure_times.index(latest)

        self.directDist = self.distance(float(self.srclat), float(self.srclng), float(self.dstlat), float(self.dstlng))
        self.logger.info("Direct Distance : %s" %self.directDist)


    #----Distance-------------------------------------------------------------------
    # https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula

    def distance(self, lat1, lon1, lat2, lon2):
        '''Distance in km'''
        p = 0.017453292519943295     #Pi/180
        a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
        return 12742 * asin(sqrt(a)) #2*R*asin...
    #-------------------------------------------------------------------------------

    def getPickups(self, pud, lat, lng):
        print("in pups")
        print(pud, lat, lng)
        near = self.geo_db.Pickups.find({ "location":
                                        { "$nearSphere":
                                          { "$geometry":
                                            { "type": "Point", "coordinates": [ float(lng), float(lat) ] }, #[ <longitude>, <latitude> ]
                                            "$maxDistance": pud * METERS_PER_KM } } })
        print("Pickups in %s KMs : %s " %(pud, near.count()))
        return(near)


if __name__ == "__main__":
    prosumer_id = 101
    ip = 'localhost'
    port = 10000
    if len(sys.argv) > 1:
        prosumer_id = int(sys.argv[1])
    if len(sys.argv) > 2:
        ip = sys.argv[2]
    if len(sys.argv) > 3:
        port = sys.argv[3]
    if len(sys.argv) > 4:
        trip_file=sys.argv[4]
    trips = (pd.read_csv(trip_file)).round(6)
    my_trip = trips.loc[trips['ID'] == prosumer_id]
    #print("my trip \n%s" %my_trip)
    srclat = my_trip.loc[1,'from_lat']
    srclng = my_trip.loc[1,'from_lng']
    dstlat = my_trip.loc[1,'to_lat']
    dstlng = my_trip.loc[1,'to_lng']

    CP = Carpooler(srclat,srclng,dstlat,dstlng)
    #pprint.pprint("all dst: %s" %list(CP.geo_db.Dests.find({})))
    #print(srclat,srclng,dstlat,dstlng)
    #pprint.pprint("dst: %s" %list(CP.geo_db.Dests.find({"location.coordinates": [dstlng, dstlat]})))
    dst = list(CP.geo_db.Dests.find({"location.coordinates": [dstlng, dstlat]}))
    CP.dst_id = dst[0]['location']['dstID']

    #print("pups: %s" %list(CP.geo_db.Pickups.find({})))
    pups = list(CP.getPickups(10, srclat, srclng))
    pprint.pprint(pups)
    CP.randomSetup()
    bid = CP.bidBuilder(pups)
    print(type(bid))
    if bid:
        pprint.pprint(bid)
        print("post offer")
        CP.post_offer(bid[0], bid[1], bid[2])
        print("run")
        CP.run()
    else:
        print("empty")