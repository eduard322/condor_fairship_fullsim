#!/bin/bash

# clear

source /cvmfs/ship.cern.ch/SHiP-2022/May/setUp.sh
source $CONDOR_FOLDER/start_ali.sh
set -ux
echo "Starting script."
DIR=$1
ProcId=$2
NJOBS=$3
LSB_JOBINDEX=$((ProcId+1))
MUONS=$4
NTOTAL=$5
SUB=$6
MUSHIELD=8

N=$(( NTOTAL/NJOBS + ( LSB_JOBINDEX == NJOBS ? NTOTAL % NJOBS : 0 ) ))
FIRST=$(((NTOTAL/NJOBS)*(LSB_JOBINDEX-1)))

python $CONDOR_FOLDER/ana_scripts/snd_planes.py -i "$DIR"/"$SUB"/"$LSB_JOBINDEX"/ --condor 0
xrdcp output_full.root root://eosuser.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/output_full.root
