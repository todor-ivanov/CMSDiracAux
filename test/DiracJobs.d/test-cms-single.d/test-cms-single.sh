#!/bin/bash
echo PWD: $PWD
sandbox=$PWD/pdmvserv_RVCMSSW_16_0_0_pre2QCD__STD_GPU_Pix_202_PU_KIT_251125_103426_8717-Sandbox.tar.bz2
package=$PWD/JobPackage.pkl
index=219128
python3 Unpacker.py --sandbox=$sandbox --package=$package --index=$index

/cvmfs/cms.cern.ch/common/cmssw-el8 -- "$PWD/Startup.sh $PWD"
