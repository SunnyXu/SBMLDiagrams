# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 10:37:16 2022

@author: Jin Xu
"""

import SBMLDiagrams
import tellurium as te

r = te.loada ('''
J0: Ethanol + NAD -> Ethanal + H + NADH; k1*Ethanol*NAD/ADH1;
i1: ADH1 -| J0;
Ethanol = 10; NAD = 6; H = 0; NADH = 0; ADH1 = 5;
k1 = 0.1;
''')

sbmlStr = r.getSBML()

# f = open("SBGN2-modifier.xml", "w")
# f.write(sbmlStr)
# f.close()

df = SBMLDiagrams.load(sbmlStr)

df.setNodeAndTextPosition("ADH1",[215,110])
df.setNodeAndTextPosition("Ethanol",[50,200])
df.setNodeAndTextPosition("NAD",[50,300])
df.setNodeAndTextPosition("Ethanal",[300,200])
df.setNodeAndTextPosition("H",[300,300])
df.setNodeAndTextPosition("NADH",[400,250])
df.setNodeShape("Ethanol","ellipse")
df.setNodeShape("NAD","ellipse")
df.setNodeShape("Ethanal","ellipse")
df.setNodeShape("H","ellipse")
df.setNodeShape("NADH","ellipse")
df.setNodeAndTextSize("Ethanol",[50,50])
df.setNodeAndTextSize("NAD",[50,50])
df.setNodeAndTextSize("Ethanal",[50,50])
df.setNodeAndTextSize("H",[50,50])
df.setNodeAndTextSize("NADH",[50,50])
df.setReactionDefaultCenterAndHandlePositions('J0')
#print(df.getReactionCenterPosition("J0"))  
df.addRectangle("centroid_sqaure", [235.0, 265.0], [20,20], 
fill_color=[91, 176, 253], border_color = [91,176,253])
df.setNodeFillLinearGradient("ADH1", [[0.0, 50.], [100.0, 50.0]],
  [[0.0, [255, 255, 255, 255]], [100.0, [192, 192, 192, 255]]])
df.setNodeBorderColor("ADH1", "black")

df.draw(output_fileName = 'output-SBGN2.png', scale = 2)
