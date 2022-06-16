from client import Client
import sys, json
import traceback

# FIXME: Wont be able to stop the resource if it was just started!
from time import sleep

from client_functions import *

if __name__ == '__main__':
    pw_user_host = sys.argv[1] # beluga.parallel.works
    pw_api_key = sys.argv[2]   # echo ${PW_API_KEY}
    user = sys.argv[3]         # echo ${PW_USER}
    resource_names = sys.argv[4].split('---') # Not case sensitive
    wf_name = sys.argv[5]
    wf_xml_args = json.loads(sys.argv[6])
    
    c = Client('https://' + pw_user_host, pw_api_key)

    # Make sure we get to stopping the resources!
    run_workflow = True

    # Exit with error code:
    exit_error = ''
    
    # Starting resources
    resource_status = []
    for rname in resource_names:
        try:
            resource_status.append(start_resource(rname, c))
        except Exception as e:
            msg = 'ERROR: Unexpected error when starting resource ' + rname
            print(msg)
            traceback.print_exec()
            run_workflow = False
            exit_error += msg 

    # Running workflow
    if run_workflow:
        if 'not-found' in resource_status:
            msg = 'ERROR: Some resources were not found'
            print(msg)
            run_workflow = False
            exit_error += '\n' + msg

    if run_workflow:
        try:
            # Launching workflow
            jid, djid = launch_workflow(wf_name, wf_xml_args, user, c)
            # Waiting for workflow to complete
            wait_workflow(djid, wf_name, c)
        except Exception:
            msg = 'Workflow launch failed'
            print(msg)
            traceback.print_exc()
            exit_error += '\n' + msg
    else:
        msg = 'Aborting workflow launch'
        print(msg)
        exit_error += '\n' + msg
            

    # Stoping resources
    sleep(5)
    for rname, rstatus in zip(resource_names, resource_status):
        print(rname, 'status', rstatus)
        # Do not stop the pool if it was already started!
        # FIXME: Even with this precaution a pool with ongoing work could be stopped
        if rstatus == 'started':
             stop_resource(rname, c)


    if exit_error:
        raise(Exception(exit_error))
