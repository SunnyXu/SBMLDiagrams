import unittest
import os
from SBMLDiagrams import importSBML
from SBMLDiagrams import editSBML
from pandas.testing import assert_frame_equal

IGNORE_TEST = False

#############################
# Tests
#############################
class TestEditSBML(unittest.TestCase):

  def setUp(self):
    DIR = os.path.dirname(os.path.abspath(__file__))
    TEST_FOLDER = os.path.join(DIR, "test_sbml_files")
    TEST_PATH_test = os.path.join(TEST_FOLDER, "test.xml")
    TEST_PATH_feedback = os.path.join(TEST_FOLDER, "feedback.xml")
    TEST_PATH_LinearChain = os.path.join(TEST_FOLDER, "LinearChain.xml")
    TEST_PATH_test_no_comp = os.path.join(TEST_FOLDER, "test_no_comp.xml")
    TEST_PATH_test_comp = os.path.join(TEST_FOLDER, "test_comp.xml")
    TEST_PATH_test_modifier = os.path.join(TEST_FOLDER, "test_modifier.xml")
    f_test = open(TEST_PATH_test, 'r')
    sbmlStr_test = f_test.read()
    f_test.close()
    f_feedback = open(TEST_PATH_feedback, 'r')
    sbmlStr_feedback = f_feedback.read()
    f_feedback.close()
    f_LinearChain = open(TEST_PATH_LinearChain, 'r')
    sbmlStr_LinearChain = f_LinearChain.read()
    f_LinearChain.close()
    f_test_no_comp = open(TEST_PATH_test_no_comp, 'r')
    sbmlStr_test_no_comp = f_test_no_comp.read()
    f_test_no_comp.close()
    f_test_comp = open(TEST_PATH_test_comp, 'r')
    sbmlStr_test_comp = f_test_comp.read()
    f_test_comp.close()
    f_test_modifier = open(TEST_PATH_test_modifier, 'r')
    sbmlStr_test_modifier = f_test_modifier.read()
    f_test_modifier.close()
    self.df_CompartmentData, self.df_NodeData, self.df_ReactionData = \
      importSBML.load(sbmlStr_test)
    self.df = importSBML.load(sbmlStr_test)
    self.df_CompartmentData_feedback, self.df_NodeData_feedback, self.df_ReactionData_feedback = \
      importSBML.load(sbmlStr_feedback)
    self.df_CompartmentData_LinearChain, self.df_NodeData_LinearChain, self.df_ReactionData_LinearChain = \
      importSBML.load(sbmlStr_LinearChain)
    self.df_CompartmentData_test_no_comp, self.df_NodeData_test_no_comp, self.df_ReactionData_test_no_comp = \
      importSBML.load(sbmlStr_test_no_comp)
    self.df_CompartmentData_test_comp, self.df_NodeData_test_comp, self.df_ReactionData_test_comp = \
      importSBML.load(sbmlStr_test_comp)
    self.df_CompartmentData_test_modifier, self.df_NodeData_test_modifier, self.df_ReactionData_test_modifier = \
      importSBML.load(sbmlStr_test_modifier)
  def testSetCompartment1(self):
    # setCompartment without editing anything but using default
    if IGNORE_TEST:
      return    
    df_CompartmentData_update = editSBML.setCompartment(self.df_CompartmentData, 0)
    df_CompartmentData_feedback_update = editSBML.setCompartment(self.df_CompartmentData_feedback, 0)
    df_CompartmentData_LinearChain_update = \
      editSBML.setCompartment(self.df_CompartmentData_LinearChain, 0)
    df_CompartmentData_test_no_comp_update = \
      editSBML.setCompartment(self.df_CompartmentData_test_no_comp, 0)
    df_CompartmentData_test_comp_update = \
      editSBML.setCompartment(self.df_CompartmentData_test_comp, 0)
    df_CompartmentData_test_modifier_update = \
      editSBML.setCompartment(self.df_CompartmentData_test_modifier, 0)

    self.assertTrue(df_CompartmentData_update.equals(self.df_CompartmentData))
    self.assertTrue(df_CompartmentData_feedback_update.equals(self.df_CompartmentData_feedback))
    self.assertTrue(df_CompartmentData_LinearChain_update.equals(self.df_CompartmentData_LinearChain))
    self.assertTrue(df_CompartmentData_test_no_comp_update.equals(self.df_CompartmentData_test_no_comp))
    self.assertTrue(df_CompartmentData_test_comp_update.equals(self.df_CompartmentData_test_comp))
    self.assertTrue(df_CompartmentData_test_modifier_update.equals(self.df_CompartmentData_test_modifier))

  def testSetCompartment2(self):
    # setCompartment with editing each parameter
    if IGNORE_TEST:
      return  
    idx = 0
    position_update = [0., 0.]
    size_update = [1000., 1000.]
    fill_color_update = [0., 0., 0.]
    border_color_update = [0., 0., 0.]
    border_width_update = 1.
    df_CompartmentData_update = editSBML.setCompartment(self.df_CompartmentData, idx, \
        position = position_update, size = size_update, fill_color = fill_color_update, \
        border_color = border_color_update, border_width = border_width_update) 
    self.assertTrue(df_CompartmentData_update.at[idx,"position"] == position_update) 
    self.assertTrue(df_CompartmentData_update.at[idx,"size"] == size_update) 
    self.assertTrue(df_CompartmentData_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_CompartmentData_update.at[idx,"border_color"] == border_color_update) 
    self.assertTrue(df_CompartmentData_update.at[idx,"border_width"] == border_width_update) 
    df_CompartmentData_feedback_update = editSBML.setCompartment(self.df_CompartmentData_feedback, idx, \
        position = position_update, size = size_update, fill_color = fill_color_update, \
        border_color = border_color_update, border_width = border_width_update) 
    self.assertTrue(df_CompartmentData_feedback_update.at[idx,"position"] == position_update) 
    self.assertTrue(df_CompartmentData_feedback_update.at[idx,"size"] == size_update) 
    self.assertTrue(df_CompartmentData_feedback_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_CompartmentData_feedback_update.at[idx,"border_color"] == border_color_update) 
    self.assertTrue(df_CompartmentData_feedback_update.at[idx,"border_width"] == border_width_update)
    df_CompartmentData_LinearChain_update = editSBML.setCompartment(self.df_CompartmentData_LinearChain, idx, \
        position = position_update, size = size_update, fill_color = fill_color_update, \
        border_color = border_color_update, border_width = border_width_update) 
    self.assertTrue(df_CompartmentData_LinearChain_update.at[idx,"position"] == position_update) 
    self.assertTrue(df_CompartmentData_LinearChain_update.at[idx,"size"] == size_update) 
    self.assertTrue(df_CompartmentData_LinearChain_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_CompartmentData_LinearChain_update.at[idx,"border_color"] == border_color_update) 
    self.assertTrue(df_CompartmentData_LinearChain_update.at[idx,"border_width"] == border_width_update)
    df_CompartmentData_test_no_comp_update = editSBML.setCompartment(self.df_CompartmentData_test_no_comp, idx, \
        position = position_update, size = size_update, fill_color = fill_color_update, \
        border_color = border_color_update, border_width = border_width_update) 
    self.assertTrue(df_CompartmentData_test_no_comp_update.at[idx,"position"] == position_update) 
    self.assertTrue(df_CompartmentData_test_no_comp_update.at[idx,"size"] == size_update) 
    self.assertTrue(df_CompartmentData_test_no_comp_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_CompartmentData_test_no_comp_update.at[idx,"border_color"] == border_color_update) 
    self.assertTrue(df_CompartmentData_test_no_comp_update.at[idx,"border_width"] == border_width_update)
    df_CompartmentData_test_comp_update = editSBML.setCompartment(self.df_CompartmentData_test_comp, idx, \
        position = position_update, size = size_update, fill_color = fill_color_update, \
        border_color = border_color_update, border_width = border_width_update) 
    self.assertTrue(df_CompartmentData_test_comp_update.at[idx,"position"] == position_update) 
    self.assertTrue(df_CompartmentData_test_comp_update.at[idx,"size"] == size_update) 
    self.assertTrue(df_CompartmentData_test_comp_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_CompartmentData_test_comp_update.at[idx,"border_color"] == border_color_update) 
    self.assertTrue(df_CompartmentData_test_comp_update.at[idx,"border_width"] == border_width_update)
    df_CompartmentData_test_modifier_update = editSBML.setCompartment(self.df_CompartmentData_test_modifier, idx, \
        position = position_update, size = size_update, fill_color = fill_color_update, \
        border_color = border_color_update, border_width = border_width_update) 
    self.assertTrue(df_CompartmentData_test_modifier_update.at[idx,"position"] == position_update) 
    self.assertTrue(df_CompartmentData_test_modifier_update.at[idx,"size"] == size_update) 
    self.assertTrue(df_CompartmentData_test_modifier_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_CompartmentData_test_modifier_update.at[idx,"border_color"] == border_color_update) 
    self.assertTrue(df_CompartmentData_test_modifier_update.at[idx,"border_width"] == border_width_update)

  def testSetCompartment3(self):
    # setCompartment one by one
    if IGNORE_TEST:
      return    
    position = [1, 0]
    size = [900, 900]
    fill_color = [255, 255, 254]
    border_color = [255, 255, 254]
    border_width = 2.

    df_update = editSBML.setCompartmentPosition(self.df, 0, position)
    df_update = editSBML.setCompartmentSize(df_update, 0, size)
    df_update = editSBML.setCompartmentFillColor(df_update, 0, fill_color)
    df_update = editSBML.setCompartmentBorderColor(df_update, 0, border_color)
    df_update = editSBML.setCompartmentBorderWidth(df_update, 0, border_width)

    self.assertTrue(importSBML.getCompartmentPosition(df_update, 0) == position)
    self.assertTrue(importSBML.getCompartmentSize(df_update, 0) == size)
    self.assertTrue(importSBML.getCompartmentFillColor(df_update, 0) == fill_color)
    self.assertTrue(importSBML.getCompartmentBorderColor(df_update, 0) == border_color)
    self.assertTrue(importSBML.getCompartmentBorderWidth(df_update, 0) == border_width)


  def testSetNode1(self):
    # setCompartment without editing anything but using default
    if IGNORE_TEST:
      return    
    df_NodeData_update = editSBML.setNode(self.df_NodeData, 0)
    df_NodeData_feedback_update = editSBML.setNode(self.df_NodeData_feedback, 0)
    df_NodeData_LinearChain_update = editSBML.setNode(self.df_NodeData_LinearChain, 0)
    df_NodeData_test_no_comp_update = editSBML.setNode(self.df_NodeData_test_no_comp, 0)
    df_NodeData_test_comp_update = editSBML.setNode(self.df_NodeData_test_comp, 0)
    df_NodeData_test_modifier_update = editSBML.setNode(self.df_NodeData_test_modifier, 0)
    self.assertTrue(df_NodeData_update.equals(self.df_NodeData))
    self.assertTrue(df_NodeData_feedback_update.equals(self.df_NodeData_feedback))
    self.assertTrue(df_NodeData_LinearChain_update.equals(self.df_NodeData_LinearChain))
    self.assertTrue(df_NodeData_test_no_comp_update.equals(self.df_NodeData_test_no_comp))
    self.assertTrue(df_NodeData_test_comp_update.equals(self.df_NodeData_test_comp))
    self.assertTrue(df_NodeData_test_modifier_update.equals(self.df_NodeData_test_modifier))

  def testSetNode2(self):
    # setCompartment with editing each parameter
    if IGNORE_TEST:
      return 
    idx = 0
    floating_node_update = False
    position_update = [0., 0.]
    size_update = [30., 20.]
    shape_idx_update = 2
    txt_position_update = [0., 0.]
    txt_size_update = [30., 20.]
    fill_color_update = [0., 0., 0.]
    border_color_update = [0., 0., 0.]
    border_width_update = 1.
    txt_font_color_update = [255, 255, 255]
    txt_line_width_update = 2.
    df_NodeData_update = editSBML.setNode(self.df_NodeData, idx, floating_node = floating_node_update, \
        position = position_update, size = size_update, shape_idx = shape_idx_update,\
        txt_position = txt_position_update, txt_size = txt_size_update, \
        fill_color = fill_color_update, border_color = border_color_update, border_width = border_width_update, \
        txt_font_color = txt_font_color_update, txt_line_width = txt_line_width_update) 
    self.assertTrue(df_NodeData_update.at[idx,"floating_node"] == floating_node_update)  
    self.assertTrue(df_NodeData_update.at[idx,"position"] == position_update) 
    self.assertTrue(df_NodeData_update.at[idx,"size"] == size_update) 
    self.assertTrue(df_NodeData_update.at[idx,"shape_idx"] == shape_idx_update) 
    self.assertTrue(df_NodeData_update.at[idx,"txt_position"] == txt_position_update) 
    self.assertTrue(df_NodeData_update.at[idx,"txt_size"] == txt_size_update) 
    self.assertTrue(df_NodeData_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_NodeData_update.at[idx,"border_color"] == border_color_update) 
    self.assertTrue(df_NodeData_update.at[idx,"border_width"] == border_width_update)
    self.assertTrue(df_NodeData_update.at[idx,"txt_font_color"] == txt_font_color_update) 
    self.assertTrue(df_NodeData_update.at[idx,"txt_line_width"] == txt_line_width_update) 
    df_NodeData_feedback_update = editSBML.setNode(self.df_NodeData_feedback, idx, floating_node = floating_node_update, \
        position = position_update, size = size_update, shape_idx = shape_idx_update,\
        txt_position = txt_position_update, txt_size = txt_size_update, \
        fill_color = fill_color_update, border_color = border_color_update, border_width = border_width_update, \
        txt_font_color = txt_font_color_update, txt_line_width = txt_line_width_update) 
    self.assertTrue(df_NodeData_feedback_update.at[idx,"floating_node"] == floating_node_update)  
    self.assertTrue(df_NodeData_feedback_update.at[idx,"position"] == position_update) 
    self.assertTrue(df_NodeData_feedback_update.at[idx,"size"] == size_update) 
    self.assertTrue(df_NodeData_feedback_update.at[idx,"shape_idx"] == shape_idx_update) 
    self.assertTrue(df_NodeData_feedback_update.at[idx,"txt_position"] == txt_position_update) 
    self.assertTrue(df_NodeData_feedback_update.at[idx,"txt_size"] == txt_size_update) 
    self.assertTrue(df_NodeData_feedback_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_NodeData_feedback_update.at[idx,"border_color"] == border_color_update) 
    self.assertTrue(df_NodeData_feedback_update.at[idx,"border_width"] == border_width_update)
    self.assertTrue(df_NodeData_feedback_update.at[idx,"txt_font_color"] == txt_font_color_update) 
    self.assertTrue(df_NodeData_feedback_update.at[idx,"txt_line_width"] == txt_line_width_update) 
    df_NodeData_LinearChain_update = editSBML.setNode(self.df_NodeData_LinearChain, idx, floating_node = floating_node_update, \
        position = position_update, size = size_update, shape_idx = shape_idx_update,\
        txt_position = txt_position_update, txt_size = txt_size_update, \
        fill_color = fill_color_update, border_color = border_color_update, border_width = border_width_update, \
        txt_font_color = txt_font_color_update, txt_line_width = txt_line_width_update) 
    self.assertTrue(df_NodeData_LinearChain_update.at[idx,"floating_node"] == floating_node_update)  
    self.assertTrue(df_NodeData_LinearChain_update.at[idx,"position"] == position_update) 
    self.assertTrue(df_NodeData_LinearChain_update.at[idx,"size"] == size_update) 
    self.assertTrue(df_NodeData_LinearChain_update.at[idx,"shape_idx"] == shape_idx_update) 
    self.assertTrue(df_NodeData_LinearChain_update.at[idx,"txt_position"] == txt_position_update) 
    self.assertTrue(df_NodeData_LinearChain_update.at[idx,"txt_size"] == txt_size_update) 
    self.assertTrue(df_NodeData_LinearChain_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_NodeData_LinearChain_update.at[idx,"border_color"] == border_color_update) 
    self.assertTrue(df_NodeData_LinearChain_update.at[idx,"border_width"] == border_width_update)
    self.assertTrue(df_NodeData_LinearChain_update.at[idx,"txt_font_color"] == txt_font_color_update) 
    self.assertTrue(df_NodeData_LinearChain_update.at[idx,"txt_line_width"] == txt_line_width_update) 
    df_NodeData_test_no_comp_update = editSBML.setNode(self.df_NodeData_test_no_comp, idx, floating_node = floating_node_update, \
        position = position_update, size = size_update, shape_idx = shape_idx_update,\
        txt_position = txt_position_update, txt_size = txt_size_update, \
        fill_color = fill_color_update, border_color = border_color_update, border_width = border_width_update, \
        txt_font_color = txt_font_color_update, txt_line_width = txt_line_width_update) 
    self.assertTrue(df_NodeData_test_no_comp_update.at[idx,"floating_node"] == floating_node_update)  
    self.assertTrue(df_NodeData_test_no_comp_update.at[idx,"position"] == position_update) 
    self.assertTrue(df_NodeData_test_no_comp_update.at[idx,"size"] == size_update) 
    self.assertTrue(df_NodeData_test_no_comp_update.at[idx,"shape_idx"] == shape_idx_update) 
    self.assertTrue(df_NodeData_test_no_comp_update.at[idx,"txt_position"] == txt_position_update) 
    self.assertTrue(df_NodeData_test_no_comp_update.at[idx,"txt_size"] == txt_size_update) 
    self.assertTrue(df_NodeData_test_no_comp_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_NodeData_test_no_comp_update.at[idx,"border_color"] == border_color_update) 
    self.assertTrue(df_NodeData_test_no_comp_update.at[idx,"border_width"] == border_width_update)
    self.assertTrue(df_NodeData_test_no_comp_update.at[idx,"txt_font_color"] == txt_font_color_update) 
    self.assertTrue(df_NodeData_test_no_comp_update.at[idx,"txt_line_width"] == txt_line_width_update) 
    df_NodeData_test_comp_update = editSBML.setNode(self.df_NodeData_test_comp, idx, floating_node = floating_node_update, \
        position = position_update, size = size_update, shape_idx = shape_idx_update,\
        txt_position = txt_position_update, txt_size = txt_size_update, \
        fill_color = fill_color_update, border_color = border_color_update, border_width = border_width_update, \
        txt_font_color = txt_font_color_update, txt_line_width = txt_line_width_update) 
    self.assertTrue(df_NodeData_test_comp_update.at[idx,"floating_node"] == floating_node_update)  
    self.assertTrue(df_NodeData_test_comp_update.at[idx,"position"] == position_update) 
    self.assertTrue(df_NodeData_test_comp_update.at[idx,"size"] == size_update) 
    self.assertTrue(df_NodeData_test_comp_update.at[idx,"shape_idx"] == shape_idx_update) 
    self.assertTrue(df_NodeData_test_comp_update.at[idx,"txt_position"] == txt_position_update) 
    self.assertTrue(df_NodeData_test_comp_update.at[idx,"txt_size"] == txt_size_update) 
    self.assertTrue(df_NodeData_test_comp_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_NodeData_test_comp_update.at[idx,"border_color"] == border_color_update) 
    self.assertTrue(df_NodeData_test_comp_update.at[idx,"border_width"] == border_width_update)
    self.assertTrue(df_NodeData_test_comp_update.at[idx,"txt_font_color"] == txt_font_color_update) 
    self.assertTrue(df_NodeData_test_comp_update.at[idx,"txt_line_width"] == txt_line_width_update) 
    df_NodeData_test_modifier_update = editSBML.setNode(self.df_NodeData_test_modifier, idx, floating_node = floating_node_update, \
        position = position_update, size = size_update, shape_idx = shape_idx_update,\
        txt_position = txt_position_update, txt_size = txt_size_update, \
        fill_color = fill_color_update, border_color = border_color_update, border_width = border_width_update, \
        txt_font_color = txt_font_color_update, txt_line_width = txt_line_width_update) 
    self.assertTrue(df_NodeData_test_modifier_update.at[idx,"floating_node"] == floating_node_update)  
    self.assertTrue(df_NodeData_test_modifier_update.at[idx,"position"] == position_update) 
    self.assertTrue(df_NodeData_test_modifier_update.at[idx,"size"] == size_update) 
    self.assertTrue(df_NodeData_test_modifier_update.at[idx,"shape_idx"] == shape_idx_update) 
    self.assertTrue(df_NodeData_test_modifier_update.at[idx,"txt_position"] == txt_position_update) 
    self.assertTrue(df_NodeData_test_modifier_update.at[idx,"txt_size"] == txt_size_update) 
    self.assertTrue(df_NodeData_test_modifier_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_NodeData_test_modifier_update.at[idx,"border_color"] == border_color_update) 
    self.assertTrue(df_NodeData_test_modifier_update.at[idx,"border_width"] == border_width_update)
    self.assertTrue(df_NodeData_test_modifier_update.at[idx,"txt_font_color"] == txt_font_color_update) 
    self.assertTrue(df_NodeData_test_modifier_update.at[idx,"txt_line_width"] == txt_line_width_update) 


  def testSetNode3(self):
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

    df_update = editSBML.setFloatingBoundaryNode(self.df, 0, floating_node)
    df_update = editSBML.setNodePosition(df_update, 0, position)
    df_update = editSBML.setNodeSize(df_update, 0, size)
    df_update = editSBML.setNodeShapeIdx(df_update, 0, shapeIdx)
    df_update = editSBML.setNodeTextPosition(df_update, 0, txt_position)
    df_update = editSBML.setNodeTextSize(df_update, 0, txt_size)
    df_update = editSBML.setNodeFillColor(df_update, 0, fill_color)
    df_update = editSBML.setNodeBorderColor(df_update, 0, border_color)
    df_update = editSBML.setNodeBorderWidth(df_update, 0, border_width)
    df_update = editSBML.setNodeTextFontColor(df_update, 0, txt_font_color)
    df_update = editSBML.setNodeTextLineWidth(df_update, 0, txt_line_width)
    
    self.assertTrue(importSBML.isFloatingNode(df_update, 0) == floating_node)
    self.assertTrue(importSBML.getNodePosition(df_update, 0) == position)
    self.assertTrue(importSBML.getNodeSize(df_update, 0) == size)
    self.assertTrue(importSBML.getNodeShape(df_update, 0)[0] == shapeIdx)
    self.assertTrue(importSBML.getNodeTextPosition(df_update, 0) == txt_position)
    self.assertTrue(importSBML.getNodeTextSize(df_update, 0) == txt_size)
    self.assertTrue(importSBML.getNodeFillColor(df_update, 0) == fill_color)
    self.assertTrue(importSBML.getNodeBorderColor(df_update, 0) == border_color)
    self.assertTrue(importSBML.getNodeBorderWidth(df_update, 0) == border_width)
    self.assertTrue(importSBML.getNodeTextFontColor(df_update, 0) == txt_font_color)
    self.assertTrue(importSBML.getNodeTextLineWidth(df_update, 0) == txt_line_width)

  def testSetReaction1(self):
    # setReaction without editing anything but using default
    if IGNORE_TEST:
      return    
    df_ReactionData_update = editSBML.setReaction(self.df_ReactionData, 0)
    df_ReactionData_feedback_update = editSBML.setReaction(self.df_ReactionData_feedback, 0)
    df_ReactionData_LinearChain_update = editSBML.setReaction(self.df_ReactionData_LinearChain, 0)
    df_ReactionData_test_no_comp_update = editSBML.setReaction(self.df_ReactionData_test_no_comp, 0)
    df_ReactionData_test_comp_update = editSBML.setReaction(self.df_ReactionData_test_comp, 0)
    df_ReactionData_test_modifier_update = editSBML.setReaction(self.df_ReactionData_test_modifier, 0)
    self.assertTrue(df_ReactionData_update.equals(self.df_ReactionData))
    self.assertTrue(df_ReactionData_feedback_update.equals(self.df_ReactionData_feedback))
    self.assertTrue(df_ReactionData_LinearChain_update.equals(self.df_ReactionData_LinearChain))
    self.assertTrue(df_ReactionData_test_no_comp_update.equals(self.df_ReactionData_test_no_comp))
    self.assertTrue(df_ReactionData_test_comp_update.equals(self.df_ReactionData_test_comp))
    self.assertTrue(df_ReactionData_test_modifier_update.equals(self.df_ReactionData_test_modifier))

  def testSetReaction2(self):
    # setCompartment with editing each parameter
    if IGNORE_TEST:
      return  
    idx = 0
    fill_color_update = [0., 0., 0.]
    line_thickness_update = 1.
    bezier_update = False
    df_ReactionData_update = editSBML.setReaction(self.df_ReactionData, idx, \
        fill_color = fill_color_update, line_thickness = line_thickness_update, \
        bezier = bezier_update)  
    self.assertTrue(df_ReactionData_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_ReactionData_update.at[idx,"line_thickness"] == line_thickness_update) 
    self.assertTrue(df_ReactionData_update.at[idx,"bezier"] == bezier_update)
    df_ReactionData_feedback_update = editSBML.setReaction(self.df_ReactionData_feedback, idx, \
        fill_color = fill_color_update, line_thickness = line_thickness_update, \
        bezier = bezier_update)  
    self.assertTrue(df_ReactionData_feedback_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_ReactionData_feedback_update.at[idx,"line_thickness"] == line_thickness_update) 
    self.assertTrue(df_ReactionData_feedback_update.at[idx,"bezier"] == bezier_update)  
    df_ReactionData_LinearChain_update = editSBML.setReaction(self.df_ReactionData_LinearChain, idx, \
        fill_color = fill_color_update, line_thickness = line_thickness_update, \
        bezier = bezier_update)  
    self.assertTrue(df_ReactionData_LinearChain_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_ReactionData_LinearChain_update.at[idx,"line_thickness"] == line_thickness_update) 
    self.assertTrue(df_ReactionData_LinearChain_update.at[idx,"bezier"] == bezier_update)  
    df_ReactionData_test_no_comp_update = editSBML.setReaction(self.df_ReactionData_test_no_comp, idx, \
        fill_color = fill_color_update, line_thickness = line_thickness_update, \
        bezier = bezier_update)  
    self.assertTrue(df_ReactionData_test_no_comp_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_ReactionData_test_no_comp_update.at[idx,"line_thickness"] == line_thickness_update) 
    self.assertTrue(df_ReactionData_test_no_comp_update.at[idx,"bezier"] == bezier_update) 
    df_ReactionData_test_comp_update = editSBML.setReaction(self.df_ReactionData_test_comp, idx, \
        fill_color = fill_color_update, line_thickness = line_thickness_update, \
        bezier = bezier_update)  
    self.assertTrue(df_ReactionData_test_comp_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_ReactionData_test_comp_update.at[idx,"line_thickness"] == line_thickness_update) 
    self.assertTrue(df_ReactionData_test_comp_update.at[idx,"bezier"] == bezier_update) 
    df_ReactionData_test_modifier_update = editSBML.setReaction(self.df_ReactionData_test_modifier, idx, \
        fill_color = fill_color_update, line_thickness = line_thickness_update, \
        bezier = bezier_update)  
    self.assertTrue(df_ReactionData_test_modifier_update.at[idx,"fill_color"] == fill_color_update) 
    self.assertTrue(df_ReactionData_test_modifier_update.at[idx,"line_thickness"] == line_thickness_update) 
    self.assertTrue(df_ReactionData_test_modifier_update.at[idx,"bezier"] == bezier_update) 

  def testSetReaction3(self):
    # set reaction one by one
    if IGNORE_TEST:
      return    

    fill_color = [92, 176, 252]
    line_thickness = 2.
    bezier = False

    df_update = editSBML.setReactionFillColor(self.df, 0, fill_color)
    df_update = editSBML.setReactionLineThickness(df_update, 0, line_thickness)
    df_update = editSBML.setBezierReactionType(df_update, 0., bezier)

    self.assertTrue(importSBML.getReactionFillColor(df_update, 0) == fill_color)
    self.assertTrue(importSBML.getReactionLineThickness(df_update, 0) == line_thickness)
    self.assertTrue(importSBML.isBezierReactionType(df_update, 0) == bezier)


if __name__ == '__main__':
  unittest.main()