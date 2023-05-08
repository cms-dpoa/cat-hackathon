# Loop Template

The ability to run large parallel processing jobs is one of the key features or Argo Workflows.  
Let's have a look at using loops to do this.

## withItems

A DAG allows you to loop over a number of items using `withItems` :

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: with-items-
spec:
  entrypoint: main
  templates:
    - name: main
      dag:
        tasks:
          - name: print-message
            template: whalesay
            arguments:
              parameters:
                - name: message
                  value: "{{item}}"
            withItems:
              - "hello world"
              - "goodbye world"

    - name: whalesay
      inputs:
        parameters:
          - name: message
      container:
        image: docker/whalesay
        command: [ cowsay ]
        args: [ "{{inputs.parameters.message}}" ]
```

In this example, it will execute once for each of the listed items. We can see a **template tag** here. `{{item}}` will be replaced with "hello world" and "goodbye world". DAGs execute in parallel, so both tasks will be started at the same time.

```bash
argo submit --watch with-items-workflow.yaml
```

You should see something like:

```python
STEP                                 TEMPLATE  PODNAME                      DURATION  MESSAGE
 ✔ with-items-4qzg9                  main                                               
 ├─✔ print-message(0:hello world)    whalesay  with-items-4qzg9-465751898   7s          
 └─✔ print-message(1:goodbye world)  whalesay  with-items-4qzg9-2410280706  5s          
```

Here the two items ran at the same time.

## withSequence

You can also loop over a sequence of numbers using `withSequence` :

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: with-sequence-
spec:
  entrypoint: main
  templates:
    - name: main
      dag:
        tasks:
          - name: print-message
            template: whalesay
            arguments:
              parameters:
                - name: message
                  value: "{{item}}"
            withSequence:
              count: 5

    - name: whalesay
      inputs:
        parameters:
          - name: message
      container:
        image: docker/whalesay
        command: [ cowsay ]
        args: [ "{{inputs.parameters.message}}" ]
```

As usual, run it:

```bash
argo submit --watch with-sequence-workflow.yaml
```

```python
STEP                     TEMPLATE  PODNAME                         DURATION  MESSAGE
 ✔ with-sequence-8nrp5   main                                                  
 ├─✔ print-message(0:0)  whalesay  with-sequence-8nrp5-3678575801  9s          
 ├─✔ print-message(1:1)  whalesay  with-sequence-8nrp5-1828425621  7s          
 ├─✔ print-message(2:2)  whalesay  with-sequence-8nrp5-1644772305  13s         
 ├─✔ print-message(3:3)  whalesay  with-sequence-8nrp5-3766794981  15s         
 └─✔ print-message(4:4)  whalesay  with-sequence-8nrp5-361941985   11s         
```

Here 5 pods were run at the same time, and that their names have the item value in them, zero-indexed?


# Exercise

Change the **withSequence** to print the numbers 10 to 20.

## Solution

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: with-sequence-
spec:
  entrypoint: main
  templates:
    - name: main
      dag:
        tasks:
          - name: print-message
            template: whalesay
            arguments:
              parameters:
                - name: message
                  value: "{{item}}"
            withSequence:
              start: "10"
              end: "20"

    - name: whalesay
      inputs:
        parameters:
          - name: message
      container:
        image: docker/whalesay
        command: [ cowsay ]
        args: [ "{{inputs.parameters.message}}" ]
```
Expected output
```python
STEP                       TEMPLATE  PODNAME                                  DURATION  MESSAGE
 ✔ with-sequence-trt54     main                                                           
 ├─✔ print-message(0:10)   whalesay  with-sequence-trt54-whalesay-2676655126  1m          
 ├─✔ print-message(1:11)   whalesay  with-sequence-trt54-whalesay-3249200728  1m          
 ├─✔ print-message(2:12)   whalesay  with-sequence-trt54-whalesay-3044606934  1m          
 ├─✔ print-message(3:13)   whalesay  with-sequence-trt54-whalesay-8539748     1m          
 ├─✔ print-message(4:14)   whalesay  with-sequence-trt54-whalesay-2936616694  1m          
 ├─✔ print-message(5:15)   whalesay  with-sequence-trt54-whalesay-2823488216  1m          
 ├─✔ print-message(6:16)   whalesay  with-sequence-trt54-whalesay-3345741286  49s         
 ├─✔ print-message(7:17)   whalesay  with-sequence-trt54-whalesay-2109538044  1m          
 ├─✔ print-message(8:18)   whalesay  with-sequence-trt54-whalesay-3854212550  1m          
 ├─✔ print-message(9:19)   whalesay  with-sequence-trt54-whalesay-499096040   1m          
 └─✔ print-message(10:20)  whalesay  with-sequence-trt54-whalesay-2515772514  1m         
```