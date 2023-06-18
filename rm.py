import os


for i in range(0,20):
	os.system(f"condor_rm 6653150.{i}")
