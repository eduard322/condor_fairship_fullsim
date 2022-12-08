#!/usr/bin/env python2
from __future__ import division
import argparse
from calendar import month_name
import numpy as np
import ROOT as r
# Fix https://root-forum.cern.ch/t/pyroot-hijacks-help/15207 :
r.PyConfig.IgnoreCommandLineOptions = True
import shipunit as u
import rootUtils as ut
import logger as log
from array import array
import os
import sys
from copy import deepcopy
condor_path = os.environ['CONDOR_FOLDER']
sys.path.append(os.path.join(condor_path, "other_scripts"))
from extract_geo import *

def check_projection(rayPoint, rayDirection, shield_x, shield_y, shield_z):
	x = rayPoint[0] - (rayPoint[2] - shield_z)*rayDirection[0]/rayDirection[2]
	y = rayPoint[1] - (rayPoint[2] - shield_z)*rayDirection[1]/rayDirection[2]
	if (-(shield_x + 10) < x and x < (shield_x + 10)) and (-(shield_y + 10)< y and y < (shield_y + 10)):
		return (True, x, y)
	else:
		return (False, x, y)

def flatten(arr):
    out = []
    for i in arr:
        for j in i:
                out.append(j)
    return out

def main():
    parser = argparse.ArgumentParser(description='Script to create flux maps.')
    parser.add_argument(
        'inputfile',
        help='''Simulation results to use as input. '''
        '''Supports retrieving files from EOS via the XRootD protocol.''')
    parser.add_argument(
        '-n',
        '--norm',
        default='flux',
        help='''File to write the flux maps to. '''
        '''Will be recreated if it already exists.''')
    

    args = parser.parse_args()

    outer_path = "/".join([i for i in args.inputfile.split("/")[:-2]])
    #print(outer_path)
    geoFile = find_file("geo*", outer_path)[0]
    shield_zx, shield_zy = muon_shield(geoFile)
    shield_y = shield_zy['y'][-4]+10
    shield_x = shield_zx['x'][-4]+10
    shield_z = np.array(deepcopy(shield_zx['z']))
    shield_z[shield_z==None]=-10000
    shield_z = np.max(shield_z)
    #print(shield_x, shield_y, shield_z)
    ch = r.TChain('cbmsim')
    ch.Add(args.inputfile)
    n = ch.GetEntries()
    B_ids = [[0,0,0] for _ in range(4)]
    B_ids_unw = [[0,0,0] for _ in range(4)]
    filtered_muons = [[0,0,0]]
    filtered_muons_unw = [[0,0,0]]
    copy_filtered_muons = filtered_muons_unw[:]
    filtered_muons_energies = []
    #filtered_muons_energies_walls = []
    normal_vector = np.array([0,0,1])


    SUM = 0
    I = 0
    for event in ch:
        ids = [[] for _ in range(4)]
        trids = {}
        momentum_trid = {}
        I += 1
        # if I == 100:
        #     break
        muon = False
        if I % 100000 == 0:
            print(I)
            pass
        
        for hit in event.strawtubesPoint:
            if hit:
                if not hit.GetEnergyLoss() > 0:
                    continue
                trid = hit.GetTrackID()
                assert trid > 0
                weight = event.MCTrack[trid].GetWeight()
                x = hit.GetX()
                y = hit.GetY()
                z = hit.GetZ()
                px = hit.GetPx()
                py = hit.GetPy()
                pz = hit.GetPz()
                pt = np.hypot(px, py)
                P = np.hypot(pz, pt)

                #####
                (key_proj,x_key,y_key) = check_projection(np.array([x,y,z]), np.array([px,py,pz]), shield_x, shield_y, shield_z)
       
                #####

                if P < 10.:
                   list_key = 0
                elif P > 150:
                   list_key = 2
                else:
                   list_key = 1
                pid = hit.PdgCode()
                assert pid not in [12, -12, 14, -14, 16, -16]
                detector_ID = hit.GetDetectorID()
                station = detector_ID // 10000000
                if abs(pid) == 13:
                    SUM += 1
                    if trid in ids[station-1]:
                        continue
                    ids[station-1].append(trid)
                    trids[trid] = list_key
                    if trid not in momentum_trid.keys():
                        momentum_trid[trid] = (P, weight, key_proj, x_key,y_key, x,y,z, px,py,pz)
                    B_ids[station-1][list_key] += weight
                    B_ids_unw[station-1][list_key] += 1
        unique_tr = np.unique(flatten(ids))
        for tr in unique_tr:
            n = 0
            for j in flatten(ids):
                if j == tr:
                    n += 1
            if n >= 3 and tr in ids[0] and tr in ids[3]:
                filtered_muons[0][trids[tr]] += event.MCTrack[int(tr)].GetWeight()
                filtered_muons_unw[0][trids[tr]] += 1
                if momentum_trid[tr][0]:
                    filtered_muons_energies.append(momentum_trid[tr])
                else:
                    filtered_muons_energies.append(momentum_trid[tr])

    
    print(filtered_muons, filtered_muons_unw)
    f = open("flux_4_energies", "w")
    for x,y in zip(B_ids_unw, B_ids):
        for x_0 in x:
            f.write(str(x_0) + "\t")
        for y_0 in y:
            f.write(str(y_0) + "\t")
        f.write("\n")
    f.close()
    f = open("flux_filtered_energies", "w")
    for x,y in zip(filtered_muons_unw, filtered_muons):
        for x_0 in x:
            f.write(str(x_0) + "\t")
        for y_0 in y:
            f.write(str(y_0) + "\t")
        f.write("\n")
    f.close()
    np.savetxt("energy_filtered_keys", np.array(filtered_muons_energies))
    #myFile = r.TFile.Open("file.root", "RECREATE")
    #myFile.WriteObject(array(filtered_muons_energies), "output_data")
    columns = ["P", "weight", "key_proj", "x_key","y_key", "x","y","z", "px","py","pz"]
    df_np = np.array(filtered_muons_energies, dtype=np.float64)
    df = r.RDF.MakeNumpyDataFrame({columns[i]: df_np[:,i] for i in range(len(columns))})
    # ... or print the content
    #df.Display().Print()
    # ... or save the data as a ROOT file
    df.Snapshot('tree', 'output_tr.root')

if __name__ == '__main__':
    r.gErrorIgnoreLevel = r.kWarning
    r.gROOT.SetBatch(True)
    main()
