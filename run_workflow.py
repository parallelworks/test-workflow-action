from client import Client
import sys, json, os
import traceback
from time import sleep

from client_functions import *

def get_resource_ids_from_workflow_inputs(workflow_inputs: dict, resource_ids: list):
    for key, value in workflow_inputs.items():
        if isinstance(value, dict):
            if 'type' in value.keys():
                if value['type'] == 'computeResource':
                    resource_ids = resource_ids + [value['id']]

            resource_ids = get_resource_ids_from_workflow_inputs(value, resource_ids)

    return resource_ids


PW_API_KEY = os.environ.get('PW_API_KEY')
PW_PLATFORM_HOST = os.environ.get('PW_PLATFORM_HOST')

c = Client(f'https://{PW_PLATFORM_HOST}', PW_API_KEY)


if __name__ == "__main__":
    printd('\n'.join(sys.argv))
    user = sys.argv[1]  # echo ${PW_USER}
    wf_name = sys.argv[2]
    wf_xml_args = json.loads(sys.argv[3])
    resource_ids = None
    if len(sys.argv) == 5:
        if sys.argv[5]:
            resource_names = sys.argv[4].split("---")  # Not case sensitive
            resource_ids = [get_resource_id_from_resource_name(rname, user, c) for rname in resource_names]
    
    if not resource_ids:
        resource_ids = get_resource_ids_from_workflow_inputs(wf_xml_args, [])

    resources = [ get_resource_from_resource_id(resource_id, c) for resource_id in resource_ids ]

    printd('Found resources with ids ' + ' '.join(resource_ids))
    # Make sure we get to stopping the resources!
    run_workflow = True

    # Exit with error code:
    exit_error = ""

    # Starting resources
    resource_status = []
    for r in resources:
        try:
            resource_status.append(start_resource(r, c))
        except Exception as e:
            msg = "ERROR: Unexpected error when starting resource {}/{} with ID {}".format(
                r['namespace'],
                r['name'],
                r['id']
            )
            printd(msg)
            traceback.print_exc()
            run_workflow = False
            exit_error += msg


    printd("\nWaiting for", len(resource_ids), "cluster(s) to be ready for job submission...")
    wait_for_resources(c, resource_ids)

    if run_workflow:
        try:
            # Launching workflow
            response = launch_workflow(wf_name, wf_xml_args, user, c)
            # Waiting for workflow to complete
            state = wait_workflow(wf_name, c)
            if state != "completed":
                msg = "Workflow final state is " + state
                printd(msg)
                exit_error += "\n" + msg
        except Exception:
            msg = "Workflow launch failed unexpectedly"
            printd(msg)
            traceback.print_exc()
            exit_error += "\n" + msg
    else:
        msg = "Aborting workflow launch"
        printd(msg)
        exit_error += "\n" + msg

    # Stoping resources
    sleep(5)
    for r, rstatus in zip(resources, resource_status):
        printd(r['id'], "status", rstatus)
        # Do not stop the pool if it was already started!
        # FIXME: Even with this precaution a pool with ongoing work could be stopped
        if rstatus == "started":
            stop_resource(r, c)

    if exit_error:
        raise (Exception(exit_error))
