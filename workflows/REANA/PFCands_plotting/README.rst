===============================
 REANA example - "hello world"
===============================

.. image:: https://github.com/reanahub/reana-demo-helloworld/workflows/CI/badge.svg
   :target: https://github.com/reanahub/reana-demo-helloworld/actions

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/reanahub/reana?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge

.. image:: https://img.shields.io/github/license/reanahub/reana-demo-helloworld.svg
   :target: https://github.com/reanahub/reana-demo-helloworld/blob/master/LICENSE

.. image:: https://www.reana.io/static/img/badges/launch-on-reana-at-cern.svg
   :target: https://reana.cern.ch/launch?url=https%3A%2F%2Fgithub.com%2Freanahub%2Freana-demo-helloworld&specification=reana.yaml&name=reana-demo-helloworld

About
=====

This repository provides a simple "hello world" application example for `REANA
<http://www.reanahub.io/>`_ reusable research data analysis plaftorm. The example
generates greetings for persons specified in an input file.

Analysis structure
==================

Making a research data analysis reproducible basically means to provide
"runnable recipes" addressing (1) where is the input data, (2) what software was
used to analyse the data, (3) which computing environments were used to run the
software and (4) which computational workflow steps were taken to run the
analysis. This will permit to instantiate the analysis on the computational
cloud and run the analysis to obtain (5) output results.

1. Input dataset
----------------

The input file is a text file containing person names:

.. code-block:: console

    $ cat data/names.txt
    Jane Doe
    Joe Bloggs

2. Analysis code
----------------

A simple "hello world" Python code for illustration:

- `helloworld.py <code/helloworld.py>`_

The program takes an input file with the names of the persons to greet and an
optional sleeptime period and produces an output file with the greetings:

.. code-block:: console

    $ python code/helloworld.py \
        --inputfile data/names.txt
        --outputfile results/greetings.txt
        --sleeptime 0
    $ cat results/greetings.txt
    Hello Jane Doe!
    Hello Joe Bloggs!

3. Compute environment
----------------------

In order to be able to rerun the analysis even several years in the future, we
need to "encapsulate the current compute environment", for example to freeze the
Jupyter notebook version and the notebook kernel that our analysis was using. We
shall achieve this by preparing a `Docker <https://www.docker.com/>`_ container
image for our analysis steps.

For example:

.. code-block:: console

    $ cat environments/python/Dockerfile
    FROM python:2.7-slim

Since we don't need any additional Python packages for this simple example to
work, we can directly rely on the ``python`` image from the Docker Hub. The
trailing ``:2.7-slim`` makes sure we are using the Python 2.7 slim image
version.

4. Analysis workflow
--------------------

This analysis is very simple because it consists basically of running only the
Python executable which will produce a text file.

The workflow can be represented as follows:

.. code-block:: console

                START
                |
                |
                V
    +-------------------------------+
    |                               | <-- inputfile=data/names.txt
    |    $ python helloworld.py ... | <-- sleeptime=0
    +-------------------------------+
                |
                | otuputfile=results/greetings.txt
                V
                STOP


Note that you can also use `CWL <http://www.commonwl.org/v1.0/>`_, `Yadage
<https://github.com/diana-hep/yadage>`_ or `Snakemake <https://snakemake.github.io>`_
workflow specifications:

- `Yadage workflow definition <workflow/yadage/workflow.yaml>`_
- `CWL workflow definition <workflow/cwl/helloworld.cwl>`_
- `Snakemake workflow definition <workflow/snakemake/Snakefile>`_

5. Output results
-----------------

The example produces a file greeting all names included in the
`names.txt <data/names.txt>`_ file.

.. code-block:: text

     Hello Jane Doe!
     Hello Joe Bloggs!

Running the above example on REANA
==================================

We are now ready to run this example and on the `REANA <http://www.reana.io/>`_ platform.

There are two ways to execute this analysis example on REANA.

If you would like to simply launch this analysis example on the REANA instance
at CERN and inspect its results using the web interface, please click on one of the following badges,
depending on which workflow system (CWL, Serial, Snakemake, Yadage) you would like to use:

.. raw:: html

   <a href="https://reana.cern.ch/launch?url=https%3A%2F%2Fgithub.com%2Freanahub%2Freana-demo-helloworld&specification=reana-cwl.yaml&name=reana-demo-helloworld-cwl">
     <img src="https://www.reana.io/static/img/badges/launch-with-cwl-on-reana-at-cern.svg" alt="Launch with CWL on REANA@CERN badge" />
   </a>
   <br />
   <a href="https://reana.cern.ch/launch?url=https%3A%2F%2Fgithub.com%2Freanahub%2Freana-demo-helloworld&specification=reana.yaml&name=reana-demo-helloworld-serial">
     <img src="https://www.reana.io/static/img/badges/launch-with-serial-on-reana-at-cern.svg" alt="Launch with Serial on REANA@CERN badge" />
   </a>
   <br />
   <a href="https://reana.cern.ch/launch?url=https%3A%2F%2Fgithub.com%2Freanahub%2Freana-demo-helloworld&specification=reana-snakemake.yaml&name=reana-demo-helloworld-snakemake">
     <img src="https://www.reana.io/static/img/badges/launch-with-snakemake-on-reana-at-cern.svg" alt="Launch with Snakemake on REANA@CERN badge"/>
   </a>
   <br />
   <a href="https://reana.cern.ch/launch?url=https%3A%2F%2Fgithub.com%2Freanahub%2Freana-demo-helloworld&specification=reana-yadage.yaml&name=reana-demo-helloworld-yadage">
     <img src="https://www.reana.io/static/img/badges/launch-with-yadage-on-reana-at-cern.svg" alt="Launch with Yadage on REANA@CERN badge"/>
   </a>

|

If you would like a step-by-step guide on how to use the REANA command-line
client to launch this analysis example, please read on.

Prepare files
-------------

First we need to create a `reana.yaml <reana.yaml>`_ file describing the
structure of our analysis with its inputs, the code, the runtime environment,
the computational workflow steps and the expected outputs:

.. code-block:: yaml

    version: 0.3.0
    inputs:
      files:
        - code/helloworld.py
        - data/names.txt
      parameters:
        helloworld: code/helloworld.py
        inputfile: data/names.txt
        outputfile: results/greetings.txt
        sleeptime: 0
    workflow:
      type: serial
      specification:
        steps:
          - environment: 'python:2.7-slim'
            commands:
              - python "${helloworld}"
                  --inputfile "${inputfile}"
                  --outputfile "${outputfile}"
                  --sleeptime ${sleeptime}
    outputs:
      files:
       - results/greetings.txt


In case you are using CWL, Yadage or Snakemake workflow specifications:

- `reana.yaml using CWL <reana-cwl.yaml>`_
- `reana.yaml using Yadage <reana-yadage.yaml>`_
- `reana.yaml using Snakemake <reana-snakemake.yaml>`_

Run the analysis
----------------

To use the command line client, follow the instructions below:

.. code-block:: console

    $ # create new virtual environment
    $ virtualenv ~/.virtualenvs/reana
    $ source ~/.virtualenvs/reana/bin/activate
    $ # install REANA client
    $ pip install reana-client
    $ # connect to some REANA cloud instance (e.g CERN instance)
    $ export REANA_SERVER_URL=https://reana.cern.ch/
    $ export REANA_ACCESS_TOKEN=XXXXXXX
    $ # create a new workflow
    $ reana-client create -n myanalysis
    $ export REANA_WORKON=myanalysis
    $ # upload input code, data and workflow to the workspace
    $ reana-client upload
    $ # start computational workflow
    $ reana-client start
    $ # should take about a minute
    $ reana-client status
    $ # list workspace files
    $ reana-client ls
    $ # download output results
    $ reana-client download results/greetings.txt

Please see the `REANA-Client <https://reana-client.readthedocs.io/>`_
documentation for more detailed explanation of typical ``reana-client`` usage
scenarios.

Contributors
============

The list of contributors in alphabetical order:

- `Anton Khodak <https://orcid.org/0000-0003-3263-4553>`_
- `Diego Rodriguez <https://orcid.org/0000-0003-0649-2002>`_
- `Dinos Kousidis <https://orcid.org/0000-0002-4914-4289>`_
- `Harri Hirvonsalo <https://orcid.org/0000-0002-5503-510X>`_
- `Jan Okraska <https://orcid.org/0000-0002-1416-3244>`_
- `Marco Vidal <https://orcid.org/0000-0002-9363-4971>`_
- `Tibor Simko <https://orcid.org/0000-0001-7202-5803>`_
