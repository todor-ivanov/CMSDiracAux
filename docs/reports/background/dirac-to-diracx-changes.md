# Changes with DiracX

This is a **concise architectural explanation of what changes with DIRACX**, focusing on **how the workflow stack evolves** relative to the classic DIRAC architecture.

```
Production
Transformation
Workload Management
```

---

# 1. Core Idea of DIRACX

DIRACX is **not just a new version of DIRAC**.

It is a **re-architecture of the control plane** intended to:

* modernize the system
* simplify deployment
* support cloud-native infrastructures
* decouple services

The main architectural shift is:

```
monolithic service cluster
          ↓
microservice-based control plane
```

---

# 2. Structural Change in the System

## Classic DIRAC

In classic DIRAC:

```
central services
        │
        ▼
Transformation / Production
        │
        ▼
WMS
        │
        ▼
pilot infrastructure
```

Many services share:

* configuration
* databases
* service runtime

---

## DIRACX

DIRACX reorganizes the architecture into **independent service layers**.

Conceptually:

```text
┌────────────────────────────────────────────┐
│              DIRACX API Layer              │
│        REST / service orchestration        │
└───────────────┬────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────┐
│        Workflow / Transformation APIs      │
│     workflow definitions and execution     │
└───────────────┬────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────┐
│       Workload Scheduling Services         │
│      job queues / resource matchmaking     │
└───────────────┬────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────┐
│       Pilot Execution Infrastructure       │
└────────────────────────────────────────────┘
```

---

# 3. Transformation System Evolution

In classic DIRAC:

```
Transformation System
   ↳ generates jobs
   ↳ interacts directly with WMS
```

In DIRACX:

```
Workflow / Transformation service
        │
        ▼
Task API
        │
        ▼
Scheduling services
```

Important changes:

* transformations become **service APIs**
* tasks become **explicit objects**
* workflows become **first-class entities**

---

# 4. Production System Evolution

The Production System becomes **workflow orchestration services**.

Instead of:

```
production definitions inside central services
```

DIRACX moves toward:

```
workflow descriptions
        ↓
workflow services
```

Workflows become easier to represent as:

* DAGs
* CWL workflows
* declarative task graphs

This is why DIRACX aligns well with **CWL-style workflows**.

---

# 5. Workload Management Changes

The classic DIRAC WMS tightly integrates:

* job queues
* matching
* pilot scheduling
* job states

DIRACX separates these responsibilities.

Conceptually:

```
task scheduling service
        │
        ▼
resource matching service
        │
        ▼
pilot services
```

This allows:

* better scaling
* more flexible scheduling policies
* cloud-native resource integration.

---

# 6. Control Plane vs Execution Plane

DIRACX clearly separates:

```
CONTROL PLANE
(workflow / scheduling)

EXECUTION PLANE
(pilots / jobs)
```

```text
CONTROL PLANE
┌──────────────────────────┐
│ Workflow Services        │
│ Transformation APIs      │
│ Scheduling Services      │
└──────────────┬───────────┘
               │
               ▼
EXECUTION PLANE
┌──────────────────────────┐
│ Pilot Infrastructure     │
│ Worker nodes             │
└──────────────────────────┘
```

Classic DIRAC mixes these concerns more tightly.

---

# 7. Impact on Workflow Abstractions

DIRACX introduces **clearer workflow abstractions**.

Classic DIRAC:

```
production
   ↓
transformation
   ↓
jobs
```

DIRACX moves toward:

```
workflow
   ↓
tasks
   ↓
jobs
```

This model maps more naturally to:

* workflow DAGs
* CWL
* modern workflow engines.

---

# 8. Why This Matters for CMSDiracAux

DIRACX architecture is actually **much closer to the CMS workflow model** than classic DIRAC.

CMS:

```
workflow
   ↓
tasks
   ↓
jobs
```

DIRACX:

```
workflow
   ↓
tasks
   ↓
jobs
```

Classic DIRAC:

```
production
   ↓
transformation
   ↓
jobs
```

So the **Translation IR layer you designed aligns extremely well with DIRACX**.

---

# 9. Key Architectural Differences

| Feature              | Classic DIRAC               | DIRACX                |
| -------------------- | --------------------------- | --------------------- |
| Architecture         | monolithic services         | microservices         |
| Interfaces           | RPC services                | REST APIs             |
| Workflow abstraction | production / transformation | workflow / tasks      |
| Scheduling           | integrated WMS              | modular services      |
| Infrastructure       | grid-centric                | cloud / grid / hybrid |

---

# 10. The Big Picture

The transition looks like this:

```text
Classic DIRAC

Production
     ↓
Transformation
     ↓
WMS
     ↓
Pilots
```

becomes

```text
DIRACX

Workflow
     ↓
Task services
     ↓
Scheduling services
     ↓
Pilots
```

---
