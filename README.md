# Test Workflow Action
This repository contains a Docker-based GitHub action designed to automate running a Parallel Works (PW) workflow using the [PW client](https://raw.githubusercontent.com/parallelworks/pw-cluster-automation/master/client.py). The action executes the following steps:

1. Starts the necessary PW resources for the job.
2. Submits the job.
3. Stops the resources initiated in step 1.

**Note:** If the required resources are already running, the workflow will utilize them without shutting them down.

The action's inputs are specified in the `action.yml` file. To integrate this action into a PW workflow (stored in a separate repository, as this repository solely contains the action), follow these steps in the **workflow repository**:

1. Store the PW client's API key as a [Github secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets) in the workflow repository (not this repository). Navigate to your workflow on GitHub.com and go to `Settings > Secrets > Actions > New Repository Secret`. Note: You must be the owner of the workflow repository or have permissions to edit/view repository secrets in the workflow repository to perform this step.
2. Configure GitHub to trigger this action whenever specified events occur in the workflow repository by adding this action to .github/workflows/main.yaml in the **workflow repository**. For instance, the code snippet below adds this action to the GitHub repository of a PW workflow, ensuring that the workflow is tested with every new push:

```
on: [push]

jobs:
  test-pw-workflow:
    runs-on: ubuntu-latest
    name: Run PW Workflow
    env:
      PW_PLATFORM_HOST: cloud.parallel.works
      PW_API_KEY: ${{ secrets.PW_API_KEY }}
    steps:
      - name: Run PW Workflow
        id: run-cloud
        uses: parallelworks/test-workflow-action@v7
        with:
          pw-user: 'alvaro'
          workflow-name: 'single_resource_command'
          workflow-parameters: ''{"command": "hostname","resource_1": {"type": "computeResource","id": "65e8529e0c1cc9f0d8448000"},"startCmd": "001_single_resource_command/main.sh"}''
```

The action requires two environment variables:
1. PW_PLATFORM_HOST: The URL of the platform deployment, e.g., cloud.parallel.works. This variable is also an environment variable in the user container.
2. PW_API_KEY: The unique API key for each user, obtainable [here](https://cloud.parallel.works/settings/authentication/apikey). This key must be stored as a GitHub secret in the repository.

Additionally, the action accepts the following inputs:
1. pw-user: The name of the PW user account to launch the job.
2. workflow-name: The name of the workflow to run.
3. workflow-parameters: A JSON-formatted string containing the inputs to the workflow. You can generate this string by filling in the input form of a given workflow, navigating to the JSON tab, and copying the inputs (see this [image](https://github.com/parallelworks/test-workflow-action/blob/main/json-input-form.png).
4. resource-names: The names of the resources required to run the workflow. Use "---" to specify multiple resources, e.g., r1---r2. The format for each resource is `<user_name>/<resource_name>`. If no user_name is provided, the user's name is used by default. This input is optional. When not provided, the resources are obtained from the computeResource parameter types in the workflow-parameters.

A sample workflow utilizing this action is provided [here](https://github.com/parallelworks/test-workflow-action/blob/main/.github/workflows/run_job.yml).

### Notes:
1. GitHub, by default does not allow users to use their PAT to add `.github/workflows/main.yaml`.  Either add this permission
to your PAT via your account's `Settings` > `Developer Settings` > `Personal Access Tokens`, selecting your PAT, and checking 
the workflow box or use an SSH key. An easy alternative is to use the GitHub GUI to add actions by clicking on the `Actions` tab
for your repository and then clicking on the `set up a workflow yourself ->` link. This issue is purely permission to **add** an
action to a repository - once that permission is added, a standard PAT (without any special GitHub workflow permission) can 
still make pushes to the repository, and if the action is already set up to run on a push, then those actions will be
executed.

2. If instead of a push the GH action in the workflow repository is launched by a GH release, be careful to specify a specific stage in the release process (creation, editing, publishing) - otherwise a general `on: [release]` will actually be interpreted at [three separate events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#release), each event lauching a different workflow run. Explicitly, to select the publishing of a release (instead of creation or editing), the following header snippet can be used:
```
on:
  release:
    type: [publish]
    
jobs:
  ...
```
