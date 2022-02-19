import simplesbml
import networkx as nx
from SBMLDiagrams import styleSBML, drawNetwork, processSBML, visualizeSBML
from collections import defaultdict

def autolayout(sbmlStr, v_info, drawArrow = True, layout="spectral", styleName = 'default',
               newStyleClass = None, output_filename="autolayout"):
    df = processSBML.load(sbmlStr)

    color_style = newStyleClass
    if not newStyleClass:
        color_style = styleSBML.Style(styleName)
    edges = v_info.edges
    allDimDict = v_info.allDimDict
    print(allDimDict)
    name_to_id = v_info.name_to_id
    model = simplesbml.loadSBMLStr(sbmlStr)

    graph = nx.Graph()
    g = defaultdict(list)
    nodes = model.getListOfAllSpecies()
    reaction_ids = model.getListOfReactionIds()

    width, height = color_style.getImageSize()
    scale = max(width, height)//2
    center = [width // 2, height // 2]

    for node in nodes:
        graph.add_node(node)
    for edge in edges:
        src = edge[0]
        dests = edge[1:]
        for dest in dests:
            graph.add_edge(src, dest)
            g[src].append(dest)

    pos = defaultdict(list)
    if layout == "spectral":
        pos = nx.spectral_layout(graph, scale=scale, center=center)
    elif layout == "spring":
        pos = nx.spring_layout(graph, scale=scale, center=center)
    elif layout == "random":
        pos = nx.random_layout(graph, center=center)
    elif layout == "circular":
        pos = nx.circular_layout(graph, scale=scale, center=center)

    for n,p in pos.items():
        if layout == "random":
            p *= scale
        df.setNodeAndTextPosition(n,p)

    for id in reaction_ids:
        df.setReactionDefaultCenterAndHandlePositions(id)

    new_sbmlStr = df.export()
    v_info = visualizeSBML._plot(new_sbmlStr, drawArrow=drawArrow, output_fileName=output_filename)
    return v_info

