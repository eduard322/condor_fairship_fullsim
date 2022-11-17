import ROOT as r 

path = "/eos/experiment/ship/data/Mbias/background-prod-2018/"


filenames = []
for i in range(20):
    if i == 0:
        input_file = path + f"pythia8_Geant4_1.0_c{i}_mu.root"
    else:
        input_file = path + f"pythia8_Geant4_1.0_c{i}000_mu.root"
    root_file = r.TFile(input_file)
    tree = root_file.Get("cbmsim")
    filenames.append(input_file + ", " + str(tree.GetEntries()) + f", {i}")
        #filenames.append(input_file + ", " + str(tree.GetEntries()) + f", {i}")

FILE = open("low_energy_cut_input.txt", "w")

for filename in filenames:
    FILE.write(filename + "\n")

FILE.close()
