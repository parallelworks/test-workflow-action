
def get_resource_ids_from_workflow_inputs(workflow_inputs: dict, resource_ids: list):
    for key, value in workflow_inputs.items():
        if isinstance(value, dict):
            if 'type' in value.keys():
                if value['type'] == 'computeResource':
                    resource_ids = resource_ids + [value['id']]

            resource_ids = get_resource_ids_from_workflow_inputs(value, resource_ids)

    return resource_ids


wf_args = {
    "command": "hostname",
    "resource_1": {
        "type": "computeResource",
        "id": "65e8529e0c1cc9f0d8448000"
    },
    "startCmd": "001_single_resource_command/main.sh",
    "section_2": {
        "resource_1": {
            "type": "computeResource",
            "id": "65e8529e0c1cc9f0d8448001"
        },
        "resource_2": {
            "type": "computeResource",
            "id": "65e8529e0c1cc9f0d8448002"
        },
    },
    "section_3": {
        "resource_1": {
            "type": "computeResource",
            "id": "65e8529e0c1cc9f0d8448001"
        },
        "resource_2": {
            "type": "computeResource",
            "id": "65e8529e0c1cc9f0d8448003"
        },
    },
    "resource_3": {
        "type": "computeResource",
        "id": "65e8529e0c1cc9f0d8448004"
    }
}

resource_ids = []
resource_ids = get_resource_ids_from_workflow_inputs(wf_args, resource_ids)
# unique resource ids:
resource_ids = list(set(resource_ids))

print(resource_ids)