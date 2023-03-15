import tellurium as te
import SBMLDiagrams


r = te.loada ('''
S1 + S2 -> S2; v;
v = 0
''')

df = SBMLDiagrams.load(r.getSBML())
df.draw(output_fileName = 'output.png')
df.autolayout()
df.draw(output_fileName = 'output_autolayout.png')
