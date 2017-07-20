# OpenDXL-ATD-MAR-Elastic

This integration is focusing on the automated real-time threat hunting with McAfee ATD, OpenDXL, Active Response and Elasticsearch. McAfee Advanced Threat Defense will produce local threat intelligence that will be pushed via DXL. An OpenDXL wrapper will subscribe and parse indicators ATD produced and execute automated Active Response searches across multiple DXL fabrics. The result will be imported in a big data analytic platform. 

![21_atd_mar_elastic](https://cloud.githubusercontent.com/assets/25227268/25066632/0b645b44-222c-11e7-9faa-e364f99e477a.PNG)

## Component Description
**McAfee Advanced Threat Defense (ATD)** is a malware analytics solution combining signatures and behavioral analysis techniques to rapidly identify malicious content and provides the local threat intelligence for our solution. ATD exports IOC data in STIX format in several ways including DXL. https://www.mcafee.com/in/products/advanced-threat-defense.aspx

**McAfee Active Response (MAR)** is an incident response solution that leverage the DXL messaging fabric to support the threat hunting process and provide real time visibility. https://www.mcafee.com/in/products/endpoint-threat-defense-response.aspx

**Elasticsearch** is a search engine that provides a distributed, multitenant-capable full-text search engine. Kibana is an open source data visualization plugin for Elasticsearch that provides visualization capabilities on top of the content indexed on Elasticsearch. https://www.elastic.co/

## Prerequisites
McAfee ATD solution (tested with ATD 3.8)

Download the [Latest Release](https://github.com/mohl1/OpenDXL-ATD-MAR-Elasticsearch/releases)
   * Extract the release .zip file
   
OpenDXL Python installation
1. Python SDK Installation ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/installation.html))
    Install the required dependencies with the requirements.txt file:
    ```sh
    $ pip install -r requirements.txt
    ```
    This will install the dxlclient, dxlmarclient, and  elasticsearch modules.     
2. Certificate Files Creation ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/certcreation.html))
3. ePO Certificate Authority (CA) Import ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/epocaimport.html))
4. ePO Broker Certificates Export ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/epobrokercertsexport.html))
5. Python SDK for MAR Installation ([Link](https://github.com/opendxl/opendxl-mar-client-python))

Elasticsearch and Kibana (tested with 5.1.2)

Elasticsearch Python client ([Link](https://github.com/elastic/elasticsearch-py)). This dependency will be installed
as part of install using the requirements.txt file.

## Configuration
McAfee ATD receives files from multiple sensors like Endpoints, Web Gateways, Network IPS or via Rest API. ATD will perform malware analytics and produce local threat intelligence. After an analysis every indicator of comprise will be published via the Data Exchange Layer (topic: /mcafee/event/atd/file/report).

### atd_subscriber.py
The atd_subscriber.py receives DXL messages from ATD, parse out the hash information and loads marc1.py and marc2.py. (This can be extended by using e.g. C2 IP's ATD discovered.)

Change the CONFIG_FILE path in the atd_subscriber.py file (line 25)

`CONFIG_FILE = "/path/to/config/file"`

Change the Elasticsearch information (line 33)

`es = Elasticsearch(['http://elasticsearchurl:port'])`

### marc1.py (First DXL fabric)
The marc1.py receives the hash information ATD discovered (including the main file hashes as well as dropped file hashes) and launches multiple Active Response searches. The client response will automatically pushed and indexed by Elasticsearch.

Change the Elasticsearch information (line 11)

`es = Elasticsearch(['http://elasticsearchurl:port'])`

Change the CONFIG_FILE path (line 16)

`CONFIG_FILE = "/path/to/config/file"`

### marc2.py (Second DXL fabric)
Repead the same steps mention under marc1.py if you want to search in other DXL fabrics (multiple DXL fabrics).

## Run the OpenDXL wrapper
> python atd_subscriber.py

or

> nohup python atd_subscriber.py &

## Summary
With this use case, ATD produces local intelligence and pushes IOC information via DXL. With OpenDXL we are able to receives these information and launch multiple Active Response lookups. The client response will automatically pushed to Elasticsearch.

It is possible to visualize the results with Kibana. Make sure to add the Index Patterns first.

The Dashboard below shows the latest ATD analysis (atd index) and the two rows below show the indicators Active Response found in DXL fabric1 (marc1 index) and DXL fabric2 (marc2 index).

![22_atd_mar_elastic](https://cloud.githubusercontent.com/assets/25227268/25066853/9b207370-2232-11e7-981b-5e84ed242d18.PNG)






