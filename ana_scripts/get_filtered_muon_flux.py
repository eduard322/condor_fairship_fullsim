#!/usr/bin/env python2
from __future__ import division
import argparse
import numpy as np
import ROOT as r
# Fix https://root-forum.cern.ch/t/pyroot-hijacks-help/15207 :
r.PyConfig.IgnoreCommandLineOptions = True
import shipunit as u
import rootUtils as ut
import logger as log


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
    SUM = 0
    I = 0
    for event in ch:
        ids = [[] for _ in range(4)]
        trids = {}
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
                #list_key = 2
                P = np.hypot(pz, pt)
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
                    muon = True
                    #print(I, weight, "\t", P, x, y, z, trid, station)
                    SUM += 1
                    if trid in ids[station-1]:
                        continue
                       #ids[station-1][trid] = weight
                    ids[station-1].append(trid)
                    trids[trid] = list_key
                    #print("UNIQUE:",I, weight, "\t", P, x, y, z, trid, station)
                    B_ids[station-1][list_key] += weight
                    B_ids_unw[station-1][list_key] += 1
                    #print("SUM:", B_ids, B_ids_unw)
        unique_tr = np.unique(flatten(ids))
        for tr in unique_tr:
            n = 0
            for j in flatten(ids):
                if j == tr:
                    n += 1
            #print("n = ", n, tr, trids[tr], event.MCTrack[int(tr)].GetWeight())
            if n >= 3 and tr in ids[0] and tr in ids[3]:
                filtered_muons[0][trids[tr]] += event.MCTrack[int(tr)].GetWeight()
                filtered_muons_unw[0][trids[tr]] += 1
        # if muon == True:
        #     print("!!!!")
        #     print(filtered_muons, filtered_muons_unw)
        #     print("!!!!")
        
                    

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


if __name__ == '__main__':
    r.gErrorIgnoreLevel = r.kWarning
    r.gROOT.SetBatch(True)
    main()
