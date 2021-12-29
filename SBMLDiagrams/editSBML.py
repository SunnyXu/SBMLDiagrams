# -*- coding: utf-8 -*-
# This script was written by Jin Xu and available on Github
# https://github.com/SunnyXu/SBMLDiagrams

"""
Created on Mon Aug 23 13:25:34 2021
@author: Jin Xu
"""

from numpy.core.fromnumeric import shape
import pandas as pd
import os

#import the color list from colors.xlsx
DIR = os.path.dirname(os.path.abspath(__file__))
color_xls = pd.ExcelFile(os.path.join(DIR, 'colors.xlsx'))
df_color = pd.read_excel(color_xls, sheet_name = 'colors')
df_color["html_name"] = df_color["html_name"].str.lower()

def _color_to_rgb(color):
    def _hex_to_rgb(value):
        value = value.lstrip('#')
        return [int(value[i:i+2], 16) for i in (0, 2, 4)]

    #rgb
    rgb = []
    if isinstance(color, list) and len(color) == 3:
        rgb = color.copy()
    elif isinstance(color, str):
        if '#' in color: #hex_string
            rgb = _hex_to_rgb(color)
        else: #html_name
            if color.lower() in df_color.values:
                index = df_color.index[df_color["html_name"] == color.lower()].tolist()[0] #row index 
                rgb_pre = df_color.iloc[index]["decimal_rgb"]
                rgb_pre = rgb_pre[1:-1].split(",")
                rgb = [int(x) for x in rgb_pre]
    return rgb


def _setCompartmentPosition(df, id, position):

    """
    Set the compartment position

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        position: list-1*2 matrix-leftup corner of the rectangle [position_x, position_y].

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    idx_list = df[0].index[df[0]["id"] == id].tolist() 
    for i in range(len(idx_list)):
        df_CompartmentData_temp.at[idx_list[i],"position"] = position
    df_temp = (df_CompartmentData_temp, df[1], df[2])

    return df_temp

def _setCompartmentSize(df, id, size):

    """
    Set the compartment size

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        size: list-1*2 matrix-size of the rectangle [width, height].

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()   
    idx_list = df[0].index[df[0]["id"] == id].tolist()  
    for i in range(len(idx_list)):
        df_CompartmentData_temp.at[idx_list[i],"size"] = size
    df_temp = (df_CompartmentData_temp, df[1], df[2])

    return df_temp

def _setCompartmentFillColor(df, id, fill_color):

    """
    Set the compartment fill color

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()      
    idx_list = df[0].index[df[0]["id"] == id].tolist() 
    fill_color = _color_to_rgb(fill_color)
    if fill_color == []:
        raise ValueError('Please enter a color in a valid format!')
    for i in range(len(idx_list)):
        df_CompartmentData_temp.at[idx_list[i],"fill_color"] = fill_color
    df_temp = (df_CompartmentData_temp, df[1], df[2])

    return df_temp

def _setCompartmentBorderColor(df, id, border_color):

    """
    Set the compartment border color

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_CompartmentData_temp = df[0].copy()
    idx_list = df[0].index[df[0]["id"] == id].tolist()  
    border_color = _color_to_rgb(border_color)
    if border_color == []:
        raise ValueError('Please enter a color in a valid format!')
    for i in range(len(idx_list)):
        df_CompartmentData_temp.at[idx_list[i],"border_color"] = border_color
    df_temp = (df_CompartmentData_temp, df[1], df[2])

    return df_temp

def _setCompartmentBorderWidth(df, id, border_width):

    """
    Set the compartment border width

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        border_width: float-compartment border line width.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    idx_list = df[0].index[df[0]["id"] == id].tolist()   
    for i in range(len(idx_list)):
        df_CompartmentData_temp.at[idx_list[i],"border_width"] = border_width  
    df_temp = (df_CompartmentData_temp, df[1], df[2])

    return df_temp

def _setFloatingBoundaryNode(df, id, floating_node):

    """
    Set a node to be floating node (True) or boundary node (False).

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        floating_node: bool-floating node (True) or not (False).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"floating_node"] = floating_node
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setNodePosition(df, id, position):

    """
    Set the node position.

    Args:  
        df: DataFrame-initial information.

        id: id-node id.

        position: list-1*2 matrix-leftup corner of the rectangle [position_x, position_y].

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"position"] = position
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setNodeSize(df, id, size):

    """
    Set the node size.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        size: list-1*2 matrix-size of the rectangle [width, height].

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"size"] = size
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setNodeShapeIdx(df, id, shape_idx):

    """
    Set the node shape index.

    Args:  
        df: DataFrame-initial information.

        id: int-node id.

        shape_idx: int-1:rectangle, 2:circle, 3:hexagon, 4:line, 5:triangle.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"shape_idx"] = shape_idx
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setNodeTextPosition(df, id, txt_position):

    """
    Set the node text position.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        txt_position: list-1*2 matrix-leftup corner of the rectangle [position_x, position_y].

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setNodeTextSize(df, id, txt_size):

    """
    Set the node text size.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        txt_size: list-1*2 matrix-size of the rectangle [width, height].

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"txt_size"] = txt_size
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setNodeFillColor(df, id, fill_color):

    """
    Set the node fill color.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    fill_color = _color_to_rgb(fill_color)
    if fill_color == []:
        raise ValueError('Please enter a color in a valid format!')
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"fill_color"] = fill_color
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setNodeBorderColor(df, id, border_color):

    """
    Set the node border color.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    border_color = _color_to_rgb(border_color)
    if border_color == []:
        raise ValueError('Please enter a color in a valid format!')
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"border_color"] = border_color
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setNodeBorderWidth(df, id, border_width):

    """
    Set the node border width.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        border_width: float-node border line width.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"border_width"] = border_width
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setNodeTextFontColor(df, id, txt_font_color):

    """
    Set the node text font color.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        txt_font_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    txt_font_color = _color_to_rgb(txt_font_color)
    if txt_font_color == []:
        raise ValueError('Please enter a color in a valid format!')
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"txt_font_color"] = txt_font_color
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setNodeTextLineWidth(df, id, txt_line_width):

    """
    Set the node text line width.

    Args:  
        df: DataFrame-initial information.

        id: id-node id.

        txt_line_width: float-node text line width.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"txt_line_width"] = txt_line_width
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setReactionFillColor(df, id, fill_color):

    """
    Set the reaction fill color.

    Args:  
        df: DataFrame-initial information.

        id: str-reaction id.

        fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    fill_color = _color_to_rgb(fill_color)
    if fill_color == []:
        raise ValueError('Please enter a color in a valid format!')
    for i in range(len(idx_list)):
        df_ReactionData_temp.at[idx_list[i],"fill_color"] = fill_color
    df_temp = (df[0], df[1], df_ReactionData_temp)
    
    return df_temp

def _setReactionLineThickness(df, id, line_thickness):

    """
    Set the reaction line thickness.

    Args:  
        df: DataFrame-initial information.

        id: str-reaction id.

        line_thickness: float-reaction border line width.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    for i in range(len(idx_list)):
        df_ReactionData_temp.at[idx_list[i],"line_thickness"] = line_thickness
    df_temp = (df[0], df[1], df_ReactionData_temp)

    return df_temp

def _setBezierReactionType(df, id, bezier):

    """
    Set the reaction line thickness.

    Args:  
        df: DataFrame-initial information.

        id: str-reaction id.

        bezier: bool-bezier reaction (True) or not (False)

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    for i in range(len(idx_list)):
        df_ReactionData_temp.at[idx_list[i],"bezier"] = bezier
    df_temp = (df[0], df[1], df_ReactionData_temp)

    return df_temp

