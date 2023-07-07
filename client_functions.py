from client import Client
import sys, json
from time import sleep
from datetime import datetime
import time


def printd(*args):
    print(datetime.now(), *args)


def start_resource(resource_name, c):
    printd("Starting resource {}".format(resource_name))
    my_clusters = c.get_resources()
    # check if resource exists and is running already
    cluster = next(
        (item for item in my_clusters if item["name"] == resource_name), None
    )
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


def stop_resource(resource_name, c):
    printd("Stopping resource {}".format(resource_name))
    my_clusters = c.get_resources()
    # check if resource exists and is stopped already
    cluster = next(
        (item for item in my_clusters if item["name"] == resource_name), None
    )
    if cluster:
        if cluster["status"] == "off":
            printd("{} already stopped".format(resource_name))
            return "already-stopped"
        else:
            c.stop_resource(cluster['id'])
            printd("{} stopped".format(resource_name))
            return "stopped"
    else:
        printd("{} not found".format(resource_name))
        return "not-found"


def launch_workflow(wf_name, wf_xml_args, user, c):
    printd("Launching workflow {wf} in user {user}".format(wf=wf_name, user=user))
    printd("XML ARGS: ", json.dumps(wf_xml_args, indent=4))
    response = c.run_workflow(wf_name, wf_xml_args)
    # jid, djid = c.start_job(wf_name, wf_xml_args, user)
    return response


def wait_workflow(wf_name, c):
    printd("Waiting for workflow", wf_name)
    while True:
        try:
            data = c.get_latest_job_status(wf_name)
            state = data["status"]
        except:
            state = "starting"

        if state in ["completed", "deleted", "error"]:
            return state

        printd("Workflow", wf_name, "state:", state)
        sleep(10)

    printd(wf_name, "completed successfully")
