#! /bin/sh

chunkID=$1
echo ${chunkID}

LAUNCH_FOLDER="/eos/user/p/pmastrap/FCCFW/Analysis/FCCAnalyses/run/Delphescard_validation"

cd ${LAUNCH_FOLDER}
source /cvmfs/sft.cern.ch/lcg/views/LCG_102/x86_64-centos7-gcc11-opt/setup.sh
python processTrees.py --ID ${chunkID}
