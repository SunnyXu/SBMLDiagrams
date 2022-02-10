import simplesbml
import networkx as nx
import skia
import matplotlib.pyplot as plt
from SBMLDiagrams import styleSBML, drawNetwork


def autolayout(sbmlStr, edges, imageSize=[1000,1000], layout="spectral", styleName = 'default', newStyleClass = None):
    surface = skia.Surface(int(imageSize[0]), int(imageSize[1]))
    canvas = surface.getCanvas()
    color_style = newStyleClass
    if not newStyleClass:
        color_style = styleSBML.Style(styleName)

    model = simplesbml.loadSBMLStr(sbmlStr)

    numRxns = model.getNumReactions()

    graph = nx.Graph()
    nodes = model.getListOfAllSpecies()
    width, height = imageSize

    for node in nodes:
        graph.add_node(node)
    for edge in edges:
        src = edge[0]
        dests = edge[1:]
        for dest in dests:
            graph.add_edge(src, dest)

    if layout == "spectral":
        pos = nx.spectral_layout(graph,center=[width // 2,height // 2])
    elif layout == "spring":
        pos = nx.spring_layout(graph, center=[width // 2, height // 2])
    elif layout == "random":
        pos = nx.random_layout(graph, center=[width // 2, height // 2])
    elif layout == "circular":
        pos = nx.circular_layout(graph, center=[width // 2, height // 2])

    nx.draw(graph, with_labels=True, node_size=1500, node_color="skyblue", pos=nx.spectral_layout(graph))
    plt.title("spectral")
    plt.show()
    plt.savefig("autolayout2.png")
    print(pos)

    for edge in edges:
        src = edge[0]
        dests = edge[1:]
        for dest in dests:
            center = [float((pos[src][0]+pos[dest][0])/2), float((pos[src][1]+pos[dest][1])/2)]
            print(center)
            src_pos = pos[src].tolist()
            dest_pos = pos[dest].tolist()
            drawNetwork.addReaction(canvas, [], [src_pos], [dest_pos], center, [src_pos,dest_pos],
                                    [[40,60]], [[40,60]],[[40,60]],
                                    color_style.getReactionLineColor(), 1)


    drawNetwork.draw(surface, fileName="test", file_format="PNG")
