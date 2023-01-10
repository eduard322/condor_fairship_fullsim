import numpy as np
import sys

num_dir = 67
num = 20

Data = []
filenames = []
DIR = sys.argv[1]
R_FILE = sys.argv[2]
for i in range(num_dir):
    print(f"Reading {i} set out of {num_dir}")
    for j in range(1, num+1):
        try:
            if int(R_FILE) < 3: 
            	filename = "/eos/user/e/edursov/ship_data/{DIR}/{dir}/{sub}/".format(DIR = DIR,dir=str(i),sub=str(j)) + f"energy_filtered_keys_sco_{R_FILE}Point"
            else:
                filename = "/eos/user/e/edursov/ship_data/{DIR}/{dir}/{sub}/".format(DIR = DIR,dir=str(i),sub=str(j)) + f"energy_filtered_keys"
            print(filename)
            file = open(filename, 'r')
        except IOError:
            print(i, j, "doesn't exist")
            continue
        #filenames.append("/eos/user/e/edursov/ship_data/{DIR}/{dir}/{sub}/".format(DIR = DIR,dir=str(i),sub=str(j)))
        #print(list(map(float, file.readline().split())))
        x = file.readline().split()
        while x:
            if len(x) > 1:
                Data.append([float(x[i]) for i in range(len(x))])
            x = file.readline().split()
        file.close()
#for filename in filenames

#merged_data_shield = np.concatenate([np.loadtxt(filenames[0] + "energy_filtered_shield")] + [np.loadtxt(filename + "energy_filtered_shield") for filename in filenames[1:3]], axis = 1)
#merged_data_walls = np.concatenate([np.loadtxt(filenames[0] + "energy_filtered_walls")] + [np.loadtxt(filename + "energy_filtered_walls") for filename in filenames[1:3]], axis = 1)

#print(np.array(Data))
if int(R_FILE) < 3:
	np.savetxt(f"/eos/user/e/edursov/ship_data/{DIR}/" + f"output_merged_energies_filtered_sco_{R_FILE}Point", np.array(Data))
else:
	np.savetxt(f"/eos/user/e/edursov/ship_data/{DIR}/" + f"output_merged_energies_filtered_strawtubes", np.array(Data))
