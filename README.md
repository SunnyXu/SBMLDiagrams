# SBMLDiagrams
[![Coverage](https://codecov.io/gh/sunnyXu/SBMLDiagrams/branch/master/graph/badge.svg)](https://codecov.io/gh/sunnyXu/SBMLDiagrams)

[![Build Status](https://app.travis-ci.com/SunnyXu/SBMLDiagrams.svg?branch=main)](https://app.travis-ci.com/SunnyXu/SBMLDiagrams)

## Introduction
SBMLDiagrams can visualize SBML to PNG/JPG files by visualizeSBML.On one hand, users can get 
all the information about Compartment, Node and Reaction from an SBML file to csv files by importSBML. On the other hand, it supports users to generate SBML files based on the information of csv files. Users can edit the csv files and update the information so that can generate a new SBML file via exportSBML.

## Setup environment and validation
1) Clone the SBMLDiagrams repository using:
```
    git clone https://github.com/SunnyXu/SBMLDiagrams
```

2) Create a virtual environment for the project.
```
    cd SBMLDiagrams
    py -m venv kv
    source kv/Scripts/activate 
    py -m pip install -r requirements.txt
```

3) verify the setup:
```
    export PYTHONPATH=`pwd`
    cd tests
    py test_importSBML.py. 
    The tests should run without error.
```
## Documentation
Please see documentation at https://sunnyxu.github.io/SBMLDiagrams/ for details.


