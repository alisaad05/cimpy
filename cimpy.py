#!/usr/bin/env python

#import math
# import sys
import numpy as np
import matplotlib.pyplot as plt
# import vtk

# All returned arrays are cast into either numpy or numarray arrays
#arr=numpy.array

# ALI: "self" in python is equivalent to "this" in C++
class Tmesh:
  """Mesh object containing nodes and elements, as well connectivity and dimension information"""
  
  def __init__(self, filename = None):
    """Creates a Tmesh object by reading the specified file."""
    
    if filename is None:
      print "The mesh filename is not specified. Please input a valid mesh name with a .t extension" 
      self.name = "Maillage1" 
    else:
      # self.gridreader = None
      if filename[-2:].lower() == ".t":
        print "Mesh filename is valid and ready for reading ..."
        self.name = filename.split()[0]
#        self.point_array = [] # TODO: obsolete ... replaced by dictionary
        self.nodes_dict = {} # or =dict()        
        self.elements_dict = {} # or =dict()        
       
#        self.element_array = [] # TODO: obsolete ... replaced by dictionary
        self.Parse_input_file(filename)
      elif filename[-4:].lower() == ".msh":
        print "Coming soon: convert " + filename + " to a cimlib compatible mesh format (Tmesh) ? "
	  # TODO link with gmsh2mtc.py
      else:
        raise Exception("ERROR: The extension of " +  filename + "  filename is not recognised")
      
      
  def unittest(self):
      """ check if constructor is running """
      print "My name is: " + self.name
      
      
  def Parse_input_file(self, filename):
      """ takes a .t mesh filename and read it into a Tmesh datastructure """
      f = open(filename)
      
      header = f.readline().strip().split()
      self.nbNodes, self.dimNode,self.nbElements, self.dimElement = header
      
      self.nbNodes = int(self.nbNodes)
      self.nbElements = int(self.nbElements)
      self.dimElement = int(self.dimElement)
      self.dimNode = int(self.dimNode)
           
      for i in range(self.nbNodes): 
          a_new_node = Tnode(i+1, f.readline().strip().split())
#          self.point_array.append(a_new_node)  # TODO obsolete line
          self.nodes_dict[i+1] = a_new_node.coordinates
     
      # A fictitious node should be considered (but NOT USED FOR MESH VIEW)
      self.nodes_dict[0]=[0,0]
          
     # nodes_dict is a map of points IDs and their coordinates
     # To access the coordinates of a node:  nodes_dict[node_id]
     # To access a component in the coord: nodes_dict[node_id][component]
                      
     # TODO : supress blank lines between nodes coord and the element connectivity   
          
      for i in range(self.nbElements): 
          a_new_element = Telement(i+1, f.readline().strip().split(), self)
#          self.element_array.append(a_new_element)   # TODO obsolete line
          self.elements_dict[i+1] = a_new_element.connectivity
          
      f.close()
      
      
  def View(self):
      """ Plots the mesh in a figure. Supports only 2D mesh for now  """

      """ a dict constructor is necessary so that the class's member
      dictionary wont be affected when fictitious triangles are suppressed"""
      real_elements_dict = dict(self.elements_dict)

      # the 'enumerate' function is really nice !
      for i,connec_list in enumerate(real_elements_dict.values()):
         if 0 in connec_list : del real_elements_dict[i]
     
      # The lists have to be cast into numpy arrays before using the TRI plot
      nodes_coord = np.asarray(self.nodes_dict.values())
      triangles = np.asarray(real_elements_dict.values())
     
      # Extracting columns
      x = nodes_coord[:,0]
      y = nodes_coord[:,1]
      
      plt.figure()
      plt.gca().set_aspect('equal')
      plt.triplot(x, y, triangles, 'go-')
      plt.title('Mesh')
    
      plt.show() 
      
      
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
         print "The output filename is not specified ... aborting"
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
        raise Exception ("Error Telement dimension" +str(self.dimension) + ": an element's dimension should be either 3 (triangle in 2D) or 4")
     
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