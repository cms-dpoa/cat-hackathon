
# DPOA Example

This example demonstrates the concept of [workflows](http://law.readthedocs.io/en/latest/workflows.html) and data flow

Resources: [luigi](http://luigi.readthedocs.io/en/stable), [law](http://law.readthedocs.io/en/latest)

There are multiple ways to setup and run this example:

In this example we will run this locally:

```
source setup.sh
``` 

Requirements:
- Have luigi installed : `pip3 install luigi`
- Have law installed: `pip3 install law`
- Have docker installed locally
- Have the desired images installed locally `docker image pull riga/py-sci:latest`

#### 1. Let law index your the tasks and their parameters (for autocompletion)

```shell
law index --verbose
```

You should see:

```shell
indexing tasks in 1 module(s)
loading module 'dpoa.tasks', done

module 'dpoa.tasks.test', 2 task(s):
    - First
    - Final

written 2 task(s) to index file '/Users/alextintin/Cernbox/DPOA/cat-hackathon/workflows/Law/HelloWorld/.law/index'
```

You will see both tasks that are created in our `/HelloWorld/dpoa/tasks/test.py

It's important to keep in mind that you have the flexibility to run any task you want, however, it's also important to note that when running a specific task, only that task and its dependent tasks will be executed. 

So, while you have the option to run any task independently, you should be aware that its dependencies will not be executed unless you **explicitly** specify them in the python file.

#### 2. Check the status of the Final task

```shell
law run Final --print-status -1
```

No tasks ran so far, so no output target should exist yet. You will get this output:

```shell
print task status with max_depth -1 and target_depth 0

0 > Final()
│     LocalFileTarget(fs=local_fs, path=$DPOA_STORE_DIR/Final/directory)
│       absent
│
└──1 > First()
         LocalFileTarget(fs=local_fs, path=$DPOA_STORE_DIR/First/some_fake_file.txt)
           absent
```

Notice that the `Final` task depends on the First `task`, this was defined in the python file as so:

```python
class Final(Task):
sandbox = "docker::riga/py-sci"
	
	def requires(self):
		return First.req(self) # <- here
```

It is possible to declare various dependencies as so:

```python
class Final(Task):
sandbox = "docker::riga/py-sci"
	
	def requires(self):
		return [First.req(self), otherDependency.req(self)] # <- here
```


#### 3. Run the Final task

```shell
law run Final
```

This should take only a few seconds to process.

#### 3. Check the status again

```shell
law run Final --print-status 1
```

When step 2 succeeded, all output targets should exist:

```shell
print task status with max_depth 1 and target_depth 0

0 > Final()
│     LocalFileTarget(fs=local_fs, path=$DPOA_STORE_DIR/Final/directory)
│       existent
│
└──1 > First()
         LocalFileTarget(fs=local_fs, path=$DPOA_STORE_DIR/First/some_fake_file.txt)
           existent
```

To see the status of the targets in the collection, i.e., the grouped outputs of the branch tasks, set the target depth via `--print-status 1,1`.

#### 4. Look at the results

```shell
cd data/store
ls
```

Given the declarations in our workflow, we have the following tree:

```python
store
├── Final
│   └── directory
│       └── some_fake_file.txt
└── First
    └── some_fake_file.txt

4 directories, 2 files
```

This workflow consists of two tasks: `First` and `Final`. The purpose of `First` task is to create a file called `some_fake_file.txt` and write "Hello!" and "World!" in it. The purpose of the `Final` task is to create a directory called `directory` and copy `some_fake_file.txt` into it.

#### 5. Cleanup the results

You can delete the results in levels of depth (the depth depends on the declarations of the dependencies).

These results can be defined as:

- Files (txt; py; root; etc)

```python
def output(self):
	return self.local_target("some_fake_file.txt")
```

- Directories

```python
def output(self):
	return self.local_target("directory")
```


## Example
Delete the outputs of our workflow in depth 0

Check the tasks of our workflow in depth 0:

```shell
law run Final --print-status 0
```

Expected output:

```output
print task status with max_depth 0 and target_depth 0

0 > Final()
      LocalFileTarget(fs=local_fs, path=$DPOA_STORE_DIR/Final/directory)
        existent
```

Our `Final` task exists here, for this task has no declared dependencies. 

Since the output is specified to be a directory, when deleting in depth 0, we will delete all the files contained in this directory. This is very convenient when working with various files and sub directories. Let's see for ourselves:

```shell 
law run Final --remove-output 0
```

```output
remove task output with max_depth 0
removal mode? [i*(interactive), d(dry), a(all)]
```

We select the option `a` and hit enter.

```
selected all mode

0 > Final()
      LocalFileTarget(fs=local_fs, path=$DPOA_STORE_DIR/Final/directory)
        removed
```

Let's check the tree:

```python
store
├── Final
└── First
    └── some_fake_file.txt

3 directories, 1 file
```

We successfully deleted all the files in our Final folder (depth 0), now we can delete files as pleased. 

To delete all the files created in a workflow, use the argument `-1` as such:

```shell
law run Final --remove-output -1
```

You have deleted all your workflow files sucessfully!

Expected output:

```output
remove task output with max_depth -1
removal mode? [i*(interactive), d(dry), a(all)] a
selected all mode

0 > Final()
│     LocalFileTarget(fs=local_fs, path=$DPOA_STORE_DIR/Final/directory)
│       removed
│
└──1 > First()
         LocalFileTarget(fs=local_fs, path=$DPOA_STORE_DIR/First/some_fake_file.txt)
           removed
```

Expected final tree:

```python
store
├── Final
└── First

3 directories, 0 files
```
