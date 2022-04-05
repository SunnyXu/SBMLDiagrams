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

df.setColorStyle(newStyle = colors["simplicity"])
df.draw(output_fileName="load_json_style/simplicity-color.png")

df.setColorStyle(newStyle = colors["default"])
df.draw(output_fileName="load_json_style/default-color.png")

df.setColorStyle(newStyle = colors["skyblue"])
df.draw(output_fileName="load_json_style/skyblue-color.png")
