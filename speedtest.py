#!/usr/bin/env python3

import os, re, time, sys, datetime
from influxdb import InfluxDBClient
from subprocess import check_output

DB_HOST = "1.2.3.4"
DB_PORT = "8086"
DB_USER = "mydb-user"
DB_PASSWORD = "VerySecurePassword"
DB_NAME = "mydb"

response = check_output(["/usr/local/bin/speedtest-cli", "--simple"]).decode("utf-8")
# for testing only:
#response = "Ping: 14.624 ms\nDownload: 11.06 Mbit/s\nUpload: 13.25 Mbit/s"

rlist = response.split('\n') # get the whole response into a list, example: ['Ping: 14.624 ms', 'Download: 11.06 Mbit/s', 'Upload: 13.25 Mbit/s']
pinglist = rlist[0] # extract the first list item which is Ping
dllist = rlist[1] # extract the second list item which is Download
ullist = rlist[2] # extract the third list item which is Upload
pv = pinglist.split(" ") # get 'Ping: 14.624 ms' into a separate list, separator is the whitespace
dlv = dllist.split(" ") # get 'Download: 11.06 Mbit/s' into a separate list, separator is the whitespace
ulv = ullist.split(" ") # get 'Upload: 13.25 Mbit/s' into a separate list, separator is the whitespace
ping = pv[1] # get the second item of the list, which is the value
dl = dlv[1] # get the second item of the list, which is the value
ul = ulv[1] # get the second item of the list, which is the value

# build the json body for influxdb
body_ping = [
    {
        "measurement": "ping",
        "time": datetime.datetime.now(),
        "fields": {
            "value": float(ping)
        }
    }
]
body_download = [
    {
        "measurement": "download",
        "time": datetime.datetime.now(),
        "fields": {
            "value": float(dl)
        }
    }
]
body_upload = [
    {
        "measurement": "upload",
        "time": datetime.datetime.now(),
        "fields": {
            "value": float(ul)
        }
    }
]

# write to influxdb
speedtest_client = InfluxDBClient(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
speedtest_client.write_points(body_ping)
speedtest_client.write_points(body_download)
speedtest_client.write_points(body_upload)