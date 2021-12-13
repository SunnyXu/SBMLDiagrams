# -*- coding: utf-8 -*-
# This script was written by Jin Xu and available on Github
# https://github.com/SunnyXu/SBMLDiagrams

"""
Created on Mon Aug 23 13:25:34 2021
@author: Jin Xu
"""

from numpy.core.fromnumeric import shape
from SBMLDiagrams.importSBML import *
from SBMLDiagrams.exportSBML import *
import pandas as pd
import os

def setCompartment(df_CompartmentData, idx, \
    position = '', size = '', fill_color = '', border_color = '', border_width = ''):

    """
    Set the dataFrame of compartmentData 

    Args:  
        df_CompartmentData: DataFrame-Compartment initial information.

        idx: int-compartment index.

        position: list-1*2 matrix-leftup corner of the rectangle [position_x, position_y].

        size: list-1*2 matrix-size of the rectangle [width, height].

        fill_color: list-rgb 1*3 matrix-compartment fill color.

        border_color: list-rgb 1*3 matrix-compartment border color.

        border_width: float-compartment border line width.

    Returns:
        df_CompartmentData_temp: DataFrame-Compartment information after updates. 
    
    """
    df_CompartmentData_temp = df_CompartmentData.copy()
    if position == '':
        position = df_CompartmentData.iloc[idx]["position"]
    if size == '':
        size = df_CompartmentData.iloc[idx]["size"]
    if fill_color == '':
        fill_color = df_CompartmentData.iloc[idx]["fill_color"]
    if border_color == '':
        border_color = df_CompartmentData.iloc[idx]["border_color"]
    if border_width == '':
        border_width = df_CompartmentData.iloc[idx]["border_width"]

    df_CompartmentData_temp.at[idx,"position"] = position
    df_CompartmentData_temp.at[idx,"size"] = size
    df_CompartmentData_temp.at[idx,"fill_color"] = fill_color
    df_CompartmentData_temp.at[idx,"border_color"] = border_color
    df_CompartmentData_temp.at[idx,"border_width"] = border_width

    return df_CompartmentData_temp

def setCompartmentPosition(df, idx, position):

    """
    Set the compartment position

    Args:  
        df: DataFrame-initial information.

        idx: int-compartment index.

        position: list-1*2 matrix-leftup corner of the rectangle [position_x, position_y].

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    df_CompartmentData_temp.at[idx,"position"] = position
    df_temp = (df_CompartmentData_temp, df[1], df[2])

    return df_temp

def setCompartmentSize(df, idx, size):

    """
    Set the compartment size

    Args:  
        df: DataFrame-initial information.

        idx: int-compartment index.

        position: list-1*2 matrix-leftup corner of the rectangle [position_x, position_y].

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    df_CompartmentData_temp.at[idx,"size"] = size
    df_temp = (df_CompartmentData_temp, df[1], df[2])

    return df_temp

def setCompartmentFillColor(df, idx, fill_color):

    """
    Set the compartment fill color

    Args:  
        df: DataFrame-initial information.

        idx: int-compartment index.

        fill_color: list-rgb 1*3 matrix-compartment fill color.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    df_CompartmentData_temp.at[idx,"fill_color"] = fill_color
    df_temp = (df_CompartmentData_temp, df[1], df[2])

    return df_temp

def setCompartmentBorderColor(df, idx, boder_color):

    """
    Set the compartment border color

    Args:  
        df: DataFrame-initial information.

        idx: int-compartment index.

        border_color: list-rgb 1*3 matrix-compartment border color.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    df_CompartmentData_temp.at[idx,"border_color"] = boder_color
    df_temp = (df_CompartmentData_temp, df[1], df[2])

    return df_temp

def setCompartmentBorderWidth(df, idx, boder_width):

    """
    Set the compartment border width

    Args:  
        df: DataFrame-initial information.

        idx: int-compartment index.

        border_width: float-compartment border line width.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    df_CompartmentData_temp.at[idx,"border_width"] = boder_width
    df_temp = (df_CompartmentData_temp, df[1], df[2])

    return df_temp

def setNode(df_NodeData, idx, floating_node = '', position = '', size = '', shape_idx = '', \
        txt_position = '', txt_size = '', \
        fill_color = '', border_color = '', border_width = '', \
        txt_font_color = '', txt_line_width = ''):

    """
    Set the dataFrame of NodeData 

    Args:
        df_CompartmentData: DataFrame-Node initial information.
        
        idx: int-compartment index.
        
        floating_node: bool-floating node (True) or not (False).
        
        position: list-1*2 matrix-leftup corner of the rectangle [position_x, position_y].
        
        size: list-1*2 matrix-size of the rectangle [width, height].
        
        shape_idx: int-1:rectangle, 2:circle, 3:hexagon, 4:line, 5:triangle.
        
        txt_position: list-1*2 matrix-leftup corner of the rectangle [position_x, position_y].
        
        txt_size: list-1*2 matrix-size of the rectangle [width, height].
        
        fill_color: list-rgb 1*3 matrix-node fill color.
        
        border_color: list-rgb 1*3 matrix-node border color.
        
        border_width: float-node border line width.
        
        txt_font_color: list-rgb 1*3 matrix-node text font color.
        
        txt_line_width: float-node line width.

    Returns: 
        df_NodeData_temp: DataFrame-Node information after updates. 
    
    """
    df_NodeData_temp = df_NodeData.copy()
    if floating_node == '':
        floating_node = df_NodeData.iloc[idx]["floating_node"]
    if position == '':
        position = df_NodeData.iloc[idx]["position"]
    if size == '':
        size = df_NodeData.iloc[idx]["size"]
    if shape_idx == '':
        shape_idx = df_NodeData.iloc[idx]["shape_idx"]
    if txt_position == '':
        txt_position = df_NodeData.iloc[idx]["txt_position"]
    if txt_size == '':
        txt_size = df_NodeData.iloc[idx]["txt_size"]
    if fill_color == '':
        fill_color = df_NodeData.iloc[idx]["fill_color"]
    if border_color == '':
        border_color = df_NodeData.iloc[idx]["border_color"]
    if border_width == '':
        border_width = df_NodeData.iloc[idx]["border_width"]
    if txt_font_color == '':
        txt_font_color = df_NodeData.iloc[idx]["txt_font_color"]
    if txt_line_width == '':
        txt_line_width = df_NodeData.iloc[idx]["txt_line_width"]

    df_NodeData_temp.at[idx,"floating_node"] = floating_node
    df_NodeData_temp.at[idx,"position"] = position
    df_NodeData_temp.at[idx,"size"] = size
    df_NodeData_temp.at[idx,"shape_idx"] = shape_idx
    df_NodeData_temp.at[idx,"txt_position"] = txt_position
    df_NodeData_temp.at[idx,"txt_size"] = txt_size
    df_NodeData_temp.at[idx,"fill_color"] = fill_color
    df_NodeData_temp.at[idx,"border_color"] = border_color
    df_NodeData_temp.at[idx,"border_width"] = border_width
    df_NodeData_temp.at[idx,"txt_font_color"] = txt_font_color
    df_NodeData_temp.at[idx,"txt_line_width"] = txt_line_width

    return df_NodeData_temp

def setFloatingBoundaryNode(df, idx, floating_node):

    """
    Set a node to be floating node (True) or boundary node (False).

    Args:  
        df: DataFrame-initial information.

        idx: int-node index.

        floating_node: bool-floating node (True) or not (False).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    df_NodeData_temp.at[idx,"floating_node"] = floating_node
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def setNodePosition(df, idx, position):

    """
    Set the node position.

    Args:  
        df: DataFrame-initial information.

        idx: int-node index.

        position: list-1*2 matrix-leftup corner of the rectangle [position_x, position_y].

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    df_NodeData_temp.at[idx,"position"] = position
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def setNodeSize(df, idx, size):

    """
    Set the node size.

    Args:  
        df: DataFrame-initial information.

        idx: int-node index.

        size: list-1*2 matrix-size of the rectangle [width, height].

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    df_NodeData_temp.at[idx,"size"] = size
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def setNodeShapeIdx(df, idx, shape_idx):

    """
    Set the node shape index.

    Args:  
        df: DataFrame-initial information.

        idx: int-node index.

        shape_idx: int-1:rectangle, 2:circle, 3:hexagon, 4:line, 5:triangle.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    df_NodeData_temp.at[idx,"shape_idx"] = shape_idx
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def setNodeTextPosition(df, idx, txt_position):

    """
    Set the node text position.

    Args:  
        df: DataFrame-initial information.

        idx: int-node index.

        txt_position: list-1*2 matrix-leftup corner of the rectangle [position_x, position_y].

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    df_NodeData_temp.at[idx,"txt_position"] = txt_position
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def setNodeTextSize(df, idx, txt_size):

    """
    Set the node text size.

    Args:  
        df: DataFrame-initial information.

        idx: int-node index.

        txt_size: list-1*2 matrix-size of the rectangle [width, height].

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    df_NodeData_temp.at[idx,"txt_size"] = txt_size
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def setNodeFillColor(df, idx, fill_color):

    """
    Set the node fill color.

    Args:  
        df: DataFrame-initial information.

        idx: int-node index.

        fill_color: list-rgb 1*3 matrix-node fill color.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    df_NodeData_temp.at[idx,"fill_color"] = fill_color
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def setNodeBorderColor(df, idx, border_color):

    """
    Set the node border color.

    Args:  
        df: DataFrame-initial information.

        idx: int-node index.

        border_color: list-rgb 1*3 matrix-node border color.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    df_NodeData_temp.at[idx,"border_color"] = border_color
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def setNodeBorderWidth(df, idx, border_width):

    """
    Set the node border width.

    Args:  
        df: DataFrame-initial information.

        idx: int-node index.

        border_width: float-node border line width.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    df_NodeData_temp.at[idx,"border_width"] = border_width
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def setNodeTextFontColor(df, idx, txt_font_color):

    """
    Set the node text font color.

    Args:  
        df: DataFrame-initial information.

        idx: int-node index.

        txt_font_color: list-rgb 1*3 matrix-node text font color.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    df_NodeData_temp.at[idx,"txt_font_color"] = txt_font_color
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def setNodeTextLineWidth(df, idx, txt_line_width):

    """
    Set the node text line width.

    Args:  
        df: DataFrame-initial information.

        idx: int-node index.

        txt_line_width: float-node text line width.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    df_NodeData_temp.at[idx,"txt_line_width"] = txt_line_width
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp


def setReaction(df_ReactionData, idx, \
    fill_color = '', line_thickness = '', bezier = ''):

    """
    Set the dataFrame of ReactionData 

    Args:  
        df_ReactionData: DataFrame-reaction initial information.
        
        idx: int-reaction index.
        
        fill_color: list-rgb 1*3 matrix-reaction fill color.
        
        line_thickness: float-reaction line thickness.
        
        bezier: bool-bezier curve (True) or not (False)

    Returns:
        df_ReactionData_temp: DataFrame-Reaction information after updates. 
    

    """
    df_ReactionData_temp = df_ReactionData.copy()
    if fill_color == '':
        fill_color = df_ReactionData.iloc[idx]["fill_color"]
    if line_thickness == '':
        line_thickness = df_ReactionData.iloc[idx]["line_thickness"]
    if bezier == '':
        bezier = df_ReactionData.iloc[idx]["bezier"]

    df_ReactionData_temp.at[idx,"fill_color"] = fill_color
    df_ReactionData_temp.at[idx,"line_thickness"] = line_thickness
    df_ReactionData_temp.at[idx,"bezier"] = bezier

    return df_ReactionData_temp

def setReactionFillColor(df, idx, fill_color):

    """
    Set the reaction fill color.

    Args:  
        df: DataFrame-initial information.

        idx: int-node index.

        fill_color: list-rgb 1*3 matrix-reaction fill color.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    df_ReactionData_temp.at[idx,"fill_color"] = fill_color
    df_temp = (df[0], df[1], df_ReactionData_temp)
    
    return df_temp

def setReactionLineThickness(df, idx, line_thickness):

    """
    Set the reaction line thickness.

    Args:  
        df: DataFrame-initial information.

        idx: int-node index.

        line_thickness: float-reaction border line width.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    df_ReactionData_temp.at[idx,"line_thickness"] = line_thickness
    df_temp = (df[0], df[1], df_ReactionData_temp)

    return df_temp

def setBezierReactionType(df, idx, bezier):

    """
    Set the reaction line thickness.

    Args:  
        df: DataFrame-initial information.

        idx: int-node index.

        bezier: bool-bezier reaction (True) or not (False)

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    df_ReactionData_temp.at[idx,"bezier"] = bezier
    df_temp = (df[0], df[1], df_ReactionData_temp)

    return df_temp

# if __name__ == '__main__':
#     DIR = os.path.dirname(os.path.abspath(__file__))
#     TEST_FOLDER = os.path.join(DIR, "test_sbml_files")

#     filename = "test.xml" 

#     f = open(os.path.join(TEST_FOLDER, filename), 'r')
#     sbmlStr = f.read()
#     f.close()

#     df = load(sbmlStr)

#     df = setCompartmentPosition(df, 0, [0,0])
#     df = setCompartmentSize(df, 0, [1000, 1000])
#     df = setCompartmentFillColor(df, 0, [255, 255, 255])
#     df = setCompartmentBorderColor(df, 0, [255, 255, 255])
#     df = setCompartmentBorderWidth(df, 0, 1.)

#     df = setFloatingBoundaryNode(df, 0, False)
#     df = setNodePosition(df, 0, [413.0, 216.0])
#     df = setNodeSize(df, 0, [50.0, 30.0])
#     df = setNodeShapeIdx(df, 0, 1)
#     df = setNodeTextPosition(df, 0, [413., 216.])
#     df = setNodeTextSize(df, 0, [50, 30])
#     df = setNodeFillColor(df, 0, [255, 204, 153])
#     df = setNodeBorderColor(df, 0, [255, 108, 9])
#     df = setNodeBorderWidth(df, 0, 2.)
#     df = setNodeTextFontColor(df, 0, [0, 0, 0])
#     df = setNodeTextLineWidth(df, 0, 2.)

#     df = setReactionFillColor(df, 0, [91, 176, 253])
#     df = setReactionLineThickness(df, 0, 3.)
#     df = setBezierReactionType(df, 0, True)

    
#     df_CompartmentData_update = setCompartment(df[0], 0)
#     df_NodeData_update = setNode(df[1], 0, floating_node=False)
#     df_ReactionData_update = setReaction(df[2], 0, bezier = False)
#     df = (df_CompartmentData_update, df_NodeData_update, df_ReactionData_update)
#     sbmlStr_layout_render = export(df)

#     f = open("output.xml", "w")
#     f.write(sbmlStr_layout_render)
#     f.close()
    

