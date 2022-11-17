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


def check_projection(rayPoint, rayDirection):
	x = rayPoint[0] - (rayPoint[2] - (-3170))*rayDirection[0]/rayDirection[2]
	y = rayPoint[1] - (rayPoint[2] - (-3170))*rayDirection[1]/rayDirection[2]
	if (-190 < x and x < 190) and (-327.9 < y and y < 327.9):
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

    ch = r.TChain('cbmsim')
    ch.Add(args.inputfile)
    n = ch.GetEntries()
    B_ids = [[0,0,0] for _ in range(4)]
    B_ids_unw = [[0,0,0] for _ in range(4)]
    filtered_muons = [[0,0,0]]
    filtered_muons_unw = [[0,0,0]]
    copy_filtered_muons = filtered_muons_unw[:]
    filtered_muons_energies_0 = []
    filtered_muons_energies_1 = []
    filtered_muons_energies_2 = []
    #filtered_muons_energies_walls = []
    normal_vector = np.array([0,0,1])
    I = 0
    for event in ch:
        momentum_trid_0 = {}
        momentum_trid_1 = {}
        momentum_trid_2 = {}
        I += 1
        # if I == 100:
        #     break
        muon = False
        if I % 100000 == 0:
            print(I)
            pass
        
        for hit in event.sco_0Point:
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
                #list_key = 2
                P = np.hypot(pz, pt)

                #####
                (key_proj,x_key,y_key) = check_projection(np.array([x,y,z]), np.array([px,py,pz]))
       
                #####

                pid = hit.PdgCode()
                assert pid not in [12, -12, 14, -14, 16, -16]
                detector_ID = hit.GetDetectorID()
                station = detector_ID // 10000000
                if abs(pid) == 13:
                    if trid not in momentum_trid_0.keys():
                        momentum_trid_0[trid] = (weight, key_proj, x,y,z, px,py,pz)
                        filtered_muons_energies_0.append(momentum_trid_0[trid])
        
        for hit in event.sco_1Point:
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
                #list_key = 2
                P = np.hypot(pz, pt)

                #####
                (key_proj,x_key,y_key) = check_projection(np.array([x,y,z]), np.array([px,py,pz]))

                #####

                pid = hit.PdgCode()
                assert pid not in [12, -12, 14, -14, 16, -16]
                detector_ID = hit.GetDetectorID()
                station = detector_ID // 10000000
                if abs(pid) == 13:
                    if trid not in momentum_trid_1.keys():
                        momentum_trid_1[trid] = (weight, key_proj, x,y,z, px,py,pz)
                        filtered_muons_energies_1.append(momentum_trid_1[trid])

        for hit in event.sco_2Point:
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
                #list_key = 2
                P = np.hypot(pz, pt)

                #####
                (key_proj,x_key,y_key) = check_projection(np.array([x,y,z]), np.array([px,py,pz]))

                #####

                pid = hit.PdgCode()
                assert pid not in [12, -12, 14, -14, 16, -16]
                detector_ID = hit.GetDetectorID()
                station = detector_ID // 10000000
                if abs(pid) == 13:
                    if trid not in momentum_trid_2.keys():
                        momentum_trid_2[trid] = (weight, key_proj, x,y,z, px,py,pz)
                        filtered_muons_energies_2.append(momentum_trid_2[trid])

    np.savetxt("energy_filtered_keys_sco_0Point", np.array(filtered_muons_energies_0))
    np.savetxt("energy_filtered_keys_sco_1Point", np.array(filtered_muons_energies_1))
    np.savetxt("energy_filtered_keys_sco_2Point", np.array(filtered_muons_energies_2))



if __name__ == '__main__':
    r.gErrorIgnoreLevel = r.kWarning
    r.gROOT.SetBatch(True)
    main()
