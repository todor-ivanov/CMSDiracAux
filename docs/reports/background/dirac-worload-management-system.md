# DIRAC Workload Management System

## Purpose of this section

The **DIRAC Workload Management System (WMS)** is responsible for scheduling and executing computational workloads across distributed computing resources.

The DIRAC WMS implements a **pilot-job based scheduling model**, where resources are acquired first and the actual workload is assigned later. This approach improves reliability and efficiency when operating on heterogeneous and unreliable distributed resources such as grid infrastructures. ([dirac.diracgrid.org][1])

Understanding the WMS architecture is essential for analyzing how workflows defined outside DIRAC (such as CMS workflows) can be executed within a DIRAC-based infrastructure.

---

# Role of the Workload Management System

Within the DIRAC architecture, the Workload Management System orchestrates the lifecycle of distributed jobs.

Conceptually the system sits between the user workflow layer and the computing infrastructure.

```text
┌──────────────────────────────┐
│     Workflow / Applications  │
│   (user or production jobs)  │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│   DIRAC Workload Management  │
│        System (WMS)          │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│ Distributed Computing Sites  │
│  (Grid / HPC / Cloud / HTC)  │
└──────────────────────────────┘
```

The WMS coordinates job submission, scheduling, monitoring, and execution across multiple computing environments.

---

# Core Scheduling Paradigm: Pilot Jobs

A defining feature of DIRAC WMS is the **pilot job model**.

Instead of directly submitting user jobs to computing sites, the system first deploys pilot jobs that reserve resources. The actual workload is then matched to these resources dynamically. ([ResearchGate][2])

```text
┌──────────────────────────┐
│  User Job Submitted      │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│  Job stored in WMS DB    │
│  (JDL description)       │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│  Pilot Job sent to site  │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Pilot starts on worker   │
│ node and contacts WMS    │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Matching user job        │
│ retrieved from queue     │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│  Payload job executed    │
└──────────────────────────┘
```

This model implements a **pull scheduling mechanism**, where compute resources pull workloads when they are ready to execute them.

---

# Job Lifecycle in DIRAC WMS

The typical lifecycle of a workload in the DIRAC WMS includes several stages.

```text
┌─────────────────────────────┐
│  Workload Preparation       │
│  (JDL + input sandbox)      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Job Submission to WMS      │
│  stored in JobDB            │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Task Queue Placement       │
│  (jobs grouped by reqs)     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Pilot Job Requests Workload │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Payload Execution on node   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Output and monitoring       │
└─────────────────────────────┘
```

This lifecycle ensures that jobs are scheduled only when suitable resources are available.

---

# Internal Architecture of the WMS

The WMS is implemented as a distributed system composed of several cooperating components.

```text
┌────────────────────────────────────┐
│        DIRAC WMS Architecture      │
├────────────────────────────────────┤
│ Services                           │
│  - Job Manager                     │
│  - Matcher Service                 │
│                                    │
│ Databases                          │
│  - JobDB                           │
│  - JobLoggingDB                    │
│  - TaskQueueDB                     │
│  - PilotAgentsDB                   │
│                                    │
│ Agents                             │
│  - Pilot Directors                 │
│  - Job Agents                      │
└────────────────────────────────────┘
```

DIRAC systems typically include several component types:

* **Services** that respond to requests and provide system functionality
* **Agents** that perform background tasks
* **Databases** storing job state and metadata ([dirac.diracgrid.org][3])

---

# Task Queues

A central concept in the WMS scheduling mechanism is the **task queue**.

Jobs with similar requirements are grouped together, allowing efficient matching between jobs and available resources.

```text
┌─────────────────────┐
│ Pending Jobs        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Task Queue Builder  │
│ groups jobs by      │
│ resource needs      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Task Queues         │
│  Queue A (CPU type) │
│  Queue B (GPU type) │
│  Queue C (memory)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Pilot matches queue │
│ with worker node    │
└─────────────────────┘
```

This mechanism enables efficient scheduling across heterogeneous infrastructures.

---

# Resource Integration

The DIRAC WMS can integrate multiple resource types.

```text
┌───────────────────────────┐
│        DIRAC WMS          │
└─────────────┬─────────────┘
              │
     ┌────────┼────────┐
     ▼        ▼        ▼
┌────────┐ ┌────────┐ ┌────────┐
│ Grid   │ │ Cloud  │ │ HPC    │
│ sites  │ │ sites  │ │ sites  │
└────────┘ └────────┘ └────────┘
```

This abstraction allows the same workflow to run across different computing environments.

---

# Monitoring and Bookkeeping

The WMS maintains detailed information about job execution.

Important data stored by the system include:

* job definitions
* job states
* execution logs
* resource usage

Key databases include:

```text
JobDB
JobLoggingDB
TaskQueueDB
PilotAgentsDB
```

These databases maintain the persistent state of the system. ([dirac.diracgrid.org][3])

---

# Comparison with CMS Workflow Scheduling

The DIRAC Workload Management System differs significantly from the CMS workflow management approach.

| Property         | CMS WMCore              | DIRAC WMS          |
| ---------------- | ----------------------- | ------------------ |
| Job generation   | predefined by splitting | dynamic via pilots |
| Scheduling       | push model              | pull model         |
| Data abstraction | dataset / run / lumi    | file-oriented      |
| Bookkeeping      | WMBS                    | WMS task queues    |

The **pilot-based pull scheduling model** used in DIRAC allows resources to request jobs dynamically rather than being assigned workloads in advance.

---

# Implications for CMSDiracAux

The CMSDiracAux project aims to translate CMS workflows into structures compatible with DIRAC execution.

Conceptually:

```text
┌──────────────────────┐
│ CMS Workflow (WMCore)│
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Translation IR       │
│ workflow abstraction │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ DIRAC WMS execution  │
│ via pilots and queues│
└──────────────────────┘
```

The Translation IR bridges the difference between the **data-driven CMS workflow model** and the **resource-driven DIRAC scheduling model**.

---

# Summary

The DIRAC Workload Management System provides a scalable infrastructure for scheduling distributed workloads using a pilot-job based architecture.

Its design emphasizes:

* late binding of jobs to resources
* dynamic job scheduling
* efficient use of heterogeneous infrastructures

However, its **file-oriented workload model** differs from the **fine-grained data-driven workflow structure of CMS**, which motivates the need for an intermediate translation layer in the CMSDiracAux architecture.

[1]: https://dirac.diracgrid.org/en/latest/AdministratorGuide/Systems/WorkloadManagement/?utm_source=chatgpt.com "10. Workload Management System (WMS)"
[2]: https://www.researchgate.net/publication/231046041_DIRAC_pilot_framework_and_the_DIRAC_workload_management_system?utm_source=chatgpt.com "(PDF) DIRAC pilot framework and the DIRAC workload ..."
[3]: https://dirac.diracgrid.org/en/latest/AdministratorGuide/Systems/WorkloadManagement/architecture.html?utm_source=chatgpt.com "10.2.1. Workload Management System architecture"
