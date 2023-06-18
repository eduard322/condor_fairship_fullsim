#!/usr/bin/env python2
from __future__ import division
import argparse
from multiprocessing import Pool
import numpy as np
import ROOT as r
import time
# Fix https://root-forum.cern.ch/t/pyroot-hijacks-help/15207 :
r.PyConfig.IgnoreCommandLineOptions = True
import shipunit as u
import rootUtils as ut
import logger as log
import os
import sys
from pathlib import Path
from copy import deepcopy
condor_path = os.environ['CONDOR_FOLDER']
EOS_PUBLIC = os.environ['EOS_PUBLIC']
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

def p_split(mom, soft = 10, hard = 150):
    if mom < soft:
        key = 0
    elif mom > soft and mom < hard:
        key = 1
    else:
        key = 2
    return key

def get_all_kinematics(event, hit):
    kinematics = {}
    trid = hit.GetTrackID()
    assert trid > 0
    kinematics["trid"] = hit.GetTrackID()
    kinematics["W"] = event.MCTrack[trid].GetWeight()
    kinematics["x"], kinematics["y"], kinematics["z"] = hit.GetX(), hit.GetY(), hit.GetZ()
    kinematics["px"], kinematics["py"], kinematics["pz"] = hit.GetPx(), hit.GetPy(), hit.GetPz()
    kinematics["pt"] = np.hypot(kinematics["px"], kinematics["py"])
    kinematics["P"] = np.hypot(kinematics["pz"], kinematics["pt"])
    kinematics["pid"] = hit.PdgCode()
    kinematics["detid"] = hit.GetDetectorID()
    kinematics["station"] = kinematics["detid"] // 10000000
    kinematics["mom_key"] = p_split(kinematics["P"])
    return kinematics
 
def get_track_rates(event, momentum_trid):
    output = {}
    output_unw = {}
    track_list = []
    momentum_trid_copy = deepcopy(momentum_trid)
    tracking_hits = momentum_trid_copy[3:]
    # print(len(tracking_hits), len(momentum_trid), tracking_hits, momentum_trid)
    tracking_hits_ids = []
    for k in range(4):
        if not len(tracking_hits[k].keys()):
            track_store = [-1]
        else:
            track_store = list(tracking_hits[k].keys())
        tracking_hits_ids.append(track_store)
    # print(tracking_hits_ids)
    for tr in np.unique(tracking_hits_ids):
        if tr < 0:
            continue
        n = 0
        for j in flatten(tracking_hits_ids):
            if j < 0:
                continue
            if j == tr:
                n += 1
        if n >= 3 and tr in tracking_hits_ids[0] and tr in tracking_hits_ids[3]:
            # print(tracking_hits[0][int(tr)])
            # output[tracking_hits[0][int(tr)]['mom_key']] += event.MCTrack[int(tr)].GetWeight()
            # output_unw[tracking_hits[0][int(tr)]['mom_key']] += 1
            tracking_hits[0][int(tr)]['plane'] = 7
            track_list.append(tracking_hits[0][int(tr)])
    # if track_list:
    #     print(track_list)
    return output, output_unw, track_list

def get_shield(input):
    input1 = input.split("/")
    geoFile = find_file("geo*", input)[0]
    # geoFile = find_file("geo*", outer_path)[0]
    #geoFile = outer_path + "/geofile_full.conical.MuonBack-TGeant4.root"
    shield_zx, shield_zy = muon_shield(geoFile)
    shield_y = shield_zy['y'][-4]+10
    shield_x = shield_zx['x'][-4]+10
    shield_z = np.array(deepcopy(shield_zx['z']))
    shield_z[shield_z==None]=-10000
    shield_z = np.max(shield_z)
    return shield_x, shield_y, shield_z

def process_batch(batch, output, shield, batch_check):
    # outer_path = "/".join([i for i in args.inputfile.split("/")[:-2]])
    #print(outer_path)

    #print(shield_x, shield_y, shield_z)
    ch = r.TChain('cbmsim')
    # tree_walk = list(os.walk("/".join([i for i in args.inputfile.split("/")[:-2]])))
    # for path in [tree_walk[i][0] for i in range(len(tree_walk[1:-1]))]:
    #     print(os.path.join(path, 'ship.conical.MuonBack-TGeant4.root'))
    #     ch.Add(os.path.join(path, 'ship.conical.MuonBack-TGeant4.root'))
    for file in batch:
        # print(str(file), type(file))
        ch.Add(str(file))

    # global_info = [[] for _ in range(8)]
    global_info = []
    sense_planes = [f"sco_{i}Point" for i in range(3)] + ["strawtubesPoint"]

    for I, event in enumerate(ch):
        # first 3 -- snd planes, last 4 -- tracking stations
        momentum_trid = [{} for _ in range(7)]
        tr_id_stations = {}
        if batch_check:
            if I % 100000 == 0: print('event ',I,' ',time.ctime())
        for iteration, plane in enumerate(sense_planes):
            for hit in eval("event." + plane):
                if not hit:
                    continue
                if not hit.GetEnergyLoss() > 0:
                    continue
                kin = get_all_kinematics(event, hit)
                if abs(kin['pid']) != 13:
                    continue
                #####
                key_proj,x_key,y_key = check_projection(np.array([kin['x'],kin['y'],kin['z']]), 
                                                          np.array([kin['px'],kin['py'],kin['pz']]), 
                                                          shield[0], shield[1], shield[2]) 
                kin['key_proj'] = key_proj
                #####
                if plane == "strawtubesPoint":
                    iteration_0 = iteration + kin["station"] - 1
                else:
                    iteration_0 = iteration
                if kin['trid'] not in momentum_trid[iteration_0].keys():
                    # momentum_trid[iteration_0][kin['trid']] = (kin['P'], kin['W'], key_proj, 
                    #                                          kin['x'],kin['y'],kin['z'], 
                    #                                          kin['px'],kin['py'],kin['pz'])
                    kin["plane"] = iteration_0
                    momentum_trid[iteration_0][kin['trid']] = kin
                    # global_info[iteration_0].append(momentum_trid[iteration_0][kin['trid']])
                    global_info.append(momentum_trid[iteration_0][kin['trid']])
        
        flux_tr, flux_tr_unw, tracks = get_track_rates(event, momentum_trid)
        if len(tracks) > 0:
            print(tracks, "\n", len(global_info))
            for track in tracks:
                global_info.append(track)

    # print(global_info[0].keys())
    # columns = ["P", "W", "x", "y","z", "px","py","pz", "key_proj"]
    columns = ['trid', 'W', 'x', 'y', 'z', 'px', 'py', 'pz', 'pt', 'P', 'pid', 'detid', 'station', 'mom_key', 'key_proj', 'plane']
    # print(global_info[1977])
    # for i, x in enumerate(global_info):
    #     print(i, x.values())
    # print(global_info[0].values())
    df_np = np.array([list(global_info[i].values()) for i in range(len(global_info))])
    # print(check[0])
    # for x in check:
    #      print(len(x))
    # df_np = np.concatenate([np.array(x, dtype=np.float64) for x in global_info])
    if ch.GetEntries() > 0:
        df = r.RDF.MakeNumpyDataFrame({key: np.array(df_np[:,i]) for i, key in enumerate(columns)})
    # ... or print the content
    #df.Display().Print()
    # ... or save the data as a ROOT file
        df.Snapshot('tree', output)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to create flux maps.')
    parser.add_argument(
        '-i',
        '--inputfile',
        type=str,
        help='''Simulation results to use as input. '''
        '''Supports retrieving files from EOS via the XRootD protocol.''')
    parser.add_argument(
        '-s',
        '--single',
        type=int,
        default = 1,
        help="single file -- 1, splitted data  -- 0")
    parser.add_argument(
        '-p',
        '--pseudoBatch',
        type=int,
        default=0,
        help="pseudobatch")
    parser.add_argument(
        '-o',
        '--output',
        type =str,
        default='output_full.root',
        help="output file")
    parser.add_argument(
        '--mp',
        type =int,
        default=0,
        help="mp")
    parser.add_argument(
        '-n',
        '--num_processes',
        type=int,
        default=4,
        help="number of parallel processes to use")
    parser.add_argument(
        '--eos',
        type=int,
        default=0,
        help="0 -- ship eos, 1 -- private eos")
    parser.add_argument(
        '--condor',
        type=int,
        default=0,
        help="0 -- lxplus, 1 -- htcondor")
    
    
    args = parser.parse_args()
    # folder = "/eos/experiment/ship/user/edursov/SC_config_04032023_spill_07032023/"

    folder = args.inputfile
    print(args.inputfile)
    if not args.condor:
        inp = os.path.join(EOS_PUBLIC, args.inputfile)
        shield = get_shield(os.path.join(EOS_PUBLIC, folder.split("/")[0]))
    else:
        inp = args.inputfile
        shield = get_shield(folder.split("/")[0])
    fileName = "ship.conical.MuonBack-TGeant4.root"
    basePath = sorted(Path(inp).glob(f'**/{fileName}'))
    print("{} files to read in {}".format(len(basePath), inp))
    if args.pseudoBatch:
        basePath = np.array_split(basePath, int(len(basePath)/args.pseudoBatch))
    else:
        basePath=[basePath]
    
    if args.single:
        basePath = [[os.path.join(inp, fileName)]]


    # r.gErrorIgnoreLevel = r.kWarning
    # r.gROOT.SetBatch(True)
    batches_in_total= len(basePath)
    

    output_files = []
    starting_time = time.time()
    if not args.mp:
        for iteration, batch in enumerate(basePath):
            if args.pseudoBatch:
                print(f"working on {iteration+1} batch out of {batches_in_total}, {time.ctime()}")
                output_files.append(args.output.split(".")[0] + f"_{iteration}.root")
                process_batch(batch, args.output.split(".")[0] + f"_{iteration}.root", shield, False)
            else:
                print(f"working without batches, starting from {time.ctime()}")
                process_batch(batch, args.output, shield, True)
                print(f"working without batches, ending {time.ctime()}")

    else:
        with Pool(args.num_processes) as pool:
            for iteration, batch in enumerate(basePath):
                if args.pseudoBatch:
                    print(f"working on {iteration+1} batch out of {batches_in_total}, {time.ctime()}")
                    output_file = args.output.split(".")[0] + f"_{iteration}.root"
                    output_files.append(output_file)
                    pool.apply_async(process_batch, (batch, output_file, shield, False))
                else:
                    print(f"working without batches, starting from {time.ctime()}")
                    pool.apply_async(process_batch, (batch, args.output, shield, True))
                    print(f"working without batches, ending {time.ctime()}")
            pool.close()
            pool.join()
    ending_time = time.time()
    print(f"Time spent: {(ending_time - starting_time)/60} min")

    if args.pseudoBatch:
        with open("output_list", "w") as f:
            for x in output_files:
                f.write(x + "\n")
        os.system(f"hadd -f {args.output} @output_list")
        os.remove("output_list")