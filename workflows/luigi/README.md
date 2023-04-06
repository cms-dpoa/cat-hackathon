This example demonstrates the concept of [workflows](http://law.readthedocs.io/en/latest/workflows.html).

The actual payload of the tasks is rather trivial. The workflow consists of 26 tasks which convert an integer between 97 and 122 (ascii) into a character. A single task collects the results in the end and writes all characters into a text file.

[[Classes]]

Resources: [luigi](http://luigi.readthedocs.io/en/stable), [law](http://law.readthedocs.io/en/latest)

There are multiple ways to setup and run this example:

1. Docker: `docker run -ti riga/law:example loremipsum`
2. Local: `source setup.sh`


#### 1. Let law index your the tasks and their parameters (for autocompletion)

```shell
law index --verbose
```

You should see:

```shell

```

#### 2. Check the status of the CreateAlphabet task

```shell
law run UploadResults --print-status -1
```

No tasks ran so far, so no output target should exist yet. You will see this output:

```shell

```


#### 3. Run the CreateAlphabet task

```shell
law run UploadResults
```

This should take only a few seconds to process.

By default, this example uses a local scheduler, which - by definition - offers no visualization tools in the browser. If you want to see how the task tree is built and subsequently run, run ``luigid`` in a second terminal. This will start a central scheduler at *localhost:8082* (the default address). To inform tasks (or rather *workers*) about the scheduler, either add ``--local-scheduler False`` to the ``law run`` command, or set the ``local-scheduler`` value in the ``[luigi_core]`` config section in the ``law.cfg`` file to ``False``.

#### 3. Check the status again

```shell
law run UploadResults --print-status 1
```

When step 2 succeeded, all output targets should exist:

```shell

```

To see the status of the targets in the collection, i.e., the grouped outputs of the branch tasks,
set the target depth via `--print-status 1,1`.

#### 4. Look at the results

```shell
cd data
ls
```

#### 5. Cleanup the results

```shell
law run UploadResults --remove-output -1
```