import os
import SBMLDiagrams


DIR = os.path.dirname(os.path.abspath(__file__))
filename = "mass_action_rxn.xml"
f = open(os.path.join(DIR, filename), 'r')
sbmlStr = f.read()
f.close()

df = SBMLDiagrams.load(sbmlStr)

df.draw(output_fileName = 'output.png')

df.exportGraphML("output_graphML")

