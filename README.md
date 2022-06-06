# Test Workflow Action
Sample [Docker-based Github action](https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action) to automatically test a PW workflow using the [PW client](https://raw.githubusercontent.com/parallelworks/pw-cluster-automation/master/client.py). The action defines the following steps:

1. Starts the PW resources required by the workflow
2. Submits the workflow
3. Stops the PW resources started in (1)

The inputs to the action are defined in the `action.yml` file. The PW client requires the API key of the account for authentication. Store this key as a [Github secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets) in the repository with your PW workflow.  
The code snippet below exemplifies how to add this action the Github repository of a PW workflow such that the worflow is tested with every new push:

```
on: [push]

jobs:
  test-pw-workflow:
    runs-on: ubuntu-latest
    name: test-pw-workflow-beluga
    steps:
      - name: run-workflow-beluga
        id: run-beluga
        uses: parallelworks/test-workflow-action@v3
        with:
          pw-user-host: 'beluga.parallel.works'
          pw-api-key: ${{ secrets.USERDEMO_BELUGA_API_KEY }}
          pw-user: 'User.Demo'
          resource-pool-names: 'gcpslurmv2'
          workflow-name: 'singlecluster_parsl_demo'
```


### TODO / Limitations:
The input parameters to the PW workflow are hardcoded in the parameter `wf_xml_args = {}` of the `run_workflow.py` script. This sample action needs to be modified to support passing inputs to the workflow. 