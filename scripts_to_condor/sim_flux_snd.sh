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

python $CONDOR_FOLDER/ana_scripts/sensitive_planes.py root://eospublic.cern.ch/"$EOS_PUBLIC"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/ship.conical.MuonBack-TGeant4.root


# xrdcp energy_filtered_keys_sco_0Point root://eosuser.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/energy_filtered_keys_sco_0Point
# xrdcp energy_filtered_keys_sco_1Point root://eosuser.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/energy_filtered_keys_sco_1Point
# xrdcp energy_filtered_keys_sco_2Point root://eosuser.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/energy_filtered_keys_sco_2Point
xrdcp output_snd_planes_0.root root://eosuser.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/output_snd_planes_0.root
xrdcp output_snd_planes_1.root root://eosuser.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/output_snd_planes_1.root
xrdcp output_snd_planes_2.root root://eosuser.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/output_snd_planes_2.root


# xrdcp output_snd_planes_0_check.root root://eosuser.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/ooutput_snd_planes_0_check.root
# xrdcp output_snd_planes_1_check.root root://eosuser.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/output_snd_planes_1_check.root
# xrdcp output_snd_planes_2_check.root root://eosuser.cern.ch/"$EOS_DATA"/"$DIR"/"$SUB"/"$LSB_JOBINDEX"/output_snd_planes_2_check.root