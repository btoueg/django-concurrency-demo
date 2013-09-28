#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script assumes you have one 'Product' in database, with id 1.
"""

from multiprocessing import Process
import time
import sys
import urllib.request
import urllib.parse
import json

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor)

def create_order():
    url = 'http://127.0.0.1:8000/order/'
    values = {'product':1}
    data  = urllib.parse.urlencode(values).encode('utf-8')
    request = urllib.request.Request(url, data)
    response = opener.open(request)
    return response

def cancel_order(order_id):
    abort_url = 'http://127.0.0.1:8000/order/{}/abort/'.format(order_id)
    values = {'product':1}
    data  = urllib.parse.urlencode(values).encode('utf-8')
    request = urllib.request.Request(abort_url, data)
    try:
        response = opener.open(request)
    except Exception as e:
        if (e.code != 403):
            print(e)
    else:
        print(response.getcode())

def main(accept=False, abort=False):
    response = create_order()
    print(response.getcode())
    data = response.read().decode('utf-8')
    order_id = data
    time.sleep(1)
    for i in range(5):
        p = Process(target=cancel_order, args=[order_id])
        p.start()

if __name__ == '__main__':
    main()
