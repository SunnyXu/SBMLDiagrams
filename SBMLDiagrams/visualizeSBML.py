# -*- coding: utf-8 -*-
# This script was written by Jin Xu and available on Github
# https://github.com/SunnyXu/SBMLDiagrams

"""
Created on Mon Aug 23 13:25:34 2021
@author: Jin Xu
"""

import os
import skia
import simplesbml
from libsbml import *
import math
import random as _random
from SBMLDiagrams import drawNetwork

def display(sbmlStr, reactionLineType = 'bezier', showBezierHandles = True, fileFormat = 'PNG', output_fileName = 'output', complexShape = ''):

    """
    Visualization from an sbml string to a PNG/JPG/PDF file.

    Args:  
        sbmlStr: str-the string of the input sbml file.

        reactionLineType: str-type of the reaction line: 'linear' or 'bezier' (default).

        showBezierHandles: bool-show the Bezier handles (True as default) or not (False).

        fileFormat: str-output file type: 'PNG' (default), 'JPEG' or 'PDF'.

        output_fileName: str-filename: 'output' (default) or ''.
        
        complexShape: str-type of complex shapes: '' (default) or 'monomer' or 'dimer' or 'trimer' or 'tetramer'.  

    """

    surface = skia.Surface(1000, 1000)
    canvas = surface.getCanvas()
    
    def hex_to_rgb(value):
        value = value.lstrip('#')
        return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))

    comp_id_list = []
    comp_dimension_list = []
    comp_position_list = []
    spec_id_list = []
    specGlyph_id_list = []
    spec_specGlyph_id_list = []
    spec_dimension_list = []
    spec_position_list = []
    spec_text_position_list = []
    spec_text_dimension_list = []
    shapeIdx = 1
    
    #set the default values without render info:
    comp_fill_color = (158, 169, 255)
    comp_border_color = (0, 29, 255)
    comp_border_width = 2.0
    spec_fill_color = (255, 204, 153)
    spec_border_color = (255, 108, 9)
    spec_border_width = 2.0
    reaction_line_color = (129, 123, 255)
    reaction_line_width = 3.0
    text_line_color = (0,0,0)
    text_line_width = 1.

    try: #invalid sbml    
        ### from here for layout ###
        document = readSBMLFromString(sbmlStr)
        model_layout = document.getModel()
        mplugin = model_layout.getPlugin("layout")
        if mplugin is not None:
            layout = mplugin.getLayout(0)    
            if layout is not None:
                numCompGlyphs = layout.getNumCompartmentGlyphs()
                numSpecGlyphs = layout.getNumSpeciesGlyphs()
                numReactionGlyphs = layout.getNumReactionGlyphs() 
                for i in range(numCompGlyphs):
                    compGlyph = layout.getCompartmentGlyph(i)
                    temp_id = compGlyph.getCompartmentId()
                    comp_id_list.append(temp_id)
                    boundingbox = compGlyph.getBoundingBox()
                    height = boundingbox.getHeight()
                    width = boundingbox.getWidth()
                    pos_x = boundingbox.getX()
                    pos_y = boundingbox.getY()
                    comp_dimension_list.append([width,height])
                    comp_position_list.append([pos_x,pos_y])
                    
                    # for i in range(numSpecGlyphs):
                    #     specGlyph = layout.getSpeciesGlyph(i)
                    #     spec_id = specGlyph.getSpeciesId()
                    #     spec_id_list.append(spec_id)
                    #     boundingbox = specGlyph.getBoundingBox()
                    #     height = boundingbox.getHeight()
                    #     width = boundingbox.getWidth()
                    #     pos_x = boundingbox.getX()
                    #     pos_y = boundingbox.getY()
                    #     spec_dimension_list.append([width,height])
                    #     spec_position_list.append([pos_x,pos_y])

                reaction_id_list = []
                reaction_center_list = []
                kinetics_list = []
                #rct_specGlyph_list = []
                #prd_specGlyph_list = []
                reaction_center_handle_list = []
                rct_specGlyph_handle_list = []
                prd_specGlyph_handle_list = []
                reaction_mod_list = []
                mod_specGlyph_list = []
                
                for i in range(numReactionGlyphs):
                    reactionGlyph = layout.getReactionGlyph(i)
                    curve = reactionGlyph.getCurve()
                    # listOfCurveSegments = curve.getListOfCurveSegments()
                    # for j in range(len(listOfCurveSegments)):
                    #     #center_x = curve.getCurveSegment(j).getStart().x()
                    #     #center_y = curve.getCurveSegment(j).getStart().y()
                    #     center_x = curve.getCurveSegment(j).getStart().getXOffset()
                    #     center_y = curve.getCurveSegment(j).getStart().getYOffset()
                    for segment in curve.getListOfCurveSegments():
                        center_x = segment.getStart().getXOffset()
                        center_y = segment.getStart().getYOffset()
                        reaction_center_list.append([center_x, center_y])
                    reaction_id = reactionGlyph.getReactionId()
                    reaction_id_list.append(reaction_id)
                    reaction = model_layout.getReaction(reaction_id)
                    kinetics = reaction.getKineticLaw().getFormula()
                    kinetics_list.append(kinetics)
                    
                    temp_mod_list = []
                    for j in range(len(reaction.getListOfModifiers())):
                        modSpecRef = reaction.getModifier(j)
                        temp_mod_list.append(modSpecRef.getSpecies())
                    reaction_mod_list.append(temp_mod_list)       
                    
                    numSpecRefGlyphs = reactionGlyph.getNumSpeciesReferenceGlyphs()

                    #rct_specGlyph_temp_list = []
                    #prd_specGlyph_temp_list = []
                    rct_specGlyph_handles_temp_list = []
                    prd_specGlyph_handles_temp_list = [] 
                    mod_specGlyph_temp_list = []

                    for j in range(numSpecRefGlyphs):
                        specRefGlyph = reactionGlyph.getSpeciesReferenceGlyph(j)
                        #specRefGlyph_id = specRefGlyph.getSpeciesReferenceGlyphId()
                                            
                        curve = specRefGlyph.getCurve()                             
                        for segment in curve.getListOfCurveSegments():
                                # print(segment.getStart().getXOffset())
                                # print(segment.getStart().getYOffset())
                                # print(segment.getEnd().getXOffset())
                                # print(segment.getEnd().getYOffset())
                                try:
                                    center_handle = [segment.getBasePoint1().getXOffset(), 
                                                segment.getBasePoint1().getYOffset()]                                
                                    spec_handle = [segment.getBasePoint2().getXOffset(),
                                            segment.getBasePoint2().getYOffset()]
                                except:
                                    center_handle = []
                                    spec_handle = []

                        role = specRefGlyph.getRoleString()
                        specGlyph_id = specRefGlyph.getSpeciesGlyphId()
                        specGlyph = layout.getSpeciesGlyph(specGlyph_id)
                        
                        for k in range(numSpecGlyphs):
                            textGlyph_temp = layout.getTextGlyph(k)
                            temp_specGlyph_id = textGlyph_temp.getOriginOfTextId()
                            if temp_specGlyph_id == specGlyph_id:
                                textGlyph = textGlyph_temp

                        spec_id = specGlyph.getSpeciesId()
                        spec_boundingbox = specGlyph.getBoundingBox()
                        width = spec_boundingbox.getWidth()
                        height = spec_boundingbox.getHeight()
                        pos_x = spec_boundingbox.getX()
                        pos_y = spec_boundingbox.getY()
                        
                        try:
                            text_boundingbox = textGlyph.getBoundingBox()
                            text_pos_x = text_boundingbox.getX()
                            text_pos_y = text_boundingbox.getY()   
                            text_dim_w = text_boundingbox.getWidth()
                            text_dim_h = text_boundingbox.getHeight()
                        except:
                            text_pos_x = pos_x
                            text_pos_y = pos_y   
                            text_dim_w = width
                            text_dim_h = height

                        if specGlyph_id not in specGlyph_id_list:
                            spec_id_list.append(spec_id)
                            specGlyph_id_list.append(specGlyph_id)
                            spec_specGlyph_id_list.append([spec_id,specGlyph_id])
                            spec_dimension_list.append([width,height])
                            spec_position_list.append([pos_x,pos_y])
                            spec_text_position_list.append([text_pos_x, text_pos_y])
                            spec_text_dimension_list.append([text_dim_w, text_dim_h])

                        if role == "substrate": #it is a rct
                            #rct_specGlyph_temp_list.append(specGlyph_id)
                            rct_specGlyph_handles_temp_list.append([specGlyph_id,spec_handle])
                        elif role == "product": #it is a prd
                            #prd_specGlyph_temp_list.append(specGlyph_id)
                            prd_specGlyph_handles_temp_list.append([specGlyph_id,spec_handle])
                        elif role == "modifier": #it is a modifier
                            mod_specGlyph_temp_list.append(specGlyph_id)
                        
                    #rct_specGlyph_list.append(rct_specGlyph_temp_list)
                    #prd_specGlyph_list.append(prd_specGlyph_temp_list)
                    reaction_center_handle_list.append(center_handle)
                    rct_specGlyph_handle_list.append(rct_specGlyph_handles_temp_list)
                    prd_specGlyph_handle_list.append(prd_specGlyph_handles_temp_list) 
                    mod_specGlyph_list.append(mod_specGlyph_temp_list)

                #print(reaction_mod_list)
                #print(mod_specGlyph_list)

                rPlugin = layout.getPlugin("render")
                if (rPlugin != None and rPlugin.getNumLocalRenderInformationObjects() > 0):
                    info = rPlugin.getRenderInformation(0)
                    color_list = []
                    comp_render = []
                    spec_render = []
                    rxn_render = []
                    text_render = []
                    for  j in range ( 0, info.getNumColorDefinitions()):
                        color = info.getColorDefinition(j)
                        color_list.append([color.getId(),color.createValueString()])

                    for j in range (0, info.getNumStyles()):
                        style = info.getStyle(j)
                        group = style.getGroup()
                        typeList = style.createTypeString()
                        idList = style.createIdString()
                        if 'COMPARTMENTGLYPH' in typeList:
                            for k in range(len(color_list)):
                                if color_list[k][0] == group.getFill():
                                    comp_fill_color = hex_to_rgb(color_list[k][1])
                                if color_list[k][0] == group.getStroke():
                                    comp_border_color = hex_to_rgb(color_list[k][1])
                            comp_border_width = group.getStrokeWidth()
                            comp_render.append([idList,comp_fill_color,comp_border_color,comp_border_width])
                        elif 'SPECIESGLYPH' in typeList:
                            for k in range(len(color_list)):
                                if color_list[k][0] == group.getFill():
                                    spec_fill_color = hex_to_rgb(color_list[k][1])
                                if color_list[k][0] == group.getStroke():
                                    spec_border_color = hex_to_rgb(color_list[k][1])
                            spec_border_width = group.getStrokeWidth()
                            name_list = []
                            for element in group.getListOfElements():
                                name = element.getElementName()
                                name_list.append(name)
                                try:
                                    NumRenderpoints = element.getListOfElements().getNumRenderPoints()
                                except:
                                    NumRenderpoints = 0
                            shapeIdx = 0
                            if name == "rectangle":
                                shapeIdx = 1
                            elif name == "ellipse": #circle
                                shapeIdx = 2
                            elif name == "polygon" and NumRenderpoints == 6: #hexagon
                                shapeIdx = 3
                            elif name == "polygon" and NumRenderpoints == 2: #line
                                shapeIdx = 4
                            elif name == "polygon" and NumRenderpoints == 3: #triangle
                                shapeIdx = 5
                            else:
                                shapeIdx = 0

                            spec_render.append([idList,spec_fill_color,spec_border_color,spec_border_width,shapeIdx])

                        elif 'REACTIONGLYPH' in typeList:
                            for k in range(len(color_list)):
                                if color_list[k][0] == group.getStroke():
                                    reaction_line_color = hex_to_rgb(color_list[k][1])
                            reaction_line_width = group.getStrokeWidth()
                            rxn_render.append([idList, reaction_line_color,reaction_line_width])
                        elif 'TEXTGLYPH' in typeList:
                            for k in range(len(color_list)):
                                if color_list[k][0] == group.getStroke():
                                    text_line_color = hex_to_rgb(color_list[k][1])
                            text_line_width = group.getStrokeWidth()
                            #text_font_size = group.getFontSize()
                            text_render.append([idList,text_line_color,text_line_width])

    #try: 
        model = simplesbml.loadSBMLStr(sbmlStr)
        numFloatingNodes  = model.getNumFloatingSpecies()
        FloatingNodes_ids = model.getListOfFloatingSpecies()
        numBoundaryNodes  = model.getNumBoundarySpecies()
        BoundaryNodes_ids = model.getListOfBoundarySpecies()
        numRxns   = model.getNumReactions()
        Rxns_ids  = model.getListOfReactionIds()
        numComps  = model.getNumCompartments()
        Comps_ids = model.getListOfCompartmentIds()
        numNodes = numFloatingNodes + numBoundaryNodes
        comp_node_list = [0]*numComps #Note: numComps is different from numCompGlyphs
        for i in range(numComps):
            comp_node_list[i] = []
        #if there is layout info:
        if len(spec_id_list) != 0:
            for i in range(numComps):
                temp_id = Comps_ids[i]
                vol= model.getCompartmentVolume(i)
                if temp_id == "_compartment_default_":
                    dimension = [1000, 1000]
                    position = [0, 0]
                    #comp_border_color = (255, 255, 255, 0) #the last digit for transparent
                    #comp_fill_color = (255, 255, 255, 0)
                    comp_border_color = (255, 255, 255)
                    comp_fill_color = (255, 255, 255)
                    drawNetwork.addCompartment(canvas, position, dimension,
                                            comp_border_color, comp_fill_color, comp_border_width)
                else:
                    if len(comp_id_list) != 0:
                    #if mplugin is not None:                    
                        for j in range(numCompGlyphs):
                            if comp_id_list[j] == temp_id:
                                dimension = comp_dimension_list[j]
                                position = comp_position_list[j]
                        for j in range(len(comp_render)):
                            if temp_id == comp_render[j][0]:
                                comp_fill_color = comp_render[j][1]
                                comp_border_color = comp_render[j][2]
                                comp_border_width = comp_render[j][3]
                    else:# no layout info about compartment,
                        # then the whole size of the canvas is the compartment size
                        # modify the compartment size using the max_rec function above
                        dimension = [1000,1000]
                        position = [0,0]
                        #comp_fill_color = (255, 255, 255, 0)
                        #comp_border_color = (255, 255, 255, 0)
                        comp_fill_color = (255, 255, 255)
                        comp_border_color = (255, 255, 255)
                    drawNetwork.addCompartment(canvas, position, dimension,
                                            comp_border_color, comp_fill_color, comp_border_width)
            #add reactions before adding nodes to help with the line positions
            numSpec_in_reaction = len(spec_specGlyph_id_list)
            for i in range (numReactionGlyphs):
                #src = []
                #dst = []
                src_position = []
                src_dimension = [] 
                dst_position = []
                dst_dimension = []
                mod_position = []
                mod_dimension = []
                src_handle = []
                dst_handle = []
                temp_id = reaction_id_list[i]
                kinetics = kinetics_list[i]
                #rct_num = len(rct_specGlyph_list[i])
                #prd_num = len(prd_specGlyph_list[i])
                rct_num = len(rct_specGlyph_handle_list[i])
                prd_num = len(prd_specGlyph_handle_list[i])
                mod_num = max(len(mod_specGlyph_list[i]),len(reaction_mod_list[i]))

                # for j in range(rct_num):
                #     temp_specGlyph_id = rct_specGlyph_list[i][j]
                #     for k in range(numSpec_in_reaction):
                #         if temp_specGlyph_id == specGlyph_id_list[k]:
                #             src_position.append(spec_position_list[k])
                #             src_dimension.append(spec_dimension_list[k])

                # for j in range(prd_num):
                #     temp_specGlyph_id = prd_specGlyph_list[i][j]
                #     for k in range(numSpec_in_reaction):
                #         if temp_specGlyph_id == specGlyph_id_list[k]:
                #             dst_position.append(spec_position_list[k])
                #             dst_dimension.append(spec_dimension_list[k])

                for j in range(rct_num):
                    temp_specGlyph_id = rct_specGlyph_handle_list[i][j][0]
                    for k in range(numSpec_in_reaction):
                        if temp_specGlyph_id == specGlyph_id_list[k]:
                            src_position.append(spec_position_list[k])
                            src_dimension.append(spec_dimension_list[k])
                    src_handle.append(rct_specGlyph_handle_list[i][j][1])

                for j in range(prd_num):
                    temp_specGlyph_id = prd_specGlyph_handle_list[i][j][0]
                    for k in range(numSpec_in_reaction):
                        if temp_specGlyph_id == specGlyph_id_list[k]:
                            dst_position.append(spec_position_list[k])
                            dst_dimension.append(spec_dimension_list[k])
                    dst_handle.append(prd_specGlyph_handle_list[i][j][1])

                for j in range(mod_num):
                    if len(mod_specGlyph_list[i]) != 0:
                        temp_specGlyph_id = mod_specGlyph_list[i][j]
                        for k in range(numSpec_in_reaction):
                            if temp_specGlyph_id == specGlyph_id_list[k]:
                                mod_position.append(spec_position_list[k])
                                mod_dimension.append(spec_dimension_list[k])
                    else:
                        for k in range(len(spec_specGlyph_id_list)):
                            if reaction_mod_list[i][j] == spec_specGlyph_id_list[k][0]:
                                temp_specGlyph_id = spec_specGlyph_id_list[k][1]
                        for k in range(numSpec_in_reaction):
                            if temp_specGlyph_id == specGlyph_id_list[k]:
                                mod_position.append(spec_position_list[k])
                                mod_dimension.append(spec_dimension_list[k])

                for j in range(len(rxn_render)):
                    if temp_id == rxn_render[j][0]:
                        reaction_line_color = rxn_render[j][1]
                        reaction_line_width = rxn_render[j][2]
                try: 
                    center_position = reaction_center_list[i]
                    center_handle = reaction_center_handle_list[i]
                    handles = [center_position]
                    handles.extend(src_handle)
                    handles.extend(dst_handle)   
                    #print(handles)
                    drawNetwork.addReaction(canvas, src_position, dst_position, mod_position,
                    center_position, handles, src_dimension, dst_dimension, mod_dimension,
                    reaction_line_color, reaction_line_width,
                    reaction_line_type = reactionLineType, show_bezier_handles = showBezierHandles)
                except:
                    center_x = 0.
                    center_y = 0.
                    for j in range(rct_num):
                        center_x += src_position[j][0]+.5*src_dimension[j][0]
                        center_y += src_position[j][1]+.5*src_dimension[j][1]
                    for j in range(prd_num):
                        center_x += dst_position[j][0]+.5*dst_dimension[j][0]
                        center_y += dst_position[j][1]+.5*dst_dimension[j][1]
                    center_x = center_x/(rct_num + prd_num) 
                    center_y = center_y/(rct_num + prd_num)
                    center_position = [center_x, center_y]
                    handles = [center_position]
                    for j in range(rct_num):
                        src_handle_x = .5*(center_position[0] + src_position[j][0] + .5*src_dimension[j][0])
                        src_handle_y = .5*(center_position[1] + src_position[j][1] + .5*src_dimension[j][1])
                        handles.append([src_handle_x,src_handle_y])
                    for j in range(prd_num):
                        dst_handle_x = .5*(center_position[0] + dst_position[j][0] + .5*dst_dimension[j][0])
                        dst_handle_y = .5*(center_position[1] + dst_position[j][1] + .5*dst_dimension[j][1])
                        handles.append([dst_handle_x,dst_handle_y])
                    #print(handles)
                    drawNetwork.addReaction(canvas, src_position, dst_position, mod_position,
                    center_position, handles, src_dimension, dst_dimension, mod_dimension,
                    reaction_line_color, reaction_line_width,
                    reaction_line_type = reactionLineType, show_bezier_handles = showBezierHandles)
                        
            id_list = []
            #numSpecGlyphs is larger than numSpec_in_reaction if there orphan nodes
            if numSpecGlyphs > numSpec_in_reaction:
                print("Orphan nodes are removed.")
            for i in range (numSpec_in_reaction):
                temp_id = spec_specGlyph_id_list[i][0]
                tempGlyph_id = spec_specGlyph_id_list[i][1]
                dimension = spec_dimension_list[i]
                position = spec_position_list[i]
                text_position = spec_text_position_list[i]
                text_dimension = spec_text_dimension_list[i]
                for j in range(numFloatingNodes):
                    if temp_id == FloatingNodes_ids[j]:
                        if temp_id not in id_list:
                            for k in range(len(spec_render)):
                                if temp_id == spec_render[k][0]:
                                    spec_fill_color = spec_render[k][1]
                                    spec_border_color = spec_render[k][2]
                                    spec_border_width = spec_render[k][3]
                                    shapeIdx = spec_render[k][4]
                            for k in range(len(text_render)):
                                if temp_id == text_render[k][0]:
                                    text_line_color = text_render[k][1]
                                    text_line_width = text_render[k][2]
                            drawNetwork.addNode(canvas, 'floating', '', position, dimension,
                                                spec_border_color, spec_fill_color, spec_border_width,
                                                shapeIdx, complex_shape = complexShape)
                            drawNetwork.addText(canvas, temp_id, text_position, text_dimension, text_line_color, text_line_width)
                            id_list.append(temp_id)                    
                        else:
                            for k in range(len(spec_render)):
                                if temp_id == spec_render[k][0]:
                                    spec_fill_color = spec_render[k][1]
                                    spec_border_color = spec_render[k][2]
                                    spec_border_width = spec_render[k][3]
                                    shapeIdx = spec_render[k][4]
                            for k in range(len(text_render)):
                                if temp_id == text_render[k][0]:
                                    text_line_color = text_render[k][1]
                                    text_line_width = text_render[k][2]
                            drawNetwork.addNode(canvas, 'floating', 'alias', position, dimension,
                                                spec_border_color, spec_fill_color, spec_border_width,
                                                shapeIdx, complex_shape=complexShape)
                            drawNetwork.addText(canvas, temp_id, text_position, text_dimension, text_line_color, text_line_width)
                            id_list.append(temp_id)
                for j in range(numBoundaryNodes):
                    if temp_id == BoundaryNodes_ids[j]:
                        if temp_id not in id_list:
                            for k in range(len(spec_render)):
                                if temp_id == spec_render[k][0]:
                                    spec_fill_color = spec_render[k][1]
                                    spec_border_color = spec_render[k][2]
                                    spec_border_width = spec_render[k][3]
                                    shapeIdx = spec_render[k][4]
                            for k in range(len(text_render)):
                                if temp_id == text_render[k][0]:
                                    text_line_color = text_render[k][1]
                                    text_line_width = text_render[k][2]        
                            drawNetwork.addNode(canvas, 'boundary', '', position, dimension,
                                                spec_border_color, spec_fill_color, spec_border_width,
                                                shapeIdx, complex_shape=complexShape)
                            drawNetwork.addText(canvas, temp_id, text_position, text_dimension, text_line_color, text_line_width)
                            id_list.append(temp_id)
                        else:
                            for k in range(len(spec_render)):
                                if temp_id == spec_render[k][0]:
                                    spec_fill_color = spec_render[k][1]
                                    spec_border_color = spec_render[k][2]
                                    spec_border_width = spec_render[k][3]
                                    shapeIdx = spec_render[k][4]
                            for k in range(len(text_render)):
                                if temp_id == text_render[k][0]:
                                    text_line_color = text_render[k][1]
                                    text_line_width = text_render[k][2] 
                            drawNetwork.addNode(canvas, 'boundary', 'alias', position, dimension,
                                                spec_border_color, spec_fill_color, spec_border_width,
                                                shapeIdx, complex_shape=complexShape)
                            drawNetwork.addText(canvas, temp_id, text_position, text_dimension, text_line_color, text_line_width)                
                            id_list.append(temp_id)

        else: # there is no layout information, assign position randomly and size as default
            comp_id_list = Comps_ids
            nodeIdx_temp = 0 #to track the node index    
            for i in range(numComps):
                temp_id = Comps_ids[i]
                vol= model.getCompartmentVolume(i)
                dimension = [1000,1000]
                position = [0,0]
                drawNetwork.addCompartment(canvas, position, dimension,
                                            comp_border_color, comp_fill_color, comp_border_width)
            spec_id_list = [] 
            spec_dimension_list = []
            spec_position_list = []
            for i in range (numFloatingNodes):
                temp_id = FloatingNodes_ids[i]
                dimension = [60,40]
                position = [40 + math.trunc (_random.random()*800), 40 + math.trunc (_random.random()*800)]
                spec_id_list.append(temp_id)
                spec_dimension_list.append(dimension)
                spec_position_list.append(position)
            for i in range (numBoundaryNodes):
                temp_id = BoundaryNodes_ids[i]
                dimension = [60,40]
                position = [40 + math.trunc (_random.random()*800), 40 + math.trunc (_random.random()*800)]
                spec_id_list.append(temp_id)
                spec_dimension_list.append(dimension)
                spec_position_list.append(position)
            for i in range (numRxns):
                src_position = []
                dst_position = []
                mod_position = []
                src_dimension = []
                dst_dimension = []
                mod_dimension = []
                temp_id = Rxns_ids[i]
                kinetics = model.getRateLaw(i)
                rct_num = model.getNumReactants(i)
                prd_num = model.getNumProducts(i)
                mod_num = model.getNumModifiers(temp_id)
                for j in range(rct_num):
                    rct_id = model.getReactant(temp_id,j)
                    for k in range(numNodes):
                        if spec_id_list[k] == rct_id:
                            src_position.append(spec_position_list[k])
                            src_dimension.append(spec_dimension_list[k])
                for j in range(prd_num):
                    prd_id = model.getProduct(temp_id,j)
                    for k in range(numNodes):
                        if spec_id_list[k] == prd_id:
                            dst_position.append(spec_position_list[k])
                            dst_dimension.append(spec_dimension_list[k])  
                modifiers = model.getListOfModifiers(temp_id)
                for j in range(mod_num):
                    mod_id = modifiers[j]
                    for k in range(numNodes):
                        if spec_id_list[k] == mod_id:
                            mod_position.append(spec_position_list[k])
                            mod_dimension.append(spec_dimension_list[k])
                center_x = 0.
                center_y = 0.
                for j in range(rct_num):
                    center_x += src_position[j][0]+.5*src_dimension[j][0]
                    center_y += src_position[j][1]+.5*src_dimension[j][1]
                for j in range(prd_num):
                    center_x += dst_position[j][0]+.5*dst_dimension[j][0]
                    center_y += dst_position[j][1]+.5*dst_dimension[j][1]
                center_x = center_x/(rct_num + prd_num) 
                center_y = center_y/(rct_num + prd_num)
                center_position = [center_x, center_y]
                handles = [center_position]
                for j in range(rct_num):
                    src_handle_x = .5*(center_position[0] + src_position[j][0] + .5*src_dimension[j][0])
                    src_handle_y = .5*(center_position[1] + src_position[j][1] + .5*src_dimension[j][1])
                    handles.append([src_handle_x,src_handle_y])
                for j in range(prd_num):
                    dst_handle_x = .5*(center_position[0] + dst_position[j][0] + .5*dst_dimension[j][0])
                    dst_handle_y = .5*(center_position[1] + dst_position[j][1] + .5*dst_dimension[j][1])
                    handles.append([dst_handle_x,dst_handle_y])
                drawNetwork.addReaction(canvas, src_position, dst_position, mod_position,
                center_position, handles, src_dimension, dst_dimension, mod_dimension,
                reaction_line_color, reaction_line_width,
                reaction_line_type = reactionLineType, show_bezier_handles = showBezierHandles)
        
            for i in range (numFloatingNodes):
                temp_id = FloatingNodes_ids[i]
                for k in range(numNodes):
                    if spec_id_list[k] == temp_id:
                        position = spec_position_list[k]
                        dimension = spec_dimension_list[k]
                drawNetwork.addNode(canvas, 'floating', '', position, dimension,
                                    spec_border_color, spec_fill_color, spec_border_width,
                                    shapeIdx, complex_shape=complexShape)
                drawNetwork.addText(canvas, temp_id, position, dimension, text_line_color, text_line_width)   
            for i in range (numBoundaryNodes):
                temp_id = BoundaryNodes_ids[i]
                for k in range(numNodes):
                    if spec_id_list[k] == temp_id:
                        position = spec_position_list[k]
                        dimension = spec_dimension_list[k]
                drawNetwork.addNode(canvas, 'boundary', '', position, dimension,
                                    spec_border_color, spec_fill_color, spec_border_width,
                                    shapeIdx, complex_shape=complexShape)
                drawNetwork.addText(canvas, temp_id, position, dimension, text_line_color, text_line_width)

        drawNetwork.draw(surface, fileName = output_fileName, file_format = fileFormat ) 
    except:
      print("invalid SBML file")



if __name__ == '__main__':
    DIR = os.path.dirname(os.path.abspath(__file__))
    TEST_FOLDER = os.path.join(DIR, "test_sbml_files")

    filename = "test.xml"

    f = open(os.path.join(TEST_FOLDER, filename), 'r')
    sbmlStr = f.read()
    f.close()

    if len(sbmlStr) == 0:
        print("empty sbml")
    else:
        display(sbmlStr, fileFormat = 'JPEG')



