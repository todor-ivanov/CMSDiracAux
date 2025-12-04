#!/bin/bash

workDir=$1

source /cvmfs/cms.cern.ch/COMP/rhel8_x86_64/external/python3/3.8.2/etc/profile.d/init.sh
source /cvmfs/cms.cern.ch/COMP/rhel8_x86_64/external/py3-future/0.18.2/etc/profile.d/init.sh

cd $workDir/job/
export WMAGENTJOBDIR=$PWD
export PYTHONPATH=$PWD/WMCore.zip:$PWD:$PYTHONPATH
python3 Startup.py
