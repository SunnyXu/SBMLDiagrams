# -*- coding: utf-8 -*-
# This script was written by Jin Xu and available on Github
# https://github.com/SunnyXu/SBMLDiagrams

"""
Created on Mon Aug 23 13:25:34 2021
@author: Jin Xu
"""

import os, sys
import simplesbml
import libsbml
import math
import random as _random
import pandas as pd
from SBMLDiagrams import exportSBML
from SBMLDiagrams import editSBML
from SBMLDiagrams import visualizeSBML
from SBMLDiagrams import styleSBML
from SBMLDiagrams import point
import simplesbml
import networkx as nx
from collections import defaultdict
import json

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
TXTCONTENT = 'txt_content'
TXTPOSITION = 'txt_position'
TXTSIZE = 'txt_size'
TXTFONTCOLOR = 'txt_font_color'
TXTLINEWIDTH = 'txt_line_width'
TXTFONTSIZE = 'txt_font_size'
SHAPENAME = 'shape_name'
SHAPETYPE = 'shape_type'
SHAPEINFO = 'shape_info'
SOURCES = 'sources'
TARGETS = 'targets'
RATELAW = 'rate_law'
MODIFIERS = 'modifiers'
LINETHICKNESS = 'line_thickness'
CENTERPOS = 'center_pos'
HANDLES = 'handles'
BEZIER = 'bezier'
ARROWHEADSIZE = 'arrow_head_size'
RXNDASH = "rxn_dash"
RXNREV = "rxn_reversible"
COLUMN_NAME_df_CompartmentData = [NETIDX, IDX, ID,\
    POSITION, SIZE, FILLCOLOR, BORDERCOLOR, BORDERWIDTH]
COLUMN_NAME_df_NodeData = [NETIDX, COMPIDX, IDX, ORIGINALIDX, ID, FLOATINGNODE,\
    CONCENTRATION, POSITION, SIZE, SHAPEIDX, TXTPOSITION, TXTSIZE, \
    FILLCOLOR, BORDERCOLOR, BORDERWIDTH, TXTFONTCOLOR, TXTLINEWIDTH, TXTFONTSIZE, 
    SHAPENAME, SHAPETYPE, SHAPEINFO]
COLUMN_NAME_df_ReactionData = [NETIDX, IDX, ID, SOURCES, TARGETS, RATELAW, MODIFIERS, \
    FILLCOLOR, LINETHICKNESS, CENTERPOS, HANDLES, BEZIER, ARROWHEADSIZE, RXNDASH, RXNREV]
COLUMN_NAME_df_TextData = [TXTCONTENT, TXTPOSITION, TXTSIZE, 
    TXTFONTCOLOR, TXTLINEWIDTH, TXTFONTSIZE]
COLUMN_NAME_df_ShapeData = [SHAPENAME, POSITION, SIZE, FILLCOLOR, BORDERCOLOR, BORDERWIDTH, 
                        SHAPETYPE, SHAPEINFO]
# #This is not supported by SBML
# COLUMN_NAME_df_text = [TXTCONTENT, TXTPOSITION, TXTFONTCOLOR, TXTLINEWIDTH, TXTFONTSIZE]

# DIR = os.path.dirname(os.path.abspath(__file__))
# color_xls = pd.ExcelFile(os.path.join(DIR, 'colors.xlsx'))
# df_color = pd.read_excel(color_xls, sheet_name = 'colors')
color_data = {"decimal_rgb": ['[240,248,255]', '[250,235,215]', '[0,255,255]', '[127,255,212]', '[240,255,255]', '[245,245,220]', '[255,228,196]', '[0,0,0]', '[255,235,205]', '[0,0,255]', '[138,43,226]', '[165,42,42]', '[222,184,135]', '[95,158,160]', '[127,255,0]', '[210,105,30]', '[255,127,80]', '[100,149,237]', '[255,248,220]', '[220,20,60]', '[0,255,255]', '[0,0,139]', '[0,139,139]', '[184,134,11]', '[169,169,169]', '[0,100,0]', '[189,183,107]', '[139,0,139]', '[85,107,47]', '[255,140,0]', '[153,50,204]', '[139,0,0]', '[233,150,122]', '[143,188,143]', '[72,61,139]', '[47,79,79]', '[0,206,209]', '[148,0,211]', '[255,20,147]', '[0,191,255]', '[105,105,105]', '[30,144,255]', '[178,34,34]', '[255,250,240]', '[34,139,34]', '[255,0,255]', '[220,220,220]', '[248,248,255]', '[255,215,0]', '[218,165,32]', '[128,128,128]', '[0,128,0]', '[173,255,47]', '[240,255,240]', '[255,105,180]', '[205,92,92]', '[75,0,130]', '[255,255,240]', '[240,230,140]', '[230,230,250]', '[255,240,245]', '[124,252,0]', '[255,250,205]', '[173,216,230]', '[240,128,128]', '[224,255,255]', '[250,250,210]', '[144,238,144]', '[211,211,211]', '[255,182,193]', '[255,160,122]', '[32,178,170]', '[135,206,250]', '[119,136,153]', '[176,196,222]', '[255,255,224]', '[0,255,0]', '[50,205,50]', '[250,240,230]', '[255,0,255]', '[128,0,0]', '[102,205,170]', '[0,0,205]', '[186,85,211]', '[147,112,219]', '[60,179,113]', '[123,104,238]', '[0,250,154]', '[72,209,204]', '[199,21,133]', '[25,25,112]', '[245,255,250]', '[255,228,225]', '[255,228,181]', '[255,222,173]', '[0,0,128]', '[253,245,230]', '[128,128,0]', '[107,142,35]', '[255,165,0]', '[255,69,0]', '[218,112,214]', '[238,232,170]', '[152,251,152]', '[175,238,238]', '[219,112,147]', '[255,239,213]', '[255,218,185]', '[205,133,63]', '[255,192,203]', '[221,160,221]', '[176,224,230]', '[128,0,128]', '[255,0,0]', '[188,143,143]', '[65,105,225]', '[139,69,19]', '[250,128,114]', '[244,164,96]', '[46,139,87]', '[255,245,238]', '[160,82,45]', '[192,192,192]', '[135,206,235]', '[106,90,205]', '[112,128,144]', '[255,250,250]', '[0,255,127]', '[70,130,180]', '[210,180,140]', '[0,128,128]', '[216,191,216]', '[255,99,71]', '[64,224,208]', '[238,130,238]', '[245,222,179]', '[255,255,255]', '[245,245,245]', '[255,255,0]', '[154,205,50]'],\
    "html_name":['AliceBlue', 'AntiqueWhite', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque', 'Black', 'BlanchedAlmond', 'Blue', 'BlueViolet', 'Brown', 'BurlyWood', 'CadetBlue', 'Chartreuse', 'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan', 'DarkBlue', 'DarkCyan', 'DarkGoldenrod', 'DarkGray', 'DarkGreen', 'DarkKhaki', 'DarkMagenta', 'DarkOliveGreen', 'DarkOrange', 'DarkOrchid', 'DarkRed', 'DarkSalmon', 'DarkSeaGreen', 'DarkSlateBlue', 'DarkSlateGray', 'DarkTurquoise', 'DarkViolet', 'DeepPink', 'DeepSkyBlue', 'DimGray', 'DodgerBlue', 'FireBrick', 'FloralWhite', 'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'Goldenrod', 'Gray', 'Green', 'GreenYellow', 'Honeydew', 'HotPink', 'IndianRed', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue', 'LightCoral', 'LightCyan', 'LightGoldenrodYellow', 'LightGreen', 'LightGrey', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue', 'LightSlateGray', 'LightSteelBlue', 'LightYellow', 'Lime', 'LimeGreen', 'Linen', 'Magenta', 'Maroon', 'MediumAquamarine', 'MediumBlue', 'MediumOrchid', 'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen', 'MediumTurquoise', 'MediumVioletRed', 'MidnightBlue', 'MintCream', 'MistyRose', 'Moccasin', 'NavajoWhite', 'Navy', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed', 'Orchid', 'PaleGoldenrod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed', 'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple', 'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Salmon', 'SandyBrown', 'SeaGreen', 'Seashell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue', 'SlateGray', 'Snow', 'SpringGreen', 'SteelBlue', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White', 'WhiteSmoke', 'Yellow', 'YellowGreen'],\
    "hex_string":['#F0F8FF', '#FAEBD7', '#00FFFF', '#7FFFD4', '#F0FFFF', '#F5F5DC', '#FFE4C4', '#000000', '#FFEBCD', '#0000FF', '#8A2BE2', '#A52A2A', '#DEB887', '#5F9EA0', '#7FFF00', '#D2691E', '#FF7F50', '#6495ED', '#FFF8DC', '#DC143C', '#00FFFF', '#00008B', '#008B8B', '#B8860B', '#A9A9A9', '#006400', '#BDB76B', '#8B008B', '#556B2F', '#FF8C00', '#9932CC', '#8B0000', '#E9967A', '#8FBC8F', '#483D8B', '#2F4F4F', '#00CED1', '#9400D3', '#FF1493', '#00BFFF', '#696969', '#1E90FF', '#B22222', '#FFFAF0', '#228B22', '#FF00FF', '#DCDCDC', '#F8F8FF', '#FFD700', '#DAA520', '#808080', '#008000', '#ADFF2F', '#F0FFF0', '#FF69B4', '#CD5C5C', '#4B0082', '#FFFFF0', '#F0E68C', '#E6E6FA', '#FFF0F5', '#7CFC00', '#FFFACD', '#ADD8E6', '#F08080', '#E0FFFF', '#FAFAD2', '#90EE90', '#D3D3D3', '#FFB6C1', '#FFA07A', '#20B2AA', '#87CEFA', '#778899', '#B0C4DE', '#FFFFE0', '#00FF00', '#32CD32', '#FAF0E6', '#FF00FF', '#800000', '#66CDAA', '#0000CD', '#BA55D3', '#9370DB', '#3CB371', '#7B68EE', '#00FA9A', '#48D1CC', '#C71585', '#191970', '#F5FFFA', '#FFE4E1', '#FFE4B5', '#FFDEAD', '#000080', '#FDF5E6', '#808000', '#6B8E23', '#FFA500', '#FF4500', '#DA70D6', '#EEE8AA', '#98FB98', '#AFEEEE', '#DB7093', '#FFEFD5', '#FFDAB9', '#CD853F', '#FFC0CB', '#DDA0DD', '#B0E0E6', '#800080', '#FF0000', '#BC8F8F', '#4169E1', '#8B4513', '#FA8072', '#F4A460', '#2E8B57', '#FFF5EE', '#A0522D', '#C0C0C0', '#87CEEB', '#6A5ACD', '#708090', '#FFFAFA', '#00FF7F', '#4682B4', '#D2B48C', '#008080', '#D8BFD8', '#FF6347', '#40E0D0', '#EE82EE', '#F5DEB3', '#FFFFFF', '#F5F5F5', '#FFFF00', '#9ACD32']}
df_color = pd.DataFrame(color_data)

def _rgb_to_color(rgb):
    """
    transfer a list of rgb to a color list with decimal_rgba, html_name and hex_string.

    Args:  
        rgb: list-1*3 or 1*4 matrix for a decimal rgb or rgba.

    Returns:
        color: list-[decimal_rgb, html_name, hex_string].
    
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

def _SBMLToDF(sbmlStr, reactionLineType = 'bezier', compartmentDefaultSize = [1000, 1000]): 
    """
    Save the information of an SBML file to a set of dataframe.

    Args:  
        sbmlStr: str-the string of the input sbml file.

        reactionLineType: str-type of the reaction line: 'straight' or 'bezier' (default).

    Returns:
        (df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData): tuple.

        df_CompartmentData: DataFrame-Compartment information.

        df_NodeData: DataFrame-Node information.

        df_ReactionData: DataFrame-Reaction information.

        df_ArbitraryTextData: DataFrame-Arbitrary text information.

        df_ArbitrartyShapeData: DataFrame-Arbitrary shape information.
    
    """

    def hex_to_rgb(value):
        value = value.lstrip('#')
        if len(value) == 6:
            value = value + 'ff'
        return [int(value[i:i+2], 16) for i in (0, 2, 4, 6)]

    df_CompartmentData = pd.DataFrame(columns = COLUMN_NAME_df_CompartmentData)
    df_NodeData = pd.DataFrame(columns = COLUMN_NAME_df_NodeData)
    df_ReactionData = pd.DataFrame(columns = COLUMN_NAME_df_ReactionData)
    df_TextData = pd.DataFrame(columns = COLUMN_NAME_df_TextData)
    df_ShapeData = pd.DataFrame(columns = COLUMN_NAME_df_ShapeData)

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
    spec_concentration_list = []
    textGlyph_id_list = []
    text_content_list = []
    text_position_list = []
    text_dimension_list = []
    gen_id_list = []
    gen_position_list = []
    gen_dimension_list = []

    
    #set the default values without render info:
    #comp_fill_color = [158, 169, 255, 200]
    #comp_border_color = [0, 29, 255, 255]
    comp_fill_color = [255, 255, 255, 255]
    comp_border_color = [255, 255, 255, 255]
    comp_border_width = 2.0
    spec_fill_color = [255, 204, 153, 200]
    spec_border_color = [255, 108, 9, 255]
    spec_border_width = 2.0
    shapeIdx = 1
    shape_name = ''
    shape_type = ''
    shape_info = []
    reaction_line_color = [91, 176, 253, 255]
    reaction_line_width = 3.0
    reaction_arrow_head_size = [reaction_line_width*4, reaction_line_width*5]
    reaction_dash = [] 
    text_content = ''
    text_line_color = [0, 0, 0, 255]
    text_line_width = 1.
    text_font_size = 12.
    gen_fill_color = [255, 255, 255, 255]
    gen_border_color = [0, 0, 0, 255]
    gen_border_width = 2.
    gen_shape_type = ''
    gen_shape_info = []
    
    mplugin = None
    try: #invalid sbml
        ### from here for layout ###
        document = libsbml.readSBMLFromString(sbmlStr)
        # if document.getNumErrors() != 0:
        #     raise Exception("There are errors in the sbml file.")
        if document.getNumErrors() != 0:
            errMsgRead = document.getErrorLog().toString()
            raise Exception("Errors in SBML Model: ", errMsgRead)
        model_layout = document.getModel()
        try:
            mplugin = model_layout.getPlugin("layout")
        except:
            raise Exception("There is no layout.")
        if mplugin is not None:
            layout = mplugin.getLayout(0)    
            if layout is not None:
                numCompGlyphs = layout.getNumCompartmentGlyphs()
                numSpecGlyphs = layout.getNumSpeciesGlyphs()
                numReactionGlyphs = layout.getNumReactionGlyphs()
                numTextGlyphs = layout.getNumTextGlyphs()
                numGenGlyphs = layout.getNumGeneralGlyphs()
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
                reaction_rev_list = []
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
                        center_pt = [center_x, center_y]
                        reaction_center_list.append(center_pt)
                    reaction_id = reactionGlyph.getReactionId()
                    reaction_id_list.append(reaction_id)
                    reaction = model_layout.getReaction(reaction_id)
                    rev = reaction.getReversible()
                    reaction_rev_list.append(rev)
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
                    
                    center_handle = []
                    for j in range(numSpecRefGlyphs):
                        specRefGlyph = reactionGlyph.getSpeciesReferenceGlyph(j)
                        #specRefGlyph_id = specRefGlyph.getSpeciesReferenceGlyphId()                   
                        curve = specRefGlyph.getCurve()
                        spec_handle = []                             
                        for segment in curve.getListOfCurveSegments():
                            line_start_x = segment.getStart().getXOffset()
                            line_start_y = segment.getStart().getYOffset()
                            line_end_x = segment.getEnd().getXOffset()
                            line_end_y = segment.getEnd().getYOffset()
                            line_start_pt =  [line_start_x, line_start_y]
                            line_end_pt = [line_end_x, line_end_y]
                            try:
                                if math.dist(line_start_pt, center_pt) <= math.dist(line_end_pt, center_pt):
                                    #line starts from center
                                    center_handle_candidate = [segment.getBasePoint1().getXOffset(), 
                                                segment.getBasePoint1().getYOffset()]                                
                                    spec_handle = [segment.getBasePoint2().getXOffset(),
                                            segment.getBasePoint2().getYOffset()]
                                else:
                                    #line does not start from center
                                    spec_handle = [segment.getBasePoint1().getXOffset(), 
                                                segment.getBasePoint1().getYOffset()]                                
                                    center_handle_candidate = [segment.getBasePoint2().getXOffset(),
                                            segment.getBasePoint2().getYOffset()]
                            except:
                                center_handle_candidate = []
                                spec_handle = []

                        role = specRefGlyph.getRoleString()
                        specGlyph_id = specRefGlyph.getSpeciesGlyphId()
                        specGlyph = layout.getSpeciesGlyph(specGlyph_id)
                        
                        for k in range(numSpecGlyphs):
                            textGlyph_temp = layout.getTextGlyph(k)
                            if textGlyph_temp.isSetOriginOfTextId():
                                temp_specGlyph_id = textGlyph_temp.getOriginOfTextId()
                            elif textGlyph_temp.isSetGraphicalObjectId():
                                temp_specGlyph_id = textGlyph_temp.getGraphicalObjectId()
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
                            if center_handle == []:
                                center_handle.append(center_handle_candidate)
                        elif role == "product": #it is a prd
                            #prd_specGlyph_temp_list.append(specGlyph_id)
                            prd_specGlyph_handles_temp_list.append([specGlyph_id,spec_handle])
                        elif role == "modifier": #it is a modifier
                            mod_specGlyph_temp_list.append(specGlyph_id)
                        
                    #rct_specGlyph_list.append(rct_specGlyph_temp_list)
                    #prd_specGlyph_list.append(prd_specGlyph_temp_list)
                    #

                    try:
                        reaction_center_handle_list.append(center_handle[0])
                    except:
                        #raise Exception("Can not find center handle information to process.")
                        reaction_center_handle_list.append([])

                    rct_specGlyph_handle_list.append(rct_specGlyph_handles_temp_list)
                    prd_specGlyph_handle_list.append(prd_specGlyph_handles_temp_list) 
                    mod_specGlyph_list.append(mod_specGlyph_temp_list)

                # print(reaction_center_handle_list)
                # print(rct_specGlyph_handle_list)
                # print(prd_specGlyph_handle_list)
                # print(mod_specGlyph_list)

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
                            if textGlyph_temp != None:
                                if textGlyph_temp.isSetOriginOfTextId():
                                    temp_specGlyph_id = textGlyph_temp.getOriginOfTextId()
                                elif textGlyph_temp.isSetGraphicalObjectId():
                                    temp_specGlyph_id = textGlyph_temp.getGraphicalObjectId()
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

                #arbitrary text
                for i in range(numTextGlyphs):
                    textGlyph = layout.getTextGlyph(i)
                    if not textGlyph.isSetOriginOfTextId() and not textGlyph.isSetGraphicalObjectId():
                        #if there is no original text id set
                        temp_id = textGlyph.getId()
                        text_content = textGlyph.getText()
                        textGlyph_id_list.append(temp_id)
                        text_content_list.append(text_content)
                        try:
                            text_boundingbox = textGlyph.getBoundingBox()
                            text_pos_x = text_boundingbox.getX()
                            text_pos_y = text_boundingbox.getY()   
                            text_dim_w = text_boundingbox.getWidth()
                            text_dim_h = text_boundingbox.getHeight()
                            text_position_list.append([text_pos_x,text_pos_y])
                            text_dimension_list.append([text_dim_w,text_dim_h])
                        except:
                            text_position_list.append([])
                            text_dimension_list.append([])
                    
                #arbitrary shape
                for i in range(numGenGlyphs):
                    genGlyph = layout.getGeneralGlyph(i)
                    temp_id = genGlyph.getId()
                    gen_id_list.append(temp_id)
                    try:
                        shape_boundingbox = genGlyph.getBoundingBox()
                        shape_pos_x = shape_boundingbox.getX()
                        shape_pos_y = shape_boundingbox.getY()   
                        shape_dim_w = shape_boundingbox.getWidth()
                        shape_dim_h = shape_boundingbox.getHeight()
                        gen_position_list.append([shape_pos_x,shape_pos_y])
                        gen_dimension_list.append([shape_dim_w,shape_dim_h])
                    except:
                        gen_position_list.append([])
                        gen_dimension_list.append([])

                rPlugin = layout.getPlugin("render")
                if (rPlugin != None and rPlugin.getNumLocalRenderInformationObjects() > 0):
                    info = rPlugin.getRenderInformation(0)
                    color_list = []
                    gradient_list = []
                    comp_render = []
                    spec_render = []
                    rxn_render = []
                    text_render = []
                    gen_render = []
                    arrowHeadSize = reaction_arrow_head_size #default if there is no lineEnding
                    id_arrowHeadSize = []
                    
                    for j in range(0, info.getNumLineEndings()):
                        lineEnding = info.getLineEnding(j)
                        temp_id = lineEnding.getId()
                        boundingbox = lineEnding.getBoundingBox()
                        width = boundingbox.getWidth()
                        height= boundingbox.getHeight()
                        pos_x = boundingbox.getX()
                        pos_y = boundingbox.getY()
                        temp_arrowHeadSize = [width, height]
                        id_arrowHeadSize.append([temp_id,temp_arrowHeadSize])
                        # group = lineEnding.getGroup()
                        # for element in group.getListOfElements():
                        #     NumRenderPoints = element.getListOfElements().getNumRenderPoints()
                        #     for k in range(NumRenderPoints):
                        #         x = element.getListOfElements().get(k).getX().getCoordinate()
                        #         y = element.getListOfElements().get(k).getY().getCoordinate()

                    for  j in range(0, info.getNumColorDefinitions()):
                        color = info.getColorDefinition(j)
                        color_list.append([color.getId(),color.createValueString()])

                    for j in range(0, info.getNumGradientDefinitions()):
                        gradient = info.getGradientDefinition(j)
                        grad_type = gradient.getElementName()
                        if grad_type == "linearGradient":
                            id = gradient.getId()
                            grad_start = [gradient.getXPoint1().getRelativeValue(),gradient.getYPoint1().getRelativeValue()]
                            grad_end = [gradient.getXPoint2().getRelativeValue(),gradient.getYPoint2().getRelativeValue()]
                            grad_info = [grad_start,grad_end]
                        elif grad_type == "radialGradient":
                            id = gradient.getId()
                            grad_center = [gradient.getCenterX().getRelativeValue(),gradient.getCenterY().getRelativeValue()]
                            grad_radius = [gradient.getRadius().getRelativeValue()]
                            grad_info = [grad_center,grad_radius]
                        stop_info = []
                        for k in range(0,gradient.getNumGradientStops()):
                            stop = gradient.getGradientStop(k)
                            offset = stop.getOffset().getRelativeValue()
                            stop_color_name = stop.getStopColor()
                            stop_color = spec_fill_color
                            for kk in range(len(color_list)):
                                if color_list[kk][0] == stop_color_name:
                                    stop_color = hex_to_rgb(color_list[kk][1])
                            stop_info.append([offset,stop_color])
                        gradient_list.append([id,grad_type, grad_info,stop_info])

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
                            
                            for k in range(len(gradient_list)):
                                if gradient_list[k][0] == group.getFill():
                                    spec_fill_color = gradient_list[k][1:]
                            spec_border_width = group.getStrokeWidth()
                            #name_list = []
                            shape_type = ''
                            #print(group.getNumElements())# There is only one element
                            #for element in group.getListOfElements():
                            element = group.getElement(0)
                            shapeIdx = 0
                            shape_name = "text_only"
                            shapeInfo = []
                            if element != None:
                                shape_type = element.getElementName()
                                if shape_type == "rectangle":
                                    shapeIdx = 1
                                    shape_name = "rectangle"
                                elif shape_type == "ellipse": #ellipse
                                    shapeIdx = 2
                                    shape_name = "ellipse"
                                    # center_x = element.getCX().getRelativeValue()
                                    # center_y = element.getCY().getRelativeValue()
                                    # radius_x = element.getRX().getRelativeValue()
                                    # radius_y = element.getRY().getRelativeValue()
                                    # shapeInfo.append([[center_x,center_y],[radius_x,radius_y]])
                                elif shape_type == "polygon":
                                    NumRenderpoints = element.getListOfElements().getNumRenderPoints()
                                    for num in range(NumRenderpoints):
                                        point_x = element.getListOfElements().get(num).getX().getRelativeValue()
                                        point_y = element.getListOfElements().get(num).getY().getRelativeValue()
                                        shapeInfo.append([point_x,point_y]) 
                                    if NumRenderpoints == 6: #hexagon:
                                        shapeIdx = 3
                                        shape_name = "hexagon"
                                    elif NumRenderpoints == 2: #line
                                        shapeIdx = 4
                                        shape_name = "line"
                                    elif NumRenderpoints == 3: #triangle
                                        shapeIdx = 5
                                        shape_name = "triangle"
                                        #triangle_vertex = [[25.0, 7.0],[100.0, 50.0],[25.0, 86.0]]
                                        upTriangle_vertex = [[50,0],[100,80.6],[0,80.6]]
                                        downTriangle_vertex = [[0,19.4],[100,19.5],[50.,100.]]
                                        leftTriangle_vertex = [[80.6,0],[80.6,100],[0,50]]
                                        rightTriangle_vertex = [[19.4,0],[100.,50],[19.4,100]]
                                        if all(item in shapeInfo for item in upTriangle_vertex):
                                            shapeIdx = 6
                                            shape_name = "upTriangle"
                                        if all(item in shapeInfo for item in downTriangle_vertex):
                                            shapeIdx = 7
                                            shape_name = "downTriangle"
                                        if all(item in shapeInfo for item in leftTriangle_vertex):
                                            shapeIdx = 8
                                            shape_name = "leftTriangle"
                                        if all(item in shapeInfo for item in rightTriangle_vertex):
                                            shapeIdx = 9
                                            shape_name = "rightTriangle"

                            spec_render.append([idList,spec_fill_color,spec_border_color,spec_border_width,
                            shapeIdx, shape_name, shape_type, shapeInfo])

                        elif 'REACTIONGLYPH' in typeList:
                            if group.isSetEndHead():
                                temp_id = group.getEndHead() 
                            reaction_dash = []
                            if group.isSetDashArray():
                                reaction_num_dash = group.getNumDashes()
                                for num in range(reaction_num_dash):
                                    reaction_dash.append(group.getDashByIndex(num))
                            for k in range(len(id_arrowHeadSize)):
                                if temp_id == id_arrowHeadSize[k][0]:
                                    arrowHeadSize = id_arrowHeadSize[k][1]
                            for k in range(len(color_list)):
                                if color_list[k][0] == group.getStroke():
                                    reaction_line_color = hex_to_rgb(color_list[k][1])
                            reaction_line_width = group.getStrokeWidth()
                            rxn_render.append([idList, reaction_line_color, reaction_line_width, 
                            arrowHeadSize, reaction_dash])
                        elif 'TEXTGLYPH' in typeList:
                            for k in range(len(color_list)):
                                if color_list[k][0] == group.getStroke():
                                    text_line_color = hex_to_rgb(color_list[k][1])
                            text_line_width = group.getStrokeWidth()
                            if math.isnan(text_line_width):
                                text_line_width = 1.
                            text_font_size = float(group.getFontSize().getCoordinate())
                            text_render.append([idList,text_line_color,text_line_width,
							text_font_size])
                        elif 'GENERALGLYPH' in typeList:
                            for k in range(len(color_list)):
                                if color_list[k][0] == group.getFill():
                                    gen_fill_color = hex_to_rgb(color_list[k][1])
                                if color_list[k][0] == group.getStroke():
                                    gen_border_color = hex_to_rgb(color_list[k][1])
                            gen_border_width = group.getStrokeWidth()
                            gen_shape_type = ''
                            gen_shape_info = []
                            element = group.getElement(0)
                            if element != None:
                                gen_shape_type = element.getElementName()
                                if gen_shape_type == "polygon":
                                    NumRenderpoints = element.getListOfElements().getNumRenderPoints()
                                    for num in range(NumRenderpoints):
                                        point_x = element.getListOfElements().get(num).getX().getRelativeValue()
                                        point_y = element.getListOfElements().get(num).getY().getRelativeValue()
                                        gen_shape_info.append([point_x,point_y]) 

                            gen_render.append([idList, gen_fill_color, gen_border_color,
                            gen_border_width, gen_shape_type, gen_shape_info])

        #print(gen_render)
        #print(gradient_list)

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
        if len(spec_id_list) != 0 or len(textGlyph_id_list) != 0 or len(gen_id_list) != 0:
            for i in range(numComps):
                temp_id = Comps_ids[i]
                comp_idx_id_list.append([i,temp_id])
                vol= model.getCompartmentVolume(i)
                if len(comp_id_list) != 0:
                #if mplugin is not None:
                    if temp_id == "_compartment_default_":
                        dimension = compartmentDefaultSize
                        position = [0, 0]
                        #comp_border_color = [255, 255, 255, 255]
                        #comp_fill_color = [255, 255, 255, 255]
                    
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
                        dimension = compartmentDefaultSize
                        position = [0,0]
                        #If there is no render info about the compartments given from sbml,
                        #they will be set as white. 
                        #comp_fill_color = [255, 255, 255, 255]
                        #comp_border_color = [255, 255, 255, 255]

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
                # for j in range(len(COLUMN_NAME_df_CompartmentData)):
                #     try: 
                #         CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]] = CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]][0]
                #     except:
                #         CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]] = ''
                # df_CompartmentData = df_CompartmentData.append(CompartmentData_row_dct, ignore_index=True)
                if len(df_CompartmentData) == 0:
                    df_CompartmentData = pd.DataFrame(CompartmentData_row_dct)
                else:
                    df_CompartmentData = pd.concat([df_CompartmentData,\
                        pd.DataFrame(CompartmentData_row_dct)], ignore_index=True)

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
                                    shape_name = spec_render[k][5]
                                    shape_type = spec_render[k][6]
                                    shape_info = spec_render[k][7]
                            for k in range(len(text_render)):
                                if temp_id == text_render[k][0]:
                                    text_line_color = text_render[k][1]
                                    text_line_width = text_render[k][2]
                                    text_font_size = text_render[k][3]
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
                            NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                            NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                            NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                            NodeData_row_dct[SHAPENAME].append(shape_name)
                            NodeData_row_dct[SHAPETYPE].append(shape_type)
                            NodeData_row_dct[SHAPEINFO].append(shape_info)
                            # for j in range(len(COLUMN_NAME_df_NodeData)):
                            #     try: 
                            #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                            #     except:
                            #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                            # df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
                            if len(df_NodeData) == 0:
                                df_NodeData = pd.DataFrame(NodeData_row_dct)
                            else:
                                df_NodeData = pd.concat([df_NodeData,\
                                    pd.DataFrame(NodeData_row_dct)], ignore_index=True)
                    
                        else:
                            original_idx = id_list.index(temp_id)
                            for k in range(len(spec_render)):
                                if temp_id == spec_render[k][0]:
                                    spec_fill_color = spec_render[k][1]
                                    spec_border_color = spec_render[k][2]
                                    spec_border_width = spec_render[k][3]
                                    shapeIdx = spec_render[k][4]
                                    shape_name = spec_render[k][5]
                                    shape_type = spec_render[k][6]
                                    shape_info = spec_render[k][7]
                            for k in range(len(text_render)):
                                if temp_id == text_render[k][0]:
                                    text_line_color = text_render[k][1]
                                    text_line_width = text_render[k][2]
                                    text_font_size = text_render[k][3]
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
                            NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                            NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                            NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                            NodeData_row_dct[SHAPENAME].append(shape_name)
                            NodeData_row_dct[SHAPETYPE].append(shape_type)
                            NodeData_row_dct[SHAPEINFO].append(shape_info)
                            # for j in range(len(COLUMN_NAME_df_NodeData)):
                            #     try: 
                            #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                            #     except:
                            #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                            # df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
                            if len(df_NodeData) == 0:
                                df_NodeData = pd.DataFrame(NodeData_row_dct)
                            else:
                                df_NodeData = pd.concat([df_NodeData,\
                                    pd.DataFrame(NodeData_row_dct)], ignore_index=True)
                for j in range(numBoundaryNodes):
                    if temp_id == BoundaryNodes_ids[j]:
                        if temp_id not in id_list:
                            for k in range(len(spec_render)):
                                if temp_id == spec_render[k][0]:
                                    spec_fill_color = spec_render[k][1]
                                    spec_border_color = spec_render[k][2]
                                    spec_border_width = spec_render[k][3]
                                    shapeIdx = spec_render[k][4]
                                    shape_name = spec_render[k][5]
                                    shape_type = spec_render[k][6]
                                    shape_info = spec_render[k][7]
                            for k in range(len(text_render)):
                                if temp_id == text_render[k][0]:
                                    text_line_color = text_render[k][1]
                                    text_line_width = text_render[k][2]  
                                    text_font_size = text_render[k][3]      
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
                            NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                            NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                            NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                            NodeData_row_dct[SHAPENAME].append(shape_name)
                            NodeData_row_dct[SHAPETYPE].append(shape_type)
                            NodeData_row_dct[SHAPEINFO].append(shape_info)
                            # for j in range(len(COLUMN_NAME_df_NodeData)):
                            #     try: 
                            #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                            #     except:
                            #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                            # df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
                            if len(df_NodeData) == 0:
                                df_NodeData = pd.DataFrame(NodeData_row_dct)
                            else:
                                df_NodeData = pd.concat([df_NodeData,\
                                    pd.DataFrame(NodeData_row_dct)], ignore_index=True)
                        else:
                            for k in range(len(spec_render)):
                                if temp_id == spec_render[k][0]:
                                    spec_fill_color = spec_render[k][1]
                                    spec_border_color = spec_render[k][2]
                                    spec_border_width = spec_render[k][3]
                                    shapeIdx = spec_render[k][4]
                                    shape_name = spec_render[k][5]
                                    shape_type = spec_render[k][6]
                                    shape_info = spec_render[k][7]
                            for k in range(len(text_render)):
                                if temp_id == text_render[k][0]:
                                    text_line_color = text_render[k][1]
                                    text_line_width = text_render[k][2] 
                                    text_font_size = text_render[k][3]

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
                            NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                            NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                            NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                            NodeData_row_dct[SHAPENAME].append(shape_name)
                            NodeData_row_dct[SHAPETYPE].append(shape_type)
                            NodeData_row_dct[SHAPEINFO].append(shape_info)
                            # for j in range(len(COLUMN_NAME_df_NodeData)):
                            #     try: 
                            #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                            #     except:
                            #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                            # df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
                            if len(df_NodeData) == 0:
                                df_NodeData = pd.DataFrame(NodeData_row_dct)
                            else:
                                df_NodeData = pd.concat([df_NodeData,\
                                    pd.DataFrame(NodeData_row_dct)], ignore_index=True)
            
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
                rxn_rev = reaction_rev_list[i]
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
                
                if rct_num != 0 and prd_num != 0:
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

                else:
                    src_idx_list = []
                    dst_idx_list = []
                    mod_idx_list = []
                    rct_num = model.getNumReactants(i)
                    prd_num = model.getNumProducts(i)
                    mod_num = model.getNumModifiers(temp_id)
             
                    for j in range(rct_num):
                        rct_id = model.getReactant(temp_id,j)
                        for k in range(len(spec_specGlyph_id_list)):
                            if spec_specGlyph_id_list[k][0] == rct_id:
                                tempGlyph_id = spec_specGlyph_id_list[k][1]
                        for k in range(len(node_idx_specGlyphid_list)):
                            if node_idx_specGlyphid_list[k][1] == tempGlyph_id:
                                src_idx_list.append(node_idx_specGlyphid_list[k][0])
                    src_idx_list_corr = []
                    [src_idx_list_corr.append(x) for x in src_idx_list if x not in src_idx_list_corr]

                    for j in range(prd_num):
                        prd_id = model.getProduct(temp_id,j)
                        for k in range(len(spec_specGlyph_id_list)):
                            if spec_specGlyph_id_list[k][0] == prd_id:
                                tempGlyph_id = spec_specGlyph_id_list[k][1]
                        for k in range(len(node_idx_specGlyphid_list)):
                            if node_idx_specGlyphid_list[k][1] == tempGlyph_id:
                                dst_idx_list.append(node_idx_specGlyphid_list[k][0]) 
                    dst_idx_list_corr = []
                    [dst_idx_list_corr.append(x) for x in dst_idx_list if x not in dst_idx_list_corr]

                    modifiers = model.getListOfModifiers(temp_id)
                    for j in range(mod_num):
                        mod_id = modifiers[j]
                        for k in range(len(spec_specGlyph_id_list)):
                            if spec_specGlyph_id_list[k][0] == mod_id:
                                tempGlyph_id = spec_specGlyph_id_list[k][1]
                        for k in range(len(node_idx_specGlyphid_list)):
                            if node_idx_specGlyphid_list[k][1] == tempGlyph_id:
                                mod_idx_list.append(node_idx_specGlyphid_list[k][0])

                for j in range(len(rxn_render)):
                    if temp_id == rxn_render[j][0]:
                        reaction_line_color = rxn_render[j][1]
                        reaction_line_width = rxn_render[j][2]
                        reaction_arrow_head_size = rxn_render[j][3]
                        reaction_dash = rxn_render[j][4]
                try: 
                    center_position = reaction_center_list[i]
                    center_handle = reaction_center_handle_list[i]
                    if center_handle != []:
                        handles = [center_handle]
                    else:
                        handles = [center_position]
                    handles.extend(src_handle)
                    handles.extend(dst_handle) 
                    #print("process:", handles) 
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
                    ReactionData_row_dct[ARROWHEADSIZE].append(reaction_arrow_head_size)
                    ReactionData_row_dct[RXNDASH].append(reaction_dash)
                    ReactionData_row_dct[RXNREV].append(rxn_rev)
                    # for j in range(len(COLUMN_NAME_df_ReactionData)):
                    #     try: 
                    #         ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]][0]
                    #     except:
                    #         ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ''
                    # df_ReactionData = df_ReactionData.append(ReactionData_row_dct, ignore_index=True)
                    if len(df_ReactionData) == 0:
                        df_ReactionData = pd.DataFrame(ReactionData_row_dct)
                    else:
                        df_ReactionData = pd.concat([df_ReactionData,\
                            pd.DataFrame(ReactionData_row_dct)], ignore_index=True)
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
                    ReactionData_row_dct[ARROWHEADSIZE].append(reaction_arrow_head_size)
                    ReactionData_row_dct[RXNDASH].append(reaction_dash)
                    ReactionData_row_dct[RXNREV].append(rxn_rev)
                    # for j in range(len(COLUMN_NAME_df_ReactionData)):
                    #     try: 
                    #         ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]][0]
                    #     except:
                    #         ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ''
                    # df_ReactionData = df_ReactionData.append(ReactionData_row_dct, ignore_index=True)
                    if len(df_ReactionData) == 0:
                        df_ReactionData = pd.DataFrame(ReactionData_row_dct)
                    else:
                        df_ReactionData = pd.concat([df_ReactionData,\
                            pd.DataFrame(ReactionData_row_dct)], ignore_index=True)

            #arbitrary text
            for i in range(len(textGlyph_id_list)):
                textGlyph = layout.getTextGlyph(textGlyph_id_list[i])
                #if not textGlyph.isSetOriginOfTextId() and not textGlyph.isSetGraphicalObjectId():
                textGlyph_id = textGlyph_id_list[i]
                text_content = text_content_list[i]
                position = text_position_list[i]
                dimension = text_dimension_list[i]
                for k in range(len(text_render)):
                    if text_content == text_render[k][0]:
                        text_line_color = text_render[k][1]
                        text_line_width = text_render[k][2]
                        text_font_size = text_render[k][3]
                TextData_row_dct = {k:[] for k in COLUMN_NAME_df_TextData}
                TextData_row_dct[TXTCONTENT].append(text_content)
                TextData_row_dct[TXTPOSITION].append(position)
                TextData_row_dct[TXTSIZE].append(dimension)
                TextData_row_dct[TXTFONTCOLOR].append(text_line_color)
                TextData_row_dct[TXTLINEWIDTH].append(text_line_width)
                TextData_row_dct[TXTFONTSIZE].append(text_font_size)
                

                if len(df_TextData) == 0:
                    df_TextData = pd.DataFrame(TextData_row_dct)
                else:
                    df_TextData = pd.concat([df_TextData,\
                        pd.DataFrame(TextData_row_dct)], ignore_index=True)

            #arbitrary shape
            for i in range(len(gen_id_list)):
                genGlyph = layout.getGeneralGlyph(gen_id_list[i])
                genGlyph_id = gen_id_list[i]
                position = gen_position_list[i]
                dimension = gen_dimension_list[i]
                for k in range(len(gen_render)):
                    if genGlyph_id == gen_render[k][0]:
                        shape_fill_color = gen_render[k][1]
                        shape_border_color = gen_render[k][2]
                        shape_border_width = gen_render[k][3]
                        shape_type = gen_render[k][4]
                        shape_info = gen_render[k][5]
                ShapeData_row_dct = {k:[] for k in COLUMN_NAME_df_ShapeData}
                ShapeData_row_dct[SHAPENAME].append(genGlyph_id)
                ShapeData_row_dct[POSITION].append(position)
                ShapeData_row_dct[SIZE].append(dimension)
                ShapeData_row_dct[FILLCOLOR].append(shape_fill_color)
                ShapeData_row_dct[BORDERCOLOR].append(shape_border_color)
                ShapeData_row_dct[BORDERWIDTH].append(shape_border_width)
                ShapeData_row_dct[SHAPETYPE].append(shape_type)
                ShapeData_row_dct[SHAPEINFO].append(shape_info)

                if len(df_ShapeData) == 0:
                    df_ShapeData = pd.DataFrame(ShapeData_row_dct)
                else:
                    df_ShapeData = pd.concat([df_ShapeData,\
                        pd.DataFrame(ShapeData_row_dct)], ignore_index=True)
    
        
        else: # there is no layout information, assign position randomly and size as default
            comp_id_list = Comps_ids
            nodeIdx_temp = 0 #to track the node index    
            for i in range(numComps):
                temp_id = Comps_ids[i]
                comp_idx_id_list.append([i,temp_id])
                vol= model.getCompartmentVolume(i)
                dimension = compartmentDefaultSize
                position = [0,0]
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
                # for j in range(len(COLUMN_NAME_df_CompartmentData)):
                #     try: 
                #         CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]] = CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]][0]
                #     except:
                #         CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]] = ''
                # df_CompartmentData = df_CompartmentData.append(CompartmentData_row_dct, ignore_index=True)
                if len(df_CompartmentData) == 0:
                    df_CompartmentData = pd.DataFrame(CompartmentData_row_dct)
                else:
                    df_CompartmentData = pd.concat([df_CompartmentData,\
                        pd.DataFrame(CompartmentData_row_dct)], ignore_index=True)

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
                NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                NodeData_row_dct[SHAPENAME].append(shape_name)
                NodeData_row_dct[SHAPETYPE].append(shape_type)
                NodeData_row_dct[SHAPEINFO].append(shape_info)
                # for j in range(len(COLUMN_NAME_df_NodeData)):
                #     try: 
                #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                #     except:
                #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                # df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
                if len(df_NodeData) == 0:
                    df_NodeData = pd.DataFrame(NodeData_row_dct)
                else:
                    df_NodeData = pd.concat([df_NodeData,\
                        pd.DataFrame(NodeData_row_dct)], ignore_index=True)
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
                NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                NodeData_row_dct[SHAPENAME].append(shape_name)
                NodeData_row_dct[SHAPETYPE].append(shape_type)
                NodeData_row_dct[SHAPEINFO].append(shape_info)
                # for j in range(len(COLUMN_NAME_df_NodeData)):
                #     try: 
                #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                #     except:
                #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                # df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
                if len(df_NodeData) == 0:
                    df_NodeData = pd.DataFrame(NodeData_row_dct)
                else:
                    df_NodeData = pd.concat([df_NodeData,\
                        pd.DataFrame(NodeData_row_dct)], ignore_index=True)
    
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
                reaction = model_layout.getReaction(temp_id)
                rxn_rev = reaction.getReversible()
                try: 
                    kinetics = model.getRateLaw(i)
                except:
                    kinetics = ""
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
                ReactionData_row_dct[ARROWHEADSIZE].append(reaction_arrow_head_size)
                ReactionData_row_dct[RXNDASH].append(reaction_dash)
                ReactionData_row_dct[RXNREV].append(rxn_rev)
                # for j in range(len(COLUMN_NAME_df_ReactionData)):
                #     try: 
                #         ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]][0]
                #     except:
                #         ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ''
                # df_ReactionData = df_ReactionData.append(ReactionData_row_dct, ignore_index=True)
                if len(df_ReactionData) == 0:
                    df_ReactionData = pd.DataFrame(ReactionData_row_dct)
                else:
                    df_ReactionData = pd.concat([df_ReactionData,\
                        pd.DataFrame(ReactionData_row_dct)], ignore_index=True)  
        
        #return (df_CompartmentData, df_NodeData, df_ReactionData, df_TextData) 
        return (df_CompartmentData, df_NodeData, df_ReactionData, df_TextData, df_ShapeData) 

    # except:
    #    raise ValueError('Invalid SBML!')

    except Exception as e:
        raise Exception (e)  


class load:
    """
    Load SBML string for further processing, i.e. read, edit, visualize the SBML string or
    export it as an updated SBML string.

    Args: 
        sbmlstr: str-the SBML string.

    """

    def __init__(self, sbmlstr):

        # self.sbmlstr = sbmlstr
        # self.df = _SBMLToDF(self.sbmlstr)
        # self.color_style = styleSBML.Style()
        # self.df_text = pd.DataFrame(columns = COLUMN_NAME_df_text)
        # if self.df == None:
        #    sys.exit("There is no valid information to process.")

        if os.path.isfile(sbmlstr):
            with open(sbmlstr) as f:
                self.sbmlstr = f.read()
        else:  
            self.sbmlstr = sbmlstr

        try:
          self.df = _SBMLToDF(self.sbmlstr)
          self.color_style = styleSBML.Style()    
          #self.df_text = pd.DataFrame(columns = COLUMN_NAME_df_text)
        except Exception as err:
            raise Exception (err)


    def getCompartmentPosition(self, id):
        """
        Get the position of a compartment with given compartment id.

        Args: 
            id: str-the id of the compartment.

        Returns:
            position: a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the compartment.  

        Examples: 
            p = sd.getCompartmentPosition('compartment_id')

            print ('x = ', p.x, 'y = ', p.y)         

        """

        p = visualizeSBML._getCompartmentPosition(self.df, id)
        num_alias = len(p)
        position_list = []
        for alias in range(num_alias):
            position = point.Point (p[alias][0], p[alias][1])
            position_list.append(position)
        if len(position_list) == 1:
            position = position_list[0]
        else:
            raise Exception("This is not a valid id.")
        return position

    def getCompartmentSize(self, id):
        """
        Get the size of a compartment with given compartment id.

        Args: 
            id: str-the id of the compartment.

        Returns:
            size: a Point object with attributes x and y representing
            the width and height of the compartment.

        Examples: 
            p = sd.getCompartmentSize('compartment_id')
            
            print ('Width = ', p.x, 'Height = ', p.y)

        """

        p = visualizeSBML._getCompartmentSize (self.df, id)
        num_alias = len(p)
        size_list = []
        for alias in range(num_alias):
            size = point.Point (p[alias][0], p[alias][1])
            size_list.append(size)
        if len(size_list) == 1:
            size = size_list[0]
        else:
            raise Exception("This is not a valid id.")
        return size

    def getCompartmentFillColor(self, id):
        """
        Get the fill color for a compartment with given compartment id.

        Args: 
            id: str-the id of the compartment.

        Returns:
            fill_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), 
            hex str (8 digits)].
        """
        idx_list = self.df[0].index[self.df[0]["id"] == id].tolist() #row index
        fill_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[0].iloc[idx_list[i]]["fill_color"]
            color = _rgb_to_color(rgb)
            fill_color_list.append(color)
        
        if len(fill_color_list) == 1:
            fill_color = fill_color_list[0]
        else:
            raise Exception("This is not a valid id.")
        return fill_color

    def getCompartmentBorderColor(self, id):
        """
        Get the border color of a compartment with a given compartment id.

        Args: 
            id: str-the id of the compartment.

        Returns:
            border_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), 
            hex str (8 digits)].

        """
        idx_list = self.df[0].index[self.df[0]["id"] == id].tolist()
        border_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[0].iloc[idx_list[i]]["border_color"]
            color = _rgb_to_color(rgb)
            border_color_list.append(color)

        if len(border_color_list) == 1:
            border_color = border_color_list[0]
        else:
            raise Exception("This is not a valid id.")
        return border_color

    def getCompartmentBorderWidth(self, id):
        """
        Get the border width of a compartment with a given compartment Id.

        Args: 
            id: str-the id of the compartment.

        Returns:
            border_width: float-compartment border line width.

        """
        
        idx_list = self.df[0].index[self.df[0]["id"] == id].tolist()
        border_width_list =[] 
        for i in range(len(idx_list)):
            border_width_list.append(self.df[0].iloc[idx_list[i]]["border_width"])

        if len(border_width_list) == 1:
            border_width = border_width_list[0]
        else:
            raise Exception("This is not a valid id.")
        return border_width

    def getNodeAliasNum(self, id):
        """
        Get the number of alias nodes with a given node Id.

        Args: 
            id: str-the id of the Node.

        Returns:
            num_alias: int-the number of alias nodes with the given node id.            

        """

        p = visualizeSBML._getNodePosition(self.df, id)
        num_alias = len(p)
        return num_alias

    def isFloatingNode(self, id, alias = 0):
        """
        Returns True if the given node is a floating node.

        Args: 
            id: str-the id of the Node.
            
            alias: int-alias node index: 0 to number if alias nodes

        Returns:
            floating_node: bool-floating node (True) or not (False).

        """
        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        floating_node_list =[] 
        if len(idx_list) == 0:
            raise Exception("This is not a valid id.")
        for i in range(len(idx_list)):
            floating_node_list.append(bool(self.df[1].iloc[idx_list[i]]["floating_node"]))
        if alias < len(idx_list) and alias >= 0:
            floating_node = floating_node_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")
        return floating_node


    def getNodePosition(self, id, alias = 0):
        """
        Get the position of a node with a given node Id.

        Args: 
            id: str-the id of the Node.
            
            alias: int-alias node index: 0 to number of alias nodes

        Returns:
            position: a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the node.

        Examples: 
            p = sd.getNodePosition('ATP')
            
            print('x = ', p.x, 'y = ', p.y)            

        """

        p = visualizeSBML._getNodePosition(self.df, id)
        num_alias = len(p)
        position_list = []
        for i in range(num_alias):
            position = point.Point (p[i][0], p[i][1])
            position_list.append(position)
        if len(position_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(position_list) and alias >= 0:
            position = position_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")
        
        return position


    def getNodeCenter(self, id, alias = 0):
        """
        Get the center point of a node with a given node Id.

        Args: 
            id: str-the id of the Node.
            
            alias: int-alias node index: 0 to number of alias nodes

        Returns:
            position-a Point object with x and y coordinates of the center of the node.
           
        Examples:
            p = sd.getNodeCenter('ATP')
                
            print(p.x, p.y)

        """   
        if not (id in self.getNodeIdList()):
            raise Exception("No such node found in model: " + id)
            
        p = visualizeSBML._getNodePosition(self.df, id) 
        size = visualizeSBML._getNodeSize(self.df, id)
        num_alias = len(p)
        position_list = []
        for i in range(num_alias):
            cx = p[i][0] + size[i][0]/2
            cy = p[i][1] + size[i][1]/2
            position = point.Point(cx, cy) 
            position_list.append(position)
        if len(position_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(position_list) and alias >= 0:
            position = position_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")
        
        return position
        

    def getNodeSize(self, id, alias = 0):
        """
        Get the size of a node with a given node Id.

        Args: 
            id: str-the id of the node.
            
            alias: int-alias node index: 0 to number of alias nodes

        Returns:
            size: a Point object with attributes x and y representing
            the width and height of the node.

        Examples: 
            p = sd.getNodeSize('ATP')
            
            print ('Width = ', p.x, 'Height = ', p.y)

        """

        p = visualizeSBML._getNodeSize (self.df, id)
        num_alias = len(p)
        size_list = []
        for i in range(num_alias):
            size = point.Point (p[i][0], p[i][1])
            size_list.append(size)
        if len(size_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(size_list) and alias >= 0:
            size =  size_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias nodes.")
        
        return size

    def getNodeShape(self, id, alias = 0):
        """
        Get the shape index and the shape of a node with a given node Id.

        Args: 
            id: str-the id of the node.
            
            alias: int-alias node index: 0 to number of alias nodes

        Returns:
            shape: tuple (shape_name, vertex_positions)
            
            shape_name: str-the name of the node shape.

            vertex_positions: list-the vertex positions if any. 

        """

        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        vertex = []
        shape_list =[] 
        for i in range(len(idx_list)):
            shape_name = self.df[1].iloc[idx_list[i]]["shape_name"]
            shape_type = self.df[1].iloc[idx_list[i]]["shape_type"]
            shape_info = self.df[1].iloc[idx_list[i]]["shape_info"]
            node_position = self.df[1].iloc[idx_list[i]]["position"]
            node_size = self.df[1].iloc[idx_list[i]]["size"]
            if shape_type == "rectangle":
                vertex = [node_position,[node_position[0]+node_size[0],node_position[1]],
                [node_position[0]+node_size[0],node_position[1]+node_size[1]],
                [node_position[0],node_position[1]+node_size[1]]]
            elif shape_type == "polygon":
                for j in range(len(shape_info)):
                    vertex_x = node_position[0]+node_size[0]*shape_info[j][0]/100.
                    vertex_y = node_position[1]+node_size[1]*shape_info[j][1]/100.
                    vertex.append([vertex_x,vertex_y])         

            shape_list.append((shape_name, vertex))
        if len(shape_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(shape_list) and alias >= 0:
            shape =  shape_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")
        return shape


    def getNodeTextPosition(self, id, alias = 0):
        """
        Get the text position of a node with a given node Id.

        Args: 
            id: str-the id of node.
            
            alias: int-alias node index: 0 to number of alias nodes

        Returns:
            txt_position: a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the node text.

        Examples: 
            p = sd.getNodeTextPosition('ATP')

            print ('x = ', p.x, 'y = ', p.y)            

        """

        p = visualizeSBML._getNodeTextPosition(self.df, id)
        num_alias = len(p)
        txt_position_list = []
        for i in range(num_alias):
            txt_position = point.Point (p[i][0], p[i][1])
            txt_position_list.append(txt_position)
        if len(txt_position_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(txt_position_list) and alias >= 0:
            txt_position =  txt_position_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")

        return txt_position

        
    def getNodeTextSize(self, id, alias = 0):
        """
        Get the text size of a node with a given node Id.

        Args: 
            id: str-the id of the node.

            alias: int-alias node index: 0 to number of alias nodes

        Returns:
            size: a Point object with attributes x and y representing
            the width and height of the node text.

        Examples:
            p = sd.getNodeTextSize('ATP')

            print ('Width = ', p.x, 'Height = ', p.y)          

        """

        p = visualizeSBML._getNodeTextSize(self.df, id)
        num_alias = len(p)
        txt_size_list = []
        for i in range(num_alias):
            txt_size = point.Point (p[i][0], p[i][1])
            txt_size_list.append(txt_size)
        if len(txt_size_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(txt_size_list) and alias >= 0:
            txt_size =  txt_size_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")

        return txt_size


    def getNodeFillColor(self, id, alias = 0):
        """
        Get the fill color of a node with a given node Id.

        Args: 
            id: str-the id of the node.

            alias: int-alias node index: 0 to number of alias nodes

        Returns:
            fill_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), 
            hex str (8 digits)]; or list-[str-gradient_type, list-gradient_info, list-stop_info],
            where gradient_type can be 'linearGradient' or 'radialGradient', while gradient_info
            and stop_info refers to setNodeFillLinearGradient() and setNodeFillRadialGradient.

        """

        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        fill_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[1].iloc[idx_list[i]]["fill_color"]
            if type(rgb[0]) == str:
                color = rgb
            else:
                color = _rgb_to_color(rgb)
            fill_color_list.append(color)
        if len(fill_color_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(fill_color_list) and alias >= 0:
            fill_color = fill_color_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")
        return fill_color


    def getNodeBorderColor(self, id, alias = 0):
        """
        Get the border color of a node with a given node Id.

        Args: 
            id: str-the id of the node.
            
            alias: int-alias node index: 0 to number of alias nodes

        Returns:
            border_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), 
            hex str (8 digits)].

        """

        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        border_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[1].iloc[idx_list[i]]["border_color"]
            color = _rgb_to_color(rgb)
            border_color_list.append(color)
        if len(border_color_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(border_color_list) and alias >= 0:
            border_color =  border_color_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")

        return border_color


    def getNodeBorderWidth(self, id, alias = 0):
        """
        Get the border width of a node with a given node Id.

        Args: 
            id: str-the id of the node.
            
            alias: int-alias node index: 0 to number of alias nodes

        Returns:
            border_width: float-node border line width.

        """
        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        border_width_list =[] 
        for i in range(len(idx_list)):
            border_width_list.append(self.df[1].iloc[idx_list[i]]["border_width"])
        if len(border_width_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(border_width_list) and alias >= 0:
            border_width =  border_width_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")

        return border_width

    def getNodeTextFontColor(self, id, alias = 0):
        """
        Get the text font color of a node with a given node Id.

        Args: 
            id: str-the id of the node.

            alias: int-alias node index: 0 to number of alias nodes.

        Returns:
            txt_font_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), 
            hex str (8 digits)].

        """

        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        txt_font_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[1].iloc[idx_list[i]]["txt_font_color"]
            color = _rgb_to_color(rgb)
            txt_font_color_list.append(color)
        if len(txt_font_color_list) == 0:
            raise Exception("This is not a valid id.")

        if alias < len(txt_font_color_list) and alias >= 0:
            txt_font_color =  txt_font_color_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")
        return txt_font_color

    def getNodeTextLineWidth(self, id, alias = 0):
        """
        Get the text line width of a node with a given node Id.

        Args: 
            id: int-the id of the node.

            alias: int-alias node index: 0 to number of alias nodes

        Returns:
            txt_line_width: float-node text line width.

        """
        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        txt_line_width_list =[] 
        for i in range(len(idx_list)):
            txt_line_width_list.append(self.df[1].iloc[idx_list[i]]["txt_line_width"])
        if len(txt_line_width_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(txt_line_width_list) and alias >= 0:
            txt_line_width =  txt_line_width_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")

        return txt_line_width

    def getNodeTextFontSize(self, id, alias = 0):
        """
        Get the text font size of a node with a given node Id.

        Args: 
            id: str-the id of the node.

            alias: int-alias node index: 0 to number of alias nodes

        Returns:
            txt_font_size: float.

        """
        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        txt_font_size_list =[] 
        for i in range(len(idx_list)):
            txt_font_size_list.append(float(self.df[1].iloc[idx_list[i]]["txt_font_size"]))
        if len(txt_font_size_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(txt_font_size_list) and alias >= 0:
            txt_font_size =  txt_font_size_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")

        return txt_font_size

    def getReactionCenterPosition(self, id):
        """
        Get the center position of a reaction with a given reaction Id.

        Args: 
            id: str-the id of the reaction.

        Returns:
            center_position: a Point object with attributes x and y representing
            the x/y position of the current center of the reaction. 

        Examples: 
            p = sd.getReactionCenterPosition('reaction_id')

            print ('x = ', p.x, 'y = ', p.y)          

        """

        p = visualizeSBML._getReactionCenterPosition(self.df, id)
        num = len(p)
        center_position_list = []
        for i in range(num):
            center_position = point.Point (p[i][0], p[i][1])
            center_position_list.append(center_position)
        if len(center_position_list) == 1:
            center_position = center_position_list[0]
        else:
            raise Exception("This is not a valid id.")

        return center_position

    def getReactionBezierHandles(self, id):
        """
        Get the bezier handle positions of a reaction with a given reaction Id.

        Args: 
            id: str-the id of the reaction.

        Returns:
            handle_positions: list-position of the handles: 
            [center handle, reactant handles, product handles].

            position: a Point object with attributes x and y representing the x/y position.          

        """

        p = visualizeSBML._getReactionBezierHandles(self.df, id)
        num = len(p)
        handle_position_list = []
        for j in range(num):
            handle_position = []
            for i in range(len(p[j])):
                handle_position.append(point.Point(p[j][i][0], p[j][i][1]))
            handle_position_list.append(handle_position)

        if len(handle_position_list) == 1:
            handle_position = handle_position_list[0]
        else:
            raise Exception("This is not a valid id.")

        return handle_position

    def getReactionFillColor(self, id):
        """
        Get the fill color of a reaction with with a given reaction Id.

        Args: 
            id: str-the id of the reaction.

        Returns:
            fill_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), 
            hex str (8 digits)].

        """
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        fill_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[2].iloc[idx_list[i]]["fill_color"]
            color = _rgb_to_color(rgb)
            fill_color_list.append(color)
        
        if len(fill_color_list) == 1:
            fill_color = fill_color_list[0]
        else:
            raise Exception("This is not a valid id.")
        
        return fill_color

    def getReactionLineThickness(self, id):
        """
        Get the line thickness of a reaction with a given reaction Id.

        Args: 
            id: str-the id of the reaction.

        Returns:
            line_thickness: float-reaction border line width.

        """
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        line_thickness_list =[] 
        for i in range(len(idx_list)):
            line_thickness_list.append(self.df[2].iloc[idx_list[i]]["line_thickness"])

        if len(line_thickness_list) == 1:
            line_thickness = line_thickness_list[0]
        else:
            raise Exception("This is not a valid id.")

        return line_thickness

    def _isBezierReactionType(self, id):
        """
        Judge whether it is a bezier reaction curve with a given reaction Id.

        Args: 
            id: str-the id of the reaction

        Returns:
            bezier: bool-bezier reaction (True) or not (False)

        """
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        bezier_list =[] 
        for i in range(len(idx_list)):
            bezier_list.append(bool(self.df[2].iloc[idx_list[i]]["bezier"]))
        
        if len(bezier_list) == 1:
            bezier = bezier_list[0]
        else:
            raise Exception("This is not a valid id.")

        return bezier

    #def getReactionArrowHeadSize(self):
    def getReactionArrowHeadSize(self, id):
        """
        Get the arrow head size of reactions with a given reaction Id.

        Args: 

        Returns:
            arrow_head_size: a Point object with attributes x and y representing
            the width and height of the arrow head.

        Examples: 
            p = sd.getReactionArrowHeadSize('reaction_id')
            
            print ('Width = ', p.x, 'Height = ', p.y)

        """
        arrow_head_size_pre = []
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        for i in range(len(idx_list)):
            arrow_head_size_pre.append(self.df[2].iloc[idx_list[i]]["arrow_head_size"]) 
        arrow_head_size_list =[]
        for i in range(len(arrow_head_size_pre)):
            arrow_head_size_list.append(point.Point(arrow_head_size_pre[i][0],arrow_head_size_pre[i][1]))
        if len(arrow_head_size_list) == 1:
            arrow_head_size = arrow_head_size_list[0]
        else:
            raise Exception("This is not a valid id.")

        return arrow_head_size

    def getReactionDash(self, id):
        """
        Get the dash information with a given reaction Id.

        Args: 
            id: str-the id of the reaction.

        Returns:
            dash: list - [] means solid; 
            [a,b] means drawing a a-point line and following a b-point gap and etc;
            [a,b,c,d] means drawing a a-point line and following a b-point gap, and then
            drawing a c-point line followed by a d-point gap.

        """
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        dash_list =[] 
        for i in range(len(idx_list)):
            dash_list.append((self.df[2].iloc[idx_list[i]]["rxn_dash"]))
        if len(dash_list) == 1:
            dash = dash_list[0]
        else:
            raise Exception("This is not a valid id.")
        
        return dash
    
    def setCompartmentPosition(self, id, position):
        """
        Set the x,y coordinates of the compartment position.

        Args:  
            id: str-compartment id.

            position: list or point.Point()
                
            list-
            [position_x, position_y], the coordinate represents the top-left hand corner of 
            the compartment.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the compartment.

        """
        self.df = editSBML._setCompartmentPosition(self.df, id, position)
        #return self.df
    
    def setCompartmentSize(self, id, size):
        """
        Set the compartment size.

        Args:  
            df: DataFrame-initial information.

            id: str-compartment id.

            size: list/point.Point()-
                
            list-
            1*2 matrix-size of the compartment [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the compartment.

        """
        self.df = editSBML._setCompartmentSize(self.df, id, size)
        #return self.df

    def setCompartmentFillColor(self, id, fill_color, opacity = 1.):
        """
        Set the compartment fill color.

        Args:  
            id: str-compartment id.

            fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

        """
        self.df = editSBML._setCompartmentFillColor(self.df, id, fill_color, opacity)
        #return self.df

    def setCompartmentBorderColor(self, id, border_color, opacity = 1.):       
        """
        Set the compartment border color.

        Args:  
            id: str-compartment id.

            border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

        """
        self.df = editSBML._setCompartmentBorderColor(self.df, id, border_color, opacity)
        #return self.df

    def setCompartmentBorderWidth(self, id, border_width):
        """
        Set the compartment border width.

        Args:  
            id: str-compartment id.

            border_width: float-compartment border line width.

        """
        self.df = editSBML._setCompartmentBorderWidth(self.df, id, border_width)
        #return self.df

    def setFloatingBoundaryNode(self, id, floating_node, alias = 0):
        """
        Set a node to be floating node (True) or boundary node (False).

        Args:  
            id: str-node id.

            floating_node: bool-floating node (True) or not (False).

            alias: int-alias node index [0, num_alias).
        
        """
        self.df = editSBML._setFloatingBoundaryNode(self.df, id, floating_node, alias=alias)
        #return self.df

    def setNodePosition(self, id, position, alias = 0):
        """
        Set the x,y coordinates of the node position.

        Args:  
            id: str-node id.

            position: list/point.Point()-
                
            list-
            [position_x, position_y], the coordinate represents the top-left hand corner of the node.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the node.

            alias: int-alias node index [0, num_alias).

        """
        self.df = editSBML._setNodePosition(self.df, id, position, alias=alias)
        #return self.df

    def setNodeAndTextPosition(self, id, position, alias = 0):
        """
        Set the x,y coordinates of the node position and node text position if they are consistent.
        Please only use this function if you want to design the node position and node text 
        position to be the same, otherwise use setNodePosition() and setNodeTextPosition() 
        separately to set the position of the node and the node text.

        Args:  
            id: str-node id.

            position: list/point.Point()-
                
            list-
            [position_x, position_y], the coordinate represents the top-left hand corner of the 
            node and the node text.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the node and the node text.

            alias: int-alias node index [0, num_alias).

        """
        self.df = editSBML._setNodePosition(self.df, id, position, alias=alias)
        self.df = editSBML._setNodeTextPosition(self.df, id, position, alias=alias)
        #return self.df

    def setNodeSize(self, id, size, alias = 0):
        """
        Set the node size.

        Args:  
            id: str-node id.

            size: list/point.Point()-
                
            list-
            1*2 matrix-size of the node [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the node.

            alias: int-alias node index [0, num_alias).

        """
        self.df = editSBML._setNodeSize(self.df, id, size, alias=alias)
        #return self.df

    def setNodeAndTextSize(self, id, size, alias = 0):
        """
        Set the node and node text size if there are consistent.

        Args:  
            id: str-node id.

            size: list/point.Point()-
                
            list-
            1*2 matrix-size of the node and text [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the node and node text.

            alias: int-alias node index [0, num_alias).

        """
        self.df = editSBML._setNodeSize(self.df, id, size, alias=alias)
        self.df = editSBML._setNodeTextSize(self.df, id, size, alias=alias)
        #return self.df

    def setNodeShape(self, id, shape, alias = 0):
        """
        Set the node shape by shape index or name string.

        Args:  
            id: str-node id.

            shape: int/str-

            int-
                0:text_only, 1:rectangle, 2:ellipse, 3:hexagon, 4:line, or 5:triangle;
                6:upTriangle, 7:downTriangle, 8:leftTriangle, 9: rightTriangle.

            str-
                "text_only", "rectangle", "ellipse", "hexagon", "line", or "triangle";
                "upTriangle", "downTriangle", "leftTriangle", "rightTriangle".

            alias: int-alias node index [0, num_alias).
            
        """
        self.df = editSBML._setNodeShape(self.df, id, shape, alias=alias)
        #return self.df

    def setNodeArbitraryPolygonShape(self, id, shape_name, shape_info, alias = 0):
        """
        Set an arbitrary polygon shape to a node by shape name and shape info.

        Args:  
            id: str-node id.

            shape_name: str-name of the arbitrary polygon shape.

            shape_info: list-[[x1,y1],[x2,y2],[x3,y3],etc], where x,y are floating numbers from 0 to 100.
            x represents the percentage of width, and y represents the percentage of height.

            alias: alias node index [0, num_alias).
            
        """
        self.df = editSBML._setNodeArbitraryPolygonShape(self.df, id, shape_name, shape_info, alias=alias)
        #return self.df

    # def _setNodeArbitraryEllipseShape(self, id, shape_name, shape_info):
    #     """
    #     Set an arbitrary ellipse shape to a node by shape name and shape info.

    #     Args:  
    #         id: str-node id.

    #         shape_name: str-name of the arbitrary ellipse shape.

    #         shape_info: list-[[[x1,y1],[r1,r2]]], where x,y,r are floating numbers from 0 to 100.
    #     """
    #     self.df = editSBML._setNodeArbitraryEllipseShape(self.df, id, shape_name, shape_info)
    #     return self.df

    def setNodeTextPosition(self, id, txt_position, alias = 0):
        """
        Set the x,y coordinates of the node text position.

        Args:  
            id: str-node id.

            txt_position: list/point.Point()-
                
            list-
            [txt_position_x, txt_position_y], the coordinate represents the top-left hand 
            corner of the node text.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the node text.

            alias: alias node index [0, num_alias).

        """
        self.df = editSBML._setNodeTextPosition(self.df, id, txt_position, alias=alias)
        #return self.df

    def moveNodeTextPosition(self, id, rel_position, alias = 0):
        """
        Move the x,y coordinates of the node text position relative to its original position.

        Args:  
            id: str-node id.

            rel_position: list/point.Point()-
                
            list-
            [rel_position_x, rel_position_y], the relative coordinates moving away from the 
            original node text position.

            point.Point()-
            a Point object with attributes x and y representing the relative coordinates moving 
            away from the original node text position.

            alias: alias node index [0, num_alias).

        """
        original_position = visualizeSBML._getNodeTextPosition(self.df, id)[alias]
        if type(rel_position) != list and type(rel_position) != type(point.Point()):
            raise Exception("Please enter a valid rel_position type.")
        if type(rel_position) == type(point.Point()):
            rel_position = [rel_position.x, rel_position.y]
        update_position = [original_position[0] + rel_position[0], 
                            original_position[1] + rel_position[1]]
        self.df = editSBML._setNodeTextPosition(self.df, id, update_position, alias=alias)
        #return self.df

    def setNodeTextPositionCenter(self, id, alias = 0):
        """
        Set the node text position to the center of the node.

        Args:  
            id: str-node id.

            alias: int-alias node index [0, num_alias).

        """
        self.df = editSBML._setNodeTextPositionCenter(self.df, id, alias=alias)
        #return self.df

    def setNodeTextPositionLeftCenter(self, id, alias = 0):
        """
        Set the node text position to the left center of the node.

        Args:  
            id: str-node id.

            alias: alias node index [0, num_alias).

        """
        self.df = editSBML._setNodeTextPositionLeftCenter(self.df, id, alias=alias)
        #return self.df

    def setNodeTextPositionRightCenter(self, id, alias = 0):
        """
        Set the node text position to the right center of the node.

        Args:  
            id: str-node id.

            alias: int- alias node index [0, num_alias).

        """
        self.df = editSBML._setNodeTextPositionRightCenter(self.df, id, alias=alias)
        #return self.df

    def setNodeTextPositionUpperCenter(self, id, alias = 0):
        """
        Set the node text position to the upper center of the node.

        Args:  
            id: str-node id.

            alias: alias node index [0, num_alias).

        """
        self.df = editSBML._setNodeTextPositionUpperCenter(self.df, id, alias=alias)
        #return self.df

    def setNodeTextPositionLowerCenter(self, id, alias = 0):
        """
        Set the node text position to the lower center of the node.

        Args:  
            id: str-node id.

            alias: int-alias node index [0, num_alias).

        """
        self.df = editSBML._setNodeTextPositionLowerCenter(self.df, id, alias=alias)
        #return self.df

    def setNodeTextPositionUpperLeft(self, id, alias = 0):
        """
        Set the node text position to the upper left of the node.

        Args:  
            id: str-node id.

            alias: int-alias node index [0, num_alias).

        """
        self.df = editSBML._setNodeTextPositionUpperLeft(self.df, id, alias=alias)
        #return self.df
    
    def setNodeTextPositionUpperRight(self, id, alias = 0):
        """
        Set the node text position to the upper right of the node.

        Args:  
            id: str-node id.

            alias: int-alias node index [0, num_alias).

        """
        self.df = editSBML._setNodeTextPositionUpperRight(self.df, id, alias=alias)
        #return self.df

    def setNodeTextPositionLowerLeft(self, id, alias = 0):
        """
        Set the node text position to the lower left of the node.

        Args:  
            id: str-node id.

            alias: int-alias node index [0, num_alias).

        """
        self.df = editSBML._setNodeTextPositionLowerLeft(self.df, id, alias=alias)
        #return self.df

    def setNodeTextPositionLowerRight(self, id, alias = 0):
        """
        Set the node text position to the lower right of the node.

        Args:  
            id: str-node id.

            alias: int-alias node index [0, num_alias).

        """
        self.df = editSBML._setNodeTextPositionLowerRight(self.df, id, alias=alias)
        #return self.df

    def setNodeTextSize(self, id, txt_size, alias = 0):
        """
        Set the node text size with given node id.

        Args:  
            id: str-node id.

            txt_size: list or point.Point()
                
            list-
            1*2 matrix-size of the node text [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the node text.

            alias: alias node index [0, num_alias).

        """
        self.df = editSBML._setNodeTextSize(self.df, id, txt_size, alias=alias)
        #return self.df
 
    def setNodeFillColor(self, id, fill_color, opacity = 1., alias = 0):
        """
        Set the node fill color with given node id.

        Args:  
            id: str-node id.

            fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            alias: int-alias node index [0, num_alias).

        """
        self.df = editSBML._setNodeFillColor(self.df, id, fill_color, opacity, alias=alias)
        #return self.df

    def setNodeFillLinearGradient(self, id, gradient_info, stop_info, alias = 0):
        """
        Set the node fill linear gradient with given node id.

        Args:  
            id: str-node id.

            gradient_info: list - [[x1,y1],[x2,y2]], where x,y are floating numbers from 0 to 100.
            x represents the percentage of width, and y represents the percentage of height.

            stop_info: list - [[x1,[r1,g1,b1,a1]],[x2,[r2,g2,b2,a2]],etc],
            where x is floating number from 0 to 100.

            alias: int-alias node index [0, num_alias).

        """
        self.df = editSBML._setNodeFillLinearGradient(self.df, id, gradient_info, stop_info, alias=alias)
        #return self.df

    def setNodeFillRadialGradient(self, id, gradient_info, stop_info, alias = 0):
        """
        Set the node fill radial gradient.

        Args:  
            id: str-node id.

            gradient_info: list - [[x1,y1],[r]], where x,y,r are floating numbers from 0 to 100.
            x represents the center with percentage of width and height; r represents the radius.

            stop_info, list - [[x1,[r1,g1,b1,a1]],[x2,[r2,g2,b2,a2]],etc],
            where x is floating number from 0 to 100.

            alias: alias node index [0, num_alias).

        """
        self.df = editSBML._setNodeFillRadialGradient(self.df, id, gradient_info, stop_info, alias=alias)
        #return self.df

    def setNodeBorderColor(self, id, border_color, opacity = 1., alias = 0):
        """
        Set the node border color of a node with a given id.

        Args:  
            id: str-node id.

            border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            alias: int-alias node index [0, num_alias).

        Example:
           la.setNodeBorderColor ('node1', 'CornflowerBlue')
        """
        self.df = editSBML._setNodeBorderColor(self.df, id, border_color, opacity, alias=alias)

    def setNodeBorderWidth(self, id, border_width, alias = 0):
        """
        Set the node border width for a node of given id.

        Args:  
            id: str-node id.

            border_width: float-node border line width.

            alias: int-alias node index [0, num_alias).

        Example:
            la.setNodeBorderWidth ('node4', 3)
        """
        self.df = editSBML._setNodeBorderWidth(self.df, id, border_width, alias=alias)
        #return self.df

    def setNodeTextFontColor(self, id, txt_font_color, opacity = 1., alias = 0):
        """
        Set the node text font color for a node of given id.

        Args:  
            id: str-node id.

            txt_font_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            alias: int-alias node index [0, num_alias).
        
        Example:
           la.setNodeTextFontColor ('node1', 'CornflowerBlue')
        """
        self.df = editSBML._setNodeTextFontColor(self.df, id, txt_font_color, opacity, alias=alias)
        #return self.df

    def setNodeTextLineWidth(self, id, txt_line_width, alias = 0):
        """
        Set the node text line width for a node of given id.

        Args:  
            id: str-node id.

            txt_line_width: float-node text line width.

            alias: int-alias node index [0, num_alias).
        
        """
        self.df = editSBML._setNodeTextLineWidth(self.df, id, txt_line_width, alias=alias)
        #return self.df

    def setNodeTextFontSize(self, id, txt_font_size, alias = 0):
        """
        Set the node text font size for a node of given id.

        Args:  
            id: str-node id.

            txt_font_size: float-node text font size.

            alias: int-alias node index [0, num_alias).
        
        """
        self.df = editSBML._setNodeTextFontSize(self.df, id, txt_font_size, alias=alias)
        #return self.df

    def setReactionStraightLine(self, id):
        """
        For a reaction of given id, use straight lines to represent the reaction. 
        The default reaction line style is to use Bezier curves.

        Args:  
            id: str-reaction id.
      
        """
        # center_x = 0.
        # center_y = 0.

        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        if len(idx_list) == 0:
            raise Exception("This is not a valid id.")
        rct_list = []
        prd_list = []
        rct_list.append(self.df[2].iloc[idx_list[0]]["sources"])
        prd_list.append(self.df[2].iloc[idx_list[0]]["targets"])

        rct_num = len(rct_list[0])
        prd_num = len(prd_list[0])

        rct_id_list = []
        prd_id_list = []
        for i in range(rct_num):
            temp_idx = self.df[1].index[self.df[1]["idx"] == rct_list[0][i]].tolist()[0]
            rct_id_list.append(self.df[1].iloc[temp_idx]["id"])
        for i in range(prd_num):
            temp_idx = self.df[1].index[self.df[1]["idx"] == prd_list[0][i]].tolist()[0]
            prd_id_list.append(self.df[1].iloc[temp_idx]["id"])

        src_position = []
        src_dimension = []
        dst_position = []
        dst_dimension = []
        for i in range(rct_num):
            temp_idx = self.df[1].index[self.df[1]["id"] == rct_id_list[i]].tolist()[0]
            src_position.append(self.df[1].iloc[temp_idx]["position"])
            src_dimension.append(self.df[1].iloc[temp_idx]["size"])
        for i in range(prd_num):
            temp_idx = self.df[1].index[self.df[1]["id"] == prd_id_list[i]].tolist()[0]
            dst_position.append(self.df[1].iloc[temp_idx]["position"])
            dst_dimension.append(self.df[1].iloc[temp_idx]["size"])
  
        # for j in range(rct_num):
        #     center_x += src_position[j][0]+.5*src_dimension[j][0]
        #     center_y += src_position[j][1]+.5*src_dimension[j][1]
        # for j in range(prd_num):
        #     center_x += dst_position[j][0]+.5*dst_dimension[j][0]
        #     center_y += dst_position[j][1]+.5*dst_dimension[j][1]
        # center_x = center_x/(rct_num + prd_num) 
        # center_y = center_y/(rct_num + prd_num)
        center_position_pt = visualizeSBML._getReactionCenterPosition(self.df, id)
        center_position = [center_position_pt[0][0], center_position_pt[0][1]]
        #center_position = [center_x, center_y]
        handles = [center_position]
        for j in range(rct_num):
            src_handle_x = .5*(center_position[0] + src_position[j][0] + .5*src_dimension[j][0])
            src_handle_y = .5*(center_position[1] + src_position[j][1] + .5*src_dimension[j][1])
            handles.append([src_handle_x,src_handle_y])
        for j in range(prd_num):
            dst_handle_x = .5*(center_position[0] + dst_position[j][0] + .5*dst_dimension[j][0])
            dst_handle_y = .5*(center_position[1] + dst_position[j][1] + .5*dst_dimension[j][1])
            handles.append([dst_handle_x,dst_handle_y])
        # print('rct:', src_position, src_dimension)
        # print('prd:', dst_position, dst_dimension)
        # print("center:", center_position)
        # print("handle:", handles)
        self.df = editSBML._setReactionCenterPosition(self.df, id, center_position)        
        self.df = editSBML._setReactionBezierHandles(self.df, id, handles)
 

    def setReactionCenterPosition(self, id, position):
        """
        Set the reaction center position for a reaction with a given reaction id. .

        Args:  
            id: str-reaction id.
            
            position: list or point.Point()
                
            list-
            1*2 matrix-[position_x, position_y].

            point.Point()-
            a Point object with attributes x and y representing the x/y position.

        """
        self.df = editSBML._setReactionCenterPosition(self.df, id, position)
    

    def setReactionBezierHandles(self, id, position):
        """
        Set the reaction bezier handle positions for a given reaction.

        Args:  
            id: str-reaction id.
            
            position: list-position of the handles: [center handle, reactant handle1, ..., product handle1, ...].
                            
            center handle/reactant handle1/product handle1: list or point.Point()
                
            list-
            [position_x, position_y], the coordinate represents the top-left hand 
            corner of the node.

            point.Point()-
            a Point object with attributes x and y representing the x/y position.
        
        """
        self.df = editSBML._setReactionBezierHandles(self.df, id, position)
        #return self.df

    def setReactionDefaultCenterAndHandlePositions(self, id):
        """
        Set detault center and handle positions. The default center is the centroid of the reaction,
        and the default handle positions are middle points of nodes (species) and the centroid.

        Args:  
            id: str-reaction id.
            
        """
        
        center_x = 0.
        center_y = 0.

        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        if len(idx_list) == 0:
            raise Exception("This is not a valid id.")
        rct_list = []
        prd_list = []
        rct_list.append(self.df[2].iloc[idx_list[0]]["sources"])
        prd_list.append(self.df[2].iloc[idx_list[0]]["targets"])

        rct_num = len(rct_list[0])
        prd_num = len(prd_list[0])

        rct_id_list = []
        prd_id_list = []
        for i in range(rct_num):
            temp_idx = self.df[1].index[self.df[1]["idx"] == rct_list[0][i]].tolist()[0]
            rct_id_list.append(self.df[1].iloc[temp_idx]["id"])
        for i in range(prd_num):
            temp_idx = self.df[1].index[self.df[1]["idx"] == prd_list[0][i]].tolist()[0]
            prd_id_list.append(self.df[1].iloc[temp_idx]["id"])

        src_position = []
        src_dimension = []
        dst_position = []
        dst_dimension = []
        for i in range(rct_num):
            temp_idx = self.df[1].index[self.df[1]["id"] == rct_id_list[i]].tolist()[0]
            src_position.append(self.df[1].iloc[temp_idx]["position"])
            src_dimension.append(self.df[1].iloc[temp_idx]["size"])
        for i in range(prd_num):
            temp_idx = self.df[1].index[self.df[1]["id"] == prd_id_list[i]].tolist()[0]
            dst_position.append(self.df[1].iloc[temp_idx]["position"])
            dst_dimension.append(self.df[1].iloc[temp_idx]["size"])
  
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
        # print('rct:', src_position, src_dimension)
        # print('prd:', dst_position, dst_dimension)
        # print("center:", center_position)
        # print("handle:", handles)
        self.df = editSBML._setReactionCenterPosition(self.df, id, center_position)        
        self.df = editSBML._setReactionBezierHandles(self.df, id, handles)

        #return self.df

    def setReactionFillColor(self, id, fill_color, opacity = 1.):
        """
        Set the reaction fill color.

        Args:  
            id: str-reaction id.

            fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

        Example:
           setReactionFillColor ('J1', "BurlyWood")
        
        """
        self.df = editSBML._setReactionFillColor(self.df, id, fill_color, opacity)
        #return self.df


    def setReactionLineThickness(self, id, line_thickness):
        """
        Set the reaction line thickness.

        Args:  
            id: str-reaction id.

            line_thickness: float-reaction border line width.
        
        """
        self.df = editSBML._setReactionLineThickness(self.df, id, line_thickness)
        #return self.df

    def _setBezierReactionType(self, id, bezier = True):
        """
        Set the reaction type to use a Bezier curve depending on the Bezier flag. 

        Args:  
            id: str-reaction id.

            bezier: bool-bezier reaction (True as default) or not (False as straightline).
        
        """
        self.df = editSBML._setBezierReactionType(self.df, id, bezier)
        #return self.df
    
    def setReactionArrowHeadSize(self, id, size):
    #def setReactionArrowHeadSize(self, size):
        """
        Set the reaction arrow head size with a certain reaction id.

        Args:  
            size: list or point.Point()
                
            list-
            1*2 matrix-size of the arrow head [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the arrow head.
        
        """
        self.df = editSBML._setReactionArrowHeadSize(self.df, id, size)

    def setReactionDashStyle(self, id, dash = []):
        """
        Set the reaction dash information with a certain reaction id.

        Args:  
            id: str-reaction id.

            dash: list-[] means solid; 
            [a,b] means drawing a a-point line and following a b-point gap and etc;
            [a,b,c,d] means drawing a a-point line and following a b-point gap, and then 
            drawing a c-point line followed by a d-point gap.
        
        """
        self.df = editSBML._setReactionDash(self.df, id, dash)
        #return self.df

    # def addText(self, txt_str, txt_position, txt_font_color = [0, 0, 0], opacity = 1., 
    #     txt_line_width = 1., txt_font_size = 12.):
    #     """
    #     Add arbitrary text onto canvas.

    #     Args:  
    #         txt_str: str-the text content.

    #         txt_position: list-[position_x, position_y], the coordinate represents the top-left hand 
    #         corner of the node text.

    #         txt_font_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

    #         opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

    #         txt_line_width: float-node text line width.

    #         txt_font_size: float-node text font size.
            
    #     """
    #     self.df_text = editSBML._addText(self.df_text, txt_str=txt_str, txt_position=txt_position, 
    #     txt_font_color=txt_font_color, opacity=opacity, txt_line_width=txt_line_width, 
    #     txt_font_size=txt_font_size) 
        
    #     return self.df_text


    # def removeText(self, txt_str):
    #     """
    #     Remove the arbitrary text from canvas.

    #     Args:  
    #         txt_str: str-the text content.
            
    #     """
    #     self.df_text = editSBML._removeText(self.df_text, txt_str=txt_str) 
        
    #     return self.df_text


    def getTextPosition(self, txt_str):
        """
        Get the arbitrary text position with its content.

        Args: 
            txt_str: str-the content of the text.

        Returns: 
            position: a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the text.

        Examples: 
            p = sd.getTextPosition('text_content')
            
            print ('x = ', p.x, 'y = ', p.y)            

        """

        p = visualizeSBML._getTextPosition(self.df, txt_str)
        num_alias = len(p)
        position_list = []
        for alias in range(num_alias):
            position = point.Point (p[alias][0], p[alias][1])
            position_list.append(position)
        if len(position_list) == 1:
            position = position_list[0]
        else:
            raise Exception("This is not a valid id.")

        return position

    def getTextSize(self, txt_str):
        """
        Get the arbitrary text size with its text content.

        Args: 
            txt_str: str-the text content.

        Returns:
            txt_size_list: list of txt_size.

            txt_size: a Point object with attributes x and y representing
            the width and height of the text.

        Examples: 
            p = sd.getTextSize('text_content')

            print ('Width = ', p.x, 'Height = ', p.y)

        """

        p = visualizeSBML._getTextSize (self.df, txt_str)
        num_alias = len(p)
        txt_size_list = []
        for alias in range(num_alias):
            txt_size = point.Point (p[alias][0], p[alias][1])
            txt_size_list.append(txt_size)
        if len(txt_size_list) == 1:
            txt_size = txt_size_list[0]
        else:
            raise Exception("This is not a valid id.")
        return txt_size

    def getTextFontColor(self, txt_str):
        """
        Get the arbitrary text font color with its text content.

        Args: 
            txt_str: str-the text content.

        Returns:
            txt_font_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), 
            hex str (8 digits)].
        """

        idx_list = self.df[3].index[self.df[3]["txt_content"] == txt_str].tolist()
        txt_font_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[3].iloc[idx_list[i]]["txt_font_color"]
            color = _rgb_to_color(rgb)
            txt_font_color_list.append(color)
        if len(txt_font_color_list) == 1:
            txt_font_color = txt_font_color_list[0]
        else:
            raise Exception("This is not a valid id.")

        return txt_font_color

    def getTextLineWidth(self, txt_str):
        """
        Get the arbitrary text line width with the text content.

        Args: 
            txt_str: str-the text content.

        Returns:
            txt_line_width: float-node text line width.
        
        """
        idx_list = self.df[3].index[self.df[3]["txt_content"] == txt_str].tolist()
        txt_line_width_list =[] 
        for i in range(len(idx_list)):
            txt_line_width_list.append(self.df[3].iloc[idx_list[i]]["txt_line_width"])
        if len(txt_line_width_list) == 1:
            txt_line_width = txt_line_width_list[0]
        else:
            raise Exception("This is not a valid id.")

        return txt_line_width

    def getTextFontSize(self, txt_str):
        """
        Get the arbitrary text font size with the text content.

        Args: 
            txt_str: str-the text content.

        Returns:
            txt_font_size: float-text font size.
        
        """
        idx_list = self.df[3].index[self.df[3]["txt_content"] == txt_str].tolist()
        txt_font_size_list =[] 
        for i in range(len(idx_list)):
            txt_font_size_list.append(float(self.df[3].iloc[idx_list[i]]["txt_font_size"]))

        if len(txt_font_size_list) == 1:
            txt_font_size = txt_font_size_list[0]
        else:
            raise Exception("This is not a valid id.")
        return txt_font_size

    def setTextPosition(self, txt_str, txt_position):
        """
        Set the x,y coordinates of the arbitrary text position.

        Args:  
            txt_str: str-the text content.

            txt_position: list/point.Point()-
                
            list-
            [txt_position_x, txt_position_y], the coordinate represents the top-left hand corner of 
            the node text.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the text.

        """
        self.df = editSBML._setTextPosition(self.df, txt_str, txt_position)
        #return self.df

    def setTextSize(self, txt_str, txt_size):
        """
        Set the arbitrary text size.

        Args:  
            txt_str: str-the text content.

            txt_size: list/point.Point()-
                
            list-
            1*2 matrix-size of the text [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the text.
        
        """
        self.df = editSBML._setTextSize(self.df, txt_str, txt_size)
        #return self.df

    def setTextFontColor(self, txt_str, txt_font_color, opacity = 1.):
        """
        Set the arbitrary text font color.

        Args:  
            txt_str: str-the text content.

            txt_font_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).
        
        """
        self.df = editSBML._setTextFontColor(self.df, txt_str, txt_font_color, opacity)
        #return self.df

    def setTextLineWidth(self, txt_str, txt_line_width):
        """
        Set the arbitrary text line width.

        Args:  
            txt_str: str-the text content.

            txt_line_width: float-node text line width.
        
        """
        self.df = editSBML._setTextLineWidth(self.df, txt_str, txt_line_width)
        #return self.df

    def setTextFontSize(self, txt_str, txt_font_size):
        """
        Set the arbitrary text font size.

        Args:  
            txt_str: str-the text content.

            txt_font_size: float-node text font size.
        
        """
        self.df = editSBML._setTextFontSize(self.df, txt_str, txt_font_size)
        #return self.df

    def addText(self, txt_str, txt_position, txt_size, txt_font_color = [0, 0, 0], opacity = 1., 
        txt_line_width = 1., txt_font_size = 12.):
        """
        Add arbitrary text onto canvas.

        Args:  
            txt_str: str-the text content.

            txt_position: list/point.Point()-
                
            list-
            [position_x, position_y], the coordinate represents the top-left hand corner of 
            the text.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the text.

            txt_size: list/point.Point()-
                
            list-
            1*2 matrix-size of the text [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the text.

            txt_font_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            txt_line_width: float-node text line width.

            txt_font_size: float-node text font size.
            
        """
        self.df = editSBML._addText(self.df, txt_str=txt_str, txt_position=txt_position,
        txt_size = txt_size, txt_font_color=txt_font_color, opacity=opacity, txt_line_width=txt_line_width, 
        txt_font_size=txt_font_size) 
        
        #return self.df

    def removeText(self, txt_str):
        """
        Remove the arbitrary text from canvas.

        Args:  
            txt_str: str-the text content.
        """
        self.df = editSBML._removeText(self.df, txt_str=txt_str) 
        
        #return self.df

    def addRectangle(self, shape_name, position, size, fill_color = [255,255,255], fill_opacity = 1., 
        border_color = [0,0,0], border_opacity = 1., border_width = 2.):
        """
        Add a rectangle onto canvas.

        Args:  
            shape_name: str-the name of the rectangle.

            position: list/point.Point()-
                
            list-
            [position_x, position_y], the coordinate represents the top-left hand corner of 
            the rectangle.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the rectangle.

            size: list/point.Point()-
                
            list-
            1*2 matrix-size of the rectangle [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the rectangle.

            fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            fill_opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            border_opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            border_width: float-node text line width.
            
        """
        self.df = editSBML._addRectangle(self.df, shape_name, position, size, fill_color=fill_color, 
        fill_opacity=fill_opacity, border_color=border_color, border_opacity = border_opacity,
        border_width=border_width) 
        
        #return self.df

    def addEllipse(self, shape_name, position, size, fill_color = [255,255,255], fill_opacity = 1., 
        border_color = [0,0,0], border_opacity = 1., border_width = 2.):
        """
        Add an ellipse onto canvas.

        Args:  
            shape_name: str-the name of the ellipse.

            position: list/point.Point()-
                
            list-
            [position_x, position_y], the coordinate represents the top-left hand corner of 
            the ellipse.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the ellipse.

            size: list/point.Point()-
                
            list-
            1*2 matrix-size of the ellipse [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the ellipse.

            fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            fill_opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            border_opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            border_width: float-node text line width.
            
        """
        self.df = editSBML._addEllipse(self.df, shape_name, position, size, fill_color=fill_color, 
        fill_opacity=fill_opacity, border_color=border_color, border_opacity = border_opacity,
        border_width=border_width) 
        
        #return self.df

    def addPolygon(self, shape_name, shape_info, position, size, fill_color = [255,255,255], 
        fill_opacity = 1., border_color = [0,0,0], border_opacity = 1., border_width = 2.):
        """
        Add an ellipse onto canvas.

        Args:  
            shape_name: str-the name of the polygon.

            shape_info: list-[[x1,y1],[x2,y2],[x3,y3],etc], where x,y are floating numbers from 0 to 100.
            x represents the percentage of width, and y represents the percentage of height.

            position: list/point.Point()-
                
            list-
            [position_x, position_y], the coordinate represents the top-left hand corner of 
            the Polygon.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the polygon.

            size: list/point.Point()-
                
            list-
            1*2 matrix-size of the polygon [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the Polygon.

            fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            fill_opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            border_opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            border_width: float-node text line width.
            
        """
        self.df = editSBML._addPolygon(self.df, shape_name, shape_info, position, size, fill_color=fill_color, 
        fill_opacity=fill_opacity, border_color=border_color, border_opacity = border_opacity, 
        border_width=border_width) 
        
        #return self.df

    def removeShape(self, shape_name_str):
        """
        Remove the arbitrary shape from canvas.

        Args:  
            shape_name_str: str-the shape name.
        
        """
        self.df = editSBML._removeShape(self.df, shape_name_str = shape_name_str) 
        
        #return self.df


    def getShapePosition(self, shape_name_str):
        """
        Get the arbitrary shape position with its shape name.

        Args: 
            shape_name_str: str-the shape name of the arbitrary shape.

        Returns:
            position: a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the shape.

        Examples: 
            p = sd.getShapePosition('shape_name')

            print ('x = ', p.x, 'y = ', p.y)

        """

        p = visualizeSBML._getShapePosition(self.df, shape_name_str)
        num_alias = len(p)
        position_list = []
        for alias in range(num_alias):
            position = point.Point (p[alias][0], p[alias][1])
            position_list.append(position)
        if len(position_list) == 1:
            position = position_list[0]
        else:
            raise Exception("This is not a valid id.")
        return position

    def getShapeSize(self, shape_name_str):
        """
        Get the arbitrary shape size with its shape name.

        Args: 
            shape_name_str: str-the shape name.

        Returns:
            shape_size: a Point object with attributes x and y representing
            the width and height of the shape.

        Examples: 
            p = sd.getShapeSize('shape_name')

            print ('Width = ', p.x, 'Height = ', p.y)
        
        """

        p = visualizeSBML._getShapeSize (self.df, shape_name_str)
        num_alias = len(p)
        shape_size_list = []
        for alias in range(num_alias):
            shape_size = point.Point (p[alias][0], p[alias][1])
            shape_size_list.append(shape_size)
        if len(shape_size_list) == 1:
            shape_size = shape_size_list[0]
        else:
            raise Exception("This is not a valid id.")
        return shape_size


    def export(self):
        """
        Generates an SBML string for the current model.

        Returns:
            SBMLStr_layout_render: str-the string of the output sbml file. 
        
        """
        sbml = exportSBML._DFToSBML(self.df)
        return sbml

    def setColorStyle(self, style):
        """
        Set the color style.

        Args:
            style: can be either the "default" string or a new color class
        
        """
        if style == "default":
            self.color_style = styleSBML.Style(style_name="default")
        else:
            self.color_style = style

    def getColorStyle(self):
        """
        Returns an object representing the current color style.

        Returns: 
            The current color style.
        
        Example:
            la.getColorStyle().getStyleName()
        """
        return self.color_style

    def getColorStyleJson(self, filename = None):
        """
        Get the current color style in json format and save to a json file if need be.

        Returns:
            The current color style. in json format
        
        """
        if filename:
            out_file = open(filename, "w")
            json.dump(self.color_style.__dict__, out_file, indent=6)
        return json.dumps(self.color_style.__dict__)


    def autolayout(self, layout="spectral", scale=200, iterations=100):

        """
        Autolayout the node positions using networkX library.

        layout: str-the layout name from networkX, which can be one of the following:

            spectral: positioning the nodes using the eigenvectors of the graph Laplacian;

            spring (default): positioning nodes using Fruchterman-Reingold force-directed algorithm;
        
            random: positioning nodes randomly.
        
            circular: positioning nodes on a circle.

        scale: float-the scaling factor to use
        
        iterations: int-maximum number of iterations to use during the calculation             
        
        """

        sbmlStr = self.export()
        v_info = visualizeSBML._draw(sbmlStr,showImage=False,newStyle=self.color_style)
        edges = v_info.edges
        model = simplesbml.loadSBMLStr(sbmlStr)

        graph = nx.Graph()
        g = defaultdict(list)
        nodes = model.getListOfAllSpecies()
        reaction_ids = model.getListOfReactionIds()

        width, height = self.color_style.getImageSize()
        if scale == None:
            scale = max(width, height) // 2
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
            pos = nx.spring_layout(graph, scale=scale, center=center, k=1, iterations=iterations)
        elif layout == "random":
            pos = nx.random_layout(graph, center=center)
        elif layout == "circular":
            pos = nx.circular_layout(graph, scale=scale, center=center)
        else:
            raise Exception("no such layout")

        for n, p in pos.items():
            if layout == "random":
                p *= scale
            p = p.tolist()
            self.setNodeAndTextPosition(n, p)

        for id in reaction_ids:
            self.setReactionDefaultCenterAndHandlePositions(id)


    def draw(self, setImageSize = '', scale = 1., output_fileName = '', 
        reactionLineType = 'bezier', showBezierHandles = False, 
        showReactionIds = False, showReversible = False, longText = 'auto-font'):

        """
        Draw to a PNG/JPG/PDF file.

        Args: 
            setImageSize: list-containing two elements indicating the szie of the image (if bitmap) [width, height].

            scale: float-determines the figure output size = scale * default output size.
            Increasing the scale will make the resolution higher.

            output_fileName: str-filename: '' (default: will not save the file), 
            or eg 'fileName.png'. Allowable extensions include '.png', '.jpg', or 'pdf'.

            reactionLineType: str-type of the reaction line: 'straight' or 'bezier' (default).
            If there is no layout information from the SBML file, all reaction lines will look like
            straight lines even when using 'bezier' curves.

            showBezierHandles: bool-show the Bezier handles (True) or not (False as default).

            showReactionIds: bool-show the reaction ids (True) or not (False as default).

            showReversible: bool-show whether the reaction is reversible (True) or not (False as default).

            longText: str-'auto-font'(default) will automatically decrease the font size to fit the 
            current dimensions of the node; 'ellipsis' will show '....' if the text is too long to fit the node
        
        """

        sbmlStr = self.export()
        visualizeSBML._draw(sbmlStr,  setImageSize = setImageSize, 
        scale = scale, output_fileName = output_fileName, 
        reactionLineType = reactionLineType, showBezierHandles = showBezierHandles, 
        showReactionIds = showReactionIds, showReversible = showReversible, longText = longText,
        newStyle = self.color_style)
        #df_text = self.df_text)

    def getNetworkTopLeftCorner(self):
        """
        Returns the top left-hand corner of the network from the SBML string.

        Returns:   
            position: a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the network.
        Examples:
            p = sd.getNetworkTopLeftConer()
                
            print(p.x, p.y)

        """ 
        sbmlStr = self.export()
        position  = visualizeSBML._getNetworkTopLeftCorner(sbmlStr)
        position = point.Point(position[0],position[1])
        return position

    def getNetworkBottomRightCorner(self):
        """
        Returns the bottom right-hand corner of the network from the SBML string.

        Returns:
            position: a Point object with attributes x and y representing
            the x/y position of the bottom-right hand corner of the network.

        Examples:
            p = sd.getNetworkBottomRightConer()
                
            print(p.x, p.y)
    
        """
        sbmlStr = self.export()
        position  = visualizeSBML._getNetworkBottomRightCorner(sbmlStr)
        position = point.Point(position[0],position[1])
        return position
    
    def getNetworkSize(self):
        """
        Returns the size of the network.

        Returns:
            size: a Point object with attributes x and y representing
            the width and height of the network.
        
        Examples: 
            p = sd.getNetworkSize()
            
            print ('Width = ', p.x, 'Height = ', p.y)

        """ 
        sbmlStr = self.export()
        size  = visualizeSBML._getNetworkSize(sbmlStr)
        size = point.Point(size[0],size[1])
        return size

    def getCompartmentIdList(self):
        """
        Returns the list of compartment ids.

        Args:  

        Returns:
            id_list-list of ids.
            
            id-str-compartment id.
        
        """ 

        id_list = self.df[0]["id"].tolist()
        return id_list

    def getNodeIdList(self):
        """
        Returns the list of node ids.

        Returns:
            id_list-list of ids.
            
            id-str-node id.
        
        """ 

        id_list = self.df[1]["id"].tolist()
        return id_list

    def getReactionIdList(self):
        """
        Returns the list of reaction ids.

        Returns:
            id_list-list of ids.
            
            id-str-reaction id.
        
        """ 

        id_list = self.df[2]["id"].tolist()
        return id_list

    def getTextContentList(self):
        """
        Returns a list of free-floating text objects.

        Returns:
            txt_content_list-list of txt_content.
            
            txt_content-str-arbitrary text content.
        
        """ 

        txt_content_list = self.df[3]["txt_content"].tolist()
        return txt_content_list

    def getShapeNameList(self):
        """
        Returns a list of possible shape names.

        Returns:
            shape_name_list-list of shape_name.
            
            shape_name-str-arbitrary shape name.
        
        """ 

        shape_name_list = self.df[4]["shape_name"].tolist()
        return shape_name_list

    def hasLayout(self):
        """
        Teturns True if the current SBML model has layout/redner information.

        Returns:
            flag: bool-true (there is layout) or false (there is no layout). 
        """

        flag = True
        sbmlStr = self.sbmlstr
        document = libsbml.readSBMLFromString(sbmlStr)
        if document.getNumErrors() != 0:
            errMsgRead = document.getErrorLog().toString()
            raise Exception("Errors in SBML Model: ", errMsgRead)
        model_layout = document.getModel()
        try:
            mplugin = model_layout.getPlugin("layout")
            layout = mplugin.getLayout(0)
            if layout == None:
                flag = False
        except:
            flag = False

        return flag
  

if __name__ == '__main__':
    DIR = os.path.dirname(os.path.abspath(__file__))
    TEST_FOLDER = os.path.join(DIR, "test_sbml_files")

    filename = "test.xml" 
    #filename = "feedback.xml"
    #filename = "LinearChain.xml"
    #filename = "test_comp.xml"
    #filename = "test_no_comp.xml"
    #filename = "test_modifier.xml"
    #filename = "node_grid.xml"
    #filename = "mass_action_rxn.xml"

    #filename = "Jana_WolfGlycolysis.xml"
    #filename = "Jana_WolfGlycolysis-original.xml" 
    #filename = "output.xml"
    #filename = "Sauro1.xml"
    #filename = "test_textGlyph.xml"
    #node shape:
    #filename = "rectangle.xml"
    #filename = "triangle.xml"
    #filename = "ellipse.xml"
    #filename = "line.xml"
    #filename = "hexagon.xml"
    #SBGN:
    #filename = "SBGN1-specComplex.xml"
    #filename = "SBGN2-modifier.xml"
    #filename = "test_genGlyph.xml"
    #gradient:
    # filename = "test_gradientLinear.xml"
    #filename = "test_gradientRadial.xml"

    #filename = "testbigmodel.xml" #sbml with errors

    #filename = "Sauro_test_sbml_files/branch1-1.xml"
    #filename = "Sauro_test_sbml_files/cycle1-1.xml"
    #filename = "Sauro_test_sbml_files/cycle2-1.xml"
    #filename = "Sauro_test_sbml_files/linearchain.xml"

    #filename = "Coyote/branch1.xml"
    #filename = "Coyote/branch2.xml"
    #filename = "Coyote/cycle1.xml"
    #filename = "Coyote/test.xml"

    #filename = "putida_sbml.xml"
    #filename = "putida_gb_newgenes.xml"

    #filename = "bart2.xml"
    #filename = "bart_arccenter.xml"
    #filename = "bart_spRefBezier.xml"
    #filename = "newSBML.xml"
    #filename = "output.xml"
    #filename = "Coyote.xml"
    #filename = "newSBML2.xml"
    #filename = "coyote2.xml"

    #filename = "BIOMD0000000006.xml"
    #filename = "nodes.xml"
    #filename = "test_arrows.xml"

    f = open(os.path.join(TEST_FOLDER, filename), 'r')
    sbmlStr = f.read()
    f.close()


    # df_excel = _SBMLToDF(sbmlStr)
    # writer = pd.ExcelWriter('output.xlsx')
    # df_excel[0].to_excel(writer, sheet_name='CompartmentData')
    # df_excel[1].to_excel(writer, sheet_name='NodeData')
    # df_excel[2].to_excel(writer, sheet_name='ReactionData')
    # df_excel[3].to_excel(writer, sheet_name='ArbitraryTextData')
    # #df_excel[4].to_excel(writer, sheet_name='ArbitraryShapeData')
    # try:
    #     df_excel[4].to_excel(writer, sheet_name='ArbitraryShapeData')
    # except:
    #     print("did not return shapeData")
    # writer.save()

    df = load(sbmlStr)
    #df = load(os.path.join(TEST_FOLDER, filename))
    #df = load("dfgdg")
    #la = load(sbmlStr)

    # print(df.getCompartmentPosition("_compartment_default_"))
    # print(df.getCompartmentSize("_compartment_default_"))
    # print(df.getCompartmentFillColor("_compartment_default_"))
    # print(df.getCompartmentBorderColor("_compartment_default_"))
    # print(df.getCompartmentBorderWidth("_compartment_default_"))

    # print(df.isFloatingNode("x_1"))
    # position = df.getNodePosition("x_1")[0]
    # print(type(position) == type(point.Point()))
    # print(df.getNodePosition("x_0")[0])
    # print(df.getNodeSize("x_0")[0])
    # print(df.getNodeCenter("x_0")[0])
    # print(df.getNodeShape("x_0"))
    #print(df.getNodeTextPosition("x_0")[0])
    # print(df.getNodeTextSize("x_0"))
    # print(df.getNodeFillColor("Species_1"))
    # print(df.getNodeBorderColor("x_1"))
    # print(df.getNodeBorderWidth("x_1"))
    # print(df.getNodeTextFontColor("x_1"))
    # print(df.getNodeTextLineWidth("x_1"))
    # print(df.getNodeTextFontSize("x_1"))

    # print("center_position:", df.getReactionCenterPosition("r_0"))
    # print("handle_position:", df.getReactionBezierHandles("r_0"))
    # print(df.getReactionFillColor("r_0"))
    # print(df.getReactionLineThickness("r_0"))
    # print(df._isBezierReactionType("r_0"))
    # print(df.getReactionArrowHeadSize("r_0"))
    # print(df.getReactionDash("r_0"))

    # df.setCompartmentPosition('_compartment_default_', [0,0])
    # df.setCompartmentSize('_compartment_default_', [1000, 1000])
    # df.setCompartmentFillColor('_compartment_default_', [255, 255, 255])
    # df.setCompartmentFillColor('_compartment_default_', 'ForestGreen')
    # df.setCompartmentFillColor('_compartment_default_', "#ff3456")
    # df.setCompartmentFillColor('_compartment_default_', "ForestGreen")
    # df.setCompartmentFillColor('c_0', 'coral')
    # print(df.getCompartmentFillColor('c_0'))
    # print(df.getCompartmentFillColor('_compartment_default_'))
    # df.setCompartmentBorderColor('_compartment_default_', [255, 255, 255])
    # df.setCompartmentBorderWidth('_compartment_default_', 2.)

    # df.getNodeAliasNum("ATP")
    # df.setFloatingBoundaryNode("x_1", True)
    # df.setNodePosition("x_0", [100.0, 100.0])
    # df.setNodePosition("x_0", point.Point(100, 100))
    # df.setNodeTextPosition("x_3", [568.0, 229.0])
    # df.setNodeSize("x_1", [50.0, 30.0])
    # print(df.getNodeShape("x_0"))
    # df.setNodeShape("x_0",0)
    # df.setNodeShape("x_0","downTriangle")
    # df.setNodeArbitraryPolygonShape("x_0","self_triangle",[[0,0],[100,0],[0,100]])
    # df.setNodeShape("x_0","ellipse")
    # print(df.getNodeShape("x_0"))
    # df.setNodeTextPosition("x_1", [413., 216.])
    #df.moveNodeTextPosition("x_0", point.Point(0,0))
    #df.setNodeTextPositionCenter("x_0")
    #df.setNodeTextPositionLeftCenter("x_0")
    #df.setNodeTextPositionRightCenter("x_0")
    #df.setNodeTextPositionUpperCenter("x_0")
    #df.setNodeTextPositionLowerCenter("x_0")
    #df.setNodeTextPositionUpperLeft("x_0")
    #df.setNodeTextPositionUpperRight("x_0")
    #df.setNodeTextPositionLowerLeft("x_0")
    #df.setNodeTextPositionLowerRight("x_0")
    #df.setNodeTextPosition("x_0", [160., 107.])
    #print(df.getNodeTextPosition("x_0")[0])
    # df.setNodeTextSize("x_1", [100, 100])
    # df.setNodeFillColor("x_1", [255, 204, 153], opacity = 0.)
    #df.setNodeFillLinearGradient("Species_1", [[0.0, 0.0], [100.0, 100.0]], [[0.0, [255, 255, 255, 255]], [100.0, [192, 192, 192, 255]]])
    # df.setNodeFillRadialGradient("Species_1", [[50.0, 50.0], [50.]], [[0.0, [255, 255, 255, 255]], [100.0, [0, 0, 0, 255]]])
    # print(df.getNodeFillColor("Species_1"))
    # df.setNodeBorderColor("x_1", [255, 108, 9])
    # print(df.getNodeBorderWidth("x_1"))
    # df.setNodeBorderWidth("x_0", 0.)
    # print(df.getNodeBorderWidth("x_1"))
    # df.setNodeTextFontColor("x_1", [0, 0, 0])
    # df.setNodeTextLineWidth("x_1", 1.)
    # print(df.getNodeTextFontSize("x_5"))
    # df.setNodeTextFontSize("x_5", 10)

    # df.setReactionFillColor("r_0", [91, 176, 253])
    # df.setReactionFillColor("r_0", [0, 0, 0])
    # df.setReactionLineThickness("r_0", 3.)
    # df._setBezierReactionType("r_0", True)
    # print(df.getReactionCenterPosition("r_0"))
    # print(df.getReactionCenterPosition("r_1"))
    # df.setReactionCenterPosition("r_0", [449.0, 200.0])
    # df.setReactionCenterPosition("r_1", [449.0, 278.0])
    # df.setReactionCenterPosition("r_0", [334.0, 232.0])
    # df.setReactionStraightLine("J1")
    # df.setReactionBezierHandles("r_0", [[334.0, 232.0], [386.0, 231.0], [282.0, 231.0]])
    # df.setReactionBezierHandles("r_0", [point.Point(334.0, 232.0), 
    # point.Point(386.0, 231.0), point.Point(282.0, 231.0)])
    #df.setReactionDefaultCenterAndHandlePositions("r_0")
    # df.setReactionArrowHeadSize("r_0", [50., 50.])
    # df.setReactionDash("r_0", [6,6])

    # df.addText("test", [413,216], [50,30])
    # df.addText("test1", [400,200], [100, 100], txt_font_color="blue", 
    # opacity= 0.5, txt_line_width=2, txt_font_size=13)
    # df.removeText("test")
    # print(df.getTextPosition("text_content1"))
    # print(df.getTextSize("text_content1"))
    # print(df.getTextFontColor("text_content1"))
    # print(df.getTextLineWidth("text_content2"))
    # print(df.getTextFontSize("text_content2"))
    # df.setTextPosition("text_content1", [413., 216.])
    # df.setTextSize("text_content1", [100, 100])
    # df.setTextFontColor("text_content1", "red")
    # df.setTextLineWidth("text_content2", 3.)
    # df.setTextFontSize("text_content2", 15)

    #df.addRectangle("selfRectangle", [400,200], [100, 100])
    #df.addEllipse("selfEllipse", [400,200], [70, 100], fill_color = "red", fill_opacity = 0.5, 
    #border_color="blue", border_width = 3.)
    #df.addPolygon("self_triangle", [[0,0],[100,0],[0,100]], [400,200], [70, 100])
    #df.removeShape("shape_name")

    # print("NetworkSize:", df.getNetworkSize())
    # print("NetworkBottomRight:", df.getNetworkBottomRightCorner())
    # print("NetworkTopLeft", df.getNetworkTopLeftCorner())

    # print(df.getNodeIdList())
    # print(df.getReactionIdList())
    # print(df.getTextContentList())
    # print(df.getCompartmentIdList())

    # print(df.hasLayout())

    # sbmlStr_layout_render = df.export()

    # f = open("output.xml", "w")
    # f.write(sbmlStr_layout_render)
    # f.close()

    # df.draw(reactionLineType='bezier', scale = 2.)
    df.draw(output_fileName = 'output.png')

