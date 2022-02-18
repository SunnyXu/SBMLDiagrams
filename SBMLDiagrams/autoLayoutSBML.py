import simplesbml
import networkx as nx
import skia
import matplotlib.pyplot as plt
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

    for id in reaction_ids:
        rct_num = model.getNumReactants(id)
        prd_num = model.getNumProducts(id)
        center_x = 0.
        center_y = 0.
        for j in range(rct_num):
            n = model.getReactant(id, j)
            src_pos = pos[n]
            src_dim = allDimDict['[' + n + ']']
            center_x += src_pos[0] + 0.5 * src_dim[0]
            center_y += src_pos[1] + 0.5 * src_dim[1]
        for j in range(prd_num):
            dest = model.getProduct(id,j)
            dest_pos = pos[dest]
            dest_dim = allDimDict['[' + dest + ']']
            center_x += dest_pos[0] + 0.5 * dest_dim[0]
            center_y += dest_pos[1] + 0.5 * dest_dim[1]
        center_x = center_x / (rct_num + prd_num)
        center_y = center_y / (rct_num + prd_num)
        center_position = [center_x, center_y]
        handles = [center_position]
        for j in range(rct_num):
            n = model.getReactant(id, j)
            src_pos = pos[n]
            src_dim = allDimDict['[' + n + ']']
            handle_x = 0.5 * (center_x + src_pos[0] + 0.5 * src_dim[0])
            handle_y = 0.5 * (center_y + src_pos[1] + 0.5 * src_dim[1])
            handles.append([handle_x,handle_y])
        for j in range(prd_num):
            dest = model.getProduct(id,j)
            dest_pos = pos[dest]
            dest_dim = allDimDict['[' + dest + ']']
            handle_x = 0.5 * (center_x + dest_pos[0] + 0.5 * dest_dim[0])
            handle_y = 0.5 * (center_y + dest_pos[1] + 0.5 * dest_dim[1])
            handles.append([handle_x, handle_y])

        df.setReactionCenterPosition(id, center_position)
        df.setReactionHandlePositions(id, handles)

    for n,p in pos.items():
        if layout == "random":
            p *= scale
        df.setNodeAndTextPosition(n,p)

    new_sbmlStr = df.export()
    v_info = visualizeSBML._plot(new_sbmlStr, drawArrow=drawArrow, output_fileName=output_filename)
    return v_info

