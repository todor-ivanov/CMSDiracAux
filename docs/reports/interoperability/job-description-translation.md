# Job Description Translation

## Purpose of this section

The final stage of the workflow translation process is the generation of **executable job descriptions** that can be submitted to the DIRAC workload management system.

While the Translation IR provides a system-independent representation of the workflow semantics, DIRAC jobs must ultimately be expressed using the **DIRAC job execution model**.

This model relies on two key components:

```
JDL job description
+
jobDescription.xml workflow definition
```

This section describes how the Translation IR is transformed into these structures.

---

# DIRAC Job Execution Model

In DIRAC, a job is executed through a generic runtime wrapper.

The job definition submitted to the system typically contains:

```
Executable
Arguments
InputSandbox
OutputSandbox
Job parameters
```

In most cases the executable is the DIRAC runtime entry point:

```
dirac-jobexec
```

The job execution flow is shown below.

```
DIRAC job submission
        │
        ▼
Worker node execution
        │
        ▼
dirac-jobexec
        │
        ▼
jobDescription.xml interpretation
        │
        ▼
Workflow step execution
```

The actual workflow logic is therefore contained inside the **XML workflow description** rather than in the JDL itself.

---

# JDL Job Definition

DIRAC jobs are submitted using a **Job Description Language (JDL)** file.

A simplified JDL example is shown below.

```
Executable = "dirac-jobexec";
Arguments = "jobDescription.xml -o LogLevel=INFO";

InputSandbox =
{
    jobDescription.xml
};

StdOutput = "std.out";
StdError  = "std.err";
```

This JDL defines the runtime environment in which the workflow described in the XML file will execute.

---

# Role of jobDescription.xml

The `jobDescription.xml` file defines the **workflow steps executed by the job**.

The structure typically includes:

```
Workflow
  ├── StepDefinition
  │
  ├── ModuleDefinition
  │
  └── StepInstance
```

Each step corresponds to a specific operation executed during the job runtime.

For example, a simple job may execute a script step defined as:

```
Script module
```

In more complex workflows, multiple steps may be chained together.

---

# Job Description Translation Pipeline

The CMSDiracAux translation process converts the Translation IR into the DIRAC job structures shown above.

The pipeline can be summarized as:

```
Translation IR
        │
        ▼
Task runtime definition
        │
        ▼
DIRAC workflow steps
        │
        ▼
jobDescription.xml
        │
        ▼
JDL job definition
```

This translation stage produces the executable job description required by the DIRAC runtime.

---

# Mapping Translation IR to DIRAC Job Structures

The mapping between Translation IR entities and DIRAC job components is summarized below.

| Translation IR      | DIRAC Representation                |
| ------------------- | ----------------------------------- |
| Workflow            | Production                          |
| Task                | Transformation                      |
| RuntimeDefinition   | Workflow step                       |
| SplittingPolicy     | Transformation plugin configuration |
| DataReference.files | Input data list                     |
| JobTemplate         | JDL + jobDescription.xml            |

This mapping ensures that the semantic information captured in the Translation IR is preserved during execution.

---

# Runtime Entry Point

During execution, the worker node runs the following command:

```
dirac-jobexec jobDescription.xml
```

The `dirac-jobexec` program performs the following tasks:

1. Initializes the DIRAC runtime environment
2. Parses the `jobDescription.xml` file
3. Executes the defined workflow steps
4. Collects job output and logs

This architecture separates **workflow execution logic** from the **job submission description**.

---

# Runtime Environment Considerations

One important difference between CMS and DIRAC execution models concerns **runtime environment distribution**.

In CMS workflows:

```
runtime environment distributed with job sandbox
```

In DIRAC:

```
runtime environment provided via CVMFS
```

This difference requires the translation layer to ensure that the required runtime environment is available to the job at execution time.

In practice, this may involve:

```
pre-installed experiment software
container execution environments
runtime bootstrap scripts
```

---

# Interaction with Job Splitting

Once datasets have been resolved into file lists, the job translation stage can construct job definitions according to the splitting policy defined in the Translation IR.

The process becomes:

```
file list
        │
        ▼
splitting policy
        │
        ▼
job templates
        │
        ▼
jobDescription.xml generation
        │
        ▼
JDL submission
```

Each generated job therefore corresponds to a specific subset of input files.

---

# Role in the CMSDiracAux Architecture

Job description translation represents the **final stage before execution** in the CMSDiracAux architecture.

```
WMCore workflow
        │
        ▼
dataset resolution
        │
        ▼
Translation IR
        │
        ▼
DIRAC job translation
        │
        ▼
DIRAC execution
```

This stage converts the abstract workflow representation into concrete executable jobs.

---

# Limitations of the Prototype

The CMSDiracAux prototype implements a simplified job translation process.

Several aspects of full CMS workflows are not yet fully represented.

These include:

```
complex runtime configuration
multi-step task chains
advanced job dependency management
```

However, the prototype demonstrates that the Translation IR contains sufficient information to construct valid DIRAC job descriptions.

---

# Importance for Workflow Interoperability

The job description translation stage demonstrates that workflows defined in the CMS workflow management system can be transformed into executable jobs for the DIRAC runtime.

This stage therefore represents the **final step in the deterministic translation pipeline** implemented by the CMSDiracAux project.

```
WMCore workflow
        ↓
Translation IR
        ↓
DIRAC job execution
```

The success of this stage confirms that the Translation IR provides a sufficiently expressive representation of workflow semantics to enable interoperability between the two systems.
