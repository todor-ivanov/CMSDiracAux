cwlVersion: v1.2
class: CommandLineTool
baseCommand:
  - bash
inputs:
  task_name:
    type: string
  transformation_name:
    type: string
  storage_element:
    type: string
  lfns:
    type:
      type: array
      items: string
outputs:
  execution_log:
    type: File
    outputBinding:
      glob: execution.log
arguments:
  - position: 1
    valueFrom: |
      set -e
      echo "Transformation: $(inputs.transformation_name)" > execution.log
      echo "Task: $(inputs.task_name)" >> execution.log
      echo "StorageElement: $(inputs.storage_element)" >> execution.log
      echo "LFNs:" >> execution.log
      for lfn in $(inputs.lfns); do
        echo "$lfn" >> execution.log
      done
      echo "Fetching CMSDiracAux runtime bundle" >> execution.log
      echo "Sourcing environment" >> execution_log
      echo "Running Startup.py" >> execution.log
stdout: execution.log
requirements:
  InlineJavascriptRequirement: {}
