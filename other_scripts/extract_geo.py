import ROOT as r
import os, fnmatch
def find_file(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def muon_shield (lgeofile):
    geofile = r.TFile(lgeofile, 'r')
    geo = geofile.Get("FAIRGeom")
    cave_node = geo.GetTopNode()
    zy = {'y':[], 'z':[]}
    zx = {'x':[], 'z':[]}

    for node in cave_node.GetNodes():
        for subnode in node.GetNodes():
            nodeName = subnode.GetName()
            if "MagRetR" in nodeName and 'Absorb' not in nodeName: 
                subnode.Print()
                zShift = subnode.GetMatrix().GetTranslation()[2]
                lVol =  subnode.GetVolume().GetShape()
                dots = lVol.GetVertices()
                dZ = lVol.GetDZ()
                vetz = [dots[i] for i in range(16)]
                Y = vetz[1::2]
                zy['z'] = zy['z'] + [-dZ+zShift, -dZ+zShift, dZ+zShift, dZ+zShift, -dZ+zShift]
                zy['y'] = zy['y'] + [-max(Y[:4]), max(Y[:4]), max(Y[4:]), -max(Y[4:]), -max(Y[:4])]
                for key, item in zy.items():
                    item.append(None)
            if "MagTopL" in nodeName and 'Absorb' not in nodeName: 
                subnode.Print()
                zShift = subnode.GetMatrix().GetTranslation()[2]
                lVol =  subnode.GetVolume().GetShape()
                dots = lVol.GetVertices()
                dZ = lVol.GetDZ()
                vetz = [dots[i] for i in range(16)]
                X = vetz[::2]
                zx['z'] = zx['z'] + [-dZ+zShift, -dZ+zShift, dZ+zShift, dZ+zShift, -dZ+zShift]
                zx['x'] = zx['x'] + [-max(X[:4]), max(X[:4]), max(X[4:]), -max(X[4:]), -max(X[:4])]
                for key, item in zx.items():
                    item.append(None)
    return zx, zy