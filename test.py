
print "\n\n \t LAUNCHING TEST SCRIPT :: ALI SAAD 2014 \n\n"


import cimpy as cim
import matplotlib.pyplot as plt
import numpy as np

import mayavi.mlab as ml
from mpl_toolkits.mplot3d import Axes3D




mesh = cim.Tmesh("CET_petit.t") # para_mesh.t  # CET_petit # mesh3d
#mesh.View("mpl")
#mesh.View("myv")



############# 3D  VIEW function MAYAVI :: use with mesh3d.t ##############
#
#x1 = []
#y1 = []
##z1 = []
#for couple in mesh.nodes_dict.values():
#        x1.append(couple[0])
#        y1.append(couple[1])
##        z1.append(couple[1])
#        
#x1 = np.array(x1)
#y1 = np.array(y1)
#z1 = np.zeros_like(x1)
#triangles = []
#
#real_elements_dict = dict(mesh.elements_dict)
#
## the 'enumerate' function is really nice !
#for i,connec_list in enumerate(real_elements_dict.values()):
#    if 0 in connec_list : del real_elements_dict[i+1]
#    # i+1 because enumerate starts at 0 while my dict starts at 1
#
#
#for trigl in real_elements_dict.values():
#    triangles.append(tuple(trigl))
#        
#ml.triangular_mesh(x1, y1, z1, triangles, 
#                   representation = 'wireframe')   

############# 3D  VIEW function SCATTER3D :: use with mesh3d.t ##############

#real_elements_dict = dict(mesh.elements_dict)
#
## the 'enumerate' function is really nice !
#for i,connec_list in enumerate(real_elements_dict.values()):
#   if 0 in connec_list : del real_elements_dict[i+1]
#   # i+1 because enumerate starts at 0 while my dict starts at 1
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
##
#ax.scatter3D(x, y, z, c='r', marker='x')
##
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