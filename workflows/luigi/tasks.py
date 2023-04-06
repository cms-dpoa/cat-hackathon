import os
import time
import random
from collections import defaultdict

from six.moves import urllib
import luigi
import law
import subprocess

law.contrib.load("tasks")  # to have the RunOnceTask

class CreateDir(law.Task):
    def run(self):
        subprocess.run("mkdir -p mydata/coffea mydata/rdf", shell=True)


class DownloadCoffeaBaseImage(law.Task):
    def run(self):
        subprocess.run("docker pull coffeateam/coffea-base", shell=True)


class RunCoffeaBaseContainer(law.Task):
    def requires(self):
        return DownloadCoffeaBaseImage()

    def run(self):
        subprocess.run("docker run --rm -v $PWD:/code coffeateam/coffea-base bash -c 'cd code/analysis/coffea/ && python coffea_plot.py && mv *.png ../../mydata/coffea/ && mv PF_n.txt ../../mydata/coffea/ && ls'", shell=True)


class DownloadRootBaseImage(law.Task):
    def run(self):
        subprocess.run("docker pull rootproject/root", shell=True)


class RunRootBaseContainer(law.Task):
    def requires(self):
        return DownloadRootBaseImage()

    def run(self):
        subprocess.run(
            "docker run --rm -v $PWD:/code rootproject/root bash -c 'cd ../code/analysis/rdataframe/ && python rdf_plot.py && mv *.png ../../mydata/rdf/ && ls'", shell=True)


class DummyStep(law.Task):
    def run(self):
        print("This will be the PFNanoAOD production step in a CMSSW docker container")


class UploadResults(law.Task):
    def requires(self):
        return [RunCoffeaBaseContainer(), RunRootBaseContainer(), DummyStep()]

    def run(self):
        subprocess.run("tar -czvf analysis_results.tar.gz mydata", shell=True)

class Task(law.Task):
    """
    Base task that provides some convenience methods to create local file and directory targets at
    the default data path, as defined in the setup.sh.
    """

    slow = luigi.BoolParameter(description="before running, wait between 5 and 15 seconds")

    def store_parts(self):
        return (self.__class__.__name__,)

    def local_path(self, *path):
        # WORKFLOWEXAMPLE_DATA_PATH is defined in setup.sh
        parts = (os.getenv("WORKFLOWEXAMPLE_DATA_PATH"),) + self.store_parts() + path
        return os.path.join(*parts)

    def local_target(self, *path):
        return law.LocalFileTarget(self.local_path(*path))