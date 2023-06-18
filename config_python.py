import os
from datetime import date
import numpy as np

#num_of_configs = 14
config_name = "SC_optimized_13052023_full_spill_flatten"
number_of_jobs = 500
input_file = "input_for_muon_prod_11_flatten.txt"
sub_type = 3
output_folder = "config_v6_low"
# output_folder = "vector_scan_v6_1_flatten"

# configs = ["config_05052023_v6", "config_05052023_v8"]
# configs = ["config_05052023_v8"]
# config_05052023_v6 = np.array([70.0, 170.0, 0.0, 353.0780575329521, 125.08255586355432, 184.8344375295139, 150.19262843951793, 186.81232063446174, 40.0, 40.0, 150.0, 150.0, 2.0, 2.0, 80.0, 80.0, 150.0, 150.0, 2.0, 2.0, 72.0, 51.0, 29.0, 46.0, 10.0, 7.0, 42.272041375581644, 45.68879164565739, 72.18387587325509, 8.0, 27.006281622278333, 16.244833417370145, 10.0, 31.0, 35.0, 31.0, 51.0, 11.0, 24.79612428119684, 48.76386379332487, 8.000000000000052, 104.73165886004907, 15.799123331055451, 16.779328771191132, 3.000000000000501, 100.0, 242.0, 242.0, 2.0000000000000475, 4.800402845273522, 3.0000000000001097, 100.0, 8.0, 172.7285434564396, 46.82853656724763, 2.0000000000006546])
# config_05052023_v8 = np.array([70.0, 170.0, 0.0, 309.38296961545626, 94.95830972105306, 166.8082001546308, 333.46867682763207, 95.38184368122768, 40.0, 40.0, 150.0, 150.0, 2.0, 2.0, 80.0, 80.0, 150.0, 150.0, 2.0, 2.0, 72.0, 51.0, 29.0, 46.0, 10.0, 7.0, 45.74968505556718, 46.10466599404622, 8.0, 60.68600201786133, 16.00125977773132, 2.0, 10.0, 31.0, 35.0, 31.0, 51.0, 11.0, 12.287238981286016, 44.88748281429583, 8.0, 240.1547709755534, 2.0, 13.782279021864408, 3.0, 100.0, 242.0, 8.0, 2.0, 2.0, 75.94187095948752, 3.0000000000000013, 242.0, 188.4836348070854, 2.000000000000054, 70.0])
# delta_vector = config_05052023_v8 - config_05052023_v6
# delta = delta_vector/10.
# # configs = [f"config_22052023_v6-v8_{i}" for i in range(1,11)]
# configs = [f"config_22052023_v6-v8_{i}" for i in range(0,1)]
# print(configs)
# exit(0)


# config_05052023_v6 = [70.0, 170.0, 0.0, 353.0780575329521, 125.08255586355432, 184.8344375295139, 150.19262843951793, 186.81232063446174, 40.0, 40.0, 150.0, 150.0, 2.0, 2.0, 80.0, 80.0, 150.0, 150.0, 2.0, 2.0, 72.0, 51.0, 29.0, 46.0, 10.0, 7.0, 42.272041375581644, 45.68879164565739, 72.18387587325509, 8.0, 27.006281622278333, 16.244833417370145, 10.0, 31.0, 35.0, 31.0, 51.0, 11.0, 24.79612428119684, 48.76386379332487, 8.000000000000052, 104.73165886004907, 15.799123331055451, 16.779328771191132, 3.000000000000501, 100.0, 242.0, 242.0, 2.0000000000000475, 4.800402845273522, 3.0000000000001097, 100.0, 8.0, 172.7285434564396, 46.82853656724763, 2.0000000000006546]


# configs = []
# for conf in range(len(config_05052023_v6)):
#     if conf != 2 and conf < len(config_05052023_v6) - 1:
#         configs.append(f"config_05052023_v6_scan_{conf}_0")
#         configs.append(f"config_05052023_v6_scan_{conf}_1")
#     elif conf == len(config_05052023_v6) - 1:
#         configs.append(f"config_05052023_v6_scan_{conf}_0")
#         configs.append(f"config_05052023_v6_scan_{conf}_1")


# config_01052023 = [f"config_01052023_v{i}" for i in range(1,12)]
# config_05052023 = [f"config_05052023_v{i}" for i in range(1,14)]
# configs = config_01052023 + config_05052023
# configs = ["config_v6_low_25", "config_v6_low_50"]
configs = ["config_v6_paral", "config_v6_paral_warm_reduced"]
date = date.today()
# os.system("export CONDOR_FOLDER=${PWD}")
# os.system("export EOS_DATA=/eos/user/e/edursov/ship_data")
# os.system("export EOS_PUBLIC=/eos/experiment/ship/user/edursov")
# os.system(f"export SUBTYPE={sub_type}")
os.system(f"source $PWD/vars.sh {sub_type}")
os.system("source /cvmfs/ship.cern.ch/SHiP-2022/May/setUp.sh")
if not os.path.exists("start_ali.sh"):
    os.system("alienv printenv FairShip/latest >> start_ali.sh")


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

for conf in configs:
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
              --geofile {conf}.root \
              --sub_type {sub_type} \
              --number {number_of_jobs} \
              --input {input_file} \
              --of {output_folder}
              '''
    os.system(COMMAND)