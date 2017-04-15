#!/usr/bin/env python

import logging
import os
import sys
import time
import json
import threading
import importlib

from dxlclient.callbacks import EventCallback
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
from dxlclient.message import Event, Request
from elasticsearch import Elasticsearch

# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")
#from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

CONFIG_FILE = "/path/to/config/file"
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# Variable MISP python
marc1search = importlib.import_module("marc1")
marc2search = importlib.import_module("marc2")

# Elasticsearch setup
es = Elasticsearch(['http://elasticsearchurl:port'])

# Create the client
with DxlClient(config) as client:

    # Connect to the fabric
    client.connect()

    # Create and add event listener
    class MyEventCallback(EventCallback):
        def on_event(self, event):
            try:
                query = event.payload.decode()
                logger.info("Event received: " + query)
                
                query = query[:-3]
                query = json.loads(query)
                
                # Push ATD analysis data into Elasticsearch / Kibana
                res = es.index(index='atd', doc_type='report', body=query)
                # Run Active Response query. Parsing out md5 hashes included in the DXL message
                md5 = query['Summary']['Subject']['md5']
                md5main = query['Summary']['Subject']['md5']
                if not md5: 
                   pass
                else: 
                   marc1search.action(md5, md5main)
                   marc2search.action(md5, md5main)
               
                for hashes in query['Summary']['Files']:
                    md5 = hashes['Md5']
                    if not md5: 
                       pass
                    else: 
                       marc1search.action(md5, md5main)
                       marc2search.action(md5, md5main)
                
            except Exception as e:
                print e

        @staticmethod
        def worker_thread(req):
            client.sync_request(req)

    # Register the callback with the client
    client.add_event_callback('#', MyEventCallback(), subscribe_to_topic=False)
    client.subscribe("/mcafee/event/atd/file/report")

    # Wait forever
    while True:
        time.sleep(60)

