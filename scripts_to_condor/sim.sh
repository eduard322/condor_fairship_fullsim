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
GEOFILE=$7
MUSHIELD=8

N=$(( NTOTAL/NJOBS + ( LSB_JOBINDEX == NJOBS ? NTOTAL % NJOBS : 0 ) ))
FIRST=$(((NTOTAL/NJOBS)*(LSB_JOBINDEX-1)))
if eos stat "$EOS_PUBLIC"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/ship.conical.MuonBack-TGeant4.root; then
	echo "Target exists, nothing to do."
	exit 0
else


	python "$FAIRSHIP"/macro/run_simScript.py --muShieldDesign $MUSHIELD --MuonBack --nEvents $N --firstEvent $FIRST -f $MUONS --FastMuon -g $CONDOR_FOLDER/geofiles/$GEOFILE 	
	xrdcp ship.conical.MuonBack-TGeant4.root root://eospublic.cern.ch/"$EOS_PUBLIC"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/ship.conical.MuonBack-TGeant4.root
	if [ "$LSB_JOBINDEX" -eq 1 ]; then
	xrdcp geofile_full.conical.MuonBack-TGeant4.root\
        root://eospublic.cern.ch/"$EOS_PUBLIC"/"$DIR"/"$SUB"/geofile_full.conical.MuonBack-TGeant4.root
	fi
fi
