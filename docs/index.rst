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

1) Visualize an SBML file to a PNG.

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
      visualizeSBML.display(sbmlStr, reactionLineType = 'bezier', showBezierHandles = True, \
      fileFormat = 'PNG', output_fileName = 'output', complexShape = '')


2) Edit and write to an SBML file.

.. code-block:: python

   from SBMLDiagrams import importSBML
   from SBMLDiagrams import exportSBML
   from SBMLDiagrams import editSBML
   import pandas as pd
   import os

   f = open(os.path.join(TEST_FOLDER, filename), 'r')
   sbmlStr = f.read()
   f.close()

   (df_CompartmentData, df_NodeData, df_ReactionData) = importSBML.load(sbmlStr)
   df_CompartmentData_update =  editSBML.setCompartment(df_CompartmentData, 0, \
        position = [0., 0.], size = [1000., 1000.], fill_color = [255, 255, 255], \
        border_color = [255, 255, 255], border_width = 2.)
   df_NodeData_update = editSBML.setNode(df_NodeData, 0, floating_node=False, \
        position = [413., 216.], size = [50, 30], shape_idx = 1,\
        txt_position = [413., 216.], txt_size = [50., 30.], \
        fill_color = [255, 204, 153], border_color = [255, 108, 9], border_width = 2., \
        txt_font_color = [0, 0, 0], txt_line_width = 1.)
   df_ReactionData_update = editSBML.setReaction(df_ReactionData, 0, \
           fill_color = [91, 176, 253], line_thickness = 3., \
        bezier = True) 
   sbmlStr_layout_render = exportSBML.export(df_CompartmentData_update, df_NodeData_update, df_ReactionData_update)

   f = open("output.xml", "w")
   f.write(sbmlStr_layout_render)
   f.close()

3)  Import an SBML file to an excel file to edit. 

.. code-block:: python

   from SBMLDiagrams import importSBML
   import os
   import pandas as pd
   
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
         
         writer = pd.ExcelWriter('test.xlsx')
         df_CompartmentData.to_excel(writer, sheet_name='CompartmentData')
         df_NodeData.to_excel(writer, sheet_name='NodeData')
         df_ReactionData.to_excel(writer, sheet_name='ReactionData')
         writer.save()
      except:
         print("Invalid SBML!")


4) Export an SBML file based on the information from an excel file.

.. code-block:: python

   from SBMLDiagrams import exportSBML
   import pandas as pd

   xls = pd.ExcelFile('path//to//test.xlsx')
   df_CompartmentData = pd.read_excel(xls, 'CompartmentData')
   df_NodeData = pd.read_excel(xls, 'NodeData')
   df_ReactionData = pd.read_excel(xls, 'ReactionData')

   sbmlStr_layout_render = exportSBML.export(df_CompartmentData, df_NodeData, df_ReactionData)
   f = open("output.xml", "w")
   f.write(sbmlStr_layout_render)
   f.close()



