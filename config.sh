#!/bin/bash


# generate start_ali.sh script
source /cvmfs/ship.cern.ch/SHiP-2022/May/setUp.sh
alienv printenv FairShip/latest >> start_ali.sh


# define variables
export CONDOR_FOLDER=${PWD}
export EOS_DATA=/eos/user/e/edursov/ship_data
export EOS_PUBLIC=/eos/experiment/ship/user/edursov


# define input parameters

OUTPUT=checking_folder_1
GEOFILE=combi.root
export SUBTYPE=1
JOB_NUMBER=20
INPUT_FILE=input_for_muon_prod_low_stat.txt

# generate execute file

cat > start_condor <<EOF
#!/bin/bash
python run_submissions.py --output ${OUTPUT} --geofile ${GEOFILE} --sub_type ${SUBTYPE} --number ${JOB_NUMBER} --input ${INPUT_FILE}
EOF

chmod +x start_condor