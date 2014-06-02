print "ffffffffffffffuuuuucckkk"


import cimpy as cim
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D


mesh = cim.Tmesh("para_mesh.t") # para_mesh.t  # CET_petit # mesh3d

mesh.View(color='r',
          linewidth=1.0,
          marker = 'x'
          )


elements = mesh.elements_dict


############# 3D  VIEW function MAYAVI ##############
##real_elements_dict = dict(mesh.elements_dict)
##
### the 'enumerate' function is really nice !
##for i,connec_list in enumerate(real_elements_dict.values()):
##    if 0 in connec_list : del real_elements_dict[i+1]
##    # i+1 because enumerate starts at 0 while my dict starts at 1
##
### The lists have to be cast into numpy arrays before using the TRI plot
##nodes_coord = np.asarray(mesh.nodes_dict.values())
##triangles = np.asarray(real_elements_dict.values())
##
### Extracting columns
##x = nodes_coord[:,0]
##y = nodes_coord[:,1]
##if mesh.dimNode == 3:
##     z = nodes_coord[:,2]
##
##fig = plt.figure()
##ax = fig.add_subplot(111, projection='3d')
##
##ax.scatter3D(x, y, z, c='r', marker='o')
##
##ax.set_xlabel('X Label')
##ax.set_ylabel('Y Label')
##ax.set_zlabel('Z Label')
##
##plt.show()
##
##

############# 3D  VIEW function SCATTER3D :: use with mesh3d ##############

#real_elements_dict = dict(mesh.elements_dict)
#
## the 'enumerate' function is really nice !
#for i,connec_list in enumerate(real_elements_dict.values()):
#    if 0 in connec_list : del real_elements_dict[i+1]
#    # i+1 because enumerate starts at 0 while my dict starts at 1
#
## The lists have to be cast into numpy arrays before using the TRI plot
#nodes_coord = np.asarray(mesh.nodes_dict.values())
#triangles = np.asarray(real_elements_dict.values())
#
## Extracting columns
#x = nodes_coord[:,0]
#y = nodes_coord[:,1]
#if mesh.dimNode == 3:
#     z = nodes_coord[:,2]
#
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#
#ax.scatter3D(x, y, z, c='r', marker='o')
#
#ax.set_xlabel('X Label')
#ax.set_ylabel('Y Label')
#ax.set_zlabel('Z Label')
#
#plt.show()


#############  VIEW function ##############

#real_elements_dict = dict(mesh.elements_dict)
#
## the 'enumerate' function is really nice !
#for i,connec_list in enumerate(real_elements_dict.values()):
#    if 0 in connec_list : del real_elements_dict[i+1]
#    # i+1 because enumerate starts at 0 while my dict starts at 1
#
## The lists have to be cast into numpy arrays before using the TRI plot
#nodes_coord = np.asarray(mesh.nodes_dict.values())
#triangles = np.asarray(real_elements_dict.values())
#
## Extracting columns
#x = nodes_coord[:,0]
#y = nodes_coord[:,1]
#if mesh.dimNode == 3:
#     z = nodes_coord[:,2]
#
#
#
#plt.figure()
#plt.gca().set_aspect('equal')
#plt.triplot(x, y, triangles, "b-")
#plt.title('Mesh')
#
#plt.show()