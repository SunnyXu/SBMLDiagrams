import tellurium as te
import SBMLDiagrams

r = te.loada('''
    A -> B; k1*A
    B -> C; k2*B
    k1 = 0.1; k2 = 0.2; A = 10
''')

sbmlStr = r.getSBML()
df = SBMLDiagrams.load(sbmlStr)
df.draw(output_fileName="without-color/default-color")

df.setColorStyle("simplicity")
df.draw(output_fileName="without-color/simplicity")