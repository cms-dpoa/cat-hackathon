# Container Template
A container template is the most common type of template, lets look at a complete example:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow                 
metadata:
  generateName: container-   
spec:
  entrypoint: main         
  templates:
  - name: main             
    container:
      image: docker/whalesay
      command: [cowsay]         
      args: ["hello world"]
```

Let's run the workflow:

```bash
argo submit --watch container-workflow.yaml
```

Port-forward to the Argo Server pod...

```bash
kubectl -n argo port-forward --address 0.0.0.0 svc/argo-server 2746:2746 > /dev/null &
```

and open the Argo Workflows UI. Then navigate to the workflow, you should see a single container running.

# Exercise
Edit the workflow to make it echo "howdy world".

## Solution
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow                 
metadata:
  generateName: container-   
spec:
  entrypoint: main         
  templates:
  - name: main             
    container:
      image: docker/whalesay
      command: [cowsay]         
      args: ["howdy world"]
```
