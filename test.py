print "ffffffffffffffuuuuucckkk"


import cimpy as cim
import matplotlib.pyplot as plt
import numpy as np


mesh = cim.Tmesh("CET_petit.t") # para_mesh.t  # CET_petit

mesh.View(color='r', 
          linewidth=1.0,
#          marker = 'x',
#          markersize=2
          )








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
#
#plt.figure()
#plt.gca().set_aspect('equal')
#plt.triplot(x, y, triangles, "b-")
#plt.title('Mesh')
#
#plt.show() 