.. SBMLDiagrams documentation master file, created by
   sphinx-quickstart on Mon Nov  8 14:18:50 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SBMLDiagrams's documentation!
========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Introduction
   Tutorial
   Network
   Compartment
   Node
   Reaction
   ArbitraryText
   ArbitraryShape
   Colors

    
------------
Introduction
------------

SBMLDiagrams is a Python package to visualize networks embedded in SBML Level 3 models. If the SBML 
layout and render extension are used, the package will use this data to display the network. 
SBMLDiagrams can export PNG, JPG, PDF files. SBMLDiagrams can be used to add SBML layout and render 
to an existing valid SBML model which can be subsequently be exported.

We also have an interface of SBMLDiagrams to NetworkX to exploit the variety of layout algorithms as well 
as SBbadger which is a tool for generating realistic but random biochemical networks. If you are 
using any of the code, please cite the article (https://doi.org/10.1093/bioinformatics/btac730) and 
the PYPI web page (https://pypi.org/project/SBMLDiagrams/). Thanks. 