# -*- coding: utf-8 -*-
# This script was written by Jin Xu and available on Github
# https://github.com/SunnyXu/SBMLDiagrams
# Input is an SBML file, and output will be a dataframe/excel files.
"""
Created on Mon Aug 23 13:25:34 2021

@author: Jin Xu
"""

import os
import simplesbml
from libsbml import *
import math
import random as _random
import pandas as pd


#create datafames for NodeData, ReactionData, CompartmentData:
# Column names
netIdx = 0
NETIDX = 'net_idx'
IDX = 'idx'
ID = 'id'
#NODES = 'nodes'
#VOLUMNE = 'volume'
POSITION = 'position'
SIZE = 'size'
FILLCOLOR = 'fill_color'
BORDERCOLOR = 'border_color'
BORDERWIDTH = 'border_width'
COMPIDX = 'comp_idx'
ORIGINALIDX = 'original_idx'
FLOATINGNODE = 'floating_node'
CONCENTRATION = 'concentration'
SHAPEIDX = 'shape_idx'
TXTPOSITION = 'txt_position'
TXTSIZE = 'txt_size'
#TXTFONTSIZE = 'txt_font_size'
TXTFONTCOLOR = 'txt_font_color'
TXTLINEWIDTH = 'txt_line_width'
SOURCES = 'sources'
TARGETS = 'targets'
RATELAW = 'rate_law'
MODIFIERS = 'modifiers'
LINETHICKNESS = 'line_thickness'
CENTERPOS = 'center_pos'
HANDLES = 'handles'
BEZIER = 'bezier'
COLUMN_NAME_df_CompartmentData = [NETIDX, IDX, ID,\
    POSITION, SIZE, FILLCOLOR, BORDERCOLOR, BORDERWIDTH]
COLUMN_NAME_df_NodeData = [NETIDX, COMPIDX, IDX, ORIGINALIDX, ID, FLOATINGNODE,\
    CONCENTRATION, POSITION, SIZE, SHAPEIDX, TXTPOSITION, TXTSIZE,
    FILLCOLOR, BORDERCOLOR, BORDERWIDTH, TXTFONTCOLOR, TXTLINEWIDTH]
COLUMN_NAME_df_ReactionData = [NETIDX, IDX, ID, SOURCES, TARGETS, RATELAW, MODIFIERS, \
    FILLCOLOR, LINETHICKNESS, CENTERPOS, HANDLES, BEZIER]



def main(sbmlStr, reactionLineType, complexShape): 
    """
    Process the classification of kinetics for BioModel dataset

    input
    -------
    SBMLStr: str-the string of the input sbml file 
    reactionLineType: str-type of the reaction line: 'linear' or 'bezier'
    complexShape: str-type of complex shapes: '' or 'monomer' or 'dimer' or 'trimer' or 'tetramer'  

    Returns
    -------
    df_CompartmentData: DataFrame-Compartment information
    df_NodeData: DataFrame-Node information
    df_ReactionData: DataFrame-Reaction information

    """

    def hex_to_rgb(value):
        value = value.lstrip('#')
        #return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))
        return [int(value[i:i+2], 16) for i in (0, 2, 4)]

    df_CompartmentData = pd.DataFrame(columns = COLUMN_NAME_df_CompartmentData)
    df_NodeData = pd.DataFrame(columns = COLUMN_NAME_df_NodeData)
    df_ReactionData = pd.DataFrame(columns = COLUMN_NAME_df_ReactionData)

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
    spec_concentration_list = []
    
    #set the default values without render info:
    comp_fill_color = [158, 169, 255]
    comp_border_color = [0, 29, 255]
    comp_border_width = 2.0
    spec_fill_color = [255, 204, 153]
    spec_border_color = [255, 108, 9]
    spec_border_width = 2.0
    reaction_line_color = [129, 123, 255]
    reaction_line_width = 3.0
    text_line_color = [0,0,0]
    text_line_width = 1.
    
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
                    spec = model_layout.getSpecies(spec_id)
                    try:
                        concentration = spec.getInitialConcentration()
                    except:
                        concentration = 1.
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
                        spec_concentration_list.append(concentration)

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
                        #text_font_size = group.getFontSize() #can not give an int
                        text_render.append([idList,text_line_color,text_line_width])

    #try: 
        model = simplesbml.loadSBMLStr(sbmlStr)
        numFloatingNodes  = model.getNumFloatingSpecies()
        FloatingNodes_ids = model.getListOfFloatingSpecies()
        numBoundaryNodes  = model.getNumBoundarySpecies()
        BoundaryNodes_ids = model.getListOfBoundarySpecies()
        numNodes = numFloatingNodes + numBoundaryNodes
        numRxns   = model.getNumReactions()
        Rxns_ids  = model.getListOfReactionIds()
        numComps  = model.getNumCompartments()
        Comps_ids = model.getListOfCompartmentIds()
        comp_idx_id_list = []
        #Is this the same as comp_node_list?
        numNodes = numFloatingNodes + numBoundaryNodes
        comp_node_list = [0]*numComps #Note: numComps is different from numCompGlyphs
        for i in range(numComps):
            comp_node_list[i] = []

        #if there is layout info:
        if len(spec_id_list) != 0:
            for i in range(numComps):
                temp_id = Comps_ids[i]
                comp_idx_id_list.append([i,temp_id])
                vol= model.getCompartmentVolume(i)
                if temp_id == "_compartment_default_":
                    dimension = [3900, 2400]
                    position = [10, 10]
                    #comp_border_color = [255, 255, 255, 0] #the last digit for transparent
                    #comp_fill_color = [255, 255, 255, 0]
                    comp_border_color = [255, 255, 255]
                    comp_fill_color = [255, 255, 255]
                    CompartmentData_row_dct = {k:[] for k in COLUMN_NAME_df_CompartmentData}
                    CompartmentData_row_dct[NETIDX].append(netIdx)
                    CompartmentData_row_dct[IDX].append(i)
                    CompartmentData_row_dct[ID].append(temp_id)
                    #CompartmentData_row_dct[VOLUMNE].append(vol)
                    CompartmentData_row_dct[POSITION].append(position)
                    CompartmentData_row_dct[SIZE].append(dimension)
                    CompartmentData_row_dct[BORDERCOLOR].append(comp_border_color)
                    CompartmentData_row_dct[FILLCOLOR].append(comp_fill_color)
                    CompartmentData_row_dct[BORDERWIDTH].append(comp_border_width)
                    
                    for j in range(len(COLUMN_NAME_df_CompartmentData)):
                        try: 
                            CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]] = CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]][0]
                        except:
                            CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]] = ''
                    df_CompartmentData = df_CompartmentData.append(CompartmentData_row_dct, ignore_index=True)
     
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
                        # random assigned network:
                        # dimension = [800,800]
                        # position = [40,40]
                        # the whole size of the compartment: 4000*2500
                        dimension = [3900,2400]
                        position = [10,10]
                        #comp_fill_color = [255, 255, 255, 0]
                        #comp_border_color = [255, 255, 255, 0]
                        comp_fill_color = [255, 255, 255]
                        comp_border_color = [255, 255, 255]

                    CompartmentData_row_dct = {k:[] for k in COLUMN_NAME_df_CompartmentData}
                    CompartmentData_row_dct[NETIDX].append(netIdx)
                    CompartmentData_row_dct[IDX].append(i)
                    CompartmentData_row_dct[ID].append(temp_id)
                    #CompartmentData_row_dct[VOLUMNE].append(vol)
                    CompartmentData_row_dct[POSITION].append(position)
                    CompartmentData_row_dct[SIZE].append(dimension)
                    CompartmentData_row_dct[BORDERCOLOR].append(comp_border_color)
                    CompartmentData_row_dct[FILLCOLOR].append(comp_fill_color)
                    CompartmentData_row_dct[BORDERWIDTH].append(comp_border_width)
                    for j in range(len(COLUMN_NAME_df_CompartmentData)):
                        try: 
                            CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]] = CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]][0]
                        except:
                            CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]] = ''
                    df_CompartmentData = df_CompartmentData.append(CompartmentData_row_dct, ignore_index=True)


            numSpec_in_reaction = len(spec_specGlyph_id_list)

            id_list = []
            node_idx_specGlyphid_list = []
            #numSpecGlyphs is larger than numSpec_in_reaction if there orphan nodes
            if numSpecGlyphs > numSpec_in_reaction:
                print("Orphan nodes are removed.")
            for i in range (numSpec_in_reaction):
                temp_id = spec_specGlyph_id_list[i][0]
                temp_concentration = spec_concentration_list[i]
                tempGlyph_id = spec_specGlyph_id_list[i][1]
                dimension = spec_dimension_list[i]
                position = spec_position_list[i]
                text_position = spec_text_position_list[i]
                text_dimension = spec_text_dimension_list[i]
                comp_id = model.getCompartmentIdSpeciesIsIn(temp_id)
                temp_comp_idx = -1
                for j in range(len(comp_idx_id_list)):
                    if comp_idx_id_list[j][1] == comp_id:
                        temp_comp_idx = comp_idx_id_list[j][0]
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
                            id_list.append(temp_id)
                            node_idx_specGlyphid_list.append([i,tempGlyph_id])
                            
                            NodeData_row_dct = {k:[] for k in COLUMN_NAME_df_NodeData}
                            NodeData_row_dct[NETIDX].append(netIdx)
                            NodeData_row_dct[COMPIDX].append(temp_comp_idx)
                            NodeData_row_dct[IDX].append(i)
                            NodeData_row_dct[ORIGINALIDX].append(-1)
                            NodeData_row_dct[ID].append(temp_id)
                            NodeData_row_dct[FLOATINGNODE].append('TRUE')
                            NodeData_row_dct[CONCENTRATION].append(temp_concentration)
                            NodeData_row_dct[POSITION].append(position)
                            NodeData_row_dct[SIZE].append(dimension)
                            NodeData_row_dct[SHAPEIDX].append(shapeIdx)
                            NodeData_row_dct[TXTPOSITION].append(text_position)
                            NodeData_row_dct[TXTSIZE].append(text_dimension)
                            NodeData_row_dct[FILLCOLOR].append(spec_fill_color)
                            NodeData_row_dct[BORDERCOLOR].append(spec_border_color)
                            NodeData_row_dct[BORDERWIDTH].append(spec_border_width)
                            #NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                            NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                            NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                            for j in range(len(COLUMN_NAME_df_NodeData)):
                                try: 
                                    NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                                except:
                                    NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                            df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
                    
                        else:
                            original_idx = id_list.index(temp_id)
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
                            #id_list.append(temp_id)
                            node_idx_specGlyphid_list.append([i,tempGlyph_id])

                            NodeData_row_dct = {k:[] for k in COLUMN_NAME_df_NodeData}
                            NodeData_row_dct[NETIDX].append(netIdx)
                            NodeData_row_dct[COMPIDX].append(temp_comp_idx)
                            NodeData_row_dct[IDX].append(i)
                            NodeData_row_dct[ORIGINALIDX].append(original_idx)
                            NodeData_row_dct[ID].append(temp_id)
                            NodeData_row_dct[FLOATINGNODE].append('TRUE')
                            NodeData_row_dct[CONCENTRATION].append(temp_concentration)
                            NodeData_row_dct[POSITION].append(position)
                            NodeData_row_dct[SIZE].append(dimension)
                            NodeData_row_dct[SHAPEIDX].append(shapeIdx)
                            NodeData_row_dct[TXTPOSITION].append(text_position)
                            NodeData_row_dct[TXTSIZE].append(text_dimension)
                            NodeData_row_dct[FILLCOLOR].append(spec_fill_color)
                            NodeData_row_dct[BORDERCOLOR].append(spec_border_color)
                            NodeData_row_dct[BORDERWIDTH].append(spec_border_width)
                            #NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                            NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                            NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                            for j in range(len(COLUMN_NAME_df_NodeData)):
                                try: 
                                    NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                                except:
                                    NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                            df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
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
                            id_list.append(temp_id)
                            node_idx_specGlyphid_list.append([i,tempGlyph_id])

                            NodeData_row_dct = {k:[] for k in COLUMN_NAME_df_NodeData}
                            NodeData_row_dct[NETIDX].append(netIdx)
                            NodeData_row_dct[COMPIDX].append(temp_comp_idx)
                            NodeData_row_dct[IDX].append(i)
                            NodeData_row_dct[ORIGINALIDX].append(-1)
                            NodeData_row_dct[ID].append(temp_id)
                            NodeData_row_dct[FLOATINGNODE].append('FALSE')
                            NodeData_row_dct[CONCENTRATION].append(temp_concentration)
                            NodeData_row_dct[POSITION].append(position)
                            NodeData_row_dct[SIZE].append(dimension)
                            NodeData_row_dct[SHAPEIDX].append(shapeIdx)
                            NodeData_row_dct[TXTPOSITION].append(text_position)
                            NodeData_row_dct[TXTSIZE].append(text_dimension)
                            NodeData_row_dct[FILLCOLOR].append(spec_fill_color)
                            NodeData_row_dct[BORDERCOLOR].append(spec_border_color)
                            NodeData_row_dct[BORDERWIDTH].append(spec_border_width)
                            #NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                            NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                            NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                            for j in range(len(COLUMN_NAME_df_NodeData)):
                                try: 
                                    NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                                except:
                                    NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                            df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
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
                            #id_list.append(temp_id)
                            node_idx_specGlyphid_list.append([i,tempGlyph_id])

                            NodeData_row_dct = {k:[] for k in COLUMN_NAME_df_NodeData}
                            NodeData_row_dct[NETIDX].append(netIdx)
                            NodeData_row_dct[COMPIDX].append(temp_comp_idx)
                            NodeData_row_dct[IDX].append(i)
                            NodeData_row_dct[ORIGINALIDX].append(original_idx)
                            NodeData_row_dct[ID].append(temp_id)
                            NodeData_row_dct[FLOATINGNODE].append('FALSE')
                            NodeData_row_dct[CONCENTRATION].append(temp_concentration)
                            NodeData_row_dct[POSITION].append(position)
                            NodeData_row_dct[SIZE].append(dimension)
                            NodeData_row_dct[SHAPEIDX].append(shapeIdx)
                            NodeData_row_dct[TXTPOSITION].append(text_position)
                            NodeData_row_dct[TXTSIZE].append(text_dimension)
                            NodeData_row_dct[FILLCOLOR].append(spec_fill_color)
                            NodeData_row_dct[BORDERCOLOR].append(spec_border_color)
                            NodeData_row_dct[BORDERWIDTH].append(spec_border_width)
                            #NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                            NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                            NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                            for j in range(len(COLUMN_NAME_df_NodeData)):
                                try: 
                                    NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                                except:
                                    NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                            df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
    

            for i in range (numReactionGlyphs):
                src_idx_list = []
                src_position = []
                src_dimension = []
                dst_idx_list = [] 
                dst_position = []
                dst_dimension = []
                mod_idx_list = []
                mod_position = []
                mod_dimension = []
                src_handle = []
                dst_handle = []
                temp_id = reaction_id_list[i]
                kinetics = kinetics_list[i]
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
                    for k in range(len(node_idx_specGlyphid_list)):
                        if temp_specGlyph_id == node_idx_specGlyphid_list[k][1]:
                            src_idx_list.append(node_idx_specGlyphid_list[k][0])
                    for k in range(numSpec_in_reaction):
                        if temp_specGlyph_id == specGlyph_id_list[k]:
                            src_position.append(spec_position_list[k])
                            src_dimension.append(spec_dimension_list[k])
                    src_handle.append(rct_specGlyph_handle_list[i][j][1])
                src_idx_list_corr = []
                [src_idx_list_corr.append(x) for x in src_idx_list if x not in src_idx_list_corr]
                
                for j in range(prd_num):
                    temp_specGlyph_id = prd_specGlyph_handle_list[i][j][0]
                    for k in range(len(node_idx_specGlyphid_list)):
                        if temp_specGlyph_id == node_idx_specGlyphid_list[k][1]:
                            dst_idx_list.append(node_idx_specGlyphid_list[k][0])
                    for k in range(numSpec_in_reaction):
                        if temp_specGlyph_id == specGlyph_id_list[k]:
                            dst_position.append(spec_position_list[k])
                            dst_dimension.append(spec_dimension_list[k])
                    dst_handle.append(prd_specGlyph_handle_list[i][j][1])
                dst_idx_list_corr = []
                [dst_idx_list_corr.append(x) for x in dst_idx_list if x not in dst_idx_list_corr]

                for j in range(mod_num):
                    if len(mod_specGlyph_list[i]) != 0:
                        temp_specGlyph_id = mod_specGlyph_list[i][j]
                        for k in range(len(node_idx_specGlyphid_list)):
                            if temp_specGlyph_id == node_idx_specGlyphid_list[k][1]:
                                mod_idx_list.append(node_idx_specGlyphid_list[k][0])
                        for k in range(numSpec_in_reaction):
                            if temp_specGlyph_id == specGlyph_id_list[k]:
                                mod_position.append(spec_position_list[k])
                                mod_dimension.append(spec_dimension_list[k])
                    else:
                        for k in range(len(spec_specGlyph_id_list)):
                            if reaction_mod_list[i][j] == spec_specGlyph_id_list[k][0]:
                                temp_specGlyph_id = spec_specGlyph_id_list[k][1]
                        for k in range(len(node_idx_specGlyphid_list)):
                            if temp_specGlyph_id == node_idx_specGlyphid_list[k][1]:
                                mod_idx_list.append(node_idx_specGlyphid_list[k][0])
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
                    #print(reaction_center_list)
                    center_handle = reaction_center_handle_list[i]
                    handles = [center_handle]
                    handles.extend(src_handle)
                    handles.extend(dst_handle)   
                    #print(handles)
                    ReactionData_row_dct = {k:[] for k in COLUMN_NAME_df_ReactionData}
                    ReactionData_row_dct[NETIDX].append(netIdx)
                    ReactionData_row_dct[IDX].append(i)
                    ReactionData_row_dct[ID].append(temp_id)
                    ReactionData_row_dct[SOURCES].append(src_idx_list_corr)
                    ReactionData_row_dct[TARGETS].append(dst_idx_list_corr)
                    ReactionData_row_dct[RATELAW].append(kinetics)
                    ReactionData_row_dct[MODIFIERS].append(mod_idx_list)
                    ReactionData_row_dct[FILLCOLOR].append(reaction_line_color)
                    ReactionData_row_dct[LINETHICKNESS].append(reaction_line_width)
                    ReactionData_row_dct[CENTERPOS].append(center_position)
                    ReactionData_row_dct[HANDLES].append(handles)
                    if reactionLineType == 'bezier':
                        ReactionData_row_dct[BEZIER].append('TRUE')
                    else:
                        ReactionData_row_dct[BEZIER].append('FALSE')
                    for j in range(len(COLUMN_NAME_df_ReactionData)):
                        try: 
                            ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]][0]
                        except:
                            ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ''
                    df_ReactionData = df_ReactionData.append(ReactionData_row_dct, ignore_index=True)
                
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
                    ReactionData_row_dct = {k:[] for k in COLUMN_NAME_df_ReactionData}
                    ReactionData_row_dct[NETIDX].append(netIdx)
                    ReactionData_row_dct[IDX].append(i)
                    ReactionData_row_dct[ID].append(temp_id)
                    ReactionData_row_dct[SOURCES].append(src_idx_list_corr)
                    ReactionData_row_dct[TARGETS].append(dst_idx_list_corr)
                    ReactionData_row_dct[RATELAW].append(kinetics)
                    ReactionData_row_dct[MODIFIERS].append(mod_idx_list)
                    ReactionData_row_dct[FILLCOLOR].append(reaction_line_color)
                    ReactionData_row_dct[LINETHICKNESS].append(reaction_line_width)
                    ReactionData_row_dct[CENTERPOS].append(center_position)
                    ReactionData_row_dct[HANDLES].append(handles)
                    if reactionLineType == 'bezier':
                        ReactionData_row_dct[BEZIER].append('TRUE')
                    else:
                        ReactionData_row_dct[BEZIER].append('FALSE')
                    for j in range(len(COLUMN_NAME_df_ReactionData)):
                        try: 
                            ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]][0]
                        except:
                            ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ''
                    df_ReactionData = df_ReactionData.append(ReactionData_row_dct, ignore_index=True)
   

        else: # there is no layout information, assign position randomly and size as default
    
            comp_id_list = Comps_ids
            nodeIdx_temp = 0 #to track the node index    
            for i in range(numComps):
                temp_id = Comps_ids[i]
                comp_idx_id_list.append([i,temp_id])
                vol= model.getCompartmentVolume(i)
                dimension = [3900,2400]
                position = [10,10]

                CompartmentData_row_dct = {k:[] for k in COLUMN_NAME_df_CompartmentData}
                CompartmentData_row_dct[NETIDX].append(netIdx)
                CompartmentData_row_dct[IDX].append(i)
                CompartmentData_row_dct[ID].append(temp_id)
                #CompartmentData_row_dct[VOLUMNE].append(vol)
                CompartmentData_row_dct[POSITION].append(position)
                CompartmentData_row_dct[SIZE].append(dimension)
                CompartmentData_row_dct[BORDERCOLOR].append(comp_border_color)
                CompartmentData_row_dct[FILLCOLOR].append(comp_fill_color)
                CompartmentData_row_dct[BORDERWIDTH].append(comp_border_width)
                for j in range(len(COLUMN_NAME_df_CompartmentData)):
                    try: 
                        CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]] = CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]][0]
                    except:
                        CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]] = ''
                df_CompartmentData = df_CompartmentData.append(CompartmentData_row_dct, ignore_index=True)
            
            spec_id_list = [] 
            spec_dimension_list = []
            spec_position_list = []
            node_idx_specid_list = []
            for i in range (numFloatingNodes):
                temp_id = FloatingNodes_ids[i]
                try:
                    temp_concentration = model.getSpeciesInitialConcentration(temp_id)
                except:
                    temp_concentration = 1.0
                dimension = [60,40]
                position = [40 + math.trunc (_random.random()*800), 40 + math.trunc (_random.random()*800)]
                spec_id_list.append(temp_id)
                spec_dimension_list.append(dimension)
                spec_position_list.append(position)
                node_idx_specid_list.append([i,temp_id])
            for i in range (numBoundaryNodes):
                temp_id = BoundaryNodes_ids[i]
                try:
                    temp_concentration = model.getSpeciesInitialConcentration(temp_id)
                except:
                    temp_concentration = 1.0
                dimension = [60,40]
                position = [40 + math.trunc (_random.random()*800), 40 + math.trunc (_random.random()*800)]
                spec_id_list.append(temp_id)
                spec_dimension_list.append(dimension)
                spec_position_list.append(position)
                node_idx_specid_list.append([i+numFloatingNodes,temp_id])
            #print(node_idx_specid_list)

            for i in range (numFloatingNodes):
                temp_id = FloatingNodes_ids[i]
                comp_id = model.getCompartmentIdSpeciesIsIn(temp_id)
                temp_comp_idx = -1
                for j in range(len(comp_idx_id_list)):
                    if comp_idx_id_list[j][1] == comp_id:
                        temp_comp_idx = comp_idx_id_list[j][0]
                for k in range(numNodes):
                    if spec_id_list[k] == temp_id:
                        position = spec_position_list[k]
                        dimension = spec_dimension_list[k]

                NodeData_row_dct = {k:[] for k in COLUMN_NAME_df_NodeData}
                NodeData_row_dct[NETIDX].append(netIdx)
                NodeData_row_dct[COMPIDX].append(temp_comp_idx)
                NodeData_row_dct[IDX].append(i)
                NodeData_row_dct[ORIGINALIDX].append(-1)
                NodeData_row_dct[ID].append(temp_id)
                NodeData_row_dct[FLOATINGNODE].append('TRUE')
                NodeData_row_dct[CONCENTRATION].append(temp_concentration)
                NodeData_row_dct[POSITION].append(position)
                NodeData_row_dct[SIZE].append(dimension)
                NodeData_row_dct[SHAPEIDX].append(shapeIdx)
                NodeData_row_dct[TXTPOSITION].append(position)
                NodeData_row_dct[TXTSIZE].append(dimension)
                NodeData_row_dct[FILLCOLOR].append(spec_fill_color)
                NodeData_row_dct[BORDERCOLOR].append(spec_border_color)
                NodeData_row_dct[BORDERWIDTH].append(spec_border_width)
                #NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                for j in range(len(COLUMN_NAME_df_NodeData)):
                    try: 
                        NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                    except:
                        NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
            for i in range (numBoundaryNodes):
                temp_id = BoundaryNodes_ids[i]
                comp_id = model.getCompartmentIdSpeciesIsIn(temp_id)
                temp_comp_idx = -1
                for j in range(len(comp_idx_id_list)):
                    if comp_idx_id_list[j][1] == comp_id:
                        temp_comp_idx = comp_idx_id_list[j][0]
                for k in range(numNodes):
                    if spec_id_list[k] == temp_id:
                        position = spec_position_list[k]
                        dimension = spec_dimension_list[k]

                
                NodeData_row_dct = {k:[] for k in COLUMN_NAME_df_NodeData}
                NodeData_row_dct[NETIDX].append(netIdx)
                NodeData_row_dct[COMPIDX].append(temp_comp_idx)
                NodeData_row_dct[IDX].append(numFloatingNodes + i)
                NodeData_row_dct[ORIGINALIDX].append(-1)
                NodeData_row_dct[ID].append(temp_id)
                NodeData_row_dct[FLOATINGNODE].append('FALSE')
                NodeData_row_dct[CONCENTRATION].append(temp_concentration)
                NodeData_row_dct[POSITION].append(position)
                NodeData_row_dct[SIZE].append(dimension)
                NodeData_row_dct[SHAPEIDX].append(shapeIdx)
                NodeData_row_dct[TXTPOSITION].append(position)
                NodeData_row_dct[TXTSIZE].append(dimension)
                NodeData_row_dct[FILLCOLOR].append(spec_fill_color)
                NodeData_row_dct[BORDERCOLOR].append(spec_border_color)
                NodeData_row_dct[BORDERWIDTH].append(spec_border_width)
                #NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                for j in range(len(COLUMN_NAME_df_NodeData)):
                    try: 
                        NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                    except:
                        NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
    
            for i in range (numRxns):
                src_idx_list = []
                dst_idx_list = []
                mod_idx_list = []
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
                    for k in range(len(node_idx_specid_list)):
                        if node_idx_specid_list[k][1] == rct_id:
                            src_idx_list.append(node_idx_specid_list[k][0])
                    for k in range(numNodes):
                        if spec_id_list[k] == rct_id:
                            src_position.append(spec_position_list[k])
                            src_dimension.append(spec_dimension_list[k])
                src_idx_list_corr = []
                [src_idx_list_corr.append(x) for x in src_idx_list if x not in src_idx_list_corr]

                for j in range(prd_num):
                    prd_id = model.getProduct(temp_id,j)
                    for k in range(len(node_idx_specid_list)):
                        if node_idx_specid_list[k][1] == prd_id:
                            dst_idx_list.append(node_idx_specid_list[k][0])
                    for k in range(numNodes):
                        if spec_id_list[k] == prd_id:
                            dst_position.append(spec_position_list[k])
                            dst_dimension.append(spec_dimension_list[k])  
                dst_idx_list_corr = []
                [dst_idx_list_corr.append(x) for x in dst_idx_list if x not in dst_idx_list_corr]

                modifiers = model.getListOfModifiers(temp_id)
                for j in range(mod_num):
                    mod_id = modifiers[j]
                    for k in range(len(node_idx_specid_list)):
                        if node_idx_specid_list[k][1] == mod_id:
                            mod_idx_list.append(node_idx_specid_list[k][0])
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
                
                ReactionData_row_dct = {k:[] for k in COLUMN_NAME_df_ReactionData}
                ReactionData_row_dct[NETIDX].append(netIdx)
                ReactionData_row_dct[IDX].append(i)
                ReactionData_row_dct[ID].append(temp_id)
                ReactionData_row_dct[SOURCES].append(src_idx_list_corr)
                ReactionData_row_dct[TARGETS].append(dst_idx_list_corr)
                ReactionData_row_dct[RATELAW].append(kinetics)
                ReactionData_row_dct[MODIFIERS].append(mod_idx_list)
                ReactionData_row_dct[FILLCOLOR].append(reaction_line_color)
                ReactionData_row_dct[LINETHICKNESS].append(reaction_line_width)
                ReactionData_row_dct[CENTERPOS].append(center_position)
                ReactionData_row_dct[HANDLES].append(handles)
                if reactionLineType == 'bezier':
                    ReactionData_row_dct[BEZIER].append('TRUE')
                else:
                    ReactionData_row_dct[BEZIER].append('FALSE')
                for j in range(len(COLUMN_NAME_df_ReactionData)):
                    try: 
                        ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]][0]
                    except:
                        ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ''
                df_ReactionData = df_ReactionData.append(ReactionData_row_dct, ignore_index=True)  

        return (df_CompartmentData, df_NodeData, df_ReactionData) 

    # except:
    #    raise ValueError('Invalid SBML!')


if __name__ == '__main__':

    dirname = "test_sbml_files"
    #simple files
    filename = "test.xml" 
    #filename = 'test_line.xml' 
    #no layout 
    #filename = "E_coli_Millard2016.xml" 
    #filename = 'feedback-self.xml' #does not work
    #part layout
    #filename = "LinearChain.xml" 
    #filename = "Feedback-Sauro.xml" 
    #filename = "Jana_WolfGlycolysis.xml" 
    #whole layout  
    #filename = 'test_center.xml' 
    #filename = 'test_handles.xml'
    #filename = 'test_arrows.xml'
    #filename = 'test_no_comp.xml'
    #filename = 'test_comp.xml'
    #invalid sbml 
    #filename = 'testbigmodel.xml' 
    #modifiers
    #filename = 'test_modifier.xml' 
    #filename = 'test_modifier_comp.xml' works from the excel file DataFrame_sample.xlsx
    #filename = "BorisEJB.xml"


    #check
    reactionLineType = 'bezier' #'linear' or 'bezier'
    complexShape = '' #'' or 'monomer' or 'dimer' or 'trimer' or 'tetramer'


    f = open(os.path.join(dirname, filename), 'r')
    sbmlStr = f.read()
    f.close()

    if len(sbmlStr) == 0:
        print("empty sbml")
    else:
        (df_CompartmentData, df_NodeData, df_ReactionData) = main(sbmlStr, reactionLineType, complexShape)
        df_CompartmentData.to_csv("CompartmentData.csv", index=False)
        df_NodeData.to_csv("NodeData.csv", index=False)
        df_ReactionData.to_csv("ReactionData.csv", index=False)


