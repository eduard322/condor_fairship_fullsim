#!/bin/bash
set -ux

export KRB5_CONFIG=krb5.conf
kinit -k -t edursov.keytab edursov@CERN.CH
/usr/local/bin/alienv enter -w /sw FairShip/latest


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

#echo $FAIRSHIP
/usr/local/bin/alienv -w /sw setenv  FairShip/latest  -c /bin/bash  -c "python \$FAIRSHIP"'/macro/run_simScript.py --muShieldDesign 8 --MuonBack --nEvents '"$N"' --firstEvent '"$FIRST"' -f '"$MUONS"' --FastMuon -g '"$GEOFILE"''
/usr/local/bin/alienv -w /sw setenv  FairShip/latest  -c /bin/bash  -c 'xrdcp ship.conical.MuonBack-TGeant4.root root://eospublic.cern.ch/'"$EOS_PUBLIC"'/'"$DIR"'/'"$SUB"'/'"$LSB_JOBINDEX"'/ship.conical.MuonBack-TGeant4.root'
/usr/local/bin/alienv -w /sw setenv  FairShip/latest  -c /bin/bash  -c 'xrdcp *.csv root://eospublic.cern.ch/'"$EOS_PUBLIC"'/'"$DIR"'/'"$SUB"'/'"$LSB_JOBINDEX"'/output.csv'
if [ "$LSB_JOBINDEX" -eq 1 ]; then
/usr/local/bin/alienv -w /sw setenv  FairShip/latest  -c /bin/bash  -c 'xrdcp geofile_full.conical.MuonBack-TGeant4.root root://eospublic.cern.ch/'"$EOS_PUBLIC"'/'"$DIR"'/'"$SUB"'/geofile_full.conical.MuonBack-TGeant4.root'
fi

