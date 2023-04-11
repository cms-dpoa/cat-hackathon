"""
Simple test tasks.
"""

import law
from dpoa.tasks.base import Task

class NanoProducer(Task):
    sandbox = "docker::rootproject/root:latest"

    def output(self):
        return self.local_target("some_fake_file.root")

    def run(self):
        self.output().touch()

class CreatePlots(Task):
    sandbox = "docker::riga/py-sci"

    def requires(self):
        return NanoProducer.req(self)

    def output(self):
        return self.local_target("some_nice_plot.png")

    @law.decorator.safe_output
    def run(self):
        # create the output directory
        output = self.output()
        output.parent.touch()

        fake_img_url = "https://raw.githubusercontent.com/garrettj403/SciencePlots/master/examples/figures/fig1.jpg"  # noqa
        cmd = f"wget -q -O {output.basename} {fake_img_url}"
        p, _, _ = law.util.interruptable_popen(
            cmd,
            shell=True,
            executable="/bin/bash",
            cwd=output.parent.path,
        )
        if p != 0:
            raise Exception("fake image download failed")