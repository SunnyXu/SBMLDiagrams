# -*- coding: utf-8 -*-
# This script was initiated by Herbert Sauro, written by Jin Xu and available on Github
# https://github.com/SunnyXu/SBMLDiagrams
# This file includes all the functions to visualize or edit the SBML file.
"""
Created on Fri Jul 16 09:57:30 2021
@author: Jin Xu and Herbert Sauro
"""

import math
import random, tempfile, string, os
from PIL import Image               # to load images
from IPython.display import display
from numpy.core.numeric import cross # to display images
import skia


def _drawRectangle (canvas, x, y, width, height, outline, fill, linewidth, dash = False):
    
    """
    Draw a rectangle on canvas.

    Args:  
        canvas: skia.Surface().getCanvas().
        x: float-left up corner position_x
        y: float-left up corner position_y
        width: float-width of the rectangle
        height: float-height of the rectangle
        outline: skia.Color()-border color
        fill: skia.Color()-fill color
        linewidth: float-line width
        dash: bool-dashline (True) or not (False as default)
    """
    
    rect = skia.Rect(x, y, x+width, y+height)    
    paintFill = skia.Paint(
      AntiAlias=True,
      Style = skia.Paint.kFill_Style,
      Color = fill
    )    
    canvas.drawRect(rect, paintFill)
    if dash:
        paintStroke = skia.Paint(
        AntiAlias=True,
        PathEffect=skia.DashPathEffect.Make([10.0, 5.0, 2.0, 5.0], 0.0),
        StrokeWidth=linewidth,
        Style = skia.Paint.kStroke_Style,
        Color = outline
        )  
    else:  
        paintStroke = skia.Paint(
        AntiAlias=True,
        StrokeWidth=linewidth,
        Style = skia.Paint.kStroke_Style,
        Color = outline
        )  
    canvas.drawRect(rect, paintStroke)

def _drawRoundedRectangle (canvas, x, y, width, height, outline, fill, linewidth, dash = False):

    """
    Draw a rounded rectangle on canvas.

    Args:  
        canvas: skia.Surface().getCanvas()
        x: float-left up corner position_x
        y: float-left up corner position_y
        width: float-width of the rectangle
        height: float-height of the rectangle
        outline: skia.Color()-border color
        fill: skia.Color()-fill color
        linewidth: float-line width
        dash: bool-dashline (True) or not (False as default)
    """

    radius = 1.*linewidth
    rect = skia.Rect(x, y, x+width, y+height)
    paintFill = skia.Paint(
      AntiAlias=True,
      Style = skia.Paint.kFill_Style,
      Color = fill
    )    
    canvas.drawRoundRect(rect, radius, radius, paintFill)
    if dash:
        paintStroke = skia.Paint(
        AntiAlias=True,
        StrokeWidth=linewidth,
        PathEffect=skia.DashPathEffect.Make([10.0, 5.0, 2.0, 5.0], 0.0),
        Style = skia.Paint.kStroke_Style,
        Color =  outline
        )    
    else:
        paintStroke = skia.Paint(
        AntiAlias=True,
        StrokeWidth=linewidth,
        Style = skia.Paint.kStroke_Style,
        Color =  outline
        )    
    canvas.drawRoundRect(rect, radius, radius, paintStroke);   
    
def _drawCircle (canvas, x1, y1, w, h, outline, fill, linewidth, dash = False):
    
    """
    Draw a circle within a certain size of rectangle on canvas.

    Args:  
        canvas: skia.Surface().getCanvas()
        x1: float-left up corner position_x of the rectangle
        y1: float-left up corner position_y of the rectangle
        w: float-width of the rectangle
        h: float-height of the rectangle
        outline: skia.Color()-border color
        fill: skia.Color()-fill color
        linewidth: float-line width
        dash: bool-dashline (True) or not (False as default)
    """

    centerX = x1 + w/2
    centerY = y1 + h/2
    radius = .5*min(w,h) # the radius of the circle should be the half of the minimum of w and h
    paint = skia.Paint(
      AntiAlias=True,
      Style = skia.Paint.kFill_Style,
      StrokeWidth=linewidth,
      Color = fill
    ) 
    canvas.drawCircle (centerX, centerY, radius, paint)
    if dash:
        paint = skia.Paint(
        AntiAlias=True,
        PathEffect=skia.DashPathEffect.Make([10.0, 5.0, 2.0, 5.0], 0.0),
        Style = skia.Paint.kStroke_Style,
        StrokeWidth=linewidth,
        Color = outline
        ) 
    else:
        paint = skia.Paint(
        AntiAlias=True,
        Style = skia.Paint.kStroke_Style,
        StrokeWidth=linewidth,
        Color = outline
        )   
    canvas.drawCircle (centerX, centerY, radius, paint)

def _drawDimer (canvas, x1, y1, w, h, outline, fill, linewidth, dash = False):

    """
    Draw a dimer (two circles) within a certain size of rectangle on canvas.

    Args:  
        canvas: skia.Surface().getCanvas()
        x1: float-left up corner position_x of the rectangle
        y1: float-left up corner position_y of the rectangle
        w: float-width of the rectangle
        h: float-height of the rectangle
        outline: skia.Color()-border color
        fill: skia.Color()-fill color
        linewidth: float-line width
        dash: bool-dashline (True) or not (False as default)
    """

    radius = .25*min(w,h)
    centerX1 = x1 + w/2 - radius
    centerY1 = y1 + h/2
    centerX2 = x1 + w/2 + radius
    centerY2 = centerY1
    paint = skia.Paint(
      AntiAlias=True,
      Style = skia.Paint.kFill_Style,
      StrokeWidth=linewidth,
      Color = fill
    ) 
    canvas.drawCircle (centerX1, centerY1, radius, paint)
    canvas.drawCircle (centerX2, centerY2, radius, paint)
    if dash:
        paint = skia.Paint(
        AntiAlias=True,
        PathEffect=skia.DashPathEffect.Make([10.0, 5.0, 2.0, 5.0], 0.0),
        Style = skia.Paint.kStroke_Style,
        StrokeWidth=linewidth,
        Color = outline
        ) 
    else:
        paint = skia.Paint(
        AntiAlias=True,
        Style = skia.Paint.kStroke_Style,
        StrokeWidth=linewidth,
        Color = outline
        )   
    canvas.drawCircle (centerX1, centerY1, radius, paint)
    canvas.drawCircle (centerX2, centerY2, radius, paint)

def _drawTrimer (canvas, x1, y1, w, h, outline, fill, linewidth, dash = False):
    
    """
    Draw a trimer (three circles) within a certain size of rectangle on canvas.

    Args:  
        canvas: skia.Surface().getCanvas()
        x1: float-left up corner position_x of the rectangle
        y1: float-left up corner position_y of the rectangle
        w: float-width of the rectangle
        h: float-height of the rectangle
        outline: skia.Color()-border color
        fill: skia.Color()-fill color
        linewidth: float-line width
        dash: bool-dashline (True) or not (False as default)
    """

    radius = .25*min(w,h)
    centerX1 = x1 + w/2
    centerY1 = y1 + h/2 - radius
    centerX3 = x1 + w/2 - radius
    centerY3 = y1 + h/2 + radius
    centerX4 = x1 + w/2 + radius
    centerY4 = centerY3
    paint = skia.Paint(
      AntiAlias=True,
      Style = skia.Paint.kFill_Style,
      StrokeWidth=linewidth,
      Color = fill
    ) 
    canvas.drawCircle (centerX1, centerY1, radius, paint)
    canvas.drawCircle (centerX3, centerY3, radius, paint)
    canvas.drawCircle (centerX4, centerY4, radius, paint)
    if dash:
        paint = skia.Paint(
        AntiAlias=True,
        PathEffect=skia.DashPathEffect.Make([10.0, 5.0, 2.0, 5.0], 0.0),
        Style = skia.Paint.kStroke_Style,
        StrokeWidth=linewidth,
        Color = outline
        ) 
    else:
        paint = skia.Paint(
        AntiAlias=True,
        Style = skia.Paint.kStroke_Style,
        StrokeWidth=linewidth,
        Color = outline
        )   
    canvas.drawCircle (centerX1, centerY1, radius, paint)
    canvas.drawCircle (centerX3, centerY3, radius, paint)
    canvas.drawCircle (centerX4, centerY4, radius, paint)

def _drawTetramer (canvas, x1, y1, w, h, outline, fill, linewidth, dash = False):
    
    """
    Draw a Tetramer (four circles) within a certain size of rectangle on canvas.

    Args:  
        canvas: skia.Surface().getCanvas()
        x1: float-left up corner position_x of the rectangle
        y1: float-left up corner position_y of the rectangle
        w: float-width of the rectangle
        h: float-height of the rectangle
        outline: skia.Color()-border color
        fill: skia.Color()-fill color
        linewidth: float-line width
        dash: bool-dashline (True) or not (False as default)
    """

    radius = .25*min(w,h)
    centerX1 = x1 + w/2 - radius
    centerY1 = y1 + h/2 - radius
    centerX2 = x1 + w/2 + radius
    centerY2 = centerY1
    centerX3 = centerX1
    centerY3 = y1 + h/2 + radius
    centerX4 = centerX2
    centerY4 = centerY3
    paint = skia.Paint(
      AntiAlias=True,
      Style = skia.Paint.kFill_Style,
      StrokeWidth=linewidth,
      Color = fill
    ) 
    canvas.drawCircle (centerX1, centerY1, radius, paint)
    canvas.drawCircle (centerX2, centerY2, radius, paint)
    canvas.drawCircle (centerX3, centerY3, radius, paint)
    canvas.drawCircle (centerX4, centerY4, radius, paint)
    if dash:
        paint = skia.Paint(
        AntiAlias=True,
        PathEffect=skia.DashPathEffect.Make([10.0, 5.0, 2.0, 5.0], 0.0),
        Style = skia.Paint.kStroke_Style,
        StrokeWidth=linewidth,
        Color = outline
        ) 
    else:
        paint = skia.Paint(
        AntiAlias=True,
        Style = skia.Paint.kStroke_Style,
        StrokeWidth=linewidth,
        Color = outline
        )   
    canvas.drawCircle (centerX1, centerY1, radius, paint)
    canvas.drawCircle (centerX2, centerY2, radius, paint)
    canvas.drawCircle (centerX3, centerY3, radius, paint)
    canvas.drawCircle (centerX4, centerY4, radius, paint)

def _drawPolygon (canvas, pts, outline, fill, linewidth, dash = False):
    
    """
    Draw a polygon.

    Args:  
        canvas: skia.Surface().getCanvas()
        pts: list of 1*2 matrix: positions of the vertices/corners of the polygon
        outline: skia.Color()-border color
        fill: skia.Color()-fill color
        linewidth: float-line width
        dash: bool-dashline (True) or not (False as default)
    """

    paintFill = skia.Paint(
        AntiAlias=True,
        Style = skia.Paint.kFill_Style,
        Color = fill
    )   
    if dash:
        paintStroke = skia.Paint(
            AntiAlias=True,
            PathEffect=skia.DashPathEffect.Make([10.0, 5.0, 2.0, 5.0], 0.0),
            Style = skia.Paint.kStroke_Style,
            StrokeWidth=linewidth,
            Color = outline
        ) 
    else:
        paintStroke = skia.Paint(
            AntiAlias=True,
            Style = skia.Paint.kStroke_Style,
            StrokeWidth=linewidth,
            Color = outline
        ) 
    paintFill.setColor (fill)
    path = skia.Path()
    path.moveTo (pts[0][0],pts[0][1])
    for i in range (1, len (pts)):
        path.lineTo (pts[i][0], pts[i][1])
    path.close()
    canvas.drawPath(path, paintFill)
    paintStroke.setColor (outline)
    canvas.drawPath(path, paintStroke)

def _drawLine (canvas, x1, y1, x2, y2, fill, linewidth, dash = False):
    
    """
    Draw a line.

    Args:  
        canvas: skia.Surface().getCanvas()
        x1: float-position_x of one end of the line
        y1: float-position_y of one end of the line
        x2: float-position_x of the other end of the line
        y2: float-position_y of the other end of the line
        fill: skia.Color()-fill color
        linewidth: float-line width
        dash: bool-dashline (True) or not (False as default)
    """    

    if dash:
        paint = skia.Paint(
            AntiAlias=True,
            PathEffect=skia.DashPathEffect.Make([10.0, 5.0, 2.0, 5.0], 0.0),
            Style = skia.Paint.kFill_Style,
            StrokeWidth=linewidth,
            Color = fill
        ) 
    else:
        paint = skia.Paint(
            AntiAlias=True,
            Style = skia.Paint.kFill_Style,
            StrokeWidth=linewidth,
            Color = fill
        )
    canvas.drawLine (x1, y1, x2, y2, paint)
    
def addCompartment(canvas, position, dimension, comp_border_color, comp_fill_color, comp_border_width):

    """
    Add a compartment.

    Args:  
        canvas: skia.Surface().getCanvas().

        position: 1*2 matrix-leftup corner of the rectangle [position_x, position_y].

        dimension: 1*2 matrix-size of the rectangle [width, height].

        comp_border_color: 1*3 matrix-compartment border color.

        comp_fill_color: 1*2 matrix-compartment fill color.

        comp_border_width: float-compartment border line width.
        
    """   

    [x, y] = position
    [width, height] = dimension
    outline = skia.Color(comp_border_color[0], comp_border_color[1], comp_border_color[2])
    fill = skia.Color(comp_fill_color[0], comp_fill_color[1], comp_fill_color[2])
    linewidth = comp_border_width    
    _drawRectangle (canvas, x, y, width, height, 
                  outline=outline, fill = fill, linewidth=linewidth)
  
    
def addNode(canvas, floating_boundary_node, alias_node, position, dimension, 
        spec_border_color, spec_fill_color, spec_border_width, shapeIdx, complex_shape = ''):
    
    """
    Add a node.

    Args:  
        canvas: skia.Surface().getCanvas().

        floating_boundary_node: str-floating node ('floating') or not ('boundary').

        alias_node: str-alias node ('alias') or not ('').

        position: 1*2 matrix-leftup corner of the rectangle [position_x, position_y].

        dimension: 1*2 matrix-size of the rectangle [width, height].

        spec_border_color: 1*3 matrix-species border color.

        spec_fill_color: 1*3 matrix-species fill color.

        spec_border_width: float-compartment border line width.

        shapeIdx: int-1:rectangle, 2:circle, 3:hexagon, 4:line, 5:triangle.

        complex_shape: str-''(default), 'monomer', 'dimer', 'trimer', or 'tetramer'.

    """

    [x, y] = position
    [width, height] = dimension
    outline = skia.Color(spec_border_color[0], spec_border_color[1], spec_border_color[2])
    fill = skia.Color(spec_fill_color[0], spec_fill_color[1], spec_fill_color[2])
    linewidth = spec_border_width  
    if floating_boundary_node == 'boundary':
        linewidth = 2*linewidth
    if complex_shape == '':
        if shapeIdx == 1: #rectangle
            # if alias_node == 'alias':
            #     _drawRectangle (canvas, x, y, width, height, 
            #                   outline, fill, linewidth, dash = True)
            # else:
            #     _drawRectangle (canvas, x, y, width, height, 
            #                   outline, fill, linewidth)
            if alias_node == 'alias':
                _drawRoundedRectangle (canvas, x, y, width, height, outline, fill, linewidth, dash = True)
            else:
                _drawRoundedRectangle (canvas, x, y, width, height, outline, fill, linewidth)
        elif shapeIdx == 2: #circle
            if alias_node == 'alias':
                _drawCircle (canvas, x, y, width, height, 
                            outline, fill, linewidth, dash=True)
            else:
                _drawCircle (canvas, x, y, width, height, 
                            outline, fill, linewidth)
        elif shapeIdx == 3: #hexagon
            pts = [[x+width,y+.5*height],[x+.75*width,y+.93*height], [x+.25*width,y+.93*height],
            [x,y+.5*height],[x+.25*width,y+.07*height],[x+.75*width,y+.07*height]]
            if alias_node == 'alias':
                _drawPolygon (canvas, pts, outline, fill, linewidth, dash=True)
            else:
                _drawPolygon (canvas, pts, outline, fill, linewidth)
        elif shapeIdx == 4: #line
            if alias_node == 'alias':
                _drawLine (canvas, x, y+.5*height, x+width, y+.5*height, outline, linewidth, dash=True)
            else:
                _drawLine (canvas, x, y+.5*height, x+width, y+.5*height, outline, linewidth)
        elif shapeIdx == 5: #triangle
            pts = [[x+width,y+.5*height],[x+.25*width,y+.07*height],[x+.25*width,y+.83*height]]
            if alias_node == 'alias':
                _drawPolygon (canvas, pts, outline, fill, linewidth, dash=True)
            else:
                _drawPolygon (canvas, pts, outline, fill, linewidth)
    elif complex_shape == 'monomer':
        if alias_node == 'alias':
            _drawCircle (canvas, x, y, width, height, 
                        outline, fill, linewidth, dash=True)
        else:
            _drawCircle (canvas, x, y, width, height, 
                        outline, fill, linewidth)
    elif complex_shape == 'dimer':
        if alias_node == 'alias':
            _drawDimer (canvas, x, y, width, height, 
                        outline, fill, linewidth, dash=True)
        else:
            _drawDimer (canvas, x, y, width, height, 
                        outline, fill, linewidth)
    elif complex_shape == 'trimer':
        if alias_node == 'alias':
            _drawTrimer (canvas, x, y, width, height, 
                        outline, fill, linewidth, dash=True)
        else:
            _drawTrimer (canvas, x, y, width, height, 
                        outline, fill, linewidth)
    elif complex_shape == 'tetramer':
        if alias_node == 'alias':
            _drawTetramer (canvas, x, y, width, height, 
                        outline, fill, linewidth, dash=True)
        else:
            _drawTetramer (canvas, x, y, width, height, 
                        outline, fill, linewidth)
  
def addReaction(canvas, rct_position, prd_position, mod_position, center_position, handles,
                rct_dimension, prd_dimension, mod_dimension, reaction_line_color, reaction_line_width, 
                reaction_line_type = 'bezier', show_bezier_handles = True):
    
    """
    Add a reaction.

    Args:  
        canvas: skia.Surface().getCanvas().

        rct_position: list of 1*2 matrix: positions of each reactant.

        prd_position: list of 1*2 matrix: positions of each product.

        mod_position: list of 1*2 matrix: positions of each modifier.

        center_position: 1*2 matrix: position of the center.

        handles: list of 1*2 matrix: position of the handles: [center handle, reactant handles, product handles].

        rct_dimension: list of 1*2 matrix: dimension/size of each reactant.

        prd_dimension: list of 1*2 matrix: dimension/size of each product.

        mod_dimension: list of 1*2 matrix: dimension/size of each modifier.

        reaction_line_color: 1*3 matrix-species fill color.

        reaction_line_width: float-reaction line width.

        reactionLineType: str-type of the reaction line: 'linear' or 'bezier' (default).

        showBezierHandles: bool-show the Bezier handles (True as default) or not (False).

    """
    
    def _cross_point(arcCenter, c2, s2):
        """
        Get the cross point of a point and a rectangle with position(leftup corner) and size given.

        Args:  
            arcCenter:  1*2 matrix-position of the point
            c2: 1*2 matrix-position of the rectangle (leftup corner)
            s2: 1*2 matrix-size of the rectangle
        """
        pt_center = [c2[0]+.5*s2[0], c2[1]+.5*s2[1]]
        pt_up_left    = c2
        pt_up_right   = [c2[0]+s2[0], c2[1]]
        pt_down_left  = [c2[0], c2[1]+s2[1]]
        pt_down_right = [c2[0]+s2[0], c2[1]+s2[1]]
        def _line_intersection(line1, line2):
            """

            Args:  
                line1: list of 1*2 matrix-two points to represent line1
                line2: list of 1*2 matrix-two points to represent line2
            Returns:
                [x,y]: 1*2 matrix-the point position of the crossed two lines
            """
            xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
            ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

            def _det(a, b):
                return a[0] * b[1] - a[1] * b[0]

            div = _det(xdiff, ydiff)
            if div == 0:
                raise Exception('lines do not intersect1')
            d = (_det(*line1), _det(*line2))
            x = round(_det(d, xdiff) / div,2)
            y = round(_det(d, ydiff) / div,2)
            if (x-line1[0][0])*(x-line1[1][0])<=0 and (x-line2[0][0])*(x-line2[1][0])<=0 \
            and (y-line1[0][1])*(y-line1[1][1])<=0 and (y-line2[0][1])*(y-line2[1][1])<=0:
                return [x, y]
            else:
                raise Exception('lines do not intersect2')
        try:
            [x,y] = _line_intersection([arcCenter, pt_center], [pt_up_left, pt_down_left])
            return [x,y]
        except:
            pass
        try:
            [x,y] = _line_intersection([arcCenter, pt_center], [pt_up_left, pt_up_right])
            return [x,y]
        except:
            pass
        try:
            [x,y] = _line_intersection([arcCenter, pt_center], [pt_down_left, pt_down_right])
            return [x,y]
        except:
            pass
        try:
            [x,y] = _line_intersection([arcCenter, pt_center], [pt_up_right, pt_down_right])
            return [x,y]
        except:
            pass
        
    def _drawArrow (canvas, pts, fill):
        """
        Draw an arrow.

        Args:  
            canvas: skia.Surface().getCanvas()
            pts: list of 1*2 matrix: points of the arrows
            fill: skia.Color(): color of the arrow
        """
        paintFill = skia.Paint(
           AntiAlias=True,
           Style = skia.Paint.kFill_Style,
           Color = fill
        )    
        paintStroke = skia.Paint(
           AntiAlias=True,
           Style = skia.Paint.kStroke_Style,
           Color = fill
        ) 
        paintFill.setColor (fill)
        path = skia.Path()
        path.moveTo (pts[0][0],pts[0][1])
        for i in range (1, len (pts)):
            path.lineTo (pts[i][0], pts[i][1])
        path.close()
        canvas.drawPath(path, paintFill)
        paintStroke.setColor (fill)
        canvas.drawPath(path, paintStroke)
        
    def _drawBezier (pts, fillcolor, linewidth):

        """
        Draw a bezier curve.

        Args:  
            pts: list of 1*2 matrix: positions of src, h1, h2 and dest ([src, h1, h2, dest])
            fillcolor: skia.Color(): color of the bezier curve
            linewidth: line width of the bezier curve
        """

        src = pts[0]; h1 = pts[1]; h2 = pts[2]; dest = pts[3]
        paint = skia.Paint(
          AntiAlias=True,
          Style = skia.Paint.kStroke_Style,
          StrokeWidth=linewidth,
          Color = fillcolor
        ) 
        path = skia.Path()
        path.moveTo(src[0], src[1])
        path.cubicTo(h1[0], h1[1], h2[0], h2[1], dest[0], dest[1])
        canvas.drawPath(path, paint)
        if show_bezier_handles:
            _drawLine(canvas, src[0], src[1], h1[0], h1[1], fillcolor, .5*linewidth)
            _drawLine(canvas, dest[0], dest[1], h2[0], h2[1], fillcolor, .5*linewidth)
            _drawCircle(canvas, h1[0]-linewidth, h1[1]-linewidth, 2*linewidth, 2*linewidth,
                        fillcolor, fillcolor, .5*linewidth)
            _drawCircle(canvas, h2[0]-linewidth, h2[1]-linewidth, 2*linewidth, 2*linewidth, 
                        fillcolor, fillcolor, .5*linewidth)
    nReactants = len(rct_position)
    nProducts = len(prd_position)
    arcCenter = center_position
    linewidth = reaction_line_width
    lineType = reaction_line_type
    lineColor = skia.Color(reaction_line_color[0], reaction_line_color[1], reaction_line_color[2])
    arrow_s1 = 5*reaction_line_width #height of the arrow
    arrow_s2 = 4*reaction_line_width #width of the arrow
    if lineType == 'bezier':
        center_handle_position = handles[0]
        center_handle_position_prd = [2*arcCenter[0]-center_handle_position[0],2*arcCenter[1]-center_handle_position[1]]
        src_handle = handles[1:nReactants+1]
        dst_handle = handles[nReactants+1:nReactants+nProducts+1]   
        for i in range(nReactants):
            pts = [center_position] #src (center_position), h1(center_handle), h2(rct/prd_handle), dst(rct/prd)
            pts.append(center_handle_position)
            rct_handle_position = src_handle[i]
            pts.append(rct_handle_position)
            c1 = rct_position[i] 
            s1 = rct_dimension[i]
            try:
                #to calculate the end point of the arrow called arrow_end_pt
                arrow_end_pt = _cross_point(rct_handle_position, c1, s1)
                if arrow_end_pt != None:
                    pts.append(arrow_end_pt)
                    _drawBezier(pts, lineColor, linewidth)
            except:
                rct_center_position =  [c1[0]+.5*s1[0], c1[1]+.5*s1[1]]
                pts.append(rct_center_position)
                _drawBezier(pts, lineColor, linewidth)
        for i in range(nProducts):
            pts = [center_position] 
            pts.append(center_handle_position_prd)
            prd_handle_position = dst_handle[i]
            pts.append(prd_handle_position)
            c2 = prd_position[i] 
            s2 = prd_dimension[i]
            try:
                #to calculate the head point of the arrow called arrow_head_pt
                arrow_head_pt = _cross_point(prd_handle_position, c2, s2)
                #draw the arrow:
                points = [arrow_head_pt]
                dis_rct_arc_center = math.sqrt((arrow_head_pt[0]-prd_handle_position[0])**2 + (arrow_head_pt[1]-prd_handle_position[1])**2)      
                pts_y_m = arrow_head_pt[1] - (arrow_head_pt[1]-prd_handle_position[1])*arrow_s1/dis_rct_arc_center
                pts_x_m = arrow_head_pt[0] - (arrow_head_pt[0]-prd_handle_position[0])*arrow_s1/dis_rct_arc_center
                pts_y_l = pts_y_m + (arrow_head_pt[0]-prd_handle_position[0])*.5*arrow_s2/dis_rct_arc_center
                pts_x_l = pts_x_m - (arrow_head_pt[1]-prd_handle_position[1])*.5*arrow_s2/dis_rct_arc_center
                points.append([pts_x_l,pts_y_l])
                points.append([pts_x_m, pts_y_m])
                pts_y_r = pts_y_m - (arrow_head_pt[0]-prd_handle_position[0])*.5*arrow_s2/dis_rct_arc_center
                pts_x_r = pts_x_m + (arrow_head_pt[1]-prd_handle_position[1])*.5*arrow_s2/dis_rct_arc_center
                points.append([pts_x_r,pts_y_r])
                _drawArrow(canvas, points, lineColor)
                if arrow_head_pt != None:
                    pts.append(arrow_head_pt)
                    _drawBezier(pts, lineColor, linewidth)
            except:
                prd_center_position = [c2[0]+.5*s2[0], c2[1]+.5*s2[1]]
                pts.append(prd_center_position)
                _drawBezier(pts, lineColor, linewidth)
    elif lineType == 'linear':
        for i in range (nReactants):
            c1 = rct_position[i] 
            s1 = rct_dimension[i]
            try:
                #to calculate the end point of the arrow called arrow_end_pt
                arrow_end_pt = _cross_point(arcCenter, c1, s1) 
            except:
                pass
            #rct_center_position =  [c1[0]+.5*s1[0], c1[1]+.5*s1[1]]
            #_drawLine(canvas, rct_center_position[0], rct_center_position[1], arcCenter[0], arcCenter[1], lineColor, linewidth)
            _drawLine(canvas, arrow_end_pt[0], arrow_end_pt[1], arcCenter[0], arcCenter[1], lineColor, linewidth)
        for i in range (nProducts):
            c2 = prd_position[i] 
            s2 = prd_dimension[i]
            try:
                #to calculate the head point of the arrow called arrow_head_pt
                arrow_head_pt = _cross_point(arcCenter, c2, s2) 
                #draw the arrow:
                points = [arrow_head_pt]
                dis_rct_arc_center = math.sqrt((arrow_head_pt[0]-arcCenter[0])**2 + (arrow_head_pt[1]-arcCenter[1])**2)      
                pts_y_m = arrow_head_pt[1] - (arrow_head_pt[1]-arcCenter[1])*arrow_s1/dis_rct_arc_center
                pts_x_m = arrow_head_pt[0] - (arrow_head_pt[0]-arcCenter[0])*arrow_s1/dis_rct_arc_center
                pts_y_l = pts_y_m + (arrow_head_pt[0]-arcCenter[0])*.5*arrow_s2/dis_rct_arc_center
                pts_x_l = pts_x_m - (arrow_head_pt[1]-arcCenter[1])*.5*arrow_s2/dis_rct_arc_center
                points.append([pts_x_l,pts_y_l])
                points.append([pts_x_m, pts_y_m])
                pts_y_r = pts_y_m - (arrow_head_pt[0]-arcCenter[0])*.5*arrow_s2/dis_rct_arc_center
                pts_x_r = pts_x_m + (arrow_head_pt[1]-arcCenter[1])*.5*arrow_s2/dis_rct_arc_center
                points.append([pts_x_r,pts_y_r])
                _drawArrow(canvas, points, lineColor)
            except:
                pass
            #prd_center_position = [c2[0]+.5*s2[0], c2[1]+.5*s2[1]]
            #_drawLine(canvas, arcCenter[0], arcCenter[1], prd_center_position[0], prd_center_position[1], lineColor, linewidth)
            _drawLine(canvas, arcCenter[0], arcCenter[1], arrow_head_pt[0], arrow_head_pt[1], lineColor, linewidth)
    #draw modifiers:
    modifier_lineColor = skia.Color(128, 0, 128)
    modifier_linewidth = 2
    mod_num = len(mod_position)
    for i in range(mod_num):
        mod_start_virtual_x = .5*mod_dimension[i][0] + mod_position[i][0]
        mod_start_virtual_y = .5*mod_dimension[i][1] + mod_position[i][1]
        try: 
            [mod_start_x, mod_start_y] = _cross_point(arcCenter, 
            [mod_position[i][0]-.25*mod_dimension[i][0], mod_position[i][1]-.25*mod_dimension[i][1]],
            [mod_dimension[i][0]*1.5, mod_dimension[i][1]*1.5]) 
            [mod_end_x, mod_end_y] = _cross_point([mod_start_virtual_x, mod_start_virtual_y],
            [arcCenter[0]-.5*mod_dimension[i][0],arcCenter[1]-.5*mod_dimension[i][1]], mod_dimension[i])
        except: 
            mod_start_x = .5*mod_dimension[i][0] + mod_position[i][0]
            mod_start_y = .5*mod_dimension[i][1] + mod_position[i][1]
            [mod_end_x, mod_end_y] = arcCenter[0], arcCenter[1] 
        _drawLine(canvas, mod_start_x, mod_start_y, mod_end_x, mod_end_y,
         modifier_lineColor, modifier_linewidth)  
        _drawCircle(canvas, mod_end_x-modifier_linewidth, mod_end_y-modifier_linewidth, 
        2*modifier_linewidth, 2*modifier_linewidth,
                        modifier_lineColor, modifier_lineColor, .5*modifier_linewidth)   
        # mod_start_x = .5*mod_dimension[i][0] + mod_position[i][0]
        # mod_start_y = .5*mod_dimension[i][1] + mod_position[i][1] 
        # _drawLine(canvas, arcCenter[0], arcCenter[1], mod_start_x, mod_start_y,
        #  modifier_lineColor, modifier_linewidth)  
        # _drawCircle(canvas, arcCenter[0]-modifier_linewidth, arcCenter[1]-modifier_linewidth, 
        # 2*modifier_linewidth, 2*modifier_linewidth,
        #                 modifier_lineColor, modifier_lineColor, .5*modifier_linewidth)     

def addText(canvas, node_id, position, dimension, text_line_color, text_line_width):

    """
    Add the text.

    Args:  
        canvas: skia.Surface().getCanvas().

        node_id: str-the content of the text.

        position: 1*2 matrix-leftup corner of the rectangle [position_x, position_y].

        dimension: 1*2 matrix-size of the rectangle [width, height].

        text_line_color: 1*3 matrix-text line color.

        text_line_width: float-text line width.

    """ 
    id = node_id
    #fontSize = 11
    #scalingFactor = 1.
    #fontSize_virtual = fontSize*scalingFactor 
    fontColor = skia.Color(text_line_color[0], text_line_color[1], text_line_color[2])    
    paintText = skia.Paint(Color = fontColor, StrokeWidth=text_line_width)  
    #paintText = skia.Paint(Colot = fontColor)  
    font = skia.Font(skia.Typeface('Arial', skia.FontStyle.Bold()))
    #font = skia.Font(skia.Typeface())
    text = skia.TextBlob.MakeFromString(id, font)
    twidth = font.measureText(id)
    theight = font.getSize() 
    position_x = position[0] + .5*(dimension[0] - twidth)
    position_y = position[1] + dimension[1] - .5*(dimension[1] - theight)
    canvas.drawTextBlob(text, position_x, position_y, paintText)

def draw(surface, fileName = '', file_format = 'PNG'):
    """
    Display the diagram and save it to the local.

    Args:  
        surface: skia.Surface().

        fileName: str-the name for the generated file: either the input filename or a randomly generated filename if '' (default).
        
        fileFormat = 'PDF' #'PNG' (default), 'JPEG' or 'PDF'.
    """ 

    if fileName == '':
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        #tmpfileName = os.path.join(tempfile.gettempdir(), random_string)    
        tmpfileName = os.path.join(os.getcwd(), random_string)
        image = surface.makeImageSnapshot()
        if file_format == 'PNG':
            tmpfileName = tmpfileName + '.png'
            image.save(tmpfileName, skia.kPNG)
            pil_im = Image.open(tmpfileName)
            display(pil_im)
            pil_im.show()
        elif file_format == 'JPEG':
            tmpfileName = tmpfileName + '.jpg'
            image.save(tmpfileName, skia.kJPEG)
            pil_im = Image.open(tmpfileName)
            display(pil_im)
            pil_im.show()
        elif file_format == 'PDF':
            tmpfileNamepdf = tmpfileName + '.pdf'
            tmpfileName = tmpfileName + '.png'
            image.save(tmpfileName, skia.kPNG)
            pil_im = Image.open(tmpfileName)
            display(pil_im)
            pil_im.show() 
            imagepdf = pil_im.convert('RGB')
            imagepdf.save(tmpfileNamepdf)
            os.remove(tmpfileName)

        #self.surface.write_to_png(tmpfileName)
        # pil_im = Image.open(tmpfileName)
        # display(pil_im)
        # pil_im.show()
    else:
        fileName = os.path.join(os.getcwd(),fileName)
        image = surface.makeImageSnapshot()
        if file_format == 'PNG':
            fileName = fileName + '.png'
            image.save(fileName, skia.kPNG)
            pil_im = Image.open(fileName)
            display(pil_im)
            pil_im.show() 
        elif file_format == 'JPEG':
            fileName = fileName + '.jpg'
            image.save(fileName, skia.kJPEG) 
            pil_im = Image.open(fileName)
            display(pil_im)
            pil_im.show()   
        elif file_format == 'PDF':
            fileNamepdf = fileName + '.pdf'
            fileName = fileName + '.png'
            image.save(fileName, skia.kPNG)
            pil_im = Image.open(fileName)
            display(pil_im)
            pil_im.show() 
            imagepdf = pil_im.convert('RGB')
            imagepdf.save(fileNamepdf)
            os.remove(fileName)


