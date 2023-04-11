# DPOA Example

## Setup

To setup the repository, call

```bash
source setup.sh
```

When executed for the first time, this will create a minimal virtual environment with law and its dependencies.


## Start tasks

Currently, there are only two dummy tasks that do nothing but to create empty output files.
However, the tasks already depend on each other and declare custom docker images as so-called *sandboxes* in which they should be executed.
To trigger the *second* task, run

```bash
law run CreatePlots
```
