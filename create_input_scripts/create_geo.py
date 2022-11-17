import sys
import numpy as np
import ROOT as r
from array import array
def generate_magnet_geofile(geofile, magnet_parameters):
 default_magnet_config = np.array([70.0, 170.0, 208.0, 207.0, 281.0, 248.0, 305.0,
 242.0, 40.0, 40.0, 150.0, 150.0, 2.0, 2.0, 80.0, 80.0, 150.0, 150.0, 2.0, 2.0,
 72.0, 51.0, 29.0, 46.0, 10.0, 7.0, 54.0, 38.0, 46.0, 192.0, 14.0, 9.0, 10.0,
 31.0, 35.0, 31.0, 51.0, 11.0, 3.0, 32.0, 54.0, 24.0, 8.0, 8.0, 22.0, 32.0,
 209.0, 35.0, 8.0, 13.0, 33.0, 77.0, 85.0, 241.0, 9.0, 26.0])

 fixed_ranges = [(0, 2), (8, 20)]
 mask = [index for interval in fixed_ranges for index in range(*interval)]
 fixed_params_mask = np.zeros(len(default_magnet_config), dtype=bool)
 fixed_params_mask[mask] = True

 full_parameters = np.zeros(len(default_magnet_config))
 full_parameters[fixed_params_mask] = default_magnet_config[fixed_params_mask]
 full_parameters[~fixed_params_mask] = np.array([float(x.strip()) for x in magnet_parameters.split(',')], dtype=float)

 f = r.TFile.Open(geofile, 'recreate')
 parray = r.TVectorD(len(full_parameters), array('d', full_parameters))
 parray.Write('params')
 f.Close()
 print('Geofile constructed at ' + geofile)

if __name__ == '__main__':
 #generate_magnet_geofile(sys.argv[1], sys.argv[2])
 
 #points = "208.0, 207.0, 281.0, 181.555, 223.283, 177.162, 72.0, 51.0, 29.0, 46.0, 10.0, 7.0, 54.0, 38.0, 46.0, 192.0, 14.0, 9.0, 10.0,31.0, 35.0, 31.0, 51.0, 11.0, 3.0, 32.0, 54.0, 24.0, 8.0, 8.0, 22.0, 32.0,209.0, 35.0, 8.0, 13.0, 33.0, 77.0, 85.0, 241.0, 9.0, 26.0"
 #points = "197.0, 248.0, 262.0, 199.0, 225.0, 315.0, 28.0, 100.0, 207.0, 234.0, 9.0, 70.0, 60.0, 52.0, 110.0, 234.0, 1.0, 32.0, 78.0, 79.0, 148.0, 234.0, 70.0, 29.0, 3.0, 98.0, 187.0, 145.0, 9.0, 1.0, 90.0, 63.0, 20.0, 171.0, 70.0, 1.0, 100.0, 100.0, 39.0, 167.0, 55.0, 50.0"
 points = "164.0, 208.0, 156.0, 218.0, 243.0, 274.0, 63.0, 100.0, 98.0, 198.0, 10.0, 47.0, 43.0, 63.0, 20.0, 234.0, 1.0, 9.0, 95.0, 56.0, 24.0, 195.0, 59.0, 35.0, 21.0, 77.0, 67.0, 117.0, 14.0, 1.0, 99.0, 50.0, 24.0, 229.0, 47.0, 21.0, 67.0, 100.0, 130.0, 159.0, 64.0, 36.0"
 #points = "70.0, 170.0, 209.5, 205.3, 279.3, 173.9, 209.5, 177.5, 40.0, 40.0, 150.0, 150.0, 2.0, 2.0, 80.0, 80.0, 150.0, 150.0, 2.0, 2.0, 87.8, 54.3, 29.7, 54.2, 9.7, 7.5, 53.7, 37.7, 45.7, 192.3, 14.9, 9.1, 8.7, 31.7, 37.2, 32.8, 51.0, 11.4, 3.0, 32.2, 56.4, 23.6, 8.1, 8.3, 21.9, 31.4, 210.2, 35.2, 8.0, 16.6, 34.5, 76.2, 85.3, 242.0, 9.0, 25.7" # 18102022 version
 generate_magnet_geofile(sys.argv[1], points)

