import tellurium as te
import SBMLDiagrams

r = te.loada ('''
A -> B; v; B -> A; v;
v = 0
''')

df = SBMLDiagrams.load(r.getSBML())
df.draw(output_fileName = 'output.png')
df.autolayout()
df.draw(output_fileName = 'output_autolayout.png')
