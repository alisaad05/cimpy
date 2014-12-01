#!/usr/bin/env python

#import math
# import sys
import numpy as np
import matplotlib.pyplot as plt
import mayavi.mlab as ml # to use mayavi mlab  scripting tools and rendering
from mpl_toolkits.mplot3d import Axes3D #to use Scatter/Scatter 3D
from tvtk.api import tvtk


# import vtk

# All returned arrays are cast into either numpy or numarray arrays
#arr=numpy.array

# ALI: "self" in python is equivalent to "this" in C++

# TODO : implement class create_grid(filename) to link with Struct_mesh_generator.cpp ==> possible use of ctypes wrapping ??

# TODO:  check doctest to parse unit tests in docstrings and run them ... can replace the "tutoriaux_testes" in cimlib
# TODO:  https://docs.python.org/2/library/doctest.html

class Tmesh:
  """Mesh object containing nodes and elements, as well connectivity and dimension information"""
  
  def __init__(self, filename = None):
    """Creates a Tmesh object by reading the specified file."""
    
    if filename is None:
      print "CIMPY:: The mesh filename is not specified. Please input a valid mesh name with a .t extension" 
      self.name = "Maillage1" 
    else:
      if filename[-2:].lower() == ".t":
        print "CIMPY:: Mesh filename is valid and ready for reading ..."
        self.name = filename.split()[0]
#        self.point_array = [] # TODO: obsolete ... replaced by dictionary
        self.nodes_dict = {} # or =dict()        
        self.elements_dict = {} # or =dict()        
       
#        self.element_array = [] # TODO: obsolete ... replaced by dictionary
        self.Parse_input_file(filename)
      elif filename[-4:].lower() == ".msh":
        print "CIMPY:: Coming soon: convert " + filename + " to a cimlib compatible mesh format (Tmesh) ? "
	  # TODO link with gmsh2mtc.py
      else:
        raise Exception("ERROR: The extension of " +  filename + "  filename is not recognised")
      
      
  def unittest(self):
      """ Not implemented yet """
      print "My name is: " + self.name
      
  
  def Parse_input_file(self, filename):
      """ takes a .t mesh filename and read it into a Tmesh datastructure """
      f = open(filename)
      
      header = f.readline().strip().split()
      # TODO: add condition: if len(header) != 4 then ...
      self.nbNodes, self.dimNode,self.nbElements, self.dimElement = header
      
      self.nbNodes = int(self.nbNodes)
      self.nbElements = int(self.nbElements)
      self.dimElement = int(self.dimElement)
      self.dimNode = int(self.dimNode)
           
      for i in xrange(self.nbNodes): 
          node = f.readline().strip().split()
          self.nodes_dict[i+1] = map(float, node)
     
      # A fictitious node should be considered (but NOT USED FOR MESH VIEW)
      if self.dimNode == 2:
          self.nodes_dict[0]=[0,0]
      elif self.dimNode == 3:
          self.nodes_dict[0]=[0,0,0]
      else : raise Exception ("dimNode ("+ str(self.dimNode) + ") should be 2 or 3")
          
     # nodes_dict is a map of points IDs and their coordinates
     # To access the coordinates of a node:  nodes_dict[node_id]
     # To access a component in the coord: nodes_dict[node_id][component]
                      
      line = f.readline().strip().split()
#
      while len(line) == 0 : line = f.readline().strip().split()
      connectivity = line # first non blank line

 
      for i in xrange(self.nbElements):           
          self.elements_dict[i+1] = map(int, connectivity)
          connectivity = f.readline().strip().split()
          
      f.close()
      
      
  def View(self, engine = "mpl" , **kwargs):
      """ 
          Plots the mesh in a figure. Supports 2D and 3D mesh with two visualization backends. Call signature ::\n
         
                 Tmesh.View()
          
          - engine: 
            -  `mpl` to use a matplotlib as 2D and 3D scatter plotting backend
            -  `myv` (default) to use Mayavi for 2D and 3D mesh rendering (using `tvtk`)
          - kwargs:
              - if 'engine' argument is set to `mpl` then Matplotlib's keywords are used:
                  - linestyle or ls	: '-' , '--' , '-.' ...
                  - linewidth or lw	float value in points
                  - marker: 'x' , 'o' , 'v' ...
                  - color: 'r' (red), 'k' (black) , 'b' (blue) ...
                  - [check url: http://matplotlib.org/1.3.1/api/artist_api.html#module-matplotlib.lines] \n\n
          
          
         - if 'engine' argument is set to "myv" then Mayavi's keywords are used:
          
           - color:	the color of the vtk object. Overides the colormap, if any, when specified. This is specified as a triplet of float ranging from 0 to 1, eg (1, 1, 1) for white.
           - colormap:	type of colormap to use.
           - extent:	[xmin, xmax, ymin, ymax, zmin, zmax] Default is the x, y, z arrays extent. Use this to change the extent of the object created.
      """
      
      dim = self.dimNode 
      nb_points_real = self.GetNumberOfPoints()
      nb_points = nb_points_real + 1 # the fictitious node of index 0 and coordinates [0,0]
      
      
      ### a dict constructor is necessary so that the class's member
      ### dictionary wont be affected when fictitious triangles are suppressed
      real_elements_dict = dict(self.elements_dict)

      # the 'enumerate' function is really nice !
      for i,connec_list in enumerate(real_elements_dict.values()):
         if 0 in connec_list : del real_elements_dict[i+1]
         # i+1 because enumerate starts at 0 while my dict starts at 1 
     
      # The lists have to be cast into numpy arrays before using the TRI plot
      points = np.asarray(self.nodes_dict.values())
      simplexes = np.asarray(real_elements_dict.values())
     
      # Extracting columns
      x = points[:,0]
      y = points[:,1]
      
      if dim == 2:
          # points_2d is used in mayavi rendering
          points_2d = np.column_stack([points, np.zeros((nb_points,1))])
      elif dim == 3:  
          # z is used in matplotlib rendering
          z = points[:,2]
          # points_3d is used in mayavi rendering
          points_3d = points
    
    
      if engine == "mpl":
          
          if dim == 2:
              plt.figure()
              plt.gca().set_aspect('equal')
              plt.triplot(x, y, simplexes, **kwargs)
              plt.title('Mesh')
              plt.show() 
              
          elif  dim == 3:
              # TODO: add line connection between scattered points
              fig = plt.figure()
              ax = fig.add_subplot(111, projection='3d', aspect ='equal')
              ax.scatter3D(x, y, z, **kwargs)
              ax.set_xlabel('X Label')
              ax.set_ylabel('Y Label')
              ax.set_zlabel('Z Label')
              plt.axis()
              plt.show()
      
      elif engine == "myv":
              
          if dim == 2:
              #this way works
#              z = np.zeros_like(x)
#              triangles = []
#              for trigl in real_elements_dict.values(): triangles.append(tuple(trigl))
#              ml.triangular_mesh(x, y, z, triangles, representation = 'wireframe')  
              
              #another way
               simplex_type = 5  # = 10 for tetrahedron 
               ug = tvtk.UnstructuredGrid(points= points_2d)
              
          if dim == 3:
              simplex_type = tvtk.Tetra().cell_type  # = 10 for tetrahedron 
              ug = tvtk.UnstructuredGrid(points= points_3d)
              
          
          ug.set_cells(simplex_type, simplexes) 
          fig = ml.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), figure=ug.class_name[3:])
          surf = ml.pipeline.surface(ug, opacity=0.01)
          RGB= (0,0,0.5)
          #edge_color = tuple(i/255 for i in RGB)
          ml.pipeline.surface(ml.pipeline.extract_edges(surf), color= RGB )
      
      
  ### Getters ###    
      
  def GetNumberOfPoints(self):
      """ returns the total number of nodes in the mesh """
      return self.nbNodes
      
  def GetNumberOfElements(self):
      """ returns the total number of elements in the mesh """
      return self.nbElements
      
  def GetMeshPointDimension(self):
      """ returns the mesh dimension 2D or 3D """
      return self.dimNode
      
  def GetMeshElementDimension(self):
      """ returns the number of nodes in a single element """
      return self.dimElement
      
  def GetPointCoordinates(self, point_id):
      """ returns a node coordinates from the index """
      return self.nodes_dict[point_id]
      
  def NodesToFile(self, filename= None):
      """ returns an array containing the nodes coordinates """
     
      if filename is None:
         print "CIMPY:: The output filename is not specified ... aborting"
      else:
          g = open(filename, "w")
          for id in range(1,self.nbNodes+1): 
              x = str(self.nodes_dict[id][0])
              y = str(self.nodes_dict[id][1])
              if self.dimNode == 3: z = str(self.nodes_dict[id][2])
              else: z=""
                  
              g.write(x + "\t" + y + "\t" + z)
              if id < self.nbNodes : g.write("\n")
          g.close()
          
  def ElementsToFile(self, filename= None):
      """ returns an array containing the triangles / connectivity"""
      
      if filename is None:
         print "CIMPY:: The output filename is not specified ... aborting"
      else:
          g = open(filename, "w")
          for id in range(1,self.nbElements+1): 
             s= ""
             for node in self.elements_dict[id]:
                  s += str(node)+ "\t"
            
             if self.dimElement == 4: s += str(self.elements_dict[id][4])
               
             g.write(s)
             if id < self.nbElements : g.write("\n")
          g.close()
    
    
#  def GetArrayOfConnectivity(self, filename= None):
#      """ returns an array containing the elements nodes indices """
#      connec_list = []
#      for element in self.element_array:          
#          connec_list.append(element.connectivity) 
#      
#      if filename is not None:
#          g = open(filename, "w")
#          for element in self.element_array:  
#              g.write(element.GetConnectivityString(self.dimNode))
#          g.close()
#      
#      return connec_list         
          
      
  def GetElement(self, element_id):
      """ returns the element from the index"""
      """ not implemented """
      return element_id    
  
#==================================================             
     
#==================================================      
class Tnode:
  """Point object with coordinates and  index information"""
  
  def __init__(self, point_id, point_coords):
    """ Initializes the point (node) by its index and coordinates as arguments """
    self.index = point_id
    # mapping is necessary to convert string list to float coordinates
    self.coordinates = map(float,point_coords)
    
#  def GetCoordinateString(self, dimension):
#     if dimension == 2:
#         return str(self.coordinates[0]) + str("\t") + str(self.coordinates[1]) + str("\n")
#     elif dimension == 3:
#            return str(self.coordinates[0]) + str("\t") + str(self.coordinates[1]) + str("\t") + str(self.coordinates[2]) + str("\n")
#             
#==================================================

#==================================================
class Telement:
  """Element object with node indices and element index information"""
  
  def __init__(self, element_id, element_connectivity, input_mesh):
    """ Initializes the element by its index and the indices of the its nodes as arguments """
    # element_id is the index of the element    
    self.index = element_id
    # connectivity is a list of indices (3 in 2D, 4 in 3D) of the triangle/tetrahedron nodes
    self.connectivity = map(int, element_connectivity)
    self.dimension = input_mesh.GetMeshElementDimension()
    
    # each element should know the coordinates of its own nodes
    if self.dimension == 3:    
        id1, id2, id3 = self.connectivity
    elif self.dimension == 4:
        id1, id2, id3, id4 = self.connectivity  
    else:
        raise Exception ("CIMPY:: Error Telement dimension" +str(self.dimension) + ": an element's dimension should be either 3 (triangle in 2D) or 4")
     
    nodes_dic = input_mesh.nodes_dict
    self.node1 = nodes_dic[id1]
    self.node2 = nodes_dic[id2]
    self.node3 = nodes_dic[id3]
    if self.dimension == 4: self.node4 = nodes_dic[id4]
    
    
  def GetConnectivityString(self, dimension):
     if dimension == 2:
         return str(self.connectivity[0]) + str("\t") + str(self.connectivity[1]) + str("\t") + str(self.connectivity[2]) + str("\n")
     elif dimension == 3:
            return str(self.connectivity[0]) + str("\t") + str(self.connectivity[1]) + str("\t") + str(self.connectivity[2]) +  + str("\t") + str(self.connectivity[3]) + str("\n")

#==================================================
def view(filename, engine= "mpl"):
    """ a cimpy function to visualize a mesh using cimpy's Tmesh class """
    """   argument: filename of the mesh
    """
    mesh = Tmesh(filename)
    mesh.View(engine)
#==================================================
