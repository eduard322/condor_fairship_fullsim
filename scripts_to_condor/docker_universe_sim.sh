#!/bin/bash

# not implemented yet

#set -m
set -ux
#/bin/sh -c yum -y install krb5-workstation
#yum -y install eos-fuse eos-fusex
#yum -y install autofs
export KRB5_CONFIG=krb5.conf
kinit -k -t edursov.keytab edursov@CERN.CH
#eosfusebind
/usr/local/bin/alienv enter -w /sw FairShip/latest

#/usr/local/bin/alienv -w /sw setenv  FairShip/latest  -c /bin/bash  -c "xrdcp root://eospublic.cern.ch//eos/experiment/ship/data/Mbias/background-prod-2018/README README"

#ls -la /eos/experiment/ship/data/Mbias/background-prod-2018/ >> LOG.txt

/usr/local/bin/alienv -w /sw setenv  FairShip/latest  -c /bin/bash  -c "python \$FAIRSHIP/macro/run_simScript.py --muShieldDesign 8 -g combi.root --FastMuon --MuonBack -f /eos/experiment/ship/data/Mbias/background-prod-2018/pythia8_Geant4_10.0_withCharmandBeauty0_mu.root -n 100"
/usr/local/bin/alienv -w /sw setenv  FairShip/latest  -c /bin/bash  -c "python \$FAIRSHIP/macro/run_simScript.py --muShieldDesign 8 -g combi.root --FastMuon --MuonBack -n 100 -f /eos/experiment/ship/data/Mbias/background-prod-2018/pythia8_Geant4_10.0_withCharmandBeauty0_mu.root"
