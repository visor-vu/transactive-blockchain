'''
Created on Jan 29, 2018
'''
import sys
import os,signal
from os.path import join
import argparse
import logging
import logging.config
import configparser

class Config(object):
    '''
    Configuration database for RIAPS tools
    Including logging configuration
    '''

    #grafana Setup
    INFLUX_DBASE_HOST='localhost'
    INFLUX_DBASE_PORT=8086
    INFLUX_DBASE_USER='riaps'
    INFLUX_DBASE_PASSWORD = 'riaps'
    INFLUX_DBASE_NAME = 'CarpoolMarket'


    def __init__(self):
        '''
        Constructor
        '''
        pass
