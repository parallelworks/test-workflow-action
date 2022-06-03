from client import Client
import sys
import traceback

from client_functions import *

if __name__ == '__main__':
    pw_user_host = sys.argv[1] # echo ${PW_USER_HOST}
    pw_api_key = sys.argv[2]   # echo ${PW_API_KEY}
    user = sys.argv[3]         # echo ${PW_USER}
    resource_names = sys.argv[4].split('---') # Not case sensitive
    wf_name = sys.argv[5]
    wf_xml_args = {}
    
    c = Client('https://' + pw_user_host, pw_api_key)

    # Make sure we get to stopping the resources!
    run_workflow = True
    
    # Starting resources
    resource_status = []
    for rname in resource_names:
        try:
            resource_status.append(start_resource(rname, c))
        except Exception as e:
            print('ERROR: Unexpected error when starting resource', rname)
            traceback.print_exec()
            run_workflow = False

    # Running workflow
    if run_workflow:
        if 'not-found' in resource_status:
            print('ERROR: Some resources were not found')
            run_workflow = False

    if run_workflow:
        try:
            # Launching workflow
            jid, djid = launch_workflow(wf_name, wf_xml_args, user, c)
            # Waiting for workflow to complete
            wait_workflow(djid, wf_name, c)
        except Exception:
            print('Failed to launch workflow')
            traceback.print_exc()
    else:
        print('Aborting workflow launch')
            

    # Stoping resources
    # FIXME: Wont be able to stop the resource if it was just started!
    from time import sleep
    sleep(5)
    for rname, rstatus in zip(resource_names, resource_status):
        print(rname, 'status', rstatus)
        # Do not stop the pool if it was already started!
        # FIXME: Even with this precaution a pool with ongoing work could be stopped
        if rstatus == 'started':
            stop_resource(rname, c)

    
