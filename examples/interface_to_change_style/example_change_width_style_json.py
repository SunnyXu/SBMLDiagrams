import SBMLDiagrams
import tellurium as te

colors = SBMLDiagrams.loadColorStyle("style.json")
r = te.loada('''
    A -> B; k1*A
    B -> C; k2*B
    k1 = 0.1; k2 = 0.2; A = 10
''')

sbmlStr = r.getSBML()
df = SBMLDiagrams.load(sbmlStr)

df.setColorStyle(colors["width"])
df.draw(output_fileName="change_width_json_style/change_width.png")
