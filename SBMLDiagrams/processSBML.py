# -*- coding: utf-8 -*-
# This script was written by Jin Xu and available on Github
# https://github.com/SunnyXu/SBMLDiagrams

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
from SBMLDiagrams import exportSBML
from SBMLDiagrams import editSBML
#import exportSBML
#import editSBML

#create datafames for NodeData, ReactionData, CompartmentData:
# Column names
netIdx = 0
NETIDX = 'net_idx'
IDX = 'idx'
ID = 'id'
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

#import the color list from colors.xlsx
DIR = os.path.dirname(os.path.abspath(__file__))
color_xls = pd.ExcelFile(os.path.join(DIR, 'colors.xlsx'))
df_color = pd.read_excel(color_xls, sheet_name = 'colors')


def _rgb_to_color(rgb):
    """
    transfer a list of rgb to a color list with decimal_rgba, html_name and hex_string

    Args:  
        rgb: list-1*3 or 1*4 matrix for a decimal rgb or rgba.

    Returns:
        color: list-[decimal_rgb, html_name, hex_string]
    
    """
    color = []
    if len(rgb) == 3:
        #decial_rgba:
        rgba = rgb.copy()
        a = 255 # default is fully opaque, the value should be int 255.
        rgba.append(a)
        #hex_string:
        hex_str = '#%02X%02X%02X%02X' % (rgba[0],rgba[1],rgba[2],rgba[3])
        #html_name:
        html_name = ''
        hex_str_search = hex_str[0:-2]
        if hex_str_search in df_color.values:
            index = df_color.index[df_color["hex_string"] == hex_str_search].tolist()[0] #row index 
            html_name = df_color.iloc[index]["html_name"]
        color.append(rgba)
        color.append(html_name)
        color.append(hex_str)
    elif len(rgb) == 4:
        #decial_rgba:
        rgba = rgb.copy()
        #hex_string:
        hex_str = '#%02X%02X%02X%02X' % (rgba[0],rgba[1],rgba[2],rgba[3])
        #html_name:
        html_name = ''
        hex_str_search = hex_str[0:-2]
        if hex_str_search in df_color.values:
            index = df_color.index[df_color["hex_string"] == hex_str_search].tolist()[0] #row index 
            html_name = df_color.iloc[index]["html_name"]
        color.append(rgba)
        color.append(html_name)
        color.append(hex_str)
    else:
        color = [[], '', '']

    return color

def _SBMLToDF(sbmlStr, reactionLineType = 'bezier'): 
    """
    Save the information of an SBML file to a set of dataframe.

    Args:  
        sbmlStr: str-the string of the input sbml file.

        reactionLineType: str-type of the reaction line: 'linear' or 'bezier' (default).

    Returns:
        (df_CompartmentData, df_NodeData, df_ReactionData): tuple

        df_CompartmentData: DataFrame-Compartment information.

        df_NodeData: DataFrame-Node information.

        df_ReactionData: DataFrame-Reaction information.
    
    """

    def hex_to_rgb(value):
        value = value.lstrip('#')
        if len(value) == 6:
            value = value + 'ff'
        return [int(value[i:i+2], 16) for i in (0, 2, 4, 6)]

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
    comp_fill_color = [158, 169, 255, 200]
    comp_border_color = [0, 29, 255, 255]
    comp_border_width = 2.0
    spec_fill_color = [255, 204, 153, 200]
    spec_border_color = [255, 108, 9, 255]
    spec_border_width = 2.0
    reaction_line_color = [91, 176, 253, 255]
    reaction_line_width = 3.0
    text_line_color = [0, 0, 0, 255]
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
                    # listOfCurveSegments = curve.getListOfCurveSegments()
                    # for j in range(len(listOfCurveSegments)):
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
                        try:
                            concentration = spec.getInitialConcentration()
                        except:
                            concentration = 1.
                        spec_concentration_list.append(concentration)

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
                    dimension = [1000, 1000]
                    position = [0, 0]
                    comp_border_color = [255, 255, 255, 255]
                    comp_fill_color = [255, 255, 255, 255]
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
                        dimension = [1000,1000]
                        position = [0,0]
                        comp_fill_color = [255, 255, 255, 255]
                        comp_border_color = [255, 255, 255, 255]

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
            # orphan nodes have been considered, so numSpec_in_reaction should equals to numSpecGlyphs
            # if numSpecGlyphs > numSpec_in_reaction:
            #     print("Orphan nodes are removed.")
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
                dimension = [1000,1000]
                position = [0,0]

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

    except Exception as e:
        print(e)

class load:
    def __init__(self, sbmlstr):
        self.sbmlstr = sbmlstr
        #self.df = _SBMLToDF(self.sbmlstr, reactionLineType='bezier')
        self.df = _SBMLToDF(self.sbmlstr)

    def getCompartmentPosition(self, id):
        """
        Get the position of a compartment with its certain compartment id

        Args: 
            id: str-the id of the compartment

        Returns:
            position_list: list of position

            position: list-1*2 matrix-leftup corner of the rectangle [position_x, position_y].
        """

        idx_list = self.df[0].index[self.df[0]["id"] == id].tolist()
        position_list =[] 
        for i in range(len(idx_list)):
            position_list.append(self.df[0].iloc[idx_list[i]]["position"])

        return position_list

    def getCompartmentSize(self, id):
        """
        Get the size of a compartment with its certain compartment id

        Args: 
            id: str-the id of the compartment

        Returns:
            size_list: list of size

            size: list-1*2 matrix-size of the rectangle [width, height].
        """

        idx_list = self.df[0].index[self.df[0]["id"] == id].tolist()
        size_list =[] 
        for i in range(len(idx_list)):
            size_list.append(self.df[0].iloc[idx_list[i]]["size"])

        return size_list

    def getCompartmentFillColor(self, id):
        """
        Get the fill color of a compartment with its certain compartment id

        Args: 
            id: str-the id of the compartment

        Returns:
            fill_color_list: list of fill_color

            fill_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), hex str (8 digits)]
        """
        idx_list = self.df[0].index[self.df[0]["id"] == id].tolist() #row index
        fill_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[0].iloc[idx_list[i]]["fill_color"]
            color = _rgb_to_color(rgb)
            fill_color_list.append(color)

        return fill_color_list

    def getCompartmentBorderColor(self, id):
        """
        Get the border color of a compartment with its certain id

        Args: 
            id: str-the id of the compartment

        Returns:
            border_color_list: list of border_color

            border_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), hex str (8 digits)]

        """
        idx_list = self.df[0].index[self.df[0]["id"] == id].tolist()
        border_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[0].iloc[idx_list[i]]["border_color"]
            color = _rgb_to_color(rgb)
            border_color_list.append(color)

        return border_color_list

    def getCompartmentBorderWidth(self, id):
        """
        Get the border width of a compartment with its certain compartment id

        Args: 
            id: str-the id of the compartment

        Returns:
            border_width_list: list of border_width

            border_width: float-compartment border line width.
        """
        
        idx_list = self.df[0].index[self.df[0]["id"] == id].tolist()
        border_width_list =[] 
        for i in range(len(idx_list)):
            border_width_list.append(self.df[0].iloc[idx_list[i]]["border_width"])

        return border_width_list


    def isFloatingNode(self, id):
        """
        Judge whether a node is floating node with its certain node id

        Args: 
            id: str-the id of the Node

        Returns:
            floating_node_list: list of floating_node

            floating_node: str-floating node (True) or not (False).
        """
        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        floating_node_list =[] 
        for i in range(len(idx_list)):
            floating_node_list.append(bool(self.df[1].iloc[idx_list[i]]["floating_node"]))

        return floating_node_list


    def getNodePosition(self, id):
        """
        Get the position of a node with its certain node id

        Args: 
            id: str-the id of the Node

        Returns:
            position_list: list of position

            position: list-1*2 matrix-leftup corner of the rectangle [position_x, position_y].
        """

        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        position_list =[] 
        for i in range(len(idx_list)):
            position_list.append(self.df[1].iloc[idx_list[i]]["position"])

        return position_list
        

    def getNodeSize(self, id):
        """
        Get the size of a node with its certain node id

        Args: 
            id: str-the id of the node

        Returns:
            size_list: list of size

            size: list-1*2 matrix-size of the rectangle [width, height].
        """
        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        size_list =[] 
        for i in range(len(idx_list)):
            size_list.append(self.df[1].iloc[idx_list[i]]["size"])

        return size_list

    def getNodeShape(self, id):
        """
        Get the shape index and the shape of a node with its certain node id

        Args: 
            id: str-the id of the node

        Returns:
            shape_list: list of tuple (shape_idx, shape)

            (shape_idx, shape): tuple
            
            shape_idx: int-1:rectangle, 2:circle, 3:hexagon, 4:line, 5:triangle.
            
            shape: str
        """

        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()

        shape_list =[] 
        for i in range(len(idx_list)):
            shape_idx = 0
            shape = "text_only"
            shape_idx = self.df[1].iloc[idx_list[i]]["shape_idx"]
            if shape_idx == 1:
                shape = "reactangle"
            elif shape_idx == 2:
                shape = "circle"
            elif shape_idx == 3:
                shape = "hexagon"
            elif shape_idx == 4:
                shape = "line"
            elif shape_idx == 5:
                shape = "triangle"

            shape_list.append((shape_idx, shape))

        return shape_list


    def getNodeTextPosition(self, id):
        """
        Get the text position of a node with its certain node id

        Args: 
            id: str-the id of node

        Returns:
            txt_position_list: list of txt_position

            txt_position: list-1*2 matrix-leftup corner of the rectangle [position_x, position_y].
        """
        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        txt_position_list =[] 
        for i in range(len(idx_list)):
            txt_position_list.append(self.df[1].iloc[idx_list[i]]["txt_position"])

        return txt_position_list

        
    def getNodeTextSize(self, id):
        """
        Get the text size of a node with its certain node id

        Args: 
            id: str-the id of the node

        Returns:
            txt_size_list: list of txt_size

            txt_size: list-1*2 matrix-size of the rectangle [width, height].
        """
        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        txt_size_list =[] 
        for i in range(len(idx_list)):
            txt_size_list.append(self.df[1].iloc[idx_list[i]]["txt_size"])

        return txt_size_list


    def getNodeFillColor(self, id):
        """
        Get the fill color of a node with its certain node id

        Args: 
            id: str-the id of the node

        Returns:
            fill_color_list: list of fill_color

            fill_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), hex str (8 digits)]
        """

        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        fill_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[1].iloc[idx_list[i]]["fill_color"]
            #print(rgb)
            #print(type(rgb))
            color = _rgb_to_color(rgb)
            fill_color_list.append(color)

        return fill_color_list


    def getNodeBorderColor(self, id):
        """
        Get the border color of a node with its certain node id

        Args: 
            id: str-the id of the node


        Returns:
            border_color_list: list of border_color

            border_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), hex str (8 digits)]
        """

        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        border_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[1].iloc[idx_list[i]]["border_color"]
            color = _rgb_to_color(rgb)
            border_color_list.append(color)

        return border_color_list


    def getNodeBorderWidth(self, id):
        """
        Get the border width of a node with its certain node id

        Args: 
            id: str-the id of the node

        Returns:
            border_width: float-node border line width.
        """
        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        border_width_list =[] 
        for i in range(len(idx_list)):
            border_width_list.append(self.df[1].iloc[idx_list[i]]["border_width"])

        return border_width_list

    def getNodeTextFontColor(self, id):
        """
        Get the text font color of a node with its certain node id

        Args: 
            id: str-the id of the node

        Returns:
            txt_font_color_list: list of txt_font_color

            txt_font_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), hex str (8 digits)]
        """

        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        txt_font_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[1].iloc[idx_list[i]]["txt_font_color"]
            color = _rgb_to_color(rgb)
            txt_font_color_list.append(color)

        return txt_font_color_list

    def getNodeTextLineWidth(self, id):
        """
        Get the text line width of a node with its certain node id

        Args: 
            id: int-the id of the node

        Returns:
            txt_line_width_list: list of txt_line_width

            txt_line_width: float-node text line width.
        """
        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        txt_line_width_list =[] 
        for i in range(len(idx_list)):
            txt_line_width_list.append(self.df[1].iloc[idx_list[i]]["txt_line_width"])

        return txt_line_width_list

    def getReactionFillColor(self, id):
        """
        Get the fill color of a reaction with its certain reaction id

        Args: 
            id: str-the id of the reaction

        Returns:
            fill_color_list: list of fill_color

            fill_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), hex str (8 digits)]
        """
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        fill_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[2].iloc[idx_list[i]]["fill_color"]
            color = _rgb_to_color(rgb)
            fill_color_list.append(color)

        return fill_color_list

    def getReactionLineThickness(self, id):
        """
        Get the line thickness of a reaction with its certain reaction id

        Args: 
            id: str-the id of the reaction

        Returns:
            line_thickness_list: list of line_thickness

            line_thickness: float-reaction border line width.
        """
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        line_thickness_list =[] 
        for i in range(len(idx_list)):
            line_thickness_list.append(self.df[2].iloc[idx_list[i]]["line_thickness"])

        return line_thickness_list

    def isBezierReactionType(self, id):
        """
        Judge whether it is a bezier reaction curve with its certain reaction id

        Args: 
            id: str-the id of the reaction

        Returns:
            bezier_list: list of bezier

            bezier: bool-bezier reaction (True) or not (False)
        """
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        bezier_list =[] 
        for i in range(len(idx_list)):
            bezier_list.append(bool(self.df[2].iloc[idx_list[i]]["bezier"]))

        return bezier_list
    
    def setCompartmentPosition(self, id, position):
        """
        Set the compartment position

        Args:  
            id: str-compartment id.

            position: list-1*2 matrix-leftup corner of the rectangle [position_x, position_y].
        """
        self.df = editSBML._setCompartmentPosition(self.df, id, position)
        return self.df
    
    def setCompartmentSize(self, id, size):
        """
        Set the compartment size

        Args:  
            id: str-compartment id.

            size: list-1*2 matrix-size of the rectangle [width, height].
        """
        self.df = editSBML._setCompartmentSize(self.df, id, size)
        return self.df

    def setCompartmentFillColor(self, id, fill_color, opacity = 1.):
        """
        Set the compartment fill color

        Args:  
            id: str-compartment iid.

            fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).
        """
        self.df = editSBML._setCompartmentFillColor(self.df, id, fill_color, opacity)
        return self.df

    def setCompartmentBorderColor(self, id, border_color, opacity = 1.):       
        """
        Set the compartment border color

        Args:  
            id: str-compartment id.

            border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

        """
        self.df = editSBML._setCompartmentBorderColor(self.df, id, border_color, opacity)
        return self.df

    def setCompartmentBorderWidth(self, id, border_width):
        """
        Set the compartment border width

        Args:  
            id: str-compartment id.

            border_width: float-compartment border line width.
        """
        self.df = editSBML._setCompartmentBorderWidth(self.df, id, border_width)
        return self.df

    def setFloatingBoundaryNode(self, id, floating_node):
        """
        Set a node to be floating node (True) or boundary node (False).

        Args:  
            id: str-node id.

            floating_node: bool-floating node (True) or not (False).
        """
        self.df = editSBML._setFloatingBoundaryNode(self.df, id, floating_node)
        return self.df

    def setNodePosition(self, id, position):
        """
        Set the node position.

        Args:  
            id: id-node id.

            position: list-1*2 matrix-leftup corner of the rectangle [position_x, position_y].
        """
        self.df = editSBML._setNodePosition(self.df, id, position)
        return self.df

    def setNodeSize(self, id, size):
        """
        Set the node size.

        Args:  
            id: str-node id.

            size: list-1*2 matrix-size of the rectangle [width, height].
        """
        self.df = editSBML._setNodeSize(self.df, id, size)
        return self.df

    def setNodeShapeIdx(self, id, shape_idx):
        """
        Set the node shape index.

        Args:  
            id: str-node id.

            shape_idx: int-1:rectangle, 2:circle, 3:hexagon, 4:line, 5:triangle.
        """
        self.df = editSBML._setNodeShapeIdx(self.df, id, shape_idx)
        return self.df

    def setNodeTextPosition(self, id, txt_position):
        """
        Set the node text position.

        Args:  
            id: str-node id.

            txt_position: list-1*2 matrix-leftup corner of the rectangle [position_x, position_y].
        """
        self.df = editSBML._setNodeTextPosition(self.df, id, txt_position)
        return self.df
    
    def setNodeTextSize(self, id, txt_size):
        """
        Set the node text size.

        Args:  
            id: str-node id.

            txt_size: list-1*2 matrix-size of the rectangle [width, height].
        """
        self.df = editSBML._setNodeTextSize(self.df, id, txt_size)
        return self.df
 
    def setNodeFillColor(self, id, fill_color, opacity = 1.):
        """
        Set the node fill color.

        Args:  
            id: str-node id.

            fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).
        """
        self.df = editSBML._setNodeFillColor(self.df, id, fill_color, opacity)
        return self.df

    def setNodeBorderColor(self, id, border_color, opacity = 1.):
        """
        Set the node border color.

        Args:  
            id: str-node id.

            border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).
        """
        self.df = editSBML._setNodeBorderColor(self.df, id, border_color, opacity)
        return self.df

    def setNodeBorderWidth(self, id, border_width):
        """
        Set the node border width.

        Args:  
            id: str-node id.

            border_width: float-node border line width.
        """
        self.df = editSBML._setNodeBorderWidth(self.df, id, border_width)
        return self.df

    def setNodeTextFontColor(self, id, txt_font_color, opacity = 1.):
        """
        Set the node text font color.

        Args:  
            id: str-node id.

            txt_font_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).
        """
        self.df = editSBML._setNodeTextFontColor(self.df, id, txt_font_color, opacity)
        return self.df

    def setNodeTextLineWidth(self, id, txt_line_width):
        """
        Set the node text line width.

        Args:  
            id: id-node id.

            txt_line_width: float-node text line width.
        """
        self.df = editSBML._setNodeTextLineWidth(self.df, id, txt_line_width)
        return self.df

    def setReactionFillColor(self, id, fill_color, opacity = 1.):
        """
        Set the reaction fill color.

        Args:  
            id: str-reaction id.

            fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).
        """
        self.df = editSBML._setReactionFillColor(self.df, id, fill_color, opacity)
        return self.df

    def setReactionLineThickness(self, id, line_thickness):
        """
        Set the reaction line thickness.

        Args:  
            id: str-reaction id.

            line_thickness: float-reaction border line width.
        """
        self.df = editSBML._setReactionLineThickness(self.df, id, line_thickness)
        return self.df

    def setBezierReactionType(self, id, bezier):
        """
        Set the reaction line thickness.

        Args:  
            id: str-reaction id.

            bezier: bool-bezier reaction (True) or not (False)
        """
        self.df = editSBML._setBezierReactionType(self.df, id, bezier)
        return self.df

    def export(self):
        """
        Write to an SBML string. 

        Returns:
            SBMLStr_layout_render: str-the string of the output sbml file. 
        
        """
        sbml = exportSBML._DFToSBML(self.df)
        return sbml

# if __name__ == '__main__':
#     DIR = os.path.dirname(os.path.abspath(__file__))
#     TEST_FOLDER = os.path.join(DIR, "test_sbml_files")

#     #filename = "test.xml" 
#     filename = "no_rxn.xml"
#     #filename = "test_4.xml"
#     #filename = "feedback.xml"
#     #filename = "LinearChain.xml"
#     #filename = "test_comp.xml"
#     #filename = "test_no_comp.xml"
#     #filename = "test_modifier.xml"

#     f = open(os.path.join(TEST_FOLDER, filename), 'r')
#     sbmlStr = f.read()
#     f.close()

#     df = load(sbmlStr)

#     # print(df.getCompartmentPosition("_compartment_default_"))
#     # print(df.getCompartmentSize("_compartment_default_"))
#     # print(df.getCompartmentFillColor("_compartment_default_"))
#     # print(df.getCompartmentBorderColor("_compartment_default_"))
#     # print(df.getCompartmentBorderWidth("_compartment_default_"))

#     # print(df.isFloatingNode("x_1"))
#     # print(df.getNodePosition("x_1"))
#     # print(df.getNodeSize("x_1"))
#     # print(df.getNodeShape("x_1"))
#     # print(df.getNodeTextPosition("x_1"))
#     # print(df.getNodeTextSize("x_1"))
#     # print(df.getNodeFillColor("x_1"))
#     # print(df.getNodeBorderColor("x_1"))
#     # print(df.getNodeBorderWidth("x_1"))
#     # print(df.getNodeTextFontColor("x_1"))
#     # print(df.getNodeTextLineWidth("x_1"))

#     # print(df.getReactionFillColor("r_0"))
#     # print(df.getReactionLineThickness("r_0"))
#     # print(df.isBezierReactionType("r_0"))

#     # df.setCompartmentPosition('_compartment_default_', [0,0])
#     # df.setCompartmentSize('_compartment_default_', [1000, 1000])
#     # df.setCompartmentFillColor('_compartment_default_', [255, 255, 255])
#     # df.setCompartmentBorderColor('_compartment_default_', [255, 255, 255])
#     # df.setCompartmentBorderWidth('_compartment_default_', 2.)

#     # df.setFloatingBoundaryNode("x_1", True)
#     # df.setNodePosition("x_1", [413.0, 216.0])
#     # df.setNodeSize("x_1", [50.0, 30.0])
#     # df.setNodeShapeIdx("x_1", 1)
#     # df.setNodeTextPosition("x_1", [413., 216.])
#     # df.setNodeTextSize("x_1", [50, 31])
#     # df.setNodeFillColor("x_1", [255, 204, 153], opacity = 0.)
#     # df.setNodeBorderColor("x_1", [255, 108, 9])
#     # df.setNodeBorderWidth("x_1", 2.)
#     # df.setNodeTextFontColor("x_1", [0, 0, 0])
#     # df.setNodeTextLineWidth("x_1", 1.)

#     # df.setReactionFillColor("r_0", [91, 176, 253])
#     # df.setReactionLineThickness("r_0", 3.)
#     # df.setBezierReactionType("r_0", True)


#     sbmlStr_layout_render = df.export()

#     f = open("output.xml", "w")
#     f.write(sbmlStr_layout_render)
#     f.close()



