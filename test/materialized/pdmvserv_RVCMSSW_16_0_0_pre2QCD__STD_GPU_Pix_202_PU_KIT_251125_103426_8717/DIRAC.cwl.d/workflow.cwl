cwlVersion: v1.2
class: Workflow
inputs:
  task_name: string
  transformation_name: string
  storage_element: string
  lfns:
    type:
      type: array
      items: string
outputs:
  execution_log:
    type: File
    outputSource: run_task/execution_log
steps:
  run_task:
    run: tool.cwl
    in:
      task_name: task_name
      transformation_name: transformation_name
      storage_element: storage_element
      lfns: lfns
    out:
      - execution_log
