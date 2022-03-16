from SBMLDiagrams import visualizeSBML
import tellurium as te
import SBMLDiagrams

colors = visualizeSBML.loadJsonColor("style.json")
r = te.loada('''
    A -> B; k1*A
    B -> C; k2*B
    k1 = 0.1; k2 = 0.2; A = 10
''')

sbmlStr = r.getSBML()
df = SBMLDiagrams.load(sbmlStr)
df.setColorStyle(newStyleClass = colors["simplicity"])
df.draw(output_fileName="load_json_style/simplicity-color")

df.setColorStyle(newStyleClass = colors["default"])
df.draw(output_fileName="load_json_style/default-color")
