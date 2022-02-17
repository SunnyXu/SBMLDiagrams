# SBMLDiagrams
[![Coverage](https://codecov.io/gh/sunnyXu/SBMLDiagrams/branch/main/graph/badge.svg)](https://codecov.io/gh/sunnyXu/SBMLDiagrams)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT) [![PyPI version](https://badge.fury.io/py/SBMLDiagrams.svg)](https://badge.fury.io/py/SBMLDiagrams) [![PyPI download month](https://img.shields.io/pypi/dm/ansicolortags.svg)](https://pypi.python.org/pypi/SBMLDiagrams/) ![Funding](https://img.shields.io/badge/Funding-NIH%20(EB028887)-blue)

## Introduction
SBMLDiagrams is a Python package to visualize networks embedded in SBML Level 3 models. If the SBML layout and render extension are used, the package will use this data to display the network. SBMLDiagrams can export PNG, JPG, PDF files. SBMLDiagrams can be used to add SBML layout and render to an existing SBML model which can be subsequently be exported. If you use this python package, please cite the Gihub website (https://github.com/SunnyXu/SBMLDiagrams).

We also plan to interface SBMLDiagrams to NetworkX to exploit the variety of layout algorithms as well as SBbadger which is a tool for generating realistic but random biochemical networks. 

Note that the API is currently undergoing rapid changes to make the package easier to use. We anticipate the release of version 1.0 at the end of Feburary 2022. 

## Installation

``pip install SBMLDiagrams``

## A Figure Example

Here is a figure example visualized by SBMLDiagrams:

<img src="https://github.com/SunnyXu/SBMLDiagrams/blob/main/docs/Figures/Jana_WolfGlycolysis.png" width="350" height="450">

Please see more figure examples in the documentation.

## Documentation
Please see the documentation at https://sunnyxu.github.io/SBMLDiagrams/ for details.


