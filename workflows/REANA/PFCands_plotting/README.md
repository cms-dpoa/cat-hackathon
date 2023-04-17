# About

This [REANA](http://www.reana.io/ "http://www.reana.io/") reproducible analysis example emulates a typical particle physics analysis where the signal and background data is processed and fitted against a model. The example will use the [RooFit](https://root.cern.ch/roofit "https://root.cern.ch/roofit") package of the [ROOT](https://root.cern.ch/ "https://root.cern.ch/") framework.

# Analysis structure

Making a research data analysis reproducible basically means to provide "runnable recipes" addressing (1) where is the input data, (2) what software was used to analyse the data, (3) which computing environments were used to run the software and (4) which computational workflow steps were taken to run the analysis. This will permit to instantiate the analysis on the computational cloud and run the analysis to obtain (5) output results.

## 1. Input data

In this example, the signal and background data will be generated; see below. Therefore there is no explicit input file to be taken care of.

## 2. Analysis code

The analysis will consist of two stages. In the first stage, signal and background are generated. In the second stage, a fit will be made for the signal and background.

For the first generation stage, [gendata.C](https://file+.vscode-resource.vscode-cdn.net/Users/alextintin/Cernbox/CAT%20Hackathon/cat-hackathon/workflows/REANA/reana-demo-root6-roofit/code/gendata.C "code/gendata.C") is a ROOT macro that generates signal and background data.

For the second fitting stage, [fitdata.C](https://file+.vscode-resource.vscode-cdn.net/Users/alextintin/Cernbox/CAT%20Hackathon/cat-hackathon/workflows/REANA/reana-demo-root6-roofit/code/fitdata.C "code/fitdata.C") is a ROOT macro that makes a fit for the signal and the background data.

The code was taken from the RooFit tutorial [rf502_wspacewrite.C](https://root.cern/doc/master/rf502__wspacewrite_8C.html "https://root.cern/doc/master/rf502__wspacewrite_8C.html") and was slightly modified.

## 3. Compute environment

In order to be able to rerun the analysis even several years in the future, we need to "encapsulate the current compute environment", for example to freeze the ROOT version our analysis is using. We shall achieve this by preparing a [Docker](https://www.docker.com/ "https://www.docker.com/") container image for our analysis steps.

This analysis example is runs within the [ROOT6](https://root.cern.ch/ "https://root.cern.ch/") analysis framework. The computing environment can be therefore easily encapsulated by using the upstream [reana-env-root6](https://github.com/reanahub/reana-env-root6 "https://github.com/reanahub/reana-env-root6") base image. (See there how it was created.)

We shall use the ROOT version 6.18.04. Note that we can actually use this container image "as is", because our two macros gendata.C and fitdata.C can be "uploaded" and "mounted" into the running container at runtime. There is no need to compile any of the analysis source code beforehand. We can therefore use the ROOT 6.18.04 base image directly, without building a new container image specially dedicated to our analysis. The ROOT 6.18.04 base image fully specifies the complete analysis environment that we need for our analysis.

## 4. Analysis workflow

The analysis workflow is simple and consists of two above-mentioned stages:

           START
            |
            |
            V
+-------------------------+
		|    hello world    |
+-------------------------+
            |
            | outputfile.txt
            V
           STOP


## 5. Output results

The example produces a plot where the signal and background data is fitted against the model:

In this example we are using a simple Serial workflow engine to represent our sequential computational workflow steps. Note that we can also use the CWL workflow specification (see [reana-cwl.yaml](https://file+.vscode-resource.vscode-cdn.net/Users/alextintin/Cernbox/CAT%20Hackathon/cat-hackathon/workflows/REANA/reana-demo-root6-roofit/reana-cwl.yaml "reana-cwl.yaml")), the Yadage workflow specification (see [reana-yadage.yaml](https://file+.vscode-resource.vscode-cdn.net/Users/alextintin/Cernbox/CAT%20Hackathon/cat-hackathon/workflows/REANA/reana-demo-root6-roofit/reana-yadage.yaml "reana-yadage.yaml")) or the Snakemake workflow specification (see [reana-snakemake.yaml](https://file+.vscode-resource.vscode-cdn.net/Users/alextintin/Cernbox/CAT%20Hackathon/cat-hackathon/workflows/REANA/reana-demo-root6-roofit/reana-snakemake.yaml "reana-snakemake.yaml")).

We can now install the REANA command-line client, run the analysis and download the resulting plots:

create new virtual environment

```shell
virtualenv ~/.virtualenvs/reana
source ~/.virtualenvs/reana/bin/activate
```

install REANA client

```shell
pip3 install reana-client
```

connect to some REANA cloud instance

```shell
export REANA_SERVER_URL=https://reana.cern.ch/
export REANA_ACCESS_TOKEN=XXXXXXX
```

create new workflow

```shell
reana-client create -n myanalysis
export REANA_WORKON=myanalysis
```

```output
export REANA_WORKON=myanalysis
==> Verifying REANA specification file... /Users/alextintin/Cernbox/CAT Hackathon/cat-hackathon/workflows/REANA/PFCands_plotting/reana.yaml
  -> SUCCESS: Valid REANA specification file.
==> Verifying REANA specification parameters...
  -> SUCCESS: REANA specification parameters appear valid.
==> Verifying workflow parameters and commands...
  -> SUCCESS: Workflow parameters and commands appear valid.
==> Verifying dangerous workflow operations...
  -> SUCCESS: Workflow operations appear valid.
==> Verifying compute backends in REANA specification file...
  -> SUCCESS: Workflow compute backends appear to be valid.
myanalysis.19
==> SUCCESS: File /reana.yaml was successfully uploaded.
```

upload input code, data and workflow to the workspace

```shell
reana-client upload
```

```output
==> SUCCESS: File /data/names.txt was successfully uploaded.
```

start computational workflow

```shell
reana-client start
```

```output
==> SUCCESS: myanalysis is pending
```

check status

```shell
reana-client status
```

```output
NAME         RUN_NUMBER   CREATED               STATUS
myanalysis   19           2023-04-17T04:37:57   pending
```

```output
NAME         RUN_NUMBER   CREATED               STARTED               ENDED                 STATUS     PROGRESS
myanalysis   19           2023-04-17T04:37:57   2023-04-17T04:38:20   2023-04-17T04:38:30   finished   1/1
```

list workspace files

```shell
reana-client ls
```

```output
NAME             SIZE   LAST-MODIFIED
outputfile.txt   14     2023-04-17T04:38:22
reana.yaml       292    2023-04-17T04:37:57
data/names.txt   5      2023-04-17T04:38:02
```

download output results

```shell
reana-client download
```

```output
==> SUCCESS: File outputfile.txt downloaded to /Users/alextintin/Cernbox/CAT Hackathon/cat-hackathon/workflows/REANA/PFCands_plotting.
```
