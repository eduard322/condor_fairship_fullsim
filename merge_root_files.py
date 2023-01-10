import os, sys


EOS_DATA = os.environ['EOS_DATA']
OUTPUT = "optimized_snd_scor_planes_18102022"

for k in range(3):
    os.system(f"hadd -f {EOS_DATA}/{OUTPUT}/{OUTPUT}_snd_merged_{k}.root {EOS_DATA}/{OUTPUT}/*/*/output_snd_planes_{k}.root")

#os.system(f"hadd -f {EOS_DATA}/{OUTPUT}/{OUTPUT}_tr_merged.root {EOS_DATA}/{OUTPUT}/*/*/output_tr.root")