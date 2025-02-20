'''
Created on Feb 20, 2017

@author: riaps
'''
import logging

import pprint
from time import time

from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError

import datetime
import random
import time
from Grafana.config import Config

class Database(object):
#     GRUNNER_DBASE_HOST='localhost'
#     GRUNNER_DBASE_PORT=8086
#
#     GRUNNER_DBASE_USER='riapsdev'
#     GRUNNER_DBASE_PASSWORD = 'riaps'
#     GRUNNER_DBASE_NAME = 'gridlabd'
    def __init__(self):
        super(Database, self).__init__()
        self.logger = logging.getLogger(__name__)
        #thing to get values I need
        #---------------------------------------------------------------------------------
        self.client = InfluxDBClient(Config.INFLUX_DBASE_HOST,Config.INFLUX_DBASE_PORT,
                                     Config.INFLUX_DBASE_USER,Config.INFLUX_DBASE_PASSWORD,
                                     Config.INFLUX_DBASE_NAME)
        self.client.create_database(Config.INFLUX_DBASE_NAME)
        self.client.switch_database(Config.INFLUX_DBASE_NAME)
        #---------------------------------------------------------------------------------

    def log(self,post_time, tag_dict,seriesName,value):
        records = []

        if value != None:
            try:
                floatValue = float(value)
            except:
                floatValue = None
        if floatValue != None:
            #---------------------------------------------------------------------------------
            record = {  "time": post_time,
                        "measurement":seriesName,
                        "tags" : tag_dict,
                        "fields" : { "value" : floatValue },
                        }
            records.append(record)
        self.logger.info("writing: %s" % str(records))
        res= self.client.write_points(records) # , retention_policy=self.retention_policy)
        #---------------------------------------------------------------------------------

        # print (res)
        # assert res

    def __destroy__(self):
        self.client.drop_database(Config.INFLUX_DBASE_NAME)
