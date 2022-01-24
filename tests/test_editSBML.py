import unittest
import os
from SBMLDiagrams import processSBML
from SBMLDiagrams import editSBML
from pandas.testing import assert_frame_equal

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

    self.df = processSBML._SBMLToDF(sbmlStr_test)

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


  def testSetNode(self):
    # set node one by one
    if IGNORE_TEST:
      return    
    floating_node = True
    position = [412., 216.]
    size = [50., 29.]
    shapeIdx = 2
    txt_position = [412., 216.]
    txt_size = [50., 29.]
    fill_color = [255, 204, 154]
    border_color = [255, 109, 9]
    border_width = 3.
    txt_font_color = [0, 0, 0]
    txt_line_width = 1.
    opacity = 1.

    df_update = editSBML._setFloatingBoundaryNode(self.df, "x_1", floating_node)
    df_update = editSBML._setNodePosition(df_update, "x_1", position)
    df_update = editSBML._setNodeSize(df_update, "x_1", size)
    df_update = editSBML._setNodeShapeIdx(df_update, "x_1", shapeIdx)
    df_update = editSBML._setNodeTextPosition(df_update, "x_1", txt_position)
    df_update = editSBML._setNodeTextSize(df_update, "x_1", txt_size)
    df_update = editSBML._setNodeFillColor(df_update, "x_1", fill_color, opacity = opacity)
    df_update = editSBML._setNodeBorderColor(df_update, "x_1", border_color, opacity = opacity)
    df_update = editSBML._setNodeBorderWidth(df_update, "x_1", border_width)
    df_update = editSBML._setNodeTextFontColor(df_update, "x_1", txt_font_color, opacity = opacity)
    df_update = editSBML._setNodeTextLineWidth(df_update, "x_1", txt_line_width)
    
    self.assertTrue(df_update[1].iloc[0]["floating_node"] == floating_node)
    self.assertTrue(df_update[1].iloc[0]["position"] == position)
    self.assertTrue(df_update[1].iloc[0]["size"] == size)
    self.assertTrue(df_update[1].iloc[0]["shape_idx"] == shapeIdx)
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

    df_update = editSBML._setReactionCenterPosition(self.df, "r_0", center_pos)
    df_update = editSBML._setReactionHandlePositions(df_update, "r_0", handles)
    df_update = editSBML._setReactionFillColor(df_update, "r_0", fill_color, opacity = opacity)
    df_update = editSBML._setReactionLineThickness(df_update, "r_0", line_thickness)
    df_update = editSBML._setBezierReactionType(df_update, "r_0", bezier)

    self.assertTrue(df_update[2].iloc[0]["center_pos"] == center_pos)
    self.assertTrue(df_update[2].iloc[0]["handles"] == handles)
    self.assertTrue(df_update[2].iloc[0]["fill_color"][0:-1] == fill_color)
    self.assertTrue(df_update[2].iloc[0]["fill_color"][3] == int(opacity*255/1.))
    self.assertTrue(df_update[2].iloc[0]["line_thickness"] == line_thickness)
    self.assertTrue(df_update[2].iloc[0]["bezier"] == bezier)


if __name__ == '__main__':
  unittest.main()
