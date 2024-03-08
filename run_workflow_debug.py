from client import Client
import sys, json
from time import sleep
from datetime import datetime
import time
import xml.etree.ElementTree as ET


def printd(*args):
    print(datetime.now(), *args)


def start_resource(resource_name, c):
    printd("Starting resource {}".format(resource_name))
    my_clusters = c.get_resources()
    # check if resource exists and is running already
    cluster = next(
        (item for item in my_clusters if item["name"] == resource_name), None
    )
    print(cluster)
    if cluster:
        if cluster["status"] == "off":
            time.sleep(0.2)
            c.start_resource(cluster["id"])
            printd("{} started".format(resource_name))
            return "started"
        else:
            printd("{} already running".format(resource_name))
            return "already-running"
    else:
        printd("{} not found".format(resource_name))
        return "not-found"
