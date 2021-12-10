# -*- coding: utf-8 -*-
# This script was written by Jin Xu and available on Github
# https://github.com/SunnyXu/SBMLDiagrams


from numpy.core.fromnumeric import shape
from SBMLDiagrams import importSBML
from SBMLDiagrams import exportSBML
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

        border_color: list- rgb 1*3 matrix-compartment border color.

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
        
        txt_position: 1*2 matrix-leftup corner of the rectangle [position_x, position_y].
        
        txt_size: 1*2 matrix-size of the rectangle [width, height].
        
        fill_color: list-rgb 1*3 matrix-compartment fill color.
        
        border_color: list-rgb 1*3 matrix-compartment border color.
        
        border_width: float-compartment border line width.
        
        txt_font_color: list-rgb 1*3 matrix-compartment border color.
        
        txt_line_width: float-compartment border line width.

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

def setReaction(df_ReactionData, idx, \
    fill_color = '', line_thickness = '', bezier = ''):

    """
    Set the dataFrame of ReactionData 

    Args:  
        df_ReactionData: DataFrame-Compartment initial information.
        
        idx: int-reaction index.
        
        fill_color: list-rgb 1*3 matrix-compartment fill color.
        
        line_thickness: float-compartment border line width.
        
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

if __name__ == '__main__':
#     DIR = os.path.dirname(os.path.abspath(__file__))
#     TEST_FOLDER = os.path.join(DIR, "test_sbml_files")

#     filename = "test.xml" 

#     f = open(os.path.join(TEST_FOLDER, filename), 'r')
#     sbmlStr = f.read()
#     f.close()

#     (df_CompartmentData, df_NodeData, df_ReactionData) = importSBML.load(sbmlStr)
#     df_CompartmentData_update = setCompartment(df_CompartmentData, 0)
#     df_NodeData_update = setNode(df_NodeData, 0, floating_node=False)
#     df_ReactionData_update = setReaction(df_ReactionData, 0, bezier = False)
#     sbmlStr_layout_render = exportSBML.export(df_CompartmentData_update, df_NodeData_update, df_ReactionData_update)

#     f = open("output.xml", "w")
#     f.write(sbmlStr_layout_render)
#     f.close()
    

