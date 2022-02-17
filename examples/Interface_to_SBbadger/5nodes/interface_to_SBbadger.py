import pydot
import simplesbml
import SBMLDiagrams
import os

DIR = os.path.dirname(os.path.abspath(__file__))
Files_FOLDER = os.path.join(DIR, "SBbadger_files")

dotfile = os.path.join(Files_FOLDER,"5nodes.dot")
graphs = pydot.graph_from_dot_file(dotfile)
graph = graphs[0]
node_set_list = []
for i in range(len(graph.get_nodes())):
  node = graph.get_nodes()[i]
  id = node.get_name()
  pos_str = node.get_pos()
  try: 
    pos_list = pos_str[1:-1].split(",")
    pos_list = [float(item) for item in pos_list]
    node_list = [id]
    node_list.append(pos_list)
    node_set_list.append(node_list)
  except:
    pass

f = open(os.path.join(Files_FOLDER, "5nodes.sbml"), 'r')
sbmlStr = f.read()
f.close()
df = SBMLDiagrams.load(sbmlStr)
for i in range(len(node_set_list)):
  df.setNodeAndTextPosition(node_set_list[i][0], node_set_list[i][1])  
model = simplesbml.loadSBMLStr(sbmlStr)
numRxns = model.getNumReactions()
Rxns_ids  = model.getListOfReactionIds()
for i in range(numRxns):
   df.setReactionDefaultCenterAndHandlePositions(Rxns_ids[i])
df.plot(scale = 2)


