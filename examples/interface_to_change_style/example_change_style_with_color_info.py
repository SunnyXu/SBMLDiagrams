import SBMLDiagrams
from SBMLDiagrams.visualizeSBML import *

DIR = os.path.dirname(os.path.abspath(__file__))
filename = "test_comp.xml"
f = open(os.path.join(DIR, filename), 'r')
sbmlStr = f.read()
f.close()
df = SBMLDiagrams.load(sbmlStr)

df.draw(output_fileName="with-color/sbml-color.png")

df.setColorStyle("default")
df.draw(output_fileName="with-color/default-color.png")

df.setColorStyle(None)
df.draw(output_fileName="with-color/back-sbml-color.png")

