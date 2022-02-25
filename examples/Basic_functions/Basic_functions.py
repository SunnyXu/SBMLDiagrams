# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 17:43:29 2022

@author: Jin Xu
"""

import SBMLDiagrams as sd

import tellurium as te

r = te.loada ('''
J1: S1 -> S2 + S3; k1*S1;
J2: S3 -> S4; k2*S3;
J3: S4 -> S5; k3*S4;
S1 = 10; S2 = 0;
S3 = 0; S4 = 0;
k1 = 0.1; k2 = 0.2; k3 = 0.45
''')

la = sd.load (r.getSBML())

# la.setNodeAndTextPosition('S1', [200, 200])
# la.setNodeAndTextPosition('S2', [300, 260])
# la.setNodeAndTextPosition('S3', [400, 200])
# la.setNodeAndTextPosition('S4', [500, 200])
# la.setNodeAndTextPosition('S5', [600, 200])
# la.setReactionDefaultCenterAndHandlePositions('J1')
# la.setReactionDefaultCenterAndHandlePositions('J2')
# la.setReactionDefaultCenterAndHandlePositions('J3')
# la.draw()

la.setNodeAndTextPosition('S1', [200, 200])
la.setNodeAndTextPosition('S2', [300, 300])
la.setNodeAndTextPosition('S3', [400, 200])
la.setNodeAndTextPosition('S4', [500, 200])
la.setNodeAndTextPosition('S5', [600, 200])
la.setNodeTextPosition('S1', [200, 180])
la.setNodeShapeIdx('S1', 2)
la.setNodeSize('S1', [10, 10])
la.setNodeShapeIdx('S2', 0)
la.setNodeTextFontSize('S2', 20)
la.setReactionDefaultCenterAndHandlePositions('J1')
la.setReactionDefaultCenterAndHandlePositions('J2')
la.setReactionDefaultCenterAndHandlePositions('J3')
la.setReactionDash("J1", [5,5])
la.setReactionCenterPosition("J3",[550,150])
la.setReactionHandlePositions("J3", [[600,150],[530,160],[600,120]])

la.draw(showReversible=True)