import os, sys


EOS_DATA = os.environ['EOS_DATA']
OUTPUT = "optimized_ecn3_spill_snd_scor_planes_fixed_fields_10012023_1"
OUTPUT= "optimized_snd_scor_planes_18102022"
OUTPUT="combi_ecn3_spill_snd_scor_planes_no_trench_26012023"
OUTPUT = "combi_cutoff_ecn3_spill_snd_scor_planes_28012023"
OUTPUT = "SC_test_1_spill_17022023"
for k in range(0):
    os.system(f"hadd -f {EOS_DATA}/{OUTPUT}/{OUTPUT}_snd_merged_{k}.root {EOS_DATA}/{OUTPUT}/*/*/output_snd_planes_{k}.root")

os.system(f"hadd -f {EOS_DATA}/{OUTPUT}/{OUTPUT}_tr_merged.root {EOS_DATA}/{OUTPUT}/*/*/output_tr.root")
