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

echo $MUONS
echo $DIR
echo $SUB
N=$(( NTOTAL/NJOBS + ( LSB_JOBINDEX == NJOBS ? NTOTAL % NJOBS : 0 ) ))
FIRST=$(((NTOTAL/NJOBS)*(LSB_JOBINDEX-1)))

python $CONDOR_FOLDER/ana_scripts/tracking_stations.py root://eospublic.cern.ch/"$EOS_PUBLIC"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/ship.conical.MuonBack-TGeant4.root
#xrdcp flux_4_energies root://eosuser.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/flux_4_energies_1
#xrdcp flux_filtered_energies root://eosuser.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/flux_filtered_energies
#xrdcp energy_filtered_keys root://eosuser.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/energy_filtered_keys
xrdcp output_tr.root root://eosuser.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/output_tr.root