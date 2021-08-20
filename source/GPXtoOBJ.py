import gpxpy
import gpxpy.gpx
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy import interpolate
import sys

interp_types = ["cubic", "linear", "nearest"]
interp = "linear"

if(len(sys.argv) == 4):
    path = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
elif(len(sys.argv) == 2):
    path = sys.argv[1]
    width = 100
    height = 100
elif(len(sys.argv) == 5):
    path = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    interp = interp_types[int(sys.argv[4])]
else:
    print("Error.\nUsage: <path> <width> <height>")
    print(sys.argv)
    exit()

def MapToObj(m, obj):
    verts = []
    tex = []
    pairs = []
    tex_size = 1/(len(m)-1)
    for i in range(len(m)):
        for j in range(len(m[0])):
            if(math.isnan(m[i][j])):
                verts.append((j, 0, i))
            else:
                verts.append((j, m[i][j], i))
            tex.append((j*tex_size, i*tex_size, 0))
            if((not i == len(m)-1) and (not j == len(m[0])-1)):
                pairs.append((i*len(m)+j+1, (i+1)*len(m)+j+1, i*len(m)+j+2))
                pairs.append(((i+1)*len(m)+j+2, i*len(m)+j+2, (i+1)*len(m)+j+1))

    out = "\n"
    for i in verts:
        out += "v {0} {1} {2}\n".format(format(i[0], ".4f"), format(i[1], ".4f"), format(i[2], ".4f"))
    out+="\n"
    for i in tex:
        out += "vt {0} {1} {2}\n".format(format(i[0], ".4f"), format(i[1], ".4f"), format(i[2], ".4f"))
    out+="\nvn 0.0000 1.0000 0.0000\n\no Mesh\ng Mesh\n"
    for j, i in enumerate(pairs):
        print(j, i)
        out += "f {0}/{0}/1 {1}/{1}/1 {2}/{2}/1\n".format(i[0], i[1], i[2])           
    
    f = open(obj, "w")
    f.write(out)
    f.close()
    print("Vertices: {0}\nTris: {1}\n-------------------".format(len(verts), len(pairs)))
    return m

mesh_map = []

for i in range(height):
    mesh_map.append([])
    for j in range(width):
        mesh_map[i].append(np.nan)


gpx_file = open(path, 'r')
gpx = gpxpy.parse(gpx_file)
x = []
y = []
elev = []
mostx = 0
mosty = 0
leastx = -999999
leasty = 999999
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            x.append(point.longitude)
            y.append(point.latitude)
            elev.append(point.elevation)
            if(point.longitude < mostx):
                mostx = point.longitude
            if(point.latitude > mosty):
                mosty = point.latitude
            if(point.longitude > leastx):
                leastx = point.longitude
            if(point.latitude < leasty):
                leasty = point.latitude

            

for i in range(len(x)):
    #x[i] = min(math.floor(((x[i]-leastx)/(mostx-leastx))*100), 99)
    #y[i] = min(math.floor(((y[i]-leasty)/(mosty-leasty))*100), 99)
    xx = min(math.floor(((x[i]-leastx)/(mostx-leastx))*width), width-1)
    yy = min(math.floor(((y[i]-leasty)/(mosty-leasty))*height), height-1)
    mesh_map[yy][xx] = elev[i]
m1 = mesh_map

mesh_map = np.array(mesh_map)
x_ = np.arange(0, mesh_map.shape[1])
y_ = np.arange(0, mesh_map.shape[0])
#mask invalid values
mesh_map = np.ma.masked_invalid(mesh_map)
xx, yy = np.meshgrid(x_, y_)
#get only the valid values
x1 = xx[~mesh_map.mask]
y1 = yy[~mesh_map.mask]
newarr = mesh_map[~mesh_map.mask]

GD1 = interpolate.griddata((x1, y1), newarr.ravel(),
                          (xx, yy),
                             method=interp)
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
axs[1].imshow(GD1)
axs[0].imshow(m1)
plt.show()
MapToObj(GD1.tolist(), path.split(".")[0]+".obj")
print("Done.")
