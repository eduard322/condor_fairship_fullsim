# Fairship muon flux simulation and analysis

This code is aimed to launch a full statistics simulation of background muons at SHiP via HTCondor.

**Before launching the simulation delete the ```start_ali.sh``` script!**


# Steps
- change the output eos folders for yours eos folders in the ```config.sh``` script: ```$EOS_DATA``` (local eos folder for secondary output) and ```$EOS_PUBLIC``` (ship eos folder for basic output)
- choose the output folder ```$OFOLDER``` that will be created (if needed) in the ```$EOS_PUBLIC``` and the output folder ```$OUTPUT``` with the output data that will be located in ``$OFOLDER```
- ```$GEOFILE``` is ```sc_v6``` (can be changed for other possible options for SC magnet)
- ```$JOB_NUMBER```  stands for the number of jobs _per one file_ from the input txt file
- ```$INPUT_FILE``` stands for the input file located in the ```input_dirs``` folder

Make sure that ```scripts_to_condor/sim_ana.sh``` and ```config.sh``` contain the last version of the ```setup.sh``` script.

Launch: ```source config.sh```. 

Code flow: ```config.sh``` -> ```run_submissions.py``` -> ```condor_submit_files/sim_ana.sub``` -> ```scripts_to_condor/sim_ana.sh``` -> ```$FAIRSHIP/run_simScript.py```
