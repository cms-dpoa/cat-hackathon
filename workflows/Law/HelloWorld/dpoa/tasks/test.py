"""
Simple test tasks.
"""

import law
from dpoa.tasks.base import Task


class First(Task):
    # Define the Docker image to be used for the task
    # Docker must be running locally
    # Using `riga/py-sci` image from docker (Must be installed locally)
    sandbox = "docker::riga/py-sci"

    # Define the output for the task
    # Can be a file or folder (this case a file)
    def output(self):
        return self.local_target("some_fake_file.txt")

    # Define the logic for running the task
    def run(self):
        # Get the output target
        output = self.output()
        # Create the parent directory of the output target if it doesn't exist
        output.parent.touch()

        # Define the shell command to be executed
        cmd = f"echo 'Hello!' >> some_fake_file.txt;"\
            "echo 'World!' >> some_fake_file.txt;"
        
        # Execute the shell command in the output directory
        p, _, _ = law.util.interruptable_popen(
            cmd,
            shell=True,
            executable="/bin/bash",
            cwd=output.parent.path,
        )

        # Raise an exception if the command failed
        if p != 0:
            raise Exception("command failed")

class Final(Task):
    # Define the Docker image to be used for the task
    # Docker must be running locally
    # Using `riga/py-sci` image from docker (Must be installed locally)
    sandbox = "docker::riga/py-sci"

    # Define the dependencies for the task
    def requires(self):
        return First.req(self)

    # Define the output for the task (this case a directory)
    def output(self):
        return self.local_target("directory")

    # Define the logic for running the task
    def run(self):
        output = self.output()
        output.parent.touch()

        # Define the shell command to be executed
        cmd = f"mkdir directory;"\
            "cp ../First/some_fake_file.txt directory/;"
        
        # Execute the shell command in the output directory
        p, _, _ = law.util.interruptable_popen(
            cmd,
            shell=True,
            executable="/bin/bash",
            cwd=output.parent.path,
        )
        
        # Raise an exception if the command failed
        if p != 0:
            raise Exception("command failed")
