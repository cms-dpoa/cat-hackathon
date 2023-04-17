#!/usr/bin/env cwl-runner

# Note that if you are working on the analysis development locally, i.e. outside
# of the REANA platform, you can proceed as follows:
#   $ mkdir cwl-local-run
#   $ cd cwl-local-run
#   $ cp ../code/* ../data/* ../workflow/cwl/helloworld-job.yml .
#   $ cwltool --quiet --outdir="../outputs"
#           ../workflow/cwl/helloworld.cwl helloworld-job.yml
#   $ cat results/greetings.txt
#   Hello Jane Doe!
#   Hello Joe Bloggs!


cwlVersion: v1.0
class: Workflow

inputs:
  helloworld: File
  inputfile: File
  sleeptime: int
  outputfile:
    type: string
    default: results/greetings.txt

outputs:
  result:
    type: File
    outputSource: first/result

steps:
  first:
    hints:
      reana:
        compute_backend: slurmcern
    run: helloworld.tool
    in:
      helloworld: helloworld

      inputfile: inputfile
      sleeptime: sleeptime
      outputfile: outputfile
    out: [result]

$namespaces:
  reana: http://reana.io
