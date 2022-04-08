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

df.setColorStyle(colors["skyblue"])
df.draw(output_fileName="load_out_json_style/skyblue-color-before.png")
df.getColorStyleJson("skyblue.json")

new_colors = SBMLDiagrams.loadColorStyle("skyblue.json")
df.setColorStyle(new_colors["skyblue"])
df.draw(output_fileName="load_out_json_style/skyblue-color-after.png")