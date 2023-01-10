#!/bin/bash


# generate start_ali.sh script
source /cvmfs/ship.cern.ch/SHiP-2022/May/setUp.sh
alienv printenv FairShip/latest >> start_ali.sh


# define variables
export CONDOR_FOLDER=${PWD}
export EOS_DATA=/eos/user/e/edursov/ship_data
export EOS_PUBLIC=/eos/experiment/ship/user/edursov


# define input parameters

#OUTPUT=optimized_ecn3_spill_snd_scor_planes_fixed_fields_23102023
OUTPUT=test_docker_2023_2
export GEOFILE=combi.root
export SUBTYPE=3
JOB_NUMBER=20
INPUT_FILE=input_for_muon_prod_1.txt
# define kerberos file 
export KERB=docker_files/edursov.keytab


# generate execute file

cat > start_condor <<EOF
#!/bin/bash
python run_submissions.py --output ${OUTPUT} --geofile ${GEOFILE} --sub_type ${SUBTYPE} --number ${JOB_NUMBER} --input ${INPUT_FILE}
EOF

chmod +x start_condor
