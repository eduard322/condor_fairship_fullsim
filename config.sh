#!/bin/bash


# generate start_ali.sh script
# rm start_ali.sh


# define variables
export CONDOR_FOLDER=${PWD}
export EOS_DATA=/eos/user/e/edursov/ship_data
export EOS_PUBLIC=/eos/experiment/ship/user/edursov


# define input parameters

OFOLDER=SC_full_opt_1
OUTPUT=sc_v6_tracks_20082023_fieldmap
#OUTPUT=test_docker_scheduler_2_full_sample
#OUTPUT=test_docker_2023_6Gb_30j_1
#OUTPUT=combi_ecn3_spill_snd_scor_planes_no_trench_26012023
#OUTPUT=combi_ecn3_spill_snd_scor_planes_fixed_fields_11102022
# OUTPUT=optimized_snd_scor_planes_down_18102022
#OUTPUT=combi_cutoff_ecn3_spill_snd_scor_planes_28012023
# OFOLDER=sc_v6_ecn3_fixed
# OUTPUT=cherry_2023-07-06
# OUTPUT=cranberry_2023-07-06
# OUTPUT=strawberry_2023-07-09
# OUTPUT=mulberry_2023-07-09
# OUTPUT=sc_v6_2023-06-26
# OUTPUT=config_04032023_v0_full_spill
# export GEOFILE=sc_v6
# export GEOFILE=cherry
# export GEOFILE=cranberry
# export GEOFILE=strawberry
export GEOFILE=sc_v6
#export GEOFILE=optimized_18102022.root
export SUBTYPE=4
JOB_NUMBER=50
INPUT_FILE=input_for_muon_prod_11_flattens.txt
# define kerberos file 
export KERB=docker_files/edursov.keytab
SCRIPT=

if [ $SUBTYPE -eq 4 ]; then
    ktmux(){
        if [[ -z "$1" ]]; then #if no argument passed
            k5reauth -f -i 3600 -p "$USER" -k "$KERB" -- tmux new-session
        else #pass the argument as the tmux session name
            k5reauth -f -i 3600 -p "$USER" -k "$KERB" -- tmux new-session -s $1
        fi
    }
    echo "Start tmux"
    # ktmux "$OUTPUT"
    SCRIPT="_universe"
fi
# generate execute file

cat > start_condor <<EOF
#!/bin/bash
source /cvmfs/ship.cern.ch/SHiP-2022/May/setUp.sh
alienv printenv FairShip/latest >> start_ali.sh
python run_submissions${SCRIPT}.py --output ${OUTPUT} --geofile ${GEOFILE} --sub_type ${SUBTYPE} --number ${JOB_NUMBER} --input ${INPUT_FILE} --of ${OFOLDER}
EOF

chmod +x start_condor
