#!/bin/bash

echo ==============================================================
echo current env print out:
echo
env
echo
echo

echo ==============================================================
echo current user:
echo
id
echo
echo

echo ==============================================================
echo current machine and arch:
echo
uname -a
echo
echo

echo ==============================================================
echo current OS:
echo
cat /etc/os-release
echo
echo

echo ==============================================================
echo probing to run apptainer:
echo executing: /cvmfs/cms.cern.ch/common/cmssw-el8 -- \'echo we are here\'

echo
set -x

/cvmfs/cms.cern.ch/common/cmssw-el8 -- 'echo we are here'
# /cvmfs/cms.cern.ch/common/cmssw-env --cmsos el8 -- 'echo we are here'
# ./cmssw-env --cmsos el8 -- 'echo we are here'
echo
echo


