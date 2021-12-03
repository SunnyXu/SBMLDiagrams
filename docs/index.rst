.. SBMLDiagrams documentation master file, created by
   sphinx-quickstart on Mon Nov  8 14:18:50 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SBMLDiagrams's documentation!
========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api
   functions

------------
Introduction
------------

SBMLDiagrams can visualize SBML to PNG/JPG/PDF files by visualizeSBML. On one hand, 
users can get all the information about Compartment, Node and Reaction from an 
SBML file to DataFrame by importSBML. On the other hand, it supports users to 
generate SBML files based on the information of DataFrame. Users can edit the 
DataFrame and update the information so that can generate a new SBML file via exportSBML.

------------
Installation 
------------

To install SBMLDiagrams use

.. code-block:: python
   
   pip install SBMLDiagrams

--------
Examples
--------

1) Visualize an SBML file to a PDF.

.. code-block:: python

   from SBMLDiagrams import visualizeSBML
   import os 

   dirname = "path//to"
   filename = "test.xml"

   f = open(os.path.join(dirname, filename), 'r')
   sbmlStr = f.read()
   f.close()

   if len(sbmlStr) == 0:
      print("Empty SBML!")
   else:
      visualizeSBML.display(sbmlStr, fileFormat = 'PNG')


2)  Import an SBML file to a set of csv files to edit. 

.. code-block:: python

   from SBMLDiagrams import importSBML
   import os
   dirname = "path//to"
   filename = "test.xml"
   f = open(os.path.join(dirname, filename), 'r')
   sbmlStr = f.read()
   f.close()
   if len(sbmlStr) == 0:
      print("Empty SBML!")
   else:
      try:
         df_CompartmentData, df_NodeData, df_ReactionData = importSBML.load(sbmlStr, reactionLineType)
         df_CompartmentData.to_csv("CompartmentData.csv", index = False)
         df_NodeData.to_csv("NodeData.csv", index = False)
         df_ReactionData.to_csv("ReactionData.csv", index = False)
      except:
         print("Invalid SBML!")


3) Export an SBML file based on the information from a set of csv files.

.. code-block:: python

   from SBMLDiagrams import exportSBML
   import pandas as pd

   df_CompartmentData = pd.read_csv('path//to//CompartmentData.csv')
   df_NodeData = pd.read_csv('path//to//NodeData.csv')
   df_ReactionData = pd.read_csv('path//to//ReactionData.csv')
   sbmlStr_layout_render = exportSBML.export(df_CompartmentData, df_NodeData, df_ReactionData)
   f = open("output.xml", "w")
   f.write(sbmlStr_layout_render)
   f.close()

