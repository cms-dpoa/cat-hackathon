#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool

requirements:
  DockerRequirement:
    dockerPull:
      python:2.7-slim

baseCommand: python

inputs:
  helloworld:
    type: File
    inputBinding:
      position: 0
  inputfile:
    type: File
    inputBinding:
      prefix: --inputfile
  sleeptime:
    type: int
    inputBinding:
      prefix: --sleeptime
  outputfile:
    type: string
    inputBinding:
      prefix: --outputfile

outputs:
  result:
    type: File
    outputBinding:
      glob: $(inputs.outputfile)