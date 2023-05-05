# Analysis structure

Making a research data analysis reproducible basically means to provide "runnable recipes" addressing (1) where is the input data, (2) what software was used to analysis the data, (3) which computing environments were used to run the software and (4) which computational workflow steps were taken to run the analysis. This will permit to instantiate the analysis on the computational cloud and run the analysis to obtain (5) output results.

## 1. Input data

In this example, we are using simple bash executables to demonstrate how the data is accessed within a simple consecutive workflow.

## 2. Analysis code

The analysis will consist of two stages. Both will append text to a file, demonstrating the data flow nature and how to use the input files.

- For the first generation stage, [script1.sh] is an executable bash file used to echo text into the expected final resulting file.
- For the second appending stage, [script2.sh] is an executable bash file, that uses the input file [input.txt] to append text to the existing result file. 

## 3. Compute environment

Since this is merely as a demonstration, this simple example is run with the `riga/py-sci` image.

## 4. Analysis workflow

The analysis workflow is simple and consists of two above-mentioned stages:

	 +---------+
	 |  START  |
	 +---------+
            |  
            V  input: "code/script1.sh"
	 +----------------+
	 |  (1)createDir  |
	 +----------------+
		   |  output: "/results/outputfile.txt"
		   |  
		   |  input: "code/script2.sh"
		   v  input: "data/input.txt"
	 +------------------+
	 |  (2)navigateDir  |
	 +------------------+
		   |  output:"/results/outputfile.txt"
		   v
	 +----------+
	 |   STOP   |
	 +----------+


## 5. Output results

The example produces a text file with the expected output:

```output
Hello World!
Hello from REANA!!
```

# Running the example

In this example we are using a simple Serial workflow engine to represent our sequential computational workflow steps.

## Deploying Locally 

If you are a researcher and would like to try out deploying a small REANA cluster on your laptop, you can proceed as follows:

1. Install `docker`, `kubectl`, `kind`, and `helm` dependencies
   
2. Deploy REANA cluster:
   
```bash
wget https://raw.githubusercontent.com/reanahub/reana/maint-0.9/etc/kind-localhost-30443.yaml 
kind create cluster --config kind-localhost-30443.yaml
wget https://raw.githubusercontent.com/reanahub/reana/maint-0.9/scripts/prefetch-images.sh 
sh prefetch-images.sh 
helm repo add reanahub https://reanahub.github.io/reana
helm repo update 
helm install reana reanahub/reana --namespace reana --create-namespace --wait
```
   
3. Create REANA admin user:

```bash
wget https://raw.githubusercontent.com/reanahub/reana/maint-0.9/scripts/create-admin-user.sh sh create-admin-user.sh
reana reana john.doe@example.org mysecretpassword
```

4. Log into your REANA instance: [https://localhost:30443](https://localhost:30443)

## Create new virtual environment

```shell
virtualenv ~/.virtualenvs/reana
source ~/.virtualenvs/reana/bin/activate
```

## Install REANA client

```shell
pip3 install reana-client
```

## Connect to some REANA cloud instance

Navigate to your [profile](https://localhost:30443/profile) and run:

```shell
export REANA_SERVER_URL=https://reana.cern.ch/
export REANA_ACCESS_TOKEN=XXXXXXX
```

These commands set two environment variables: `REANA_SERVER_URL` and `REANA_ACCESS_TOKEN`.

-   `REANA_SERVER_URL` is being set to the URL of the REANA server, which is [https://reana.cern.ch/](https://reana.cern.ch/) in this case.
-   `REANA_ACCESS_TOKEN` is being set to a token that provides authorization to access the REANA server. The value `XXXXXXX` is a placeholder and should be replaced with the actual access token.

Setting these environment variables will allow you to use the REANA client to interact with the REANA server, such as submitting and managing workflow jobs.

# Create new workflow

When running a workflow, you will have to start from here.

### Create new workflow called "HelloWorld"

```shell
reana-client create -n PFCands_analysis
```

Expected output:

```python
==> Verifying REANA specification file... /Users/alextintin/Cernbox/DPOA/cat-hackathon(local)/workflows/REANA/PFCands_plotting/reana.yaml
  -> SUCCESS: Valid REANA specification file.
==> Verifying REANA specification parameters...
  -> SUCCESS: REANA specification parameters appear valid.
==> Verifying workflow parameters and commands...
  -> SUCCESS: Workflow parameters and commands appear valid.
==> Verifying dangerous workflow operations...
  -> SUCCESS: Workflow operations appear valid.
==> Verifying compute backends in REANA specification file...
  -> SUCCESS: Workflow compute backends appear to be valid.
PFCands_analysis.1
==> SUCCESS: File /reana.yaml was successfully uploaded.
```

### Save workflow name we are currently working on

```shell
export REANA_WORKON=PFCands_analysis
```

### Upload code and inputs to remote workspace

```shell
reana-client upload
```

Expected output:

```python
==> SUCCESS: File /data/coffea_plot.py was successfully uploaded.
==> SUCCESS: File /data/rdf_plot.py was successfully uploaded.
==> SUCCESS: File /data/doubleeg_nanoaod_eg.root was successfully uploaded.
```

### Start the workflow

```shell
reana-client start
```

Expected output:

```python
==> SUCCESS: PFCands_analysis has been queued
```

### Check its status

```shell
reana-client status
```

Expected outputs:

```python
NAME               RUN_NUMBER   CREATED               STATUS
PFCands_analysis   1            2023-04-21T19:22:04   pending
```

... wait a minute or so for workflow to finish

```python
NAME               RUN_NUMBER   CREATED               STARTED               ENDED                 STATUS     PROGRESS
PFCands_analysis   1            2023-04-21T19:22:04   2023-04-21T19:22:41   2023-04-21T19:24:50   finished   9/9
```

### List workspace files

```shell
reana-client ls
```
 
 Expected output:

```python
NAME                     SIZE   LAST-MODIFIED
reana.yaml               1117   2023-04-21T01:35:26
code/script1.sh          38     2023-04-21T01:36:10
code/script2.sh          174    2023-04-21T01:36:10
data/input.txt           11     2023-04-21T01:36:10
results/outputfile.txt   32     2023-04-21T01:37:16
```

### Download output results

```shell
reana-client download
```

The output files that were specified in the yaml configuration file will be downloaded, in this case, our `results/outputfile.txt`.  You will downloaded a `results` directory with the following content:

```python
../PFCands_plotting
├── LICENSE
├── README.md
├── README.rst
├── code
├── data
│   ├── coffea_plot.py
│   ├── doubleeg_nanoaod_eg.root
│   └── rdf_plot.py
├── reana.yaml
└── results
    ├── coffea_output
    │   ├── PF_n.png
    │   ├── PF_n.txt
    │   └── PF_pt.png
    └── rdf_output
        ├── PFCands_pt.png
        └── nPFCands.png

6 directories, 12 files
```

You will have created a series of plots:

![[Pasted image 20230421143107.png]]

Plus a text file in `results/coffea_output` called `PF_n.txt` with the following content:

```output
[826, 747, 1255, 1116, 741, 930, 1368, 1462, 906, 1071]
```

### Check its output logs

```shell
reana-client logs
```

In the expected output you will get:
- Workflow engine logs
- Job logs

### Delete

```shell
reana-client delete -w PFCands_analysis.1 --include-all-runs
```

```output
==> SUCCESS: All workflows named 'HelloWorld' have been deleted.
```

### More...

If you will to know more commands, you can check out the [reana-client CLI API documentation](https://docs.reana.io/reference/reana-client-cli-api/).

### Fast test

To rapidly test your workflow you can copy and run:

```shell
reana-client create -n PFCands_analysis
reana-client upload
reana-client start
```

```shell
reana-client delete -w PFCands_analysis.1 --include-all-runs
```