# coding: utf-8

"""
Base tasks.
"""

import os

import law

# load contrib packages
law.contrib.load("docker")


class Task(law.SandboxTask):

    def local_path(self, *path):
        # DPOA_STORE_DIR is defined in setup.sh
        parts = ("$DPOA_STORE_DIR", self.task_family) + path
        return os.path.join(*(str(p) for p in parts))

    def local_target(self, *path, **kwargs):
        return law.LocalFileTarget(self.local_path(*path), **kwargs)
