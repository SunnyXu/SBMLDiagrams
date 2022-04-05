# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 11:07:06 2022

@author: Jin Xu
"""

import SBMLDiagrams
import tellurium as te

r = te.loada ('''
J1: ATP + myosin -> myosinATP; k1*ATP*myosin;
ATP = 10; myosin = 10; myosinATP = 0
k1 = 0.1;
''')

sbmlStr = r.getSBML()

# f = open("SBGN1-specComplex.xml", "w")
# f.write(sbmlStr)
# f.close()

df = SBMLDiagrams.load(sbmlStr)

df.setNodeAndTextPosition("ATP",[100,100])
df.setNodeAndTextPosition("myosin",[50,200])
df.setNodeAndTextPosition("myosinATP",[300,120])
df.setNodeShape("ATP","ellipse")
df.setNodeAndTextSize("ATP",[50,50])
df.setNodeAndTextSize("myosinATP",[70,100])
df.setNodeArbitraryPolygonShape("myosinATP","myosinATP-polygon", [[12.5,0],[87.5,0],[100,12.5],[100,87.5],
[87.5,100],[12.5,100],[0,87.5],[0,12.5]])
df.setReactionDefaultCenterAndHandlePositions('J1')
df.addRectangle("myosinATP_ATP", [305,130], [60,40])
df.addEllipse("myosinATP_myosin", [315,175], [40,40])
df.addText("myosin", [305,130], [60,40])
df.addText("ATP", [315,175], [40,40])
#print(df.getReactionCenterPosition("J1"))
#print(df.getReactionFillColor("J1"))
df.addEllipse("left_small_circle", [176.0, 166.], [10,10], 
fill_color=[91, 176, 253], border_color = [91,176,253])
df.addEllipse("right_small_circle", [216.0, 166.], [10,10], 
fill_color=[91, 176, 253], border_color = [91,176,253])
df.addEllipse("middle_big_circle", [191.0, 160.], [20,20], 
fill_color=[91, 176, 253], border_color = [91,176,253])

df.draw(output_fileName = 'output-SBGN1.png')