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

python $CONDOR_FOLDER/ana_scripts/get_filtered_muon_flux_energy_full.py root://eospublic.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/ship.conical.MuonBack-TGeant4.root


xrdcp energy_filtered_keys_sco_0Point root://eosuser.cern.ch"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/energy_filtered_keys_sco_0Point
xrdcp energy_filtered_keys_sco_1Point root://eosuser.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/energy_filtered_keys_sco_1Point
xrdcp energy_filtered_keys_sco_2Point root://eosuser.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/energy_filtered_keys_sco_2Point