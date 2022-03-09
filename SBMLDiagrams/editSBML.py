# -*- coding: utf-8 -*-
# This script was written by Jin Xu and available on Github
# https://github.com/SunnyXu/SBMLDiagrams

"""
Created on Mon Aug 23 13:25:34 2021
@author: Jin Xu
"""

#from numpy.core.fromnumeric import shape
import pandas as pd
import os
from SBMLDiagrams import processSBML

color_data = {"decimal_rgb": ['[240,248,255]', '[250,235,215]', '[0,255,255]', '[127,255,212]', '[240,255,255]', '[245,245,220]', '[255,228,196]', '[0,0,0]', '[255,235,205]', '[0,0,255]', '[138,43,226]', '[165,42,42]', '[222,184,135]', '[95,158,160]', '[127,255,0]', '[210,105,30]', '[255,127,80]', '[100,149,237]', '[255,248,220]', '[220,20,60]', '[0,255,255]', '[0,0,139]', '[0,139,139]', '[184,134,11]', '[169,169,169]', '[0,100,0]', '[189,183,107]', '[139,0,139]', '[85,107,47]', '[255,140,0]', '[153,50,204]', '[139,0,0]', '[233,150,122]', '[143,188,143]', '[72,61,139]', '[47,79,79]', '[0,206,209]', '[148,0,211]', '[255,20,147]', '[0,191,255]', '[105,105,105]', '[30,144,255]', '[178,34,34]', '[255,250,240]', '[34,139,34]', '[255,0,255]', '[220,220,220]', '[248,248,255]', '[255,215,0]', '[218,165,32]', '[128,128,128]', '[0,128,0]', '[173,255,47]', '[240,255,240]', '[255,105,180]', '[205,92,92]', '[75,0,130]', '[255,255,240]', '[240,230,140]', '[230,230,250]', '[255,240,245]', '[124,252,0]', '[255,250,205]', '[173,216,230]', '[240,128,128]', '[224,255,255]', '[250,250,210]', '[144,238,144]', '[211,211,211]', '[255,182,193]', '[255,160,122]', '[32,178,170]', '[135,206,250]', '[119,136,153]', '[176,196,222]', '[255,255,224]', '[0,255,0]', '[50,205,50]', '[250,240,230]', '[255,0,255]', '[128,0,0]', '[102,205,170]', '[0,0,205]', '[186,85,211]', '[147,112,219]', '[60,179,113]', '[123,104,238]', '[0,250,154]', '[72,209,204]', '[199,21,133]', '[25,25,112]', '[245,255,250]', '[255,228,225]', '[255,228,181]', '[255,222,173]', '[0,0,128]', '[253,245,230]', '[128,128,0]', '[107,142,35]', '[255,165,0]', '[255,69,0]', '[218,112,214]', '[238,232,170]', '[152,251,152]', '[175,238,238]', '[219,112,147]', '[255,239,213]', '[255,218,185]', '[205,133,63]', '[255,192,203]', '[221,160,221]', '[176,224,230]', '[128,0,128]', '[255,0,0]', '[188,143,143]', '[65,105,225]', '[139,69,19]', '[250,128,114]', '[244,164,96]', '[46,139,87]', '[255,245,238]', '[160,82,45]', '[192,192,192]', '[135,206,235]', '[106,90,205]', '[112,128,144]', '[255,250,250]', '[0,255,127]', '[70,130,180]', '[210,180,140]', '[0,128,128]', '[216,191,216]', '[255,99,71]', '[64,224,208]', '[238,130,238]', '[245,222,179]', '[255,255,255]', '[245,245,245]', '[255,255,0]', '[154,205,50]'],\
    "html_name":['AliceBlue', 'AntiqueWhite', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque', 'Black', 'BlanchedAlmond', 'Blue', 'BlueViolet', 'Brown', 'BurlyWood', 'CadetBlue', 'Chartreuse', 'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan', 'DarkBlue', 'DarkCyan', 'DarkGoldenrod', 'DarkGray', 'DarkGreen', 'DarkKhaki', 'DarkMagenta', 'DarkOliveGreen', 'DarkOrange', 'DarkOrchid', 'DarkRed', 'DarkSalmon', 'DarkSeaGreen', 'DarkSlateBlue', 'DarkSlateGray', 'DarkTurquoise', 'DarkViolet', 'DeepPink', 'DeepSkyBlue', 'DimGray', 'DodgerBlue', 'FireBrick', 'FloralWhite', 'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'Goldenrod', 'Gray', 'Green', 'GreenYellow', 'Honeydew', 'HotPink', 'IndianRed', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue', 'LightCoral', 'LightCyan', 'LightGoldenrodYellow', 'LightGreen', 'LightGrey', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue', 'LightSlateGray', 'LightSteelBlue', 'LightYellow', 'Lime', 'LimeGreen', 'Linen', 'Magenta', 'Maroon', 'MediumAquamarine', 'MediumBlue', 'MediumOrchid', 'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen', 'MediumTurquoise', 'MediumVioletRed', 'MidnightBlue', 'MintCream', 'MistyRose', 'Moccasin', 'NavajoWhite', 'Navy', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed', 'Orchid', 'PaleGoldenrod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed', 'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple', 'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Salmon', 'SandyBrown', 'SeaGreen', 'Seashell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue', 'SlateGray', 'Snow', 'SpringGreen', 'SteelBlue', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White', 'WhiteSmoke', 'Yellow', 'YellowGreen'],\
    "hex_string":['#F0F8FF', '#FAEBD7', '#00FFFF', '#7FFFD4', '#F0FFFF', '#F5F5DC', '#FFE4C4', '#000000', '#FFEBCD', '#0000FF', '#8A2BE2', '#A52A2A', '#DEB887', '#5F9EA0', '#7FFF00', '#D2691E', '#FF7F50', '#6495ED', '#FFF8DC', '#DC143C', '#00FFFF', '#00008B', '#008B8B', '#B8860B', '#A9A9A9', '#006400', '#BDB76B', '#8B008B', '#556B2F', '#FF8C00', '#9932CC', '#8B0000', '#E9967A', '#8FBC8F', '#483D8B', '#2F4F4F', '#00CED1', '#9400D3', '#FF1493', '#00BFFF', '#696969', '#1E90FF', '#B22222', '#FFFAF0', '#228B22', '#FF00FF', '#DCDCDC', '#F8F8FF', '#FFD700', '#DAA520', '#808080', '#008000', '#ADFF2F', '#F0FFF0', '#FF69B4', '#CD5C5C', '#4B0082', '#FFFFF0', '#F0E68C', '#E6E6FA', '#FFF0F5', '#7CFC00', '#FFFACD', '#ADD8E6', '#F08080', '#E0FFFF', '#FAFAD2', '#90EE90', '#D3D3D3', '#FFB6C1', '#FFA07A', '#20B2AA', '#87CEFA', '#778899', '#B0C4DE', '#FFFFE0', '#00FF00', '#32CD32', '#FAF0E6', '#FF00FF', '#800000', '#66CDAA', '#0000CD', '#BA55D3', '#9370DB', '#3CB371', '#7B68EE', '#00FA9A', '#48D1CC', '#C71585', '#191970', '#F5FFFA', '#FFE4E1', '#FFE4B5', '#FFDEAD', '#000080', '#FDF5E6', '#808000', '#6B8E23', '#FFA500', '#FF4500', '#DA70D6', '#EEE8AA', '#98FB98', '#AFEEEE', '#DB7093', '#FFEFD5', '#FFDAB9', '#CD853F', '#FFC0CB', '#DDA0DD', '#B0E0E6', '#800080', '#FF0000', '#BC8F8F', '#4169E1', '#8B4513', '#FA8072', '#F4A460', '#2E8B57', '#FFF5EE', '#A0522D', '#C0C0C0', '#87CEEB', '#6A5ACD', '#708090', '#FFFAFA', '#00FF7F', '#4682B4', '#D2B48C', '#008080', '#D8BFD8', '#FF6347', '#40E0D0', '#EE82EE', '#F5DEB3', '#FFFFFF', '#F5F5F5', '#FFFF00', '#9ACD32']}
df_color = pd.DataFrame(color_data)
#DIR = os.path.dirname(os.path.abspath(__file__))
#df_color = pd.read_csv(os.path.join(DIR, 'colors.txt'), sep="\t")
df_color["html_name"] = df_color["html_name"].str.lower()

def _color_to_rgb(color, opacity):
    def _hex_to_rgb(value):
        value = value.lstrip('#')
        return [int(value[i:i+2], 16) for i in (0, 2, 4)]

    #rgba
    rgb = []
    if isinstance(color, list) and len(color) == 3:
        rgb = color.copy()
    elif isinstance(color, str):
        if '#' in color and len(color) == 7: #hex_string
            rgb = _hex_to_rgb(color)
        else: #html_name
            if color.lower() in df_color.values:
                index = df_color.index[df_color["html_name"] == color.lower()].tolist()[0] #row index 
                rgb_pre = df_color.iloc[index]["decimal_rgb"]
                rgb_pre = rgb_pre[1:-1].split(",")
                rgb = [int(x) for x in rgb_pre]

    if rgb == [] or opacity > 1. or opacity < 0.:
        raise ValueError('Please enter a color or/and opacity in a valid format!')
    else:
        rgba = rgb.copy()
        rgba.append(int(opacity*255/1.))
    return rgba

def _setCompartmentPosition(df, id, position):

    """
    Set the x,y coordinates of the compartment position.

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        position: [position_x, position_y], the coordinate represents the top-left hand corner of 
        the compartment.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    idx_list = df[0].index[df[0]["id"] == id].tolist() 
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_CompartmentData_temp.at[idx_list[i],"position"] = position
    df_temp = (df_CompartmentData_temp, df[1], df[2])

    return df_temp

def _setCompartmentSize(df, id, size):

    """
    Set the compartment size.

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        size: list-1*2 matrix-size of the rectangle [width, height].

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()   
    idx_list = df[0].index[df[0]["id"] == id].tolist() 
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.") 
    for i in range(len(idx_list)):
        df_CompartmentData_temp.at[idx_list[i],"size"] = size
    df_temp = (df_CompartmentData_temp, df[1], df[2])

    return df_temp

def _setCompartmentFillColor(df, id, fill_color, opacity):

    """
    Set the compartment fill color

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()      
    idx_list = df[0].index[df[0]["id"] == id].tolist() 
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    fill_color = _color_to_rgb(fill_color, opacity)
    for i in range(len(idx_list)):
        df_CompartmentData_temp.at[idx_list[i],"fill_color"] = fill_color
    df_temp = (df_CompartmentData_temp, df[1], df[2])

    return df_temp

def _setCompartmentBorderColor(df, id, border_color, opacity):

    """
    Set the compartment border color.

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_CompartmentData_temp = df[0].copy()
    idx_list = df[0].index[df[0]["id"] == id].tolist() 
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    border_color = _color_to_rgb(border_color, opacity)
    for i in range(len(idx_list)):
        df_CompartmentData_temp.at[idx_list[i],"border_color"] = border_color
    df_temp = (df_CompartmentData_temp, df[1], df[2])

    return df_temp

def _setCompartmentBorderWidth(df, id, border_width):

    """
    Set the compartment border width.

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        border_width: float-compartment border line width.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    idx_list = df[0].index[df[0]["id"] == id].tolist() 
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")  
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
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"floating_node"] = floating_node
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setNodePosition(df, id, position):

    """
    Set the x,y coordinates of the node position.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        position: list-[position_x, position_y], the coordinate represents the top-left hand corner of the node. 

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
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
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"size"] = size
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setNodeShape(df, id, shape):

    """
    Set the node shape by shape index or name string.

    Args:  
        df: DataFrame-initial information.

        id: int-node id.

        shape: int/str-
        int-0:text_only, 1:rectangle, 2:circle, 3:hexagon, 4:line, or 5:triangle;
            6:upTriangle, 7:downTriangle, 8:leftTriangle, 9: rightTriangle.
        str-"text_only", "rectangle", "circle", "hexagon", "line", or "triangle";
            "upTriangle", "downTriangle", "leftTriangle", "rightTriangle".
            
    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    shape_idx = -1 #undefined shape
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    shape_info = []
    shape_type = ''
    if isinstance(shape, str):
        shape_name = shape
        if shape == 'text_only':
            shape_idx = 0
        elif shape == 'rectangle':
            shape_idx = 1
            shape_type = 'rectangle'
        elif shape == 'circle':
            shape_idx = 2
            shape_type = 'ellipse'
            shape_info = [[[50.0, 50.0], [100.0, 100.0]]]
        elif shape == 'hexagon':
            shape_idx = 3
            shape_type = 'polygon'
            shape_info = [[100.0, 50.0], [75.0, 7.0], [25.0, 7.0], [0.0, 50.0], [25.0, 86.0], [75.0, 86.0]]
        elif shape == "line":
            shape_idx = 4
            shape_type = 'polygon'
            shape_info = [[0.0, 50.0], [100.0, 50.0]]
        elif shape == "triangle":
            shape_idx = 5
            shape_type = 'polygon'
            shape_info = [[100.0, 50.0], [25.0, 7.0], [25.0, 86.0]]
        elif shape == "upTriangle":
            shape_idx = 6
            shape_type = 'polygon'
            shape_info = [[50.0, 0.0], [100.0, 80.6], [0.0, 80.6]]
        elif shape == "downTriangle":
            shape_idx = 7
            shape_type = 'polygon'
            shape_info = [[0.0, 0.0], [100.0, 0.0], [50.0, 80.6]]
        elif shape == "leftTriangle":
            shape_idx = 8
            shape_type = 'polygon'
            shape_info = [[80.6, 0.0], [80.6, 100.0], [0.0, 50.0]]
        elif shape == "rightTriangle":
            shape_idx = 9
            shape_type = 'polygon'
            shape_info = [[0.0, 0.0], [80.6, 50.0], [0.0, 100.0]]
        else:
            raise Exception("This is not a valid node shape information.")
    elif isinstance(shape, int):
        if 0 <= shape <= 9:
            shape_idx = shape
            if shape == 0:
                shape_name = 'text_only'
            elif shape == 1:
                shape_name = 'rectangle'
                shape_type = 'rectangle'
            elif shape == 2:
                shape_name = 'circle'
                shape_type = 'ellipse'
                shape_info = [[[50.0, 50.0], [100.0, 100.0]]]
            elif shape == 3:
                shape_name = 'hexagon'
                shape_type = 'polygon'
                shape_info = [[100.0, 50.0], [75.0, 7.0], [25.0, 7.0], [0.0, 50.0], [25.0, 86.0], [75.0, 86.0]]
            elif shape == 4:
                shape_name = 'line'
                shape_type = 'polygon'
                shape_info = [[0.0, 50.0], [100.0, 50.0]]
            elif shape == 5:
                shape_name = 'triangle'
                shape_type = 'polygon'
                shape_info = [[100.0, 50.0], [25.0, 7.0], [25.0, 86.0]]
            elif shape == 6:
                shape_name = 'upTriangle'
                shape_type = 'polygon'
                shape_info = [[50.0, 0.0], [100.0, 80.6], [0.0, 80.6]]
            elif shape == 7:
                shape_name = 'downTirangle'
                shape_type = 'polygon'
                shape_info = [[0.0, 0.0], [100.0, 0.0], [50.0, 80.6]] 
            elif shape == 8:
                shape_name = 'leftTriangle'
                shape_type = 'polygon'
                shape_info = [[80.6, 0.0], [80.6, 100.0], [0.0, 50.0]]
            elif shape == 9:
                shape_name = 'rightTriangle'
                shape_type = 'polygon'
                shape_info = [[0.0, 0.0], [80.6, 50.0], [0.0, 100.0]]
        else:
            raise Exception("This is not a valid node shape information.")
    else:
        raise Exception("This is not a valid node shape information.")
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"shape_idx"] = shape_idx
        df_NodeData_temp.at[idx_list[i],"shape_name"] = shape_name
        df_NodeData_temp.at[idx_list[i],"shape_type"] = shape_type
        df_NodeData_temp.at[idx_list[i],"shape_info"] = shape_info
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setNodeArbitraryPolygonShape(df, id, shape_name, shape_info):

    """
        Set an arbitrary polygon shape to a node by shape name and shape info.

        Args:  
            id: str-node id.

            shape_name: str-name of the arbitrary polygon shape.

            shape_info: list-[[x1,y1],[x2,y2],[x3,y3],etc], where x,y are floating numbers from 0 to 100.        
    
    """
    shape_idx = -2 #arbitrary polygon
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    if isinstance(shape_name, str):
        for i in range(len(idx_list)):
            df_NodeData_temp.at[idx_list[i],"shape_name"] = shape_name
    else:
        raise Exception("This is not a valid node shape name.")
    #check the shape_info is in the correct format:
    shape_info_flag = True
    if isinstance(shape_info, list) and len(shape_info) >= 2:
        for ii in range(len(shape_info)):
            if isinstance(shape_info[ii], list) and len(shape_info[ii]) == 2:
                if all(isinstance(float(item), float) for item in shape_info[ii]):
                    pass
                else:
                    shape_info_flag = False
                    raise Exception("This is not a valid node shape info1.")
            else:
                shape_info_flag = False
                raise Exception("This is not a valid node shape info2.")               
    else:
        shape_info_flag = False
        raise Exception("This is not a valid node shape info3.")
    if shape_info_flag == True:
        for i in range(len(idx_list)):
            df_NodeData_temp.at[idx_list[i],"shape_info"] = shape_info
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"shape_idx"] = shape_idx
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setNodeTextPosition(df, id, txt_position):

    """
    Set the x,y coordinates of the node text position.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        txt_position: [position_x, position_y], the coordinate represents the top-left hand corner of the node text.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
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
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"txt_size"] = txt_size
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setNodeFillColor(df, id, fill_color, opacity):

    """
    Set the node fill color.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    fill_color = _color_to_rgb(fill_color, opacity)
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"fill_color"] = fill_color
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setNodeBorderColor(df, id, border_color, opacity):

    """
    Set the node border color.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    border_color = _color_to_rgb(border_color, opacity)
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
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
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"border_width"] = border_width
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setNodeTextFontColor(df, id, txt_font_color, opacity):

    """
    Set the node text font color.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        txt_font_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    txt_font_color = _color_to_rgb(txt_font_color, opacity)
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
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"txt_line_width"] = txt_line_width
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp


def _setNodeTextFontSize(df, id, txt_font_size):

    """
    Set the node text font size.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        txt_font_size: float-node text font size.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_NodeData_temp.at[idx_list[i],"txt_font_size"] = txt_font_size
    df_temp = (df[0], df_NodeData_temp, df[2])

    return df_temp

def _setReactionCenterPosition(df, id, position):

    """
    Set the reaction center position.

    Args:  
        df: DataFrame-initial information.

        id: str-reaction id.
        
        position: list-1*2 matrix-[position_x, position_y]

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_ReactionData_temp.at[idx_list[i],"center_pos"] = position
    df_temp = (df[0], df[1], df_ReactionData_temp)
    
    return df_temp

def _setReactionHandlePositions(df, id, position):

    """
    Set the reaction handle positions.

    Args:  
        df: DataFrame-initial information.

        id: str-reaction id.
        
        position: list-position of the handles: [center handle, reactant handles, product handles].

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_ReactionData_temp.at[idx_list[i],"handles"] = position
    df_temp = (df[0], df[1], df_ReactionData_temp)
    
    return df_temp

def _setReactionFillColor(df, id, fill_color, opacity):

    """
    Set the reaction fill color.

    Args:  
        df: DataFrame-initial information.

        id: str-reaction id.

        fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    fill_color = _color_to_rgb(fill_color, opacity)
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
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_ReactionData_temp.at[idx_list[i],"line_thickness"] = line_thickness
    df_temp = (df[0], df[1], df_ReactionData_temp)

    return df_temp

def _setBezierReactionType(df, id, bezier):

    """
    Set the reaction type to bezier curve or not with a certain reaction id.

    Args:  
        df: DataFrame-initial information.

        id: str-reaction id.
 
        bezier: bool-bezier reaction (True as default) or not (False as straightline).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_ReactionData_temp.at[idx_list[i],"bezier"] = bezier
    df_temp = (df[0], df[1], df_ReactionData_temp)

    return df_temp

def _setReactionArrowHeadSize(df, id, size):
#def _setReactionArrowHeadSize(df, size):

    """
    Set the reaction arrow head size with a certain reaction id.

    Args:  
        df: DataFrame-initial information.

        size: list-1*2 matrix-size of the rectangle [width, height].

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_ReactionData_temp.at[idx_list[i],"arrow_head_size"] = size
    df_temp = (df[0], df[1], df_ReactionData_temp)
    # df_ReactionData_temp = df[2].copy()
    # for i in range(len(df_ReactionData_temp)):
    #     df_ReactionData_temp.at[i,"arrow_head_size"] = size
    # df_temp = (df[0], df[1], df_ReactionData_temp)

    return df_temp

def _setReactionDash(df, id, dash):

    """
    Set the reaction dash information with a certain reaction id.

    Args:  
        df: DataFrame-initial information.

        id: str-reaction id.
 
        dash: list - [] means solid; 
            [a,b] means drawing a a-point line and following a b-point gap and etc;
            [a,b,c,d] means drawing a a-point line and following a b-point gap, and then
            drawing a c-point line followed by a d-point gap.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_ReactionData_temp.at[idx_list[i],"rxn_dash"] = dash
    df_temp = (df[0], df[1], df_ReactionData_temp)

    return df_temp

def _addText(df_text, txt_str, txt_position, txt_font_color = [0, 0, 0], opacity = 1., 
    txt_line_width = 1., txt_font_size = 12.):
    """
    Set arbitray text onto canvas.

    Args:  
        txt_str: str-the text content.

        txt_position: list-[position_x, position_y], the coordinate represents the top-left hand 
        corner of the node text.

        txt_font_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

        txt_line_width: float-node text line width.

        txt_font_size: float-node text font size.
        
    """
    txt_font_color_rgba = _color_to_rgb(txt_font_color, opacity)
    df_text_temp = df_text.copy()
    text_row_dct = {k:[] for k in processSBML.COLUMN_NAME_df_text}
    text_row_dct[processSBML.ID].append(txt_str)
    text_row_dct[processSBML.TXTPOSITION].append(txt_position)
    text_row_dct[processSBML.TXTFONTCOLOR].append(txt_font_color_rgba)
    text_row_dct[processSBML.TXTLINEWIDTH].append(txt_line_width)
    text_row_dct[processSBML.TXTFONTSIZE].append(txt_font_size)
    if len(df_text_temp) == 0:
        df_text_temp = pd.DataFrame(text_row_dct)
    else:
        df_text_temp = pd.concat([df_text_temp,\
            pd.DataFrame(text_row_dct)], ignore_index=True)

    return df_text_temp

def _removeText(df_text, txt_str):
    """
    Set arbitray text onto canvas.

    Args:  
        txt_str: str-the text content.
        
    """
    df_text_temp = df_text.copy()
    idx_list = df_text_temp.index[df_text_temp[processSBML.ID] == txt_str].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid text content.")
    df_text_temp = df_text_temp.drop(idx_list)

    return df_text_temp