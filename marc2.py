import os
import sys

from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient
from dxlmarclient import MarClient, ResultConstants, ProjectionConstants, \
    ConditionConstants, SortConstants, OperatorConstants
from elasticsearch import Elasticsearch

# Elasticsearch setup
es = Elasticsearch(['http://elasticsearchurl:port'])

def action(md5, md5main):

  # Create DXL configuration from file
  CONFIG_FILE = "/path/to/config/file"
  config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

  # Create the client
  with DxlClient(config) as client:

    # Connect to the fabric
    client.connect()

    # Create the McAfee Active Response (MAR) client
    marclient = MarClient(client)

    # Start the search
    results_context = \
        marclient.search(
           projections=[{
                 "name": "HostInfo",
                 "outputs": ["hostname","ip_address"]
           }, {
                 "name": "Files",
                 "outputs": ["md5","status"]
           }],
           conditions={
               "or": [{
                  "and": [{
                  "name": "Files",
                  "output": "md5",
                  "op": "EQUALS",
                  "value": md5
                  }]
               }]
           }
        )

    # Iterate the results of the search in pages
    if results_context.has_results:
         results = results_context.get_results()
         # Display items in the current page
         for item in results[ResultConstants.ITEMS]:
                #print "    " + item["output"]["HostInfo|hostname"] + "    " + item["output"]["HostInfo|ip_address"] + "     " + item["output"]["Files|md5"]
                item[u'Summary'] = {u'Subject': {u'md5': md5main}} 
                item[u'Customer'] = {u'name': 'customer2'}
                res = es.index(index='marc2', doc_type='response', body=item)
