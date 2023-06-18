import os
import sys
import shutil
from argparse import ArgumentParser
import time

parser = ArgumentParser()
parser.add_argument("--output", dest="output", help="Output", required=False,  default=".")
parser.add_argument("--geofile",   dest="geofile",  help="Geofile", required=False,  default="combi.root")
parser.add_argument("--sub_type",   dest="sub_type",  help="sub_type, 0 -- sim.sub, 1 -- sim_flux.sub", required=False,  default="0")
parser.add_argument("--number",   dest="job_num",  help="Number of jobs", required=False,  default="20")
parser.add_argument("--input",   dest="input",  help="Enter input file", required=False,  default="input_for_muon_prod.txt")
parser.add_argument("--of",   dest="of",  help="output folder", required=False,  default="default")

options = parser.parse_args()

DATA_DIR = options.output
GF = options.geofile
sub_type = int(options.sub_type)
N_JOBS= int(options.job_num)

if sub_type == 0:
    submit = os.path.join("condor_submit_files", "sim.sub")
    EOS = os.environ['EOS_PUBLIC']
elif sub_type == 1:
    submit = os.path.join("condor_submit_files", "sim_flux.sub")
    EOS = os.environ['EOS_DATA']
elif sub_type == 2:
    submit = os.path.join("condor_submit_files", "sim_flux_snd.sub")
    EOS = os.environ['EOS_DATA']
elif sub_type == 4:
    submit = os.path.join("condor_submit_files", "docker_universe.sub")
    EOS = os.environ['EOS_PUBLIC']



if os.path.exists(os.path.join("logs", str(sub_type))): 
    shutil.rmtree(os.path.join("logs", str(sub_type)))

os.makedirs(os.path.join("logs", str(sub_type)))

with open(os.path.join("input_dirs", options.input), "r") as f:
    for iter, line in enumerate(f):
        filepath, n_events, foldername = line.strip().split(", ")
        directory = os.path.join(EOS, DATA_DIR, foldername)

        os.makedirs(os.path.join("logs", str(sub_type), foldername))
        for i in range(N_JOBS):
            os.makedirs(os.path.join("logs", str(sub_type), foldername, str(i)))

        if not os.path.exists(directory): 
            os.makedirs(directory)
        
        if iter % 100 == 0 and iter != 0:
            time.sleep(1*60*60*6)
        os.system("condor_submit directory={dir} N={n_jobs} muon_file={mf} n_events={ne} SUB={sub} GEOFILE={geofile} {sim_submit}".format(dir=DATA_DIR,
                                                                                                         n_jobs=N_JOBS,
                                                                                                         mf=filepath,
                                                                                                         ne=n_events,
                                                                                                         sub = foldername,
                                                                                                         geofile = GF,
                                                                                                         sim_submit = submit))

