# -*- coding: utf-8 -*-
# This script was written by Jin Xu and available on Github
# https://github.com/SunnyXu/SBMLDiagrams

"""
Created on Mon Aug 23 13:25:34 2021
@author: Jin Xu
"""

import os
from collections import defaultdict

import skia
import simplesbml
from libsbml import *
import cv2
import numpy as np
import math
import random as _random
import string
from SBMLDiagrams import drawNetwork
from SBMLDiagrams import styleSBML


def animate(simulationData, baseImageArray, posDict, numDigit=5, folderName='animation', offset=20,
            textColor=None, textWidth=None, textDimension=None):
    """
    Animation for tellurium simulation

    Args:
        simulationData: numpy array for the simulation data

        baseImageArray: base image array used for generating the change

        posDict: position dictionary for the Floating Species

        numDigit: number of digits saved for display

        folderName: generated images folder place

        offset: text offset from the center of the compartment

        textColor: text color

        textWidth: text width

        textDimension: text dimension size

    Returns:
    """
    for i in range(len(simulationData)):
        surface = skia.Surface(np.array(baseImageArray, copy=True))
        canvas = surface.getCanvas()
        for letter, pos in posDict.items():
            new_pos = [pos[0] - offset, pos[1] - offset]
            drawNetwork.addText(canvas, str(simulationData[letter][i])[:numDigit],
                                new_pos, [40, 60], (0, 0, 0, 255), 1.)
        drawNetwork.draw(surface, folderName='animation', fileName='a' + str(i), file_format='PNG')

    imgs = []
    size = None
    files = sorted(os.listdir(os.getcwd() + '/' + folderName))
    for filename in files:
        imgName = os.path.join(os.getcwd() + '/' + folderName, filename)
        img = cv2.imread(imgName)
        height, width, layers = img.shape
        size = (width, height)
        imgs.append(img)

    out = cv2.VideoWriter(os.path.join(os.getcwd() + '/' + folderName, "output.mp4"), cv2.VideoWriter_fourcc(*'MP4V'),
                          1, size)

    for i in range(len(imgs)):
        out.write(imgs[i])
    out.release()

def display(sbmlStr, imageSize = [1000, 1000], fileFormat = 'PNG', output_fileName = 'output', \
    complexShape = '', reactionLineType = 'bezier', showBezierHandles = False, styleName = 'default',\
    newStyleClass = None):

    """
    Visualization from an sbml string to a PNG/JPG/PDF file.

    Args:  
        sbmlStr: str-the string of the input sbml file.

        imageSize: list-1*2 matrix-size of the rectangle [width, height]

        fileFormat: str-output file type: 'PNG' (default), 'JPEG' or 'PDF'.

        output_fileName: str-filename: 'output' (default) or '' (result in a random file name) or 'fileName' (self-designed file name).
        
        complexShape: str-type of complex shapes: '' (default) or 'monomer' or 'dimer' or 'trimer' or 'tetramer'.

        reactionLineType: str-type of the reaction line: 'linear' or 'bezier' (default).
        If there is no layout information from the SBML file, all reaction line will be drawn in
        straight lines even set as 'bezier'.

        showBezierHandles: bool-show the Bezier handles (True) or not (False as default).

        color_style: pre-existing color style for the graph

        newStyleClass: user-customized new color style

    Returns:
        The tuple of base image's array, position dictionary for the Floating Species, color style of the image
    """

    def draw_on_canvas(canvas):
        def hex_to_rgb(value):
            value = value.lstrip('#')
            if len(value) == 6:
                value = value + 'ff'
            return tuple(int(value[i:i+2], 16) for i in (0, 2, 4, 6))

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
        floatingNodes_pos_dict = defaultdict(list)
        shapeIdx = 1
        
        #set the default values without render info:
        color_style = newStyleClass
        if not newStyleClass:
            color_style = styleSBML.Style(styleName)
        comp_border_width = 2.0
        spec_border_width = 2.0
        reaction_line_width = 3.0
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

                    #orphan nodes
                    for i in range(numSpecGlyphs):
                        specGlyph = layout.getSpeciesGlyph(i)
                        specGlyph_id = specGlyph.getId()
                        if specGlyph_id not in specGlyph_id_list:
                            specGlyph_id_list.append(specGlyph_id)
                            spec_id = specGlyph.getSpeciesId()
                            spec_id_list.append(spec_id)
                            spec_specGlyph_id_list.append([spec_id,specGlyph_id])
                            boundingbox = specGlyph.getBoundingBox()
                            height = boundingbox.getHeight()
                            width = boundingbox.getWidth()
                            pos_x = boundingbox.getX()
                            pos_y = boundingbox.getY()
                            spec_dimension_list.append([width,height])
                            spec_position_list.append([pos_x,pos_y])
                            for k in range(numSpecGlyphs):
                                textGlyph_temp = layout.getTextGlyph(k)
                                temp_specGlyph_id = textGlyph_temp.getOriginOfTextId()
                                if temp_specGlyph_id == specGlyph_id:
                                    textGlyph = textGlyph_temp
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
                            spec_text_position_list.append([text_pos_x, text_pos_y])
                            spec_text_dimension_list.append([text_dim_w, text_dim_h])


                    #print(reaction_mod_list)
                    #print(mod_specGlyph_list)
                    #print(spec_specGlyph_id_list)

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
                            #group = color_style.getGroup()
                            group = style.getGroup()
                            typeList = style.createTypeString()
                            idList = style.createIdString()
                            if 'COMPARTMENTGLYPH' in typeList:
                                for k in range(len(color_list)):
                                    if color_list[k][0] == group.getFill():
                                        color_style.setCompFillColor(hex_to_rgb(color_list[k][1]))
                                    if color_list[k][0] == group.getStroke():
                                        color_style.setCompBorderColor(hex_to_rgb(color_list[k][1]))
                                comp_border_width = group.getStrokeWidth()
                                comp_render.append([idList, color_style.getCompFillColor(),
                                                    color_style.getCompBorderColor(),comp_border_width])
                            elif 'SPECIESGLYPH' in typeList:
                                for k in range(len(color_list)):
                                    if color_list[k][0] == group.getFill():
                                        color_style.setSpecFillColor(hex_to_rgb(color_list[k][1]))
                                    if color_list[k][0] == group.getStroke():
                                        color_style.setSpecBorderColor(hex_to_rgb(color_list[k][1]))
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

                                spec_render.append([idList,color_style.getSpecFillColor(),
                                                    color_style.getSpecBorderColor(),spec_border_width,shapeIdx])

                            elif 'REACTIONGLYPH' in typeList:
                                for k in range(len(color_list)):
                                    if color_list[k][0] == group.getStroke():
                                        color_style.setReactionLineColor(hex_to_rgb(color_list[k][1]))
                                reaction_line_width = group.getStrokeWidth()
                                rxn_render.append([idList, color_style.getReactionLineColor(), reaction_line_width])
                            elif 'TEXTGLYPH' in typeList:
                                for k in range(len(color_list)):
                                    if color_list[k][0] == group.getStroke():
                                        color_style.setTextLineColor(hex_to_rgb(color_list[k][1]))
                                text_line_width = group.getStrokeWidth()
                                #print(text_line_width)
                                #text_font_size = group.getFontSize()  #cannot give the fontsize
                                #text_font_size = group.getFontSize()
                                #print(group)
                                text_render.append([idList,color_style.getTextLineColor(),text_line_width])

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
                        color_style.setCompBorderColor((255, 255, 255, 255))
                        color_style.setCompFillColor((255, 255, 255, 255))
                        drawNetwork.addCompartment(canvas, position, dimension,
                                                color_style.getCompBorderColor(),
                                                   color_style.getCompFillColor(), comp_border_width)
                    else:
                        if len(comp_id_list) != 0:
                        #if mplugin is not None:                    
                            for j in range(numCompGlyphs):
                                if comp_id_list[j] == temp_id:
                                    dimension = comp_dimension_list[j]
                                    position = comp_position_list[j]
                            for j in range(len(comp_render)):
                                if temp_id == comp_render[j][0]:
                                    color_style.setCompFillColor(comp_render[j][1])
                                    color_style.setCompBorderColor(comp_render[j][2])
                                    comp_border_width = comp_render[j][3]
                        else:# no layout info about compartment,
                            # then the whole size of the canvas is the compartment size
                            # modify the compartment size using the max_rec function above
                            dimension = [1000, 1000]
                            position = [0,0]
                            color_style.setCompBorderColor((255, 255, 255, 255))
                            color_style.setCompFillColor((255, 255, 255, 255))
                        drawNetwork.addCompartment(canvas, position, dimension,
                                                color_style.getCompBorderColor(), color_style.getCompFillColor(),
                                                   comp_border_width)
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
                            color_style.setReactionLineColor(rxn_render[j][1])
                            reaction_line_width = rxn_render[j][2]
                    try: 
                        center_position = reaction_center_list[i]
                        center_handle = reaction_center_handle_list[i]
                        handles = [center_position]
                        handles.extend(src_handle)
                        handles.extend(dst_handle)   
                        drawNetwork.addReaction(canvas, src_position, dst_position, mod_position,
                        center_position, handles, src_dimension, dst_dimension, mod_dimension,
                        color_style.getReactionLineColor(), reaction_line_width,
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
                        drawNetwork.addReaction(canvas, src_position, dst_position, mod_position,
                        center_position, handles, src_dimension, dst_dimension, mod_dimension,
                        color_style.getReactionLineColor(), reaction_line_width,
                        reaction_line_type = reactionLineType, show_bezier_handles = showBezierHandles)
                            
                id_list = []
                # orphan nodes have been considered, so numSpec_in_reaction should equals to numSpecGlyphs
                # if numSpecGlyphs > numSpec_in_reaction:
                #     print("Orphan nodes are removed.")
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
                                        color_style.setSpecFillColor(spec_render[k][1])
                                        color_style.setSpecBorderColor(spec_render[k][2])
                                        spec_border_width = spec_render[k][3]
                                        shapeIdx = spec_render[k][4]
                                for k in range(len(text_render)):
                                    if temp_id == text_render[k][0]:
                                        color_style.setTextLineColor(text_render[k][1])
                                        text_line_width = text_render[k][2]
                                floatingNodes_pos_dict['[' + temp_id + ']'] = position
                                drawNetwork.addNode(canvas, 'floating', '', position, dimension,
                                                    color_style.getSpecBorderColor(), color_style.getSpecFillColor(),
                                                    spec_border_width, shapeIdx, complex_shape = complexShape)
                                drawNetwork.addText(canvas, temp_id, text_position, text_dimension,
                                                    color_style.getTextLineColor(), text_line_width)
                                id_list.append(temp_id)                    
                            else:
                                for k in range(len(spec_render)):
                                    if temp_id == spec_render[k][0]:
                                        color_style.setSpecFillColor(spec_render[k][1])
                                        color_style.setSpecBorderColor(spec_render[k][2])
                                        spec_border_width = spec_render[k][3]
                                        shapeIdx = spec_render[k][4]
                                for k in range(len(text_render)):
                                    if temp_id == text_render[k][0]:
                                        color_style.setTextLineColor(text_render[k][1])
                                        text_line_width = text_render[k][2]
                                floatingNodes_pos_dict['[' + temp_id + ']'] = position
                                drawNetwork.addNode(canvas, 'floating', 'alias', position, dimension,
                                                    color_style.getSpecBorderColor(), color_style.getSpecFillColor(),
                                                    spec_border_width, shapeIdx, complex_shape=complexShape)
                                drawNetwork.addText(canvas, temp_id, text_position, text_dimension,
                                                    color_style.getTextLineColor(), text_line_width)
                                id_list.append(temp_id)
                    for j in range(numBoundaryNodes):
                        if temp_id == BoundaryNodes_ids[j]:
                            if temp_id not in id_list:
                                for k in range(len(spec_render)):
                                    if temp_id == spec_render[k][0]:
                                        color_style.setSpecFillColor(spec_render[k][1])
                                        color_style.setSpecBorderColor(spec_render[k][2])
                                        spec_border_width = spec_render[k][3]
                                        shapeIdx = spec_render[k][4]
                                for k in range(len(text_render)):
                                    if temp_id == text_render[k][0]:
                                        color_style.setTextLineColor(text_render[k][1])
                                        text_line_width = text_render[k][2]
                                drawNetwork.addNode(canvas, 'boundary', '', position, dimension,
                                                    color_style.getSpecBorderColor(), color_style.getSpecFillColor(),
                                                    spec_border_width, shapeIdx, complex_shape=complexShape)
                                drawNetwork.addText(canvas, temp_id, text_position, text_dimension,
                                                    color_style.getTextLineColor(), text_line_width)
                                id_list.append(temp_id)
                            else:
                                for k in range(len(spec_render)):
                                    if temp_id == spec_render[k][0]:
                                        color_style.setSpecFillColor(spec_render[k][1])
                                        color_style.setSpecBorderColor(spec_render[k][2])
                                        spec_border_width = spec_render[k][3]
                                        shapeIdx = spec_render[k][4]
                                for k in range(len(text_render)):
                                    if temp_id == text_render[k][0]:
                                        color_style.setTextLineColor(text_render[k][1])
                                        text_line_width = text_render[k][2] 
                                drawNetwork.addNode(canvas, 'boundary', 'alias', position, dimension,
                                                    color_style.getSpecBorderColor(), color_style.getSpecFillColor(),
                                                    spec_border_width, shapeIdx, complex_shape=complexShape)
                                drawNetwork.addText(canvas, temp_id, text_position, text_dimension,
                                                    color_style.getTextLineColor(), text_line_width)
                                id_list.append(temp_id)

            else: # there is no layout information, assign position randomly and size as default
                comp_id_list = Comps_ids
                nodeIdx_temp = 0 #to track the node index    
                for i in range(numComps):
                    temp_id = Comps_ids[i]
                    vol= model.getCompartmentVolume(i)
                    dimension = [1000, 1000]
                    position = [0,0]
                    drawNetwork.addCompartment(canvas, position, dimension,
                                                color_style.getCompBorderColor(), color_style.getCompFillColor(),
                                               comp_border_width)
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
                    color_style.getReactionLineColor(), reaction_line_width,
                    reaction_line_type = reactionLineType, show_bezier_handles = showBezierHandles)
            
                for i in range (numFloatingNodes):
                    temp_id = FloatingNodes_ids[i]
                    for k in range(numNodes):
                        if spec_id_list[k] == temp_id:
                            position = spec_position_list[k]
                            dimension = spec_dimension_list[k]
                    floatingNodes_pos_dict['[' + temp_id + ']'] = position
                    drawNetwork.addNode(canvas, 'floating', '', position, dimension,
                                        color_style.getSpecBorderColor(), color_style.getSpecFillColor(), spec_border_width,
                                        shapeIdx, complex_shape=complexShape)
                    drawNetwork.addText(canvas, temp_id, position, dimension, color_style.getTextLineColor(), text_line_width)
                for i in range (numBoundaryNodes):
                    temp_id = BoundaryNodes_ids[i]
                    for k in range(numNodes):
                        if spec_id_list[k] == temp_id:
                            position = spec_position_list[k]
                            dimension = spec_dimension_list[k]
                    drawNetwork.addNode(canvas, 'boundary', '', position, dimension,
                                        color_style.getSpecBorderColor(), color_style.getSpecFillColor(), spec_border_width,
                                        shapeIdx, complex_shape=complexShape)
                    drawNetwork.addText(canvas, temp_id, position, dimension, color_style.getTextLineColor(), text_line_width)

        except Exception as e:
            print(e)
        return floatingNodes_pos_dict, color_style

    baseImageArray = []
    if fileFormat == "PNG" or fileFormat == "JPEG":
        surface = skia.Surface(imageSize[0], imageSize[1])
        canvas = surface.getCanvas()
        pos_dict, color_style = draw_on_canvas(canvas)
        baseImageArray = drawNetwork.draw(surface, fileName = output_fileName, file_format = fileFormat)
    else: #fileFormat == "PDF"
        if output_fileName == '':
            random_string = ''.join(_random.choices(string.ascii_uppercase + string.digits, k=10)) 
            fileName = os.path.join(os.getcwd(), random_string)
            fileNamepdf = fileName + '.pdf'
        else:
            fileName = os.path.join(os.getcwd(), output_fileName)
            fileNamepdf = fileName + '.pdf'
        stream = skia.FILEWStream(fileNamepdf)
        with skia.PDF.MakeDocument(stream) as document:
            with document.page(imageSize[0], imageSize[1]) as canvas:
                pos_dict, color_style = draw_on_canvas(canvas)
    return baseImageArray, pos_dict, color_style


# if __name__ == '__main__':
#     DIR = os.path.dirname(os.path.abspath(__file__))
#     TEST_FOLDER = os.path.join(DIR, "test_sbml_files")

#     filename = "test.xml"
#     #filename = "feedback.xml"
#     #filename = "LinearChain.xml"
#     #filename = "test_no_comp.xml"
#     #filename = "mass_action_rxn.xml"
#     #filename = "test_comp.xml"
#     #filename = "test_modifier.xml"
#     #filename = "node_grid.xml"

#     #filename = "Jana_WolfGlycolysis.xml"


#     f = open(os.path.join(TEST_FOLDER, filename), 'r')
#     sbmlStr = f.read()
#     f.close()

#     if len(sbmlStr) == 0:
#         print("empty sbml")
#     else:
#         display(sbmlStr, fileFormat='PNG')



