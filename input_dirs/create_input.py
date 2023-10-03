import os 
import ROOT


output_strings = []
file_name = "/eos/experiment/ship/data/Mbias/background-prod-2018/pythia8_Geant4_10.0_withCharmandBeauty{}_mu.root"
number_of_files = 67
for i in range(number_of_files):
    root_file = ROOT.TFile(file_name.format(i*1000))
    tree = root_file.Get("cbmsim")
    output_strings.append(f"{file_name.format(i*1000)}, {str(tree.GetEntries() - 1)}")
with open("input_file_10_spills.txt", "w") as f:
    for j in range(10):
        for i in range(number_of_files):
            print(output_strings[i] + f", {number_of_files*j + i}", file = f)


