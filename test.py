#!/usr/bin/env python
#coding:utf-8

import http.client
import requests
import json

url = 'https://api.aminer.org/'
s = json.dumps({'keys': 'jie tang'})
r = requests.post(url, data=s)
print(r)

# param={'key':'jie tang'}
# r=requests.get(url,params=param)
# print(r.status_code)
# print(r.url)
#
