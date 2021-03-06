#!/usr/bin/env python
# Coded By Joel A. Ossi

import socket
import urllib3
import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

f = open('domains.txt', 'r')
for line in f:
    try:
        response = session.get(line[:-1], timeout=5, verify=False)
        if '/' or '(' in response:
            print ("[+] GRABBING SERVER DATA: " + line)
            with open('output.txt', 'a') as servers:
                servers.write('[Host: ' + str(line[:-1]) + ', Header: ' + str(response.headers) + ']')
                servers.write('\n')
    except Exception as e:
        print('[!] An error occurred with: ' + line + ' Error Code: ' + str(e.args) + '\n')
        with open('errors.txt', 'a') as servers:
            servers.write('[Host: ' + str(line[:-1]) + ']')
            servers.write('\n')
        pass
    except socket.timeout:
        print ("Socket Timeout Detected")
        pass
