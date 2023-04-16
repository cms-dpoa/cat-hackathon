cwlVersion: v1.0
class: CommandLineTool

requirements:
  DockerRequirement:
    dockerPull:
      reanahub/reana-env-root6:6.18.04
  InitialWorkDirRequirement:
    listing:
      - $(inputs.fitdata)
      - $(inputs.data)

inputs:
  fitdata: File
  data: File
  outfile:
    type: string
    default: plot.png

baseCommand: /bin/sh

arguments:
  - prefix: -c
    valueFrom: |
      root -b -q '$(inputs.fitdata.basename)("$(inputs.data.basename)","$(runtime.outdir)/$(inputs.outfile)")'

outputs:
  result:
    type: File
    outputBinding:
      glob: $(inputs.outfile)
