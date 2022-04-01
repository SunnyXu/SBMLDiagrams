.. _Introduction:
 

Introduction
=============

SBMLDiagrams is a Python package to visualize networks embedded in SBML Level 3 models. If the SBML 
layout and render extension are used, the package will use this data to display the network. 
SBMLDiagrams can export PNG, JPG, PDF files. SBMLDiagrams can be used to add SBML layout and render 
to an existing valid SBML model which can be subsequently be exported.

We also have an interface of SBMLDiagrams to NetworkX to exploit the variety of layout algorithms as well 
as SBbadger which is a tool for generating realistic but random biochemical networks. If you are
using any of the code, please cite the PYPI web page (https://pypi.org/project/SBMLDiagrams/). Thanks. 

------------
Installation 
------------

To install SBMLDiagrams use

.. code-block:: python
   
   pip install SBMLDiagrams


---------------
Figure Examples
---------------

1) An example without compartment. There are different shapes of nodes with different fill colors. 
Texts can be placed outside the nodes with designed positions. There are also reactions with different 
fill colors. x_1 is an example of alias node.

.. image:: Figures/test_no_comp.png
  :width: 400

2) An example with compartments. The compartments are filled with different colors. There are 
different shapes of nodes with different border colors. x_1 and x_5 are examples of alias nodes.

.. image:: Figures/test_comp.png
  :width: 400

3) An example with only nodes (no reactions in the network). There are five types of node shapes
with different fill colors and border colors.

.. image:: Figures/node_grid.png
  :width: 400

4) An example with long text contents.

.. image:: Figures/Jana_WolfGlycolysis.png
  :width: 400
