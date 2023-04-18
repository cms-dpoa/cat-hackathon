"""
Simple test tasks.
"""

import law
from dpoa.tasks.base import Task

class Repository(Task):
    sandbox = "docker::riga/py-sci"

    def output(self):
        return self.local_target("cat-hackathon")
    def run(self):
        output = self.output()
        output.parent.touch()

        # Download repository
        github = "https://github.com/cms-dpoa/cat-hackathon.git"
        cmd = f"git clone {github};"
        p, _, _ = law.util.interruptable_popen(
            cmd,
            shell=True,
            executable="/bin/bash",
            cwd=output.parent.path
        )
        if p != 0:
            raise Exception("command failed")

class CoffeaPlotting(Task):
    sandbox = "docker::coffeateam/coffea-base:latest"

    def requires(self):
        return Repository.req(self)
    def output(self):
        return self.local_target("coffea_output")
    def run(self):
        output = self.output()
        output.parent.touch()

        cmd = f"mkdir coffea_output;"\
            "cd ../Repository/cat-hackathon/analysis/coffea/;"\
            "python coffea_plot.py;"\
            "mv *.png ../../../../CoffeaPlotting/coffea_output;"\
            "mv PF_n.txt ../../../../CoffeaPlotting/coffea_output;"
        p, _, _ = law.util.interruptable_popen(
            cmd,
            shell=True,
            executable="/bin/bash",
            cwd=output.parent.path
        )
        if p != 0:
            raise Exception("command failed")

class RDFPlotting(Task):
    sandbox = "docker::rootproject/root:latest"

    def requires(self):
        return Repository.req(self)
    def output(self):
        return self.local_target("rdataframe_output")
    def run(self):
        output = self.output()
        output.parent.touch()

        cmd = f"mkdir rdataframe_output;"\
            "cd ../Repository/cat-hackathon/analysis/rdataframe/;"\
            "python rdf_plot.py;"\
            "mv *.png ../../../../RDFPlotting/rdataframe_output;"
        p, _, _ = law.util.interruptable_popen(
            cmd,
            shell=True,
            executable="/bin/bash",
            cwd=output.parent.path
        )
        if p != 0:
            raise Exception("command failed")

class Final(Task):
    sandbox = "docker::riga/py-sci"

    def requires(self):
        return [RDFPlotting.req(self), CoffeaPlotting.req(self)]
    def output(self):
        return self.local_target("some_fake_file.txt")
    def run(self):
        output = self.output()
        output.parent.touch()

        cmd = f"echo 'Hello!' > {output.basename};echo 'World!' >> {output.basename}"
        p, _, _ = law.util.interruptable_popen(
			cmd,
			shell=True,
			executable="/bin/bash",
			cwd=output.parent.path,
		)
        if p != 0:
            raise Exception("command failed")