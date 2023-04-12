
# DPOA Example

## Setup

Resources: [luigi](http://luigi.readthedocs.io/en/stable), [law](http://law.readthedocs.io/en/latest)

To setup the repository, call:

```bash
source setup.sh
```

When executed for the first time, this will create a minimal virtual environment with law and its dependencies.

## Start tasks

Currently, there are only two dummy tasks that do nothing but to create empty output files.

However, the tasks already depend on each other and declare custom docker images as so-called *sandboxes* in which they should be executed.

#### 1. Let law index your the tasks and their parameters (for autocompletion)

```shell
law index --verbose
```

You should see:

```output
indexing tasks in 1 module(s)
loading module 'dpoa.tasks', done

module 'dpoa.tasks.test', 2 task(s):
    - NanoProducer
    - CreatePlots

written 2 task(s) to index file 
'/law-dpoa-example-main/.law/index'
```

#### 2. Check the status of the CreatePlots task

```shell
law run CreatePlots --print-status -1
```

No tasks ran so far, so no output target should exist yet. You will see this output:

```output
print task status with max_depth -1 and target_depth 0

0 > CreatePlots()
│     LocalFileTarget(fs=local_fs, path=$DPOA_STORE_DIR/CreatePlots/some_nice_plot.png)
│       absent
│
└──1 > NanoProducer()
         LocalFileTarget(fs=local_fs, path=$DPOA_STORE_DIR/NanoProducer/some_fake_file.root)
           absent
```

#### 3. Run the CreatePlots task

To trigger the *second* task, run:

```shell
law run CreatePlots
```

This should take only a few seconds to process.

```output
===== Luigi Execution Summary =====

Scheduled 2 tasks of which:
* 1 complete ones were encountered:
    - 1 NanoProducer(...)
* 1 ran successfully:
    - 1 CreatePlots(...)

This progress looks :) because there were no failed tasks or missing dependencies

===== Luigi Execution Summary =====

```

By default, this example uses a local scheduler, which - by definition - offers no visualization tools in the browser. If you want to see how the task tree is built and subsequently run ``luigid`` in a second terminal. This will start a central scheduler at [localhost:8082](localhost:8082) (the default address). To inform tasks (or rather *workers*) about the scheduler, either add ``--local-scheduler False`` to the ``law run`` command as such:

```shell
law run CreatePlots --local-scheduler False
```

or set the ``local-scheduler`` value in the ``[luigi_core]`` config section in the ``law.cfg`` file to ``False``.

The task tree should look like this in the scheduler app:

FIXME

#### 4. Check the status again

```shell
law run CreatePlots --print-status 1
```

When step 2 succeeded, all output targets should exist:

```output
print task status with max_depth 1 and target_depth 0

0 > CreatePlots()
│     LocalFileTarget(fs=local_fs, path=$DPOA_STORE_DIR/CreatePlots/some_nice_plot.png)
│       existent
│
└──1 > NanoProducer()
         LocalFileTarget(fs=local_fs, path=$DPOA_STORE_DIR/NanoProducer/some_fake_file.root)
           existent
```

To see the status of the targets in the collection, i.e., the grouped outputs of the branch tasks,
set the target depth via `--print-status 1,1`.

#### 5. Look at the results

```shell
cd data/store
```

You will have created the following tree in your directory:

```output
store
├── CreatePlots
│   └── some_nice_plot.png
└── NanoProducer
    └── some_fake_file.root

3 directories, 2 files
```

#### 6. Cleanup the results

```shell
law run CreatePlots --remove-output -1
```

You should see:

```shell
remove task output with max_depth -1
removal mode? [i*(interactive), d(dry), a(all)] a
selected all mode

0 > CreatePlots()
│     LocalFileTarget(fs=local_fs, path=$DPOA_STORE_DIR/CreatePlots/some_nice_plot.png)
│       removed
│
└──1 > NanoProducer()
         LocalFileTarget(fs=local_fs, path=$DPOA_STORE_DIR/NanoProducer/some_fake_file.root)
           removed
```