# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 12:33:46 2015

@author: swanand
"""
import requests
import json
import dweepy
from flask import Flask
from pymongo import MongoClient
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/calories', methods=['GET'])
def getCaloriesForBarcode():
    url='http://world.openfoodfacts.org/api/v0/product/737628064502.json'
    data = requests.get(url)

    info = dumpToMongo(data.json())
    dumpToDweet(data.json())
    return json.dumps(json.dumps(info),indent=4)
    
def dumpToMongo(data):
    info ={'user':'1',
           'genericName': data['product']['generic_name'],
           'code': data['code'],
           'calories':data['product']['nutriments']['energy']
          }
    client = MongoClient()
    cnag = client['calnagger']
    conColl = cnag['consumption']
    conColl.update_one({'user':'1'},{'$set':info},True)
    return {'user':'1',
           'genericName': data['product']['generic_name'],
           'code': data['code'],
           'calories':data['product']['nutriments']['energy']
          }

def dumpToDweet(data):
    dweetUrl = 'http://dweet.io:80/dweet/for/decisive-train/'
    info ={'user':'1',
           'genericName': data['product']['generic_name'],
           'code': data['code'],
           'calories':data['product']['nutriments']['energy']
          }
    resp = requests.post(dweetUrl, data=json.dumps(info))
    print resp
         

if __name__ == '__main__':
    app.run()