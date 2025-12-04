# CMSDiracAux
Auxiliary scripts and tests for running CMS workflows within Dirac distributed computing system for the CMS experiment at CERN

## Running CMS jobs with Dirac

These are notes collected during the process of initial tests of running CMS speciiffic jobs/workflows wihthin the Dirac distributed computing system.

### CMS Workflow type chosen:
 * Relval Workflow
 * Montecarlo from scratch
 * No Input
 * No Pileup

### Goals:
 * Run a minimal workflow within a minimal Dirac instance setup (hopefully provided by the Dirac Team)
 * Run the workflow, monitor the jobs progress, collect the output
 * If needed dissect the workflow on a joblevel basis and
 * Investigate how Dirac expects the payload to be packaged
 * Investigate how is the payload sent and monitored during runtime at the workernodes
 * Investigate how the jobs accounting works
 * Investigate what are the regular mechanisms for jobs and workflows debugging
 * Investigate the advanced job managing mechanisms

### Dirac client deployment

### Tests

#### Explore job runtime environment && cvmfs mounts && Singularity images tests

* Inject the simple script prepared for this job: [test-cvmfs.sh](https://github.com/todor-ivanov/CMSDiracAux/blob/main/jobs.d/test-cvmfs.d/test-cvmfs.sh)

```
[tivanov@vocms0290 ~]$ source /data/DiracAux/diracos/diracosrc
(base) [tivanov@vocms0290 ~]$ git clone https://github.com/todor-ivanov/CMSDiracAux.git
(base) [tivanov@vocms0290 ~]$ cd CMSDiracAux/jobs.d/test-cvmfs.d/
(base) [tivanov@vocms0290 test-cvmfs.d]$ dirac-wms-job-submit test-cvmfs.jdl
(base) [tivanov@vocms0290 test-cvmfs.d]$ dirac-wms-job-get-output 9554
```

<details>

<summary>* Printout the job runtime environment and run a single command from within a singularity image:</summary>

```
(base) [tivanov@vocms0290 test-cvmfs.d]$ cat 9554/std.out
==============================================================
current env print out:

_CONDOR_ANCESTOR_3502=1287248:1762239815:705256318
DIRACSITE=LCG.UKI-SCOTGRID-GLASGOW.uk
NVIDIA_VISIBLE_DEVICES=none
SINGULARITY_CACHEDIR=/var/lib/condor/execute/dir_3814407
_CONDOR_CHIRP_CONFIG=/var/lib/condor/execute/dir_3814407/.chirp.config
_CONDOR_JOB_IWD=/var/lib/condor/execute/dir_3814407
PYTHONUNBUFFERED=yes
HISTCONTROL=ignoredups
_CONDOR_MACHINE_AD=/var/lib/condor/execute/dir_3814407/.machine.ad
ROOT_MAX_THREADS=8
HOSTNAME=wn-d20-020.beowulf.cluster
HISTSIZE=1000
DAVIX_DISABLE_REDIRECT_CACHING=1
NUMEXPR_NUM_THREADS=8
GRID_GLOBAL_JOBURL=https://ce04.gla.scotgrid.ac.uk:443/arex/76816b56e41a
CUBACORES=8
_CHIRP_DELAYED_UPDATE_PREFIX=Chirp*
OMP_THREAD_LIMIT=8
OPENSSL_ALLOW_PROXY_CERTS=1
XML_CATALOG_FILES=file:///cvmfs/dirac.egi.eu/dirac/v9.0.9/Linux-x86_64/etc/xml/catalog file:///etc/xml/catalog
PWD=/var/lib/condor/execute/dir_3814407/76816b56e41a/DIRAC_9bv84jj6pilot/9554
GSETTINGS_SCHEMA_DIR=/cvmfs/dirac.egi.eu/dirac/v9.0.9/Linux-x86_64/share/glib-2.0/schemas
LOGNAME=****
CONDA_PREFIX=/cvmfs/dirac.egi.eu/dirac/v9.0.9/Linux-x86_64
DIRAC_PROCESSORS=1
MAMBA_ROOT_PREFIX=/cvmfs/dirac.egi.eu/dirac/v9.0.9/Linux-x86_64
_CONDOR_JOB_AD=/var/lib/condor/execute/dir_3814407/.job.ad
DIRACSYSCONFIG=/var/lib/condor/execute/dir_3814407/76816b56e41a/DIRAC_9bv84jj6pilot/pilot.cfg
GSETTINGS_SCHEMA_DIR_CONDA_BACKUP=
X509_USER_CERT=/var/lib/condor/execute/dir_3814407/76816b56e41a/user.proxy
X509_VOMS_DIR=/cvmfs/grid.cern.ch/etc/grid-security/vomsdir
PYTHON_CPU_COUNT=8
OPENBLAS_NUM_THREADS=8
_CONDOR_BIN=/usr/bin
_CONDOR_ANCESTOR_3814407=3814445:1764325172:3695656950
HOME=/var/lib/condor/execute/dir_3814407/76816b56e41a
LANG=en_GB.UTF-8
DAVIX_USE_LIBCURL=1
X509_VOMSES=/cvmfs/grid.cern.ch/etc/grid-security/vomses
JOBID=9554
CONDA_PROMPT_MODIFIER=(base)
DIRAC_JOB_PROCESSORS=1
TMPDIR=/tmp
_CONDOR_SCRATCH_DIR=/var/lib/condor/execute/dir_3814407
DIRAC_VOMSES=/cvmfs/grid.cern.ch/etc/grid-security/vomses
DIRAC_PILOT_STAMP=962303fa83b64334a47c3efd3dfe81a0
CONDOR_STARTER_PID=3814407
CUDA_VISIBLE_DEVICES=10000
LESSOPEN=||/usr/bin/lesspipe.sh %s
USER=******
_CONDOR_JOB_PIDS=
GPU_DEVICE_ORDINAL=10000
CONDA_BACKUP_CONDOR_CONFIG=empty
CONDA_SHLVL=1
TEMP=/tmp
X509_CERT_DIR=/cvmfs/grid.cern.ch/etc/grid-security/certificates
GRID_GLOBAL_JOBINTERFACE=org.nordugrid.arcrest
GOMAXPROCS=8
SHLVL=4
_CONDOR_LOWPORT=30000
TF_NUM_THREADS=8
APPTAINER_CACHEDIR=/var/lib/condor/execute/dir_3814407
_CONDOR_ANCESTOR_1287248=3814407:1764325170:1233910696
BATCH_SYSTEM=HTCondor
_CONDOR_AssignedGPUs=10000
CONDOR_CONFIG=/cvmfs/dirac.egi.eu/dirac/v9.0.9/Linux-x86_64/etc/condor/condor_config
_CONDOR_SLOT=slot1_12
_CONDOR_HIGHPORT=32000
DIRACOS=/cvmfs/dirac.egi.eu/dirac/v9.0.9/Linux-x86_64
TF_LOOP_PARALLEL_ITERATIONS=8
S_COLORS=auto
CONDA_DEFAULT_ENV=base
GRID_GLOBAL_JOBHOST=ce04.gla.scotgrid.ac.uk
OMP_NUM_THREADS=8
DEBUGINFOD_IMA_CERT_PATH=/etc/keys/ima:
AGENT_WORKDIRECTORY=/var/lib/condor/execute/dir_3814407/76816b56e41a/DIRAC_9bv84jj6pilot/work/WorkloadManagement/JobAgent
which_declare=declare -f
XRD_WRITERECOVERY=0
TMP=/tmp
PATH=/cvmfs/dirac.egi.eu/dirac/v9.0.9/Linux-x86_64/bin:/cvmfs/dirac.egi.eu/dirac/v9.0.9/Linux-x86_64/condabin:/home/***/.local/bin:/home/****/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
JULIA_NUM_THREADS=8
PYTHONWARNINGS=ignore
MKL_NUM_THREADS=8
MAIL=/var/spool/mail/****
DIRAC_WHOLENODE=False
X509_USER_PROXY=/tmp/tmp2pxyb5g7
DIRAC_RC_PATH=/cvmfs/dirac.egi.eu/dirac/v9.0.9/Linux-x86_64/diracosrc
OLDPWD=/var/lib/condor/execute/dir_3814407
GRID_GLOBAL_JOBID=76816b56e41a
BASH_FUNC_which%%=() {  ( alias;
 eval ${which_declare} ) | /usr/bin/which --tty-only --read-alias --read-functions --show-tilde --show-dot $@
}
_=/usr/bin/env


==============================================================
current user:

***


==============================================================
current machine and arch:

Linux wn-d20-020.beowulf.cluster 5.14.0-570.44.1.el9_6.x86_64 #1 SMP PREEMPT_DYNAMIC Wed Sep 17 10:32:11 EDT 2025 x86_64 x86_64 x86_64 GNU/Linux


==============================================================
current OS:

NAME="AlmaLinux"
VERSION="9.6 (Sage Margay)"
ID="almalinux"
ID_LIKE="rhel centos fedora"
VERSION_ID="9.6"
PLATFORM_ID="platform:el9"
PRETTY_NAME="AlmaLinux 9.6 (Sage Margay)"
ANSI_COLOR="0;34"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:almalinux:almalinux:9::baseos"
HOME_URL="https://almalinux.org/"
DOCUMENTATION_URL="https://wiki.almalinux.org/"
BUG_REPORT_URL="https://bugs.almalinux.org/"

ALMALINUX_MANTISBT_PROJECT="AlmaLinux-9"
ALMALINUX_MANTISBT_PROJECT_VERSION="9.6"
REDHAT_SUPPORT_PRODUCT="AlmaLinux"
REDHAT_SUPPORT_PRODUCT_VERSION="9.6"
SUPPORT_END=2032-06-01


==============================================================
probing to run apptainer:
executing: /cvmfs/cms.cern.ch/common/cmssw-el8 -- 'echo we are here'

we are here
```
</details>


#### CMSSW single job tests

* Dissemble a CMS production workflow and run a single CMSSW job locally:
The procedures here follows the instructions provided with the WMCore documentation at:
[Running WMCore jobs interactively](https://cms-wmcore.docs.cern.ch/training/interactive_jobs/)

 * The workflow chosen: [pdmvserv_RVCMSSW_16_0_0_pre2QCD__STD_GPU_Pix_202_PU_KIT_251125_103426_8717](https://cmsweb.cern.ch/reqmgr2/fetch?rid=pdmvserv_RVCMSSW_16_0_0_pre2QCD__STD_GPU_Pix_202_PU_KIT_251125_103426_8717)

 * Get all the files you'd need from the agent running the workflow:

```
(base) [tivanov@vocms0290 ~] cd CMSDiracAux/CMSWorkflows.d/

```



* Run one production job with Dirac

 * Submitting a job:
```
(base) [tivanov@vocms0290 test-cms-single.d]$ dirac-wms-job-submit test-cms-single.jdl
JobID = 9558
```

 * Getting the JDL description of an already submitted job:
```
(base) [tivanov@vocms0290 test-cms-single.d]$ dirac-wms-job-get-jdl 9558
{'Arguments': '',
 'CPUTime': '100',
 'Executable': './test-cms-single.sh',
 'InputSandbox': ['test-cms-single.sh',
                  'Startup.sh',
                  'JobPackage.pkl',
                  'pdmvserv_RVCMSSW_16_0_0_pre2QCD__STD_GPU_Pix_202_PU_KIT_251125_103426_8717-Sandbox.tar.bz2',
                  'Unpacker.py',
                  'SB:SandboxSE|/S3/diracx-cert-sandboxes/dteam/dteam_user/tivanov/sha256:17a9ff288a0c831f072220f1723080ae206c93c15ea6d42cdced69ceeb6f5d78.tar.bz2'],
 'JobID': '9558',
 'JobName': 'test cms single job',
 'JobRequirements': '[    CPUTime = 100;    Owner = tivanov;    OwnerGroup = '
                    'dteam_user;    UserPriority = 1;    VirtualOrganization = '
                    'dteam;  ]',
 'OutputSandbox': ['std.out',
                   'std.err',
                   'job',
                   'job/WMTaskSpace/',
                   'job/WMTaskSpace/cmsRun1',
                   'job/WMTaskSpace/logArch1',
                   'job/runtimeInfo.json',
                   'job/WMTaskSpace/cmsRun1/Report.pkl',
                   'job/WMTaskSpace/cmsRun1/PSetTweak.json',
                   'job/WMTaskSpace/cmsRun1/cmsRun1-main.sh',
                   'job/WMTaskSpace/cmsRun1/cmsRun1-stderr.log',
                   'job/WMTaskSpace/cmsRun1/cmsRun1-stdout.log',
                   'job/WMTaskSpace/logArch1/Report.pkl',
                   'job/WMTaskSpace/logArch1/logArchive.tar.gz',
                   'Report.0.pkl',
                   'wmagentJob.log'],
 'Owner': 'tivanov',
 'OwnerGroup': 'dteam_user',
 'Priority': '1',
 'StdError': 'std.err',
 'StdOutput': 'std.out',
 'VirtualOrganization': 'dteam'}
```


 * Checking the list of the current user's jobs and states:
```
(base) [tivanov@vocms0290 test-cms-single.d]$ dstat -a
JobID  Owner    JobName              OwnerGroup  JobGroup  Site                         Status  MinorStatus                       SubmissionTime
=======================================================================================================================================================
 9540  tivanov  Unknown              dteam_user  00000000  LCG.RAL.uk                   Done    Execution Complete                2025-11-26 10:11:25
 9541  tivanov  test cvmfs           dteam_user  00000000  LCG.UKI-SOUTHGRID-RALPP.uk   Done    Execution Complete                2025-11-26 13:50:46
 9542  tivanov  test cvmfs           dteam_user  00000000  LCG.UKI-SCOTGRID-GLASGOW.uk  Done    Execution Complete                2025-11-26 13:54:02
 9543  tivanov  test cvmfs           dteam_user  00000000  LCG.UKI-SCOTGRID-GLASGOW.uk  Failed  Application Finished With Errors  2025-11-27 17:02:09
 9544  tivanov  test cvmfs           dteam_user  00000000  LCG.NCBJ.pl                  Done    Execution Complete                2025-11-27 17:24:26
 9545  tivanov  test cvmfs           dteam_user  00000000  LCG.UKI-LT2-IC-HEP.uk        Done    Execution Complete                2025-11-27 17:45:14
 9546  tivanov  test cvmfs           dteam_user  00000000  LCG.IN2P3.fr                 Done    Execution Complete                2025-11-27 17:56:09
 9547  tivanov  test cvmfs           dteam_user  00000000  LCG.NCBJ.pl                  Done    Execution Complete                2025-11-27 18:14:01
 9548  tivanov  test cvmfs           dteam_user  00000000  LCG.UKI-LT2-IC-HEP.uk        Done    Execution Complete                2025-11-27 18:25:14
 9549  tivanov  test cvmfs           dteam_user  00000000  DIRAC.IC.uk                  Done    Execution Complete                2025-11-27 18:25:45
 9550  tivanov  test cvmfs           dteam_user  00000000  LCG.RAL.uk                   Done    Execution Complete                2025-11-28 10:15:35
 9551  tivanov  test cvmfs           dteam_user  00000000  LCG.UKI-LT2-IC-HEP.uk        Done    Execution Complete                2025-11-28 10:25:01
 9552  tivanov  test cvmfs           dteam_user  00000000  LCG.UKI-SOUTHGRID-RALPP.uk   Done    Execution Complete                2025-11-28 10:28:48
 9553  tivanov  test cvmfs           dteam_user  00000000  LCG.RAL.uk                   Done    Execution Complete                2025-11-28 10:30:59
 9554  tivanov  test cvmfs           dteam_user  00000000  LCG.UKI-SCOTGRID-GLASGOW.uk  Done    Execution Complete                2025-11-28 10:37:44
 9556  tivanov  test cms single job  dteam_user  00000000  LCG.RAL.uk                   Failed  Application Finished With Errors  2025-11-28 13:59:10
 9557  tivanov  test cms single job  dteam_user  00000000  LCG.UKI-SCOTGRID-GLASGOW.uk  Failed  Output Data Uploaded              2025-11-28 14:08:29
 9558  tivanov  test cms single job  dteam_user  00000000  LCG.UKI-SOUTHGRID-RALPP.uk   Done    Execution Complete                2025-12-01 11:14:30
```

 * Look at the StdOut of a currently running job:
```
(base) [tivanov@vocms0290 test-cms-single.d]$ dirac-wms-job-peek   9558

======================================================================================
Last 20 lines of application output from Watchdog on 2025-12-01 11:16:03.746428 [UTC]:
Last reported CPU consumed for job is 00:00:06 (h:m:s)
======================================================================================
INFO:root:create(/scratch/condor/dir_560131/n3dMDm32Gk8nGKVDjqUVj3jqqRTY0pABFKDmYrGKDmS5MKDmPvl5Mo/DIRAC_66kcbtnapilot/9558/job/WMTaskSpace/logArch1)
INFO:root:Builders.LogArchive.build called on logArch1
INFO:root:Executing task at directory: /scratch/condor/dir_560131/n3dMDm32Gk8nGKVDjqUVj3jqqRTY0pABFKDmYrGKDmS5MKDmPvl5Mo/DIRAC_66kcbtnapilot/9558/job
INFO:root:In Watchdog.setupMonitors
INFO:root:Set Watchdog interval to 300
INFO:root:Initializing monitor PerformanceMonitor
INFO:root:Not resizing job
INFO:root:Watchdog modified: False. Final settings:
INFO:root:  hardTimeout: 159900
INFO:root:  softTimeout: 159600
INFO:root:  maxPSS: 20000
INFO:root:  cores: 8
INFO:root:MonitorThread: JobStarted
INFO:root:Steps.Executor logging started
INFO:root:Steps.Executors.CMSSW.pre called
INFO:root:Steps.Executors.CMSSW.execute called
INFO:root:CMSSW configured for 8 cores and 1 event streams
INFO:root:CMSSW configured for GPU required: forbidden, with these settings: None
INFO:root:Executing CMSSW step
INFO:root:Running SCRAM

...

(base) [tivanov@vocms0290 test-cms-single.d]$ dirac-wms-job-peek   9558

===================================================================================
Last 20 lines of application output from JobWrapper on 2025-12-01 11:45:54.018276 :
CPU Total: 00:28:57 (h:m:s) Normalized CPU Total 100924.3 s @ HEP'06
===================================================================================
Stage-out succeeded with the current environment.
INFO:root:attempting stageOut
INFO:root:===> Stage Out Successful: {'LFN': '/store/unmerged/logs/prod/2025/12/1/pdmvserv_RVCMSSW_16_0_0_pre2QCD__STD_GPU_Pix_202_PU_KIT_251125_103426_8717/GenSimFull/0000/0/fc873065-b21d-4c00-843e-cf58702751f8-0-0-logArchive.tar.gz', 'PFN': 'davs://mover.pp.rl.ac.uk:2880/pnfs/pp.rl.ac.uk/data/cms/store/unmerged/logs/prod/2025/12/1/pdmvserv_RVCMSSW_16_0_0_pre2QCD__STD_GPU_Pix_202_PU_KIT_251125_103426_8717/GenSimFull/0000/0/fc873065-b21d-4c00-843e-cf58702751f8-0-0-logArchive.tar.gz', 'PNN': 'T2_UK_SGrid_RALPP', 'GUID': None, 'StageOutReport': [], 'StageOutCommand': 'gfal2'}
INFO:root:addOutputFile method called with outputModule: logArchive, aFile: {'lfn': '/store/unmerged/logs/prod/2025/12/1/pdmvserv_RVCMSSW_16_0_0_pre2QCD__STD_GPU_Pix_202_PU_KIT_251125_103426_8717/GenSimFull/0000/0/fc873065-b21d-4c00-843e-cf58702751f8-0-0-logArchive.tar.gz', 'pfn': 'davs://mover.pp.rl.ac.uk:2880/pnfs/pp.rl.ac.uk/data/cms/store/unmerged/logs/prod/2025/12/1/pdmvserv_RVCMSSW_16_0_0_pre2QCD__STD_GPU_Pix_202_PU_KIT_251125_103426_8717/GenSimFull/0000/0/fc873065-b21d-4c00-843e-cf58702751f8-0-0-logArchive.tar.gz', 'location': 'T2_UK_SGrid_RALPP', 'module_label': 'logArchive', 'events': 0, 'size': 0, 'merged': False, 'checksums': {'adler32': '29d91801', 'cksum': '1422532435'}}
INFO:root:addOutputFile method fileRef: , whole tree: {}
INFO:root:Success job! Not saving its logs to CERN EOS recent area.
INFO:root:Steps.Executors.LogArchive.post called
INFO:root:StepName: logArch1, StepType: LogArchive, with result: 0
INFO:root:MonitorThread: JobEnded
INFO:root:MonitorState: Shutdown called
INFO:root:Completing task at directory: /scratch/condor/dir_560131/n3dMDm32Gk8nGKVDjqUVj3jqqRTY0pABFKDmYrGKDmS5MKDmPvl5Mo/DIRAC_66kcbtnapilot/9558/job/WMTaskSpace
INFO:root:Looking for master report at /scratch/condor/dir_560131/n3dMDm32Gk8nGKVDjqUVj3jqqRTY0pABFKDmYrGKDmS5MKDmPvl5Mo/DIRAC_66kcbtnapilot/9558/job/WMTaskSpace/../../Report.0.pkl
INFO:root:  found it!
INFO:root:Looking for a taskStep report at /scratch/condor/dir_560131/n3dMDm32Gk8nGKVDjqUVj3jqqRTY0pABFKDmYrGKDmS5MKDmPvl5Mo/DIRAC_66kcbtnapilot/9558/job/WMTaskSpace/cmsRun1/Report.pkl
INFO:root:  found it!
INFO:root:Looking for a taskStep report at /scratch/condor/dir_560131/n3dMDm32Gk8nGKVDjqUVj3jqqRTY0pABFKDmYrGKDmS5MKDmPvl5Mo/DIRAC_66kcbtnapilot/9558/job/WMTaskSpace/stageOut1/Report.pkl
INFO:root:  found it!
INFO:root:Looking for a taskStep report at /scratch/condor/dir_560131/n3dMDm32Gk8nGKVDjqUVj3jqqRTY0pABFKDmYrGKDmS5MKDmPvl5Mo/DIRAC_66kcbtnapilot/9558/job/WMTaskSpace/logArch1/Report.pkl
INFO:root:  found it!
INFO:root:Shutting down monitor

```

 * Getting the job status:
```
(base) [tivanov@vocms0290 test-cms-single.d]$ dirac-wms-job-status 9558
JobID=9558 ApplicationStatus=Unknown; MinorStatus=Execution Complete; Status=Done; Site=LCG.UKI-SOUTHGRID-RALPP.uk;

```

 * Getting the job state progress:
```
(base) [tivanov@vocms0290 test-cms-single.d]$ dirac-wms-job-logging-info 9558
Source                            Status      MinorStatus                        ApplicationStatus  DateTime
=========================================================================================================================
JobManager                        Received    Job accepted                       Unknown            2025-12-01 11:14:30
JobPath                           Checking    JobSanity                          Unknown            2025-12-01 11:14:31
JobSanity                         Checking    JobScheduling                      Unknown            2025-12-01 11:14:31
JobScheduling                     Waiting     Pilot Agent Submission             Unknown            2025-12-01 11:14:31
Matcher                           Matched     Assigned                           Unknown            2025-12-01 11:15:49
JobAgent@LCG.UKI-SOUTHGRID-RALPP  Matched     Job Received by Agent              Unknown            2025-12-01 11:15:49
JobAgent@LCG.UKI-SOUTHGRID-RALPP  Matched     Installing Software                Unknown            2025-12-01 11:15:50
JobAgent@LCG.UKI-SOUTHGRID-RALPP  Matched     Submitting To CE                   Unknown            2025-12-01 11:15:50
JobWrapper                        Running     Job Initialization                 Unknown            2025-12-01 11:15:53
JobWrapper                        Running     Downloading InputSandbox           Unknown            2025-12-01 11:15:54
JobWrapper                        Running     Application                        Unknown            2025-12-01 11:15:57
JobWrapper                        Completing  Application Finished Successfully  Unknown            2025-12-01 11:45:54
JobWrapper                        Completing  Uploading Output Sandbox           Unknown            2025-12-01 11:45:56
JobWrapper                        Completing  Uploading Output Data              Unknown            2025-12-01 11:46:39
JobWrapper                        Completing  Output Data Uploaded               Unknown            2025-12-01 11:46:47
JobWrapper                        Done        Execution Complete                 Unknown            2025-12-01 11:46:48
```


 * Getting the output of a finished job:
```
[tivanov@vocms0290 WMCoreDev.d]$ . /data/DiracAux/diracos/diracosrc
(base) [tivanov@vocms0290 WMCoreDev.d]$ cd ~/CMSDiracAux/jobs.d/test-cms-single.d/
(base) [tivanov@vocms0290 test-cms-single.d]$ dirac-wms-job-get-jdl 9562
{'Arguments': '',
 'CPUTime': '1000',
 'Executable': './test-cms-single.sh',
 'InputSandbox': ['test-cms-single.sh',
                  'Startup.sh',
                  'JobPackage.pkl',
                  'pdmvserv_RVCMSSW_16_0_0_pre2QCD__STD_GPU_Pix_202_PU_KIT_251125_103426_8717-Sandbox.tar.bz2',
                  'Unpacker.py',
                  'SB:SandboxSE|/S3/diracx-cert-sandboxes/dteam/dteam_user/tivanov/sha256:a9471df1b98a089293903cb840e848f4528d56eabffb15e50dba59bf21b197c0.tar.bz2'],
 'JobID': '9562',
 'JobName': 'test cms single job',
 'JobRequirements': '[    CPUTime = 1000;    Owner = tivanov;    OwnerGroup = '
                    'dteam_user;    UserPriority = 1;    VirtualOrganization = '
                    'dteam;    Sites = LCG.UKI-SOUTHGRID-RALPP.uk;  ]',
 'OutputSandbox': ['std.out', 'std.err', 'Report.0.pkl', 'wmagentJob.log'],
 'Owner': 'tivanov',
 'OwnerGroup': 'dteam_user',
 'Priority': '1',
 'Site': 'LCG.UKI-SOUTHGRID-RALPP.uk',
 'StdError': 'std.err',
 'StdOutput': 'std.out',
 'VirtualOrganization': 'dteam'}

(base) [tivanov@vocms0290 test-cms-single.d]$
(base) [tivanov@vocms0290 test-cms-single.d]$ dirac-wms-job-get-output 9562
Files retrieved and extracted in /afs/cern.ch/user/t/tivanov/CMSDiracAux/jobs.d/test-cms-single.d/9562
Job output sandbox retrieved in /afs/cern.ch/user/t/tivanov/CMSDiracAux/jobs.d/test-cms-single.d/9562/

(base) [tivanov@vocms0290 test-cms-single.d]$ cd 9562
(base) [tivanov@vocms0290 9562]$ ll
total 134
drwxr-xr-x. 2 tivanov zh  2048 Dec  4 14:18 .
drwxr-xr-x. 5 tivanov zh  2048 Dec  4 14:18 ..
-rw-r--r--. 1 tivanov zh   691 Dec  2 16:15 Report.0.pkl
-rw-r--r--. 1 tivanov zh 63110 Dec  2 16:47 std.err
-rw-r--r--. 1 tivanov zh   112 Dec  2 16:14 std.out
-rw-r--r--. 1 tivanov zh 67442 Dec  2 16:47 wmagentJob.log
```

 * Reading the regular `Report.0.pkl` and the `wmagentJob.log` files from the WMCore runtime code
```
(base) [tivanov@vocms0290 9562]$ . /data/WMAgent.venv3/bin/activate
Setting up WMCore related environment variables:
(WMAgent.venv3) (base) [tivanov@vocms0290 9562]$ unpkl Report.0.pkl
FrameworkJobReport.jobFeatures = {'hs06_job': None, 'allocated_cpu': 8.0}
FrameworkJobReport.siteName = 'T2_UK_SGrid_RALPP'
FrameworkJobReport.hostName = 'heplnc153.pp.rl.ac.uk'
FrameworkJobReport.steps = []
FrameworkJobReport.machineFeatures = {}
FrameworkJobReport.ceName = 'heplnc153.pp.rl.ac.uk'
FrameworkJobReport.WMAgentJobName = 'fc873065-b21d-4c00-843e-cf58702751f8-0'
FrameworkJobReport.workload = 'Unknown'
FrameworkJobReport.pnn = 'T2_UK_SGrid_RALPP'
FrameworkJobReport.WMAgentJobID = 219128
FrameworkJobReport.completed = False
FrameworkJobReport.task = '/pdmvserv_RVCMSSW_16_0_0_pre2QCD__STD_GPU_Pix_202_PU_KIT_251125_103426_8717/GenSimFull'

<WMCore.Configuration.ConfigSection object at 0x7f475c446a60>
```

* Disassemble a CMS analysis workflow

* Run the Analysis workflow with Dirac
