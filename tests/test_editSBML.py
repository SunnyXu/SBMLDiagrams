import unittest
import os
from SBMLDiagrams import processSBML
from SBMLDiagrams import editSBML
import pandas as pd

IGNORE_TEST = False

#############################
# Tests
#############################
class TestEditSBML(unittest.TestCase):
#test all the _set functions in editSBML module

  def setUp(self):
    DIR = os.path.dirname(os.path.abspath(__file__))
    TEST_FOLDER = os.path.join(DIR, "test_sbml_files")
    TEST_PATH_test = os.path.join(TEST_FOLDER, "test.xml")
    f_test = open(TEST_PATH_test, 'r')
    sbmlStr_test = f_test.read()
    f_test.close()
    TEST_PATH_test_text = os.path.join(TEST_FOLDER, "test_textGlyph.xml")
    f_test_text = open(TEST_PATH_test_text, 'r')
    sbmlStr_test_text = f_test_text.read()
    f_test_text.close()

    self.df = processSBML._SBMLToDF(sbmlStr_test)
    self.df_text = processSBML._SBMLToDF(sbmlStr_test_text)

  def testSetCompartment(self):
    # setCompartment one by one
    if IGNORE_TEST:
      return    
    position = [1, 0]
    size = [900, 900]
    fill_color = [255, 255, 254]
    border_color = [255, 255, 254]
    border_width = 2.
    opacity = 0.

    df_update = editSBML._setCompartmentPosition(self.df, "_compartment_default_", position)
    df_update = editSBML._setCompartmentSize(df_update, "_compartment_default_", size)
    df_update = editSBML._setCompartmentFillColor(df_update, "_compartment_default_", fill_color, opacity = opacity)
    df_update = editSBML._setCompartmentBorderColor(df_update, "_compartment_default_", border_color, opacity = opacity)
    df_update = editSBML._setCompartmentBorderWidth(df_update, "_compartment_default_", border_width)

    self.assertTrue(df_update[0].iloc[0]["position"] == position)
    self.assertTrue(df_update[0].iloc[0]["size"] == size) 
    self.assertTrue(df_update[0].iloc[0]["fill_color"][0:-1] == fill_color)
    self.assertTrue(df_update[0].iloc[0]["fill_color"][3] == int(opacity*255/1.))
    self.assertTrue(df_update[0].iloc[0]["border_color"][0:-1] == border_color)
    self.assertTrue(df_update[0].iloc[0]["border_color"][3] == int(opacity*255/1.))
    self.assertTrue(df_update[0].iloc[0]["border_width"] == border_width)
       
    with self.assertRaises(Exception):
      editSBML._setCompartmentPosition(df_update, "XX", position)
    with self.assertRaises(Exception):
      editSBML._setCompartmentSize(df_update, "XX", size)
    with self.assertRaises(Exception):
      editSBML._setCompartmentFillColor(df_update, "XX", fill_color)
    with self.assertRaises(Exception):
      editSBML._setCompartmentBorderColor(df_update, "XX", border_color)
    with self.assertRaises(Exception):
      editSBML._setCompartmentBorderWidth(df_update, "XX", border_width)

  def testSetNode(self):
    # set node one by one
    if IGNORE_TEST:
      return    
    floating_node = True
    position = [412., 216.]
    size = [50., 29.]
    shapeIdx = 2
    shape = 'ellipse'
    shape_name = 'self_shape'
    shape_info_polygon = [[0,0],[100,0],[0,100]]
    shape_info_ellipse = [[[50,50],[100,100]]]
    txt_position = [412., 216.]
    txt_size = [50., 29.]
    fill_color = [255, 204, 154]
    border_color = [255, 109, 9]
    border_width = 3.
    txt_font_color = [0, 0, 0]
    txt_line_width = 1.
    txt_font_size = 12.
    opacity = 1.

    df_update = editSBML._setFloatingBoundaryNode(self.df, "x_1", floating_node)
    df_update = editSBML._setNodePosition(df_update, "x_1", position)
    df_update = editSBML._setNodeSize(df_update, "x_1", size)
    df_update = editSBML._setNodeShape(df_update, "x_1", shapeIdx)
    df_update = editSBML._setNodeShape(df_update, "x_1", shape)
    df_update = editSBML._setNodeArbitraryPolygonShape(df_update, "x_0", shape_name, shape_info_polygon)
    # df_update = editSBML._setNodeArbitraryEllipseShape(df_update, "x_0", shape_name, shape_info_ellipse)
    df_update = editSBML._setNodeTextPosition(df_update, "x_1", txt_position)
    df_update = editSBML._setNodeTextSize(df_update, "x_1", txt_size)
    df_update = editSBML._setNodeFillColor(df_update, "x_1", fill_color, opacity = opacity)
    df_update = editSBML._setNodeBorderColor(df_update, "x_1", border_color, opacity = opacity)
    df_update = editSBML._setNodeBorderWidth(df_update, "x_1", border_width)
    df_update = editSBML._setNodeTextFontColor(df_update, "x_1", txt_font_color, opacity = opacity)
    df_update = editSBML._setNodeTextLineWidth(df_update, "x_1", txt_line_width)
    df_update = editSBML._setNodeTextFontSize(df_update, "x_1", txt_font_size)
    
    self.assertTrue(df_update[1].iloc[0]["floating_node"] == floating_node)
    self.assertTrue(df_update[1].iloc[0]["position"] == position)
    self.assertTrue(df_update[1].iloc[0]["size"] == size)
    self.assertTrue(df_update[1].iloc[0]["shape_idx"] == shapeIdx)
    self.assertTrue(df_update[1].iloc[0]["shape_type"] == shape)
    self.assertTrue(df_update[1].iloc[1]["shape_name"] == shape_name)
    self.assertTrue(df_update[1].iloc[1]["shape_info"] == shape_info_polygon)
    self.assertTrue(df_update[1].iloc[0]["txt_position"] == txt_position)
    self.assertTrue(df_update[1].iloc[0]["txt_size"] == txt_size)
    self.assertTrue(df_update[1].iloc[0]["fill_color"][0:-1] == fill_color)
    self.assertTrue(df_update[1].iloc[0]["fill_color"][3] == int(opacity*255/1.))
    self.assertTrue(df_update[1].iloc[0]["border_color"][0:-1] == border_color)
    self.assertTrue(df_update[1].iloc[0]["border_color"][3] == int(opacity*255/1.))
    self.assertTrue(df_update[1].iloc[0]["border_width"] == border_width)
    self.assertTrue(df_update[1].iloc[0]["txt_font_color"][0:-1] == txt_font_color)
    self.assertTrue(df_update[1].iloc[0]["txt_font_color"][3] == int(opacity*255/1.))
    self.assertTrue(df_update[1].iloc[0]["txt_line_width"] == txt_line_width)
    self.assertTrue(df_update[1].iloc[0]["txt_font_size"] == txt_font_size)

    with self.assertRaises(Exception):
      editSBML._setFloatingBoundaryNode(df_update, "XX", floating_node)
    with self.assertRaises(Exception):  
      editSBML._setNodePosition(df_update, "XX", position)
    with self.assertRaises(Exception):
      editSBML._setNodeSize(df_update, "XX", size)
    with self.assertRaises(Exception):
      editSBML._setNodeShape(df_update, "XX", shapeIdx)
    with self.assertRaises(Exception):
      editSBML._setNodeShape(df_update, "x_1", 4.5)
    with self.assertRaises(Exception):
      editSBML._setNodeShape(df_update, "x_1", 100)
    with self.assertRaises(Exception):
      editSBML._setNodeArbitraryPolygonShape(df_update, "XX", shape_name, shape_info_polygon)
    with self.assertRaises(Exception):
      editSBML._setNodeArbitraryPolygonShape(df_update, "x_0", 0, shape_info_polygon)
    with self.assertRaises(Exception):
      editSBML._setNodeArbitraryPolygonShape(df_update, "x_0", shape_name, shape_info_ellipse)
    # with self.assertRaises(Exception):
    #   editSBML._setNodeArbitraryEllipseShape(df_update, "XX", shape_name, shape_info_ellipse)
    # with self.assertRaises(Exception):
    #   editSBML._setNodeArbitraryEllipseShape(df_update, "x_0", 0, shape_info_ellipse)
    # with self.assertRaises(Exception):
    #   editSBML._setNodeArbitraryEllipseShape(df_update, "x_0", shape_name, shape_info_polygon)
    with self.assertRaises(Exception):
      editSBML._setNodeTextPosition(df_update, "XX", txt_position)
    with self.assertRaises(Exception):
      editSBML._setNodeTextSize(df_update, "XX", txt_size)
    with self.assertRaises(Exception):
      editSBML._setNodeFillColor(df_update, "XX", fill_color, opacity = opacity)
    with self.assertRaises(Exception):
      editSBML._setNodeBorderColor(df_update, "XX", border_color, opacity = opacity)
    with self.assertRaises(Exception):
      editSBML._setNodeBorderWidth(df_update, "XX", border_width)
    with self.assertRaises(Exception):
      editSBML._setNodeTextFontColor(df_update, "XX", txt_font_color, opacity = opacity)
    with self.assertRaises(Exception):
      editSBML._setNodeTextLineWidth(df_update, "XX", txt_line_width)
    with self.assertRaises(Exception):
      editSBML._setNodeTextFontSize(df_update, "XX", txt_font_size)

  def testSetReaction(self):
    # set reaction one by one
    if IGNORE_TEST:
      return    

    center_pos = [334.0, 232.0]
    handles = [[334.0, 232.0], [386.0, 231.0], [282.0, 231.0]]
    fill_color = [92, 176, 252]
    opacity = 0.5
    line_thickness = 2.
    bezier = False
    arrowHeadSize = [20, 20]
    rxn_dash = [5, 10]

    df_update = editSBML._setReactionCenterPosition(self.df, "r_0", center_pos)
    df_update = editSBML._setReactionHandlePositions(df_update, "r_0", handles)
    df_update = editSBML._setReactionFillColor(df_update, "r_0", fill_color, opacity = opacity)
    df_update = editSBML._setReactionLineThickness(df_update, "r_0", line_thickness)
    df_update = editSBML._setBezierReactionType(df_update, "r_0", bezier)
    df_update = editSBML._setReactionArrowHeadSize(df_update, "r_0", arrowHeadSize)
    df_update = editSBML._setReactionDash(df_update, "r_0", rxn_dash)

    self.assertTrue(df_update[2].iloc[0]["center_pos"] == center_pos)
    self.assertTrue(df_update[2].iloc[0]["handles"] == handles)
    self.assertTrue(df_update[2].iloc[0]["fill_color"][0:-1] == fill_color)
    self.assertTrue(df_update[2].iloc[0]["fill_color"][3] == int(opacity*255/1.))
    self.assertTrue(df_update[2].iloc[0]["line_thickness"] == line_thickness)
    self.assertTrue(df_update[2].iloc[0]["bezier"] == bezier)
    self.assertTrue(df_update[2].iloc[0]["arrow_head_size"] == arrowHeadSize)
    self.assertTrue(df_update[2].iloc[0]["rxn_dash"] == rxn_dash)

    with self.assertRaises(Exception):
      editSBML._setReactionCenterPosition(df_update, "XX", center_pos)
      editSBML._setReactionHandlePositions(df_update, "XX", handles)
      editSBML._setReactionFillColor(df_update, "XX", fill_color, opacity = opacity)
      editSBML._setReactionLineThickness(df_update, "XX", line_thickness)
      editSBML._setBezierReactionType(df_update, "XX", bezier)
      editSBML._setReactionArrowHeadSize(df_update, "XX", arrowHeadSize)
      editSBML._setReactionDash(df_update, "XX", rxn_dash)

  def testSetArbitraryText(self):
    # set arbitrary text one by one
    if IGNORE_TEST:
      return

    text_position = [413., 216.]
    text_size = [413., 216.]
    text_font_color = [5,0,0]
    opacity = 1.
    text_line_width = 3.
    text_font_size = 15.

    df_update = editSBML._setTextPosition(self.df_text, "text_content1", text_position)
    df_update = editSBML._setTextSize(df_update, "text_content1", text_size)
    df_update = editSBML._setTextFontColor(df_update, "text_content1", text_font_color, opacity)
    df_update = editSBML._setTextLineWidth(df_update, "text_content2", text_line_width)
    df_update = editSBML._setTextFontSize(df_update, "text_content2", text_font_size)
    
    self.assertTrue(df_update[3].iloc[0]["txt_position"] == text_position)
    self.assertTrue(df_update[3].iloc[0]["txt_size"] == text_size)
    self.assertTrue(df_update[3].iloc[0]["txt_font_color"] == [5,0,0,255])
    self.assertTrue(df_update[3].iloc[1]["txt_line_width"] == text_line_width)
    self.assertTrue(df_update[3].iloc[1]["txt_font_size"] == text_font_size)

    with self.assertRaises(Exception):
      editSBML._setTextPosition(df_update, "XX", text_position)
    with self.assertRaises(Exception):  
      editSBML._setTextSize(df_update, "XX", text_size)
    with self.assertRaises(Exception):
      editSBML._setTextFontColor(df_update, "XX", text_font_color,opacity)
    with self.assertRaises(Exception):  
      editSBML._setTextLineWidth(df_update, "XX", text_line_width)
    with self.assertRaises(Exception):
      editSBML._setTextFontSize(df_update, "XX", text_font_size)

  def testArbitraryText(self):
    # set arbitrary text one by one
    if IGNORE_TEST:
      return

    txt_content = "test1"
    txt_position = [205,216]
    txt_size = [10,10]
    txt_font_color="black" 
    opacity= 1
    txt_line_width=2.
    txt_font_size=13.

    df_text_update = editSBML._addText(self.df_text,txt_content,txt_position,txt_size,txt_font_color,
    opacity,txt_line_width, txt_font_size)
    self.assertTrue(df_text_update[3].iloc[2][processSBML.TXTCONTENT] == txt_content)
    self.assertTrue(df_text_update[3].iloc[2][processSBML.TXTPOSITION] == txt_position)
    self.assertTrue(df_text_update[3].iloc[2][processSBML.TXTSIZE] == txt_size)
    self.assertTrue(df_text_update[3].iloc[2][processSBML.TXTFONTCOLOR] == [0,0,0,255])
    self.assertTrue(df_text_update[3].iloc[2][processSBML.TXTLINEWIDTH] == txt_line_width)
    self.assertTrue(df_text_update[3].iloc[2][processSBML.TXTFONTSIZE] == txt_font_size)

    df_text_update = editSBML._removeText(df_text_update, txt_content)
    self.assertTrue(len(df_text_update[3]) == 2)

    with self.assertRaises(Exception):
      editSBML._removeText(df_text_update, "text")

  # def testText(self):
  #   # set text one by one
  #   if IGNORE_TEST:
  #     return

  #   txt_content = "test1"
  #   txt_position = [205,216]
  #   txt_font_color="black" 
  #   opacity= 1
  #   txt_line_width=2.
  #   txt_font_size=13.

  #   df_text = pd.DataFrame(columns=processSBML.COLUMN_NAME_df_text).copy()
  #   df_text_update = editSBML._addText(df_text,txt_content,txt_position,txt_font_color,
  #   opacity,txt_line_width, txt_font_size)
  #   self.assertTrue(df_text_update.iloc[0][processSBML.ID] == txt_content)
  #   self.assertTrue(df_text_update.iloc[0][processSBML.TXTPOSITION] == txt_position)
  #   self.assertTrue(df_text_update.iloc[0][processSBML.TXTFONTCOLOR] == [0,0,0,255])
  #   self.assertTrue(df_text_update.iloc[0][processSBML.TXTLINEWIDTH] == txt_line_width)
  #   self.assertTrue(df_text_update.iloc[0][processSBML.TXTFONTSIZE] == txt_font_size)

  #   df_text_update = editSBML._removeText(df_text_update, txt_content)
  #   self.assertTrue(len(df_text_update) == 0)

  #   with self.assertRaises(Exception):
  #     editSBML._removeText(df_text_update, "text")


if __name__ == '__main__':
  unittest.main()
