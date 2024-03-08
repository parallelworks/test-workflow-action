from client import Client
import sys, json
from time import sleep
from datetime import datetime
import time
import xml.etree.ElementTree as ET


class ResourceNotFoundError(Exception):
    pass

def printd(*args):
    print(datetime.now(), *args)

def get_resource_id_from_resource_name(rname, user, c):
    resources = c.get_resources()
    if '/' in rname:
        rnamespace = rname.split('/')[0]
        rname = rname.split('/')[1]
    else:
        rnamespace = user

    for r in resources:
        if r['name'] == rname and r['namespace'] == rnamespace:
            return r['id']
        
    raise ResourceNotFoundError(f"No resource found with name '{rname}' and namespace '{rnamespace}'.")

def get_resource_from_resource_id(rid, c):
    resources = c.get_resources()

    for r in resources:
        if r['id'] == rid:
            return r
        
    raise ResourceNotFoundError(f"No resource found with id '{rid}'.")


def start_resource(resource, c):
    printd("Starting resource {}".format(resource['id']))

    if resource["status"] == "off":
        time.sleep(0.2)
        c.start_resource(resource["id"])
        printd("Resource {}/{} with id {} started".format(resource['namespace'], resource['name'], resource['id']))
        return "started"
    else:
        printd("Resource {}/{} with id {} is already started".format(resource['namespace'], resource['name'], resource['id']))
        return "already-running"


def stop_resource(resource, c):
    printd("Stopping resource {}".format(resource['id']))
    c.stop_resource(resource['id'])
    printd("Resource {}/{} with ID {} stopped".format(
        resource['namespace'], 
        resource['name'], 
        resource['id'])
    )

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
            printd(wf_name, "completed successfully")
            return state

        printd("Workflow", wf_name, "state:", state)
        sleep(10)


def wait_for_resources(c, resource_ids):
    job_resources_started_prev = []
    while True:
        updated_resources = c.get_resources()
        job_resources = [ r for r in updated_resources if r['id'] in resource_ids ]
        job_resources_running = [ r for r in job_resources if r['status'] == 'on' ]
        job_resources_started = [ r for r in job_resources_running if 'masterNode' in r['state'] ] 
        job_resources_started = [ r for r in job_resources_started if r['state']['masterNode'] != None ] 

        for r in job_resources_started:
            if r not in job_resources_started_prev:
                printd('Resource {} is ready'.format(r['name']))
                job_resources_started_prev.append(r)

        if len(job_resources_started) == len(resource_ids):
            printd("Started all clusters")
            return

        time.sleep(5)