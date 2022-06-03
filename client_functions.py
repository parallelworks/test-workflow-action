from client import Client
import sys, json
from time import sleep

def start_resource(resource_name, c):
    print('Starting resource {}'.format(resource_name))
    # check if resource exists and is running already
    resource = c.get_resource(resource_name)
    if resource:
        if resource['status'] == "off":
            c.start_resource(resource_name)
            print('{} started'.format(resource_name))
            return 'started'
        else:
            print('{} already running'.format(resource_name))
            return 'already-running'
    else:
        print('{} not found'.format(resource_name))
        return 'not-found'

def stop_resource(resource_name, c):
    print('Stopping resource {}'.format(resource_name))
    # check if resource exists and is stopped already
    resource = c.get_resource(resource_name)
    if resource:
        if resource['status'] == "off":
            print('{} already stopped'.format(resource_name))
            return 'already-stopped'
        else:
            c.stop_resource(resource_name)
            print('{} stopped'.format(resource_name))
            return 'stopped'
    else:
        print('{} not found'.format(resource_name))
        return 'not-found'
    
    
def launch_workflow(wf_name, wf_xml_args, user, c):
    print('Launching workflow {wf} in user {user}'.format(
        wf = wf_name,
        user = user
    ))   
    print('XML ARGS: ', json.dumps(wf_xml_args, indent = 4))
    jid,djid = c.start_job(wf_name, wf_xml_args, user)
    return jid, djid


def wait_workflow(djid, wf_name):
    print('Waiting for workflow', wf_name)
    while True:
        try:
            state = c.get_job_state(djid)
        except:
            state = 'starting'

        if state == 'ok':
            break
        elif (state == 'deleted' or state == 'error'):
            raise Exception('Simulation had an error. Please try again')

        print('Workflow', wf_name, 'state:', state)
        sleep(2)

    print(wf_name, 'completed successfully')
