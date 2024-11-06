import os
from datetime import date
import numpy as np

#num_of_configs = 14
config_name = "SC_optimized_flatten_ecn3_2023"
number_of_jobs = 200
input_file = "input_for_muon_prod_11_flatten.txt"
sub_type = 3
output_folder = "sc_v6_ecn3_fixed"
# output_folder = "vector_scan_v6_1_flatten"


# geo_num_list = [1229, 1142, 1210, 1201, 1134, 1200, 1525, 1606, 1785]
# configs = [f"blueberry_{num}" for num in geo_num_list]
# configs += ["sc_v6"]
configs = ["sc_v6"]
# geo_num_list = [1557, 1439, 1426, 821, 1529, 945]
# configs = [f"blueberry_{num}" for num in geo_num_list]
# blueberry_list = [2328, 2493, 1863, 1864, 2171, 2668, 2701]
# configs = [f"blueberry_{i}" for i in blueberry_list]
# configs = ['raspberry_621', 'raspberry_1672', 'raspberry_1358', 'raspberry_1207', 'raspberry_1421', 'raspberry_1872', 'raspberry_1337', 'raspberry_1804', 'raspberry_1543', 'raspberry_1658']
#configs = [0.7 + i*0.05 for i in range(13)]
date = str(date.today())
date += "_may2024"
# date = "fieldmap_inv_peach"
# os.system("export CONDOR_FOLDER=${PWD}")
# os.system("export EOS_DATA=/eos/user/e/edursov/ship_data")
# os.system("export EOS_PUBLIC=/eos/experiment/ship/user/edursov")
# os.system(f"export SUBTYPE={sub_type}")
os.system(f"source $PWD/vars.sh {sub_type}")
os.system("source /cvmfs/ship.cern.ch/SHiP-2022/May/setUp.sh")
# if os.path.exists("start_ali.sh"):
#     os.system("rm start_ali.sh")
# os.system("alienv printenv FairShip/latest >> start_ali.sh")


# for i in range(1, num_of_configs + 1):
#     label = f'''{config_name}_v{i}_{"spill_" if input_file == "input_for_muon_prod.txt" else ""}{date}'''
#     print(f"Launching {config_name} with sub_type {sub_type}. Output in {label}. Inpit in {input_file}")
#     # os.system(f'''python run_submissions.py \\
#     #           --output {label} 
#     #           --geofile {config_name}_v{i}.root 
#     #           --sub_type {sub_type}
#     #           --number {number_of_jobs}
#     #           --input {input_file}
#     #           ''')
#     COMMAND = f'''python run_submissions.py \
#               --output {label} \
#               --geofile {config_name}_v{i}.root \
#               --sub_type {sub_type} \
#               --number {number_of_jobs} \
#               --input {input_file} \
#               --of {output_folder}
#               '''
#     os.system(COMMAND)

for iter, conf in enumerate(configs):
    label = f'''{conf}_{"spill_" if input_file == "input_for_muon_prod.txt" else ""}{date}'''
    print(f"Launching {config_name} with sub_type {sub_type}. Output in {label}. Input in {input_file}")
    # os.system(f'''python run_submissions.py \\
    #           --output {label} 
    #           --geofile {config_name}_v{i}.root 
    #           --sub_type {sub_type}
    #           --number {number_of_jobs}
    #           --input {input_file}
    #           ''')
    COMMAND = f'''python run_submissions.py \
              --output {label} \
              --geofile {conf} \
              --sub_type {sub_type} \
              --number {number_of_jobs} \
              --input {input_file} \
              --of {output_folder}
              '''
    os.system(COMMAND)
