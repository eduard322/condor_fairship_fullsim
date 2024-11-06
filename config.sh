#!/bin/bash


# generate start_ali.sh script
# rm start_ali.sh


# define variables
export CONDOR_FOLDER=${PWD}
export EOS_DATA=/eos/user/e/edursov/ship_data
export EOS_PUBLIC=/eos/experiment/ship/user/edursov


# define input parameters

OFOLDER=SC_full_opt_1
OUTPUT=sc_v6
export GEOFILE=sc_v6
#export GEOFILE=optimized_18102022.root
export SUBTYPE=3
JOB_NUMBER=50
INPUT_FILE=input_file_10_spills.txt
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
source /cvmfs/ship.cern.ch/24.10/setUp.sh
alienv printenv FairShip/latest >> start_ali.sh
python run_submissions${SCRIPT}.py --output ${OUTPUT} --geofile ${GEOFILE} --sub_type ${SUBTYPE} --number ${JOB_NUMBER} --input ${INPUT_FILE} --of ${OFOLDER}
EOF

chmod +x start_condor
