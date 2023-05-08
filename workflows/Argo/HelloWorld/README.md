# Hello World

This README provides instructions and information for completing the cloud pre-exercise. Please follow the steps below to install the necessary tools, set up the environment, and perform the exercise tasks.

# Prerequisites

Before starting the pre-exercise, ensure that you have the following prerequisites installed on your machine:

- Minikube - A tool to run a Kubernetes cluster locally.
- kubectl - The Kubernetes command-line tool.
- Argo - Argo Workflows CLI for submitting and managing workflows.

# Setup

Follow the steps below to set up the environment:

## Create the argo namespace:
Open a terminal and run the following command:
```shell
kubectl create ns argo
```

## Deploy Argo Workflows:
Apply the Argo Workflows manifests by running the following command:
```shell
kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo-workflows/master/manifests/quick-start-postgres.yaml
```
Download and configure the Argo CLI:
```shell
curl -sLO https://github.com/argoproj/argo-workflows/releases/download/v3.4.7/argo-darwin-amd64.gz
gunzip argo-darwin-amd64.gz
chmod +x argo-darwin-amd64
sudo mv ./argo-darwin-amd64 /usr/local/bin/argo
argo version
```

This will download the Argo CLI binary, make it executable, and move it to the /usr/local/bin directory.

## Create K8S infrastructure

```shell
kubectl apply -f pv.yaml
kubectl apply -f pvc.yaml -n argo
kubectl apply -f pv-pod.yaml -n argo
```

Every time you want to download your pv files into your local directory run:
```bash
kubectl cp task-pv-pod:/mnt/vol /tmp/poddata -n argo
```

# Usage
## Running Argo Workflows
Access the Minikube dashboard by opening a terminal and run the following command:
```shell
minikube dashboard
```
This will open the Minikube dashboard in your default web browser.
## Submitting a Workflow
To submit a workflow, run the following command:
```shell
argo submit -n argo argo-wf-volume.yaml
```
This will submit the workflow defined in the argo-wf-volume.yaml file to the argo namespace. You can replace argo-wf-volume.yaml with the path to your desired workflow configuration file.
## Checking Workflow Status:
To check the status of a workflow, run the following command:

```shell
argo list -n argo
```
This will display the list of workflows along with their status.
Viewing Workflow Logs:
To view the logs of a specific workflow, run the following command:
```shell
argo logs <workflow-name> -n argo main
```
# Accessing the Argo UI:
The Argo UI provides a graphical interface to view and manage workflows. To access the Argo UI, follow these steps:
Port-forward the Argo server:
Run the following command in a terminal:
```shell
kubectl -n argo port-forward deployment/argo-server 2746:2746
```
## Open the Argo UI:
Open a web browser and navigate to [https://localhost:2746/](https://localhost:2746/) to access the Argo UI.