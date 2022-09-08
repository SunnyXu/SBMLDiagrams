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

la.setNodeAndTextPosition('S1', [200, 200])
la.setNodeAndTextPosition('S2', [300, 300])
la.setNodeAndTextPosition('S3', [400, 200])
la.setNodeAndTextPosition('S4', [500, 200])
la.setNodeAndTextPosition('S5', [600, 200])

# Move the text only
la.setNodeTextPosition('S1', [200, 180])
la.setNodeTextPosition('S2', [300, 294])

la.setNodeShape('S1', 'ellipse')
la.setNodeSize('S1', [20, 20])
la.setNodeBorderWidth ('S1', 3)
la.setNodeBorderColor('S1', 'white')
la.setNodeShape('S2', 'text_only')
la.setNodeTextFontSize('S2', 20)

# Set up defaults for reaction center and bezier handles
la.setReactionDefaultCenterAndHandlePositions('J1')
la.setReactionDefaultCenterAndHandlePositions('J2')
la.setReactionDefaultCenterAndHandlePositions('J3')
la.setReactionDashStyle("J1", [5,5])
la.setReactionCenterPosition("J3",[550,150])
la.setReactionBezierHandles("J3", [[550,150],[530,155],[600,120]])

la.draw(setImageSize=[600,300], output_fileName='output.png')
