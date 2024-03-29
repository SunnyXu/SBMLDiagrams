import unittest
import os
import SBMLDiagrams
from SBMLDiagrams.processSBML import *
from SBMLDiagrams.processSBML import _SBMLToDF
from SBMLDiagrams import point

IGNORE_TEST = False

#############################
# Tests
#############################
class TestImportSBML(unittest.TestCase):
#tests for _SBMLToDF, get, set, export in importSBML module

  def setUp(self):

    DIR = os.path.dirname(os.path.abspath(__file__))
    TEST_FOLDER = os.path.join(DIR, "test_sbml_files")
    TEST_PATH_test = os.path.join(TEST_FOLDER, "test.xml")
    TEST_PATH_feedback = os.path.join(TEST_FOLDER, "feedback.xml")
    TEST_PATH_LinearChain = os.path.join(TEST_FOLDER, "LinearChain.xml")
    TEST_PATH_test_no_comp = os.path.join(TEST_FOLDER, "test_no_comp.xml")
    TEST_PATH_test_comp = os.path.join(TEST_FOLDER, "test_comp.xml")
    TEST_PATH_test_modifier = os.path.join(TEST_FOLDER, "test_modifier.xml")
    TEST_PATH_node_grid = os.path.join(TEST_FOLDER, "node_grid.xml")
    TEST_PATH_mass_action_rxn = os.path.join(TEST_FOLDER, "mass_action_rxn.xml")
    TEST_PATH_test_textGlyph = os.path.join(TEST_FOLDER, "test_textGlyph.xml")
    TEST_PATH_test_genGlyph = os.path.join(TEST_FOLDER, "test_genGlyph.xml")
    TEST_PATH_test_lineEnding = os.path.join(TEST_FOLDER, "pdmap-nucleoid.xml")

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
    f_node_grid = open(TEST_PATH_node_grid, 'r')
    sbmlStr_node_grid = f_node_grid.read()
    f_node_grid.close()
    f_mass_action_rxn = open(TEST_PATH_mass_action_rxn, 'r')
    sbmlStr_mass_action_rxn = f_mass_action_rxn.read()
    f_mass_action_rxn.close()
    f_test_textGlyph = open(TEST_PATH_test_textGlyph, 'r')
    sbmlStr_test_textGlyph = f_test_textGlyph.read()
    f_test_textGlyph.close()
    f_test_genGlyph = open(TEST_PATH_test_genGlyph, 'r')
    sbmlStr_test_genGlyph = f_test_genGlyph.read()
    f_test_genGlyph.close()
    f_test_lineEnding = open(TEST_PATH_test_lineEnding, 'r')
    sbmlStr_test_lineEnding = f_test_lineEnding.read()
    f_test_lineEnding.close()
    self.df_CompartmentData, self.df_NodeData, self.df_ReactionData, _, _, _, _ = _SBMLToDF(sbmlStr_test)
    self.df_CompartmentData_feedback, self.df_NodeData_feedback, self.df_ReactionData_feedback, _, _, _, _ = \
      _SBMLToDF(sbmlStr_feedback)
    self.df_CompartmentData_LinearChain, self.df_NodeData_LinearChain, self.df_ReactionData_LinearChain, _ , _, _, _= \
      _SBMLToDF(sbmlStr_LinearChain)
    self.df_CompartmentData_test_no_comp, self.df_NodeData_test_no_comp, self.df_ReactionData_test_no_comp, _, _, _, _ = \
      _SBMLToDF(sbmlStr_test_no_comp)
    self.df_CompartmentData_test_comp, self.df_NodeData_test_comp, self.df_ReactionData_test_comp, _, _ , _, _= \
      _SBMLToDF(sbmlStr_test_comp)
    self.df_CompartmentData_test_modifier, self.df_NodeData_test_modifier, self.df_ReactionData_test_modifier, _, _, _, _ = \
      _SBMLToDF(sbmlStr_test_modifier)
    self.df_CompartmentData_node_grid, self.df_NodeData_node_grid, self.df_ReactionData_node_grid, _, _, _, _= \
      _SBMLToDF(sbmlStr_node_grid)
    self.df_CompartmentData_mass_action_rxn, self.df_NodeData_mass_action_rxn, self.df_ReactionData_mass_action_rxn, _, _, _, _ = \
      _SBMLToDF(sbmlStr_mass_action_rxn)
    _, _, _, self.df_TextData_test_textGlyph, _, _, _ = _SBMLToDF(sbmlStr_test_textGlyph)
    _, _, _, _, self.df_ShapeData_test_genGlyph, _, _ = _SBMLToDF(sbmlStr_test_genGlyph)
    self.df = SBMLDiagrams.load(sbmlStr_test)
    self.df_text = SBMLDiagrams.load(sbmlStr_test_textGlyph)
    self.df_shape = SBMLDiagrams.load(sbmlStr_test_genGlyph)
    self.df_lineEnding = SBMLDiagrams.load(sbmlStr_test_lineEnding)

  def loadInvalidStr(self):
    # an exception raises if load an invalid string
    if IGNORE_TEST:
      return   
       
    with self.assertRaises(Exception):
      load("aba")


  def testCompartment1(self):
    # Test all the column names
    if IGNORE_TEST:
      return    
    test = all(item in self.df_CompartmentData.columns \
      for item in COLUMN_NAME_df_CompartmentData)
    test_feedback = all(item in self.df_CompartmentData_feedback.columns \
      for item in COLUMN_NAME_df_CompartmentData)
    test_LinearChain = all(item in self.df_CompartmentData_LinearChain.columns \
      for item in COLUMN_NAME_df_CompartmentData)
    test_no_comp = all(item in self.df_CompartmentData_test_no_comp.columns \
      for item in COLUMN_NAME_df_CompartmentData)
    test_comp = all(item in self.df_CompartmentData_test_comp.columns \
      for item in COLUMN_NAME_df_CompartmentData)
    test_modifier = all(item in self.df_CompartmentData_test_modifier.columns \
      for item in COLUMN_NAME_df_CompartmentData)
    test_node_grid = all(item in self.df_CompartmentData_node_grid.columns \
      for item in COLUMN_NAME_df_CompartmentData)
    test_mass_action_rxn = all(item in self.df_CompartmentData_mass_action_rxn.columns \
      for item in COLUMN_NAME_df_CompartmentData)
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)
    self.assertTrue(test_node_grid)
    self.assertTrue(test_mass_action_rxn)

  def testCompartment2(self):
    # Test whether there is at least one row
    if IGNORE_TEST:
      return    
    self.assertTrue(len(self.df_CompartmentData.index)>0) 
    self.assertTrue(len(self.df_CompartmentData_feedback.index)>0)
    self.assertTrue(len(self.df_CompartmentData_LinearChain.index)>0)
    self.assertTrue(len(self.df_CompartmentData_test_no_comp.index)>0)
    self.assertTrue(len(self.df_CompartmentData_test_comp.index)>0)
    self.assertTrue(len(self.df_CompartmentData_test_modifier.index)>0)
    self.assertTrue(len(self.df_CompartmentData_node_grid.index)>0)
    self.assertTrue(len(self.df_CompartmentData_mass_action_rxn.index)>0)

  def testCompartment3(self):
    # Test column 'net_idx' and 'idx' of df_CompartmentData are integers
    if IGNORE_TEST:
      return    
    list_compartment = []
    list_compartment += self.df_CompartmentData[COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment += self.df_CompartmentData[COLUMN_NAME_df_CompartmentData[1]].tolist()
    test = all(isinstance(item, int) for item in list_compartment)
    list_compartment_feedback = []
    list_compartment_feedback += self.df_CompartmentData_feedback[COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_feedback += self.df_CompartmentData_feedback[COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_feedback = all(isinstance(item, int) for item in list_compartment_feedback)
    list_compartment_LinearChain = []
    list_compartment_LinearChain += self.df_CompartmentData_LinearChain[COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_LinearChain += self.df_CompartmentData_LinearChain[COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_LinearChain = all(isinstance(item, int) for item in list_compartment_LinearChain)
    list_compartment_test_no_comp = []
    list_compartment_test_no_comp += self.df_CompartmentData_test_no_comp[COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_test_no_comp += self.df_CompartmentData_test_no_comp[COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_no_comp = all(isinstance(item, int) for item in list_compartment_test_no_comp)
    list_compartment_test_comp = []
    list_compartment_test_comp += self.df_CompartmentData_test_comp[COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_test_comp += self.df_CompartmentData_test_comp[COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_comp = all(isinstance(item, int) for item in list_compartment_test_comp)
    list_compartment_test_modifier = []
    list_compartment_test_modifier += self.df_CompartmentData_test_modifier[COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_test_modifier += self.df_CompartmentData_test_modifier[COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_modifier = all(isinstance(item, int) for item in list_compartment_test_modifier)
    list_compartment_node_grid = []
    list_compartment_node_grid += self.df_CompartmentData_node_grid[COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_node_grid += self.df_CompartmentData_node_grid[COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_node_grid = all(isinstance(item, int) for item in list_compartment_node_grid)
    list_compartment_mass_action_rxn = []
    list_compartment_mass_action_rxn += self.df_CompartmentData_mass_action_rxn[COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_mass_action_rxn += self.df_CompartmentData_mass_action_rxn[COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_mass_action_rxn = all(isinstance(item, int) for item in list_compartment_mass_action_rxn)
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)
    self.assertTrue(test_node_grid)
    self.assertTrue(test_mass_action_rxn)


  def testCompartment4(self):
    # Test column 'id' of df_CompartmentData is string
    if IGNORE_TEST:
      return    
    list_compartment = []
    list_compartment += self.df_CompartmentData[COLUMN_NAME_df_CompartmentData[2]].tolist()
    test = all(isinstance(item, str) for item in list_compartment)
    list_compartment_feedback = []
    list_compartment_feedback += self.df_CompartmentData_feedback[COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_feedback = all(isinstance(item, str) for item in list_compartment_feedback)
    list_compartment_feedback = []
    list_compartment_feedback += self.df_CompartmentData_feedback[COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_feedback = all(isinstance(item, str) for item in list_compartment_feedback)
    list_compartment_LinearChain = []
    list_compartment_LinearChain += self.df_CompartmentData_LinearChain[COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_LinearChain = all(isinstance(item, str) for item in list_compartment_LinearChain)
    list_compartment_test_no_comp = []
    list_compartment_test_no_comp += self.df_CompartmentData_test_no_comp[COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_no_comp = all(isinstance(item, str) for item in list_compartment_test_no_comp)
    list_compartment_test_comp = []
    list_compartment_test_comp += self.df_CompartmentData_test_comp[COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_comp = all(isinstance(item, str) for item in list_compartment_test_comp)
    list_compartment_test_modifier = []
    list_compartment_test_modifier += self.df_CompartmentData_test_modifier[COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_modifier = all(isinstance(item, str) for item in list_compartment_test_modifier)
    list_compartment_node_grid = []
    list_compartment_node_grid += self.df_CompartmentData_node_grid[COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_node_grid = all(isinstance(item, str) for item in list_compartment_node_grid)
    list_compartment_mass_action_rxn = []
    list_compartment_mass_action_rxn += self.df_CompartmentData_mass_action_rxn[COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_mass_action_rxn = all(isinstance(item, str) for item in list_compartment_mass_action_rxn)
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)
    self.assertTrue(test_node_grid)
    self.assertTrue(test_mass_action_rxn)

  def testCompartment5(self):
    # Test column 'position' 'size' 'fill color' 'border color' of df_CompartmentData are lists
    if IGNORE_TEST:
      return    
    list_compartment = []
    for i in range(3,7):
      list_compartment += self.df_CompartmentData.iloc[:,i].tolist()
    test = all(isinstance(item, list) for item in list_compartment)
    list_compartment_feedback = []
    for i in range(3,7):
      list_compartment_feedback += self.df_CompartmentData_feedback.iloc[:,i].tolist()
    test_feedback = all(isinstance(item, list) for item in list_compartment_feedback)
    list_compartment_LinearChain = []
    for i in range(3,7):
      list_compartment_LinearChain += self.df_CompartmentData_LinearChain.iloc[:,i].tolist()
    test_LinearChain = all(isinstance(item, list) for item in list_compartment_LinearChain)
    list_compartment_test_no_comp = []
    for i in range(3,7):
      list_compartment_test_no_comp += self.df_CompartmentData_test_no_comp.iloc[:,i].tolist()
    test_no_comp = all(isinstance(item, list) for item in list_compartment_test_no_comp)
    list_compartment_test_comp = []
    for i in range(3,7):
      list_compartment_test_comp += self.df_CompartmentData_test_comp.iloc[:,i].tolist()
    test_comp = all(isinstance(item, list) for item in list_compartment_test_comp)
    list_compartment_test_modifier = []
    for i in range(3,7):
      list_compartment_test_modifier += self.df_CompartmentData_test_modifier.iloc[:,i].tolist()
    test_modifier = all(isinstance(item, list) for item in list_compartment_test_modifier)
    list_compartment_node_grid = []
    for i in range(3,7):
      list_compartment_node_grid += self.df_CompartmentData_node_grid.iloc[:,i].tolist()
    test_node_grid = all(isinstance(item, list) for item in list_compartment_node_grid)
    list_compartment_mass_action_rxn = []
    for i in range(3,7):
      list_compartment_mass_action_rxn += self.df_CompartmentData_mass_action_rxn.iloc[:,i].tolist()
    test_mass_action_rxn = all(isinstance(item, list) for item in list_compartment_mass_action_rxn)
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)
    self.assertTrue(test_node_grid)
    self.assertTrue(test_mass_action_rxn)

  def testCompartment6(self):
    # Test column 'border width' of df_CompartmentData is a floating number
    if IGNORE_TEST:
      return    
    list_compartment = []
    list_compartment += self.df_CompartmentData[COLUMN_NAME_df_CompartmentData[7]].tolist()
    test = all(isinstance(item, float) for item in list_compartment)
    list_compartment_feedback = []
    list_compartment_feedback += self.df_CompartmentData_feedback[COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_feedback = all(isinstance(item, float) for item in list_compartment_feedback)
    list_compartment_LinearChain = []
    list_compartment_LinearChain += self.df_CompartmentData_LinearChain[COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_LinearChain = all(isinstance(item, float) for item in list_compartment_LinearChain)
    list_compartment_LinearChain = []
    list_compartment_LinearChain += self.df_CompartmentData_LinearChain[COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_LinearChain = all(isinstance(item, float) for item in list_compartment_LinearChain)
    list_compartment_test_no_comp = []
    list_compartment_test_no_comp += self.df_CompartmentData_test_no_comp[COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_no_comp = all(isinstance(item, float) for item in list_compartment_test_no_comp)
    list_compartment_test_comp = []
    list_compartment_test_comp += self.df_CompartmentData_test_comp[COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_comp = all(isinstance(item, float) for item in list_compartment_test_comp)
    list_compartment_test_modifier = []
    list_compartment_test_modifier += self.df_CompartmentData_test_modifier[COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_modifier = all(isinstance(item, float) for item in list_compartment_test_modifier)
    list_compartment_node_grid = []
    list_compartment_node_grid += self.df_CompartmentData_node_grid[COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_node_grid = all(isinstance(item, float) for item in list_compartment_node_grid)
    list_compartment_mass_action_rxn = []
    list_compartment_mass_action_rxn += self.df_CompartmentData_mass_action_rxn[COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_mass_action_rxn = all(isinstance(item, float) for item in list_compartment_mass_action_rxn)

    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)
    self.assertTrue(test_node_grid)
    self.assertTrue(test_mass_action_rxn)

  def testNode1(self):
    # Test all the column names
    if IGNORE_TEST:
      return    
    test = all(item in self.df_NodeData.columns for item in COLUMN_NAME_df_NodeData)
    test_feedback = all(item in self.df_NodeData_feedback.columns \
      for item in COLUMN_NAME_df_NodeData)
    test_LinearChain = all(item in self.df_NodeData_LinearChain.columns \
      for item in COLUMN_NAME_df_NodeData)
    test_no_comp = all(item in self.df_NodeData_test_no_comp.columns \
      for item in COLUMN_NAME_df_NodeData)
    test_comp = all(item in self.df_NodeData_test_comp.columns \
      for item in COLUMN_NAME_df_NodeData)
    test_modifier = all(item in self.df_NodeData_test_modifier.columns \
      for item in COLUMN_NAME_df_NodeData)
    test_node_grid = all(item in self.df_NodeData_node_grid.columns \
      for item in COLUMN_NAME_df_NodeData)
    test_mass_action_rxn = all(item in self.df_NodeData_mass_action_rxn.columns \
      for item in COLUMN_NAME_df_NodeData)
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)
    self.assertTrue(test_node_grid)
    self.assertTrue(test_mass_action_rxn)

  def testNode2(self):
    # Test whether there is at least one row
    if IGNORE_TEST:
      return    
    self.assertTrue(len(self.df_NodeData.index)>0) 
    self.assertTrue(len(self.df_NodeData_feedback.index)>0)
    self.assertTrue(len(self.df_NodeData_LinearChain.index)>0)
    self.assertTrue(len(self.df_NodeData_test_no_comp.index)>0)
    self.assertTrue(len(self.df_NodeData_test_comp.index)>0)
    self.assertTrue(len(self.df_NodeData_test_modifier.index)>0)
    self.assertTrue(len(self.df_NodeData_node_grid.index)>0)
    self.assertTrue(len(self.df_NodeData_mass_action_rxn.index)>0)

  def testNode3(self):
    # Test column 'net_idx' 'comp_idx' 'idx' 'original_idx' and 'shape_idx' of df_NodeData 
    # are integers
    if IGNORE_TEST:
      return    
    list_node = []
    for i in range(0,3):
      list_node += self.df_NodeData.iloc[:,i].tolist()
    list_node += self.df_NodeData.iloc[:,9].tolist()
    test = all(isinstance(item, int) for item in list_node)
    list_node_feedback = []
    for i in range(0,3):
      list_node_feedback += self.df_NodeData_feedback.iloc[:,i].tolist()
    list_node_feedback += self.df_NodeData_feedback.iloc[:,9].tolist()
    test_feedback = all(isinstance(item, int) for item in list_node_feedback)
    list_node_LinearChain = []
    for i in range(0,3):
      list_node_LinearChain += self.df_NodeData_LinearChain.iloc[:,i].tolist()
    list_node_LinearChain += self.df_NodeData_LinearChain.iloc[:,9].tolist()
    test_LinearChain = all(isinstance(item, int) for item in list_node_LinearChain)
    list_node_test_no_comp = []
    for i in range(0,3):
      list_node_test_no_comp += self.df_NodeData_test_no_comp.iloc[:,i].tolist()
    list_node_test_no_comp += self.df_NodeData_test_no_comp.iloc[:,9].tolist()
    test_no_comp = all(isinstance(item, int) for item in list_node_test_no_comp)
    list_node_test_comp = []
    for i in range(0,3):
      list_node_test_comp += self.df_NodeData_test_comp.iloc[:,i].tolist()
    list_node_test_comp += self.df_NodeData_test_comp.iloc[:,9].tolist()
    test_comp = all(isinstance(item, int) for item in list_node_test_comp)
    list_node_test_modifier = []
    for i in range(0,3):
      list_node_test_modifier += self.df_NodeData_test_modifier.iloc[:,i].tolist()
    list_node_test_modifier += self.df_NodeData_test_modifier.iloc[:,9].tolist()
    test_modifier = all(isinstance(item, int) for item in list_node_test_modifier)
    list_node_node_grid = []
    for i in range(0,3):
      list_node_node_grid += self.df_NodeData_node_grid.iloc[:,i].tolist()
    list_node_node_grid += self.df_NodeData_node_grid.iloc[:,9].tolist()
    test_node_grid = all(isinstance(item, int) for item in list_node_node_grid)
    list_node_mass_action_rxn = []
    for i in range(0,3):
      list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn.iloc[:,i].tolist()
    list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn.iloc[:,9].tolist()
    test_mass_action_rxn = all(isinstance(item, int) for item in list_node_mass_action_rxn)
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)
    self.assertTrue(test_node_grid)
    self.assertTrue(test_mass_action_rxn)


  def testNode4(self):
    # Test column 'position' 'size' 'txt_position' 'txt_size' 'fill color' 'border color'
    #  'txt_font_color' of df_NodeData are lists
    if IGNORE_TEST:
      return    
    list_node = []
    for i in range(7,9):
      list_node += self.df_NodeData.iloc[:,i].tolist()
    for i in range(10,14):
      list_node += self.df_NodeData.iloc[:,i].tolist()
    list_node += self.df_NodeData.iloc[:,15].tolist()
    test = all(isinstance(item, list) for item in list_node)
    list_node_feedback = []
    for i in range(7,9):
      list_node_feedback += self.df_NodeData_feedback.iloc[:,i].tolist()
    for i in range(10,14):
      list_node_feedback += self.df_NodeData_feedback.iloc[:,i].tolist()
    list_node_feedback += self.df_NodeData_feedback.iloc[:,15].tolist()
    test_feedback = all(isinstance(item, list) for item in list_node_feedback)
    list_node_LinearChain = []
    for i in range(7,9):
      list_node_LinearChain += self.df_NodeData_LinearChain.iloc[:,i].tolist()
    for i in range(10,14):
      list_node_LinearChain += self.df_NodeData_LinearChain.iloc[:,i].tolist()
    list_node_LinearChain += self.df_NodeData_LinearChain.iloc[:,15].tolist()
    test_LinearChain = all(isinstance(item, list) for item in list_node_LinearChain)
    list_node_test_no_comp = []
    for i in range(7,9):
      list_node_test_no_comp += self.df_NodeData_test_no_comp.iloc[:,i].tolist()
    for i in range(10,14):
      list_node_test_no_comp += self.df_NodeData_test_no_comp.iloc[:,i].tolist()
    list_node_test_no_comp += self.df_NodeData_test_no_comp.iloc[:,15].tolist()
    test_no_comp = all(isinstance(item, list) for item in list_node_test_no_comp)
    list_node_test_comp = []
    for i in range(7,9):
      list_node_test_comp += self.df_NodeData_test_comp.iloc[:,i].tolist()
    for i in range(10,14):
      list_node_test_comp += self.df_NodeData_test_comp.iloc[:,i].tolist()
    list_node_test_comp += self.df_NodeData_test_comp.iloc[:,15].tolist()
    test_comp = all(isinstance(item, list) for item in list_node_test_comp)
    list_node_test_modifier = []
    for i in range(7,9):
      list_node_test_modifier += self.df_NodeData_test_modifier.iloc[:,i].tolist()
    for i in range(10,14):
      list_node_test_modifier += self.df_NodeData_test_modifier.iloc[:,i].tolist()
    list_node_test_modifier += self.df_NodeData_test_modifier.iloc[:,15].tolist()
    test_modifier = all(isinstance(item, list) for item in list_node_test_modifier)
    list_node_node_grid = []
    for i in range(7,9):
      list_node_node_grid += self.df_NodeData_node_grid.iloc[:,i].tolist()
    for i in range(10,14):
      list_node_node_grid += self.df_NodeData_node_grid.iloc[:,i].tolist()
    list_node_node_grid += self.df_NodeData_node_grid.iloc[:,15].tolist()
    test_node_grid = all(isinstance(item, list) for item in list_node_node_grid)
    list_node_mass_action_rxn = []
    for i in range(7,9):
      list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn.iloc[:,i].tolist()
    for i in range(10,14):
      list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn.iloc[:,i].tolist()
    list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn.iloc[:,15].tolist()
    test_node_mass_action_rxn = all(isinstance(item, list) for item in list_node_mass_action_rxn)

    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)
    self.assertTrue(test_node_grid)
    self.assertTrue(test_node_mass_action_rxn)

  def testNode5(self):
    # Test column 'id', 'floating node' of df_NodeData is str
    if IGNORE_TEST:
      return    
    list_node = []
    list_node += self.df_NodeData[COLUMN_NAME_df_NodeData[4]].tolist()
    list_node += self.df_NodeData[COLUMN_NAME_df_NodeData[5]].tolist()
    test = all(isinstance(item, str) for item in list_node)
    list_node_feedback = []
    list_node_feedback += self.df_NodeData_feedback[COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_feedback += self.df_NodeData_feedback[COLUMN_NAME_df_NodeData[5]].tolist()
    test_feedback = all(isinstance(item, str) for item in list_node_feedback)
    list_node_LinearChain = []
    list_node_LinearChain += self.df_NodeData_LinearChain[COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_LinearChain += self.df_NodeData_LinearChain[COLUMN_NAME_df_NodeData[5]].tolist()
    test_LinearChain = all(isinstance(item, str) for item in list_node_LinearChain)
    list_node_test_no_comp = []
    list_node_test_no_comp += self.df_NodeData_test_no_comp[COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_test_no_comp += self.df_NodeData_test_no_comp[COLUMN_NAME_df_NodeData[5]].tolist()
    test_no_comp = all(isinstance(item, str) for item in list_node_test_no_comp)
    list_node_test_comp = []
    list_node_test_comp += self.df_NodeData_test_comp[COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_test_comp += self.df_NodeData_test_comp[COLUMN_NAME_df_NodeData[5]].tolist()
    test_comp = all(isinstance(item, str) for item in list_node_test_comp)
    list_node_test_modifier = []
    list_node_test_modifier += self.df_NodeData_test_modifier[COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_test_modifier += self.df_NodeData_test_modifier[COLUMN_NAME_df_NodeData[5]].tolist()
    test_modifier = all(isinstance(item, str) for item in list_node_test_modifier)
    list_node_node_grid = []
    list_node_node_grid += self.df_NodeData_node_grid[COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_node_grid += self.df_NodeData_node_grid[COLUMN_NAME_df_NodeData[5]].tolist()
    test_node_grid = all(isinstance(item, str) for item in list_node_node_grid)
    list_node_mass_action_rxn = []
    list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn[COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn[COLUMN_NAME_df_NodeData[5]].tolist()
    test_mass_action_rxn = all(isinstance(item, str) for item in list_node_mass_action_rxn)

    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)
    self.assertTrue(test_node_grid)
    self.assertTrue(test_mass_action_rxn)

  def testNode6(self):
    # Test column 'concentration', 'border width', 'txt_line_width', "txt_font_size" of df_NodeData 
    # are floating numbers
    if IGNORE_TEST:
      return    
    list_node = []
    list_node += self.df_NodeData[COLUMN_NAME_df_NodeData[6]].tolist()
    list_node += self.df_NodeData[COLUMN_NAME_df_NodeData[14]].tolist()
    list_node += self.df_NodeData[COLUMN_NAME_df_NodeData[16]].tolist()
    list_node += self.df_NodeData[COLUMN_NAME_df_NodeData[17]].tolist()
    test = all(isinstance(item, float) for item in list_node)
    list_node_feedback = []
    list_node_feedback += self.df_NodeData_feedback[COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_feedback += self.df_NodeData_feedback[COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_feedback += self.df_NodeData_feedback[COLUMN_NAME_df_NodeData[16]].tolist()
    list_node_feedback += self.df_NodeData_feedback[COLUMN_NAME_df_NodeData[17]].tolist()
    test_feedback = all(isinstance(item, float) for item in list_node_feedback)
    list_node_LinearChain = []
    list_node_LinearChain += self.df_NodeData_LinearChain[COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_LinearChain += self.df_NodeData_LinearChain[COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_LinearChain += self.df_NodeData_LinearChain[COLUMN_NAME_df_NodeData[16]].tolist()
    list_node_LinearChain += self.df_NodeData_LinearChain[COLUMN_NAME_df_NodeData[17]].tolist()
    test_LinearChain = all(isinstance(item, float) for item in list_node_LinearChain)
    list_node_test_no_comp = []
    list_node_test_no_comp += self.df_NodeData_test_no_comp[COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_test_no_comp += self.df_NodeData_test_no_comp[COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_test_no_comp += self.df_NodeData_test_no_comp[COLUMN_NAME_df_NodeData[16]].tolist()
    list_node_test_no_comp += self.df_NodeData_test_no_comp[COLUMN_NAME_df_NodeData[17]].tolist()
    test_no_comp = all(isinstance(item, float) for item in list_node_test_no_comp)
    list_node_test_comp = []
    list_node_test_comp += self.df_NodeData_test_comp[COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_test_comp += self.df_NodeData_test_comp[COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_test_comp += self.df_NodeData_test_comp[COLUMN_NAME_df_NodeData[16]].tolist()
    list_node_test_comp += self.df_NodeData_test_comp[COLUMN_NAME_df_NodeData[17]].tolist()
    test_comp = all(isinstance(item, float) for item in list_node_test_comp)
    list_node_test_modifier = []
    list_node_test_modifier += self.df_NodeData_test_modifier[COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_test_modifier += self.df_NodeData_test_modifier[COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_test_modifier += self.df_NodeData_test_modifier[COLUMN_NAME_df_NodeData[16]].tolist()
    list_node_test_modifier += self.df_NodeData_test_modifier[COLUMN_NAME_df_NodeData[17]].tolist()
    test_modifier = all(isinstance(item, float) for item in list_node_test_modifier)
    list_node_node_grid = []
    list_node_node_grid += self.df_NodeData_node_grid[COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_node_grid += self.df_NodeData_node_grid[COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_node_grid += self.df_NodeData_node_grid[COLUMN_NAME_df_NodeData[16]].tolist()
    list_node_node_grid += self.df_NodeData_node_grid[COLUMN_NAME_df_NodeData[17]].tolist()
    test_node_grid = all(isinstance(item, float) for item in list_node_node_grid)
    list_node_mass_action_rxn = []
    list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn[COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn[COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn[COLUMN_NAME_df_NodeData[16]].tolist()
    list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn[COLUMN_NAME_df_NodeData[17]].tolist()
    test_mass_action_rxn = all(isinstance(item, float) for item in list_node_mass_action_rxn)

    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)
    self.assertTrue(test_node_grid)
    self.assertTrue(test_mass_action_rxn)

  def testReaction1(self):
    # Test all the column names
    if IGNORE_TEST:
      return    
    test = all(item in self.df_ReactionData.columns for item in COLUMN_NAME_df_ReactionData)
    test_feedback = all(item in self.df_ReactionData_feedback.columns \
      for item in COLUMN_NAME_df_ReactionData)
    test_LinearChain = all(item in self.df_ReactionData_LinearChain.columns \
      for item in COLUMN_NAME_df_ReactionData)
    test_no_comp = all(item in self.df_ReactionData_test_no_comp.columns \
      for item in COLUMN_NAME_df_ReactionData)
    test_comp = all(item in self.df_ReactionData_test_comp.columns \
      for item in COLUMN_NAME_df_ReactionData)
    test_modifier = all(item in self.df_ReactionData_test_modifier.columns \
      for item in COLUMN_NAME_df_ReactionData)
    test_node_grid = all(item in self.df_ReactionData_node_grid.columns \
      for item in COLUMN_NAME_df_ReactionData)
    test_mass_action_rxn = all(item in self.df_ReactionData_mass_action_rxn.columns \
      for item in COLUMN_NAME_df_ReactionData)
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)
    self.assertTrue(test_node_grid)
    self.assertTrue(test_mass_action_rxn)

  def testReaction2(self):
    # Test whether there is at least one row
    if IGNORE_TEST:
      return    
    self.assertTrue(len(self.df_ReactionData.index)>0) 
    self.assertTrue(len(self.df_ReactionData_feedback.index)>0)
    self.assertTrue(len(self.df_ReactionData_LinearChain.index)>0)
    self.assertTrue(len(self.df_ReactionData_test_no_comp.index)>0)
    self.assertTrue(len(self.df_ReactionData_test_comp.index)>0)
    self.assertTrue(len(self.df_ReactionData_test_modifier.index)>0)
    self.assertTrue(len(self.df_ReactionData_node_grid.index)==0)
    self.assertTrue(len(self.df_ReactionData_mass_action_rxn.index)>0)

  def testReaction3(self):
    # Test column 'net_idx' 'idx' of df_ReactionData are integers
    if IGNORE_TEST:
      return    
    list_reaction = []
    for i in range(0,2):
      list_reaction += self.df_ReactionData.iloc[:,i].tolist()
    test = all(isinstance(item, int) for item in list_reaction)
    list_reaction_feedback = []
    for i in range(0,2):
      list_reaction_feedback += self.df_ReactionData_feedback.iloc[:,i].tolist()
    test_feedback = all(isinstance(item, int) for item in list_reaction_feedback)
    list_reaction_LinearChain = []
    for i in range(0,2):
      list_reaction_LinearChain += self.df_ReactionData_LinearChain.iloc[:,i].tolist()
    test_LinearChain = all(isinstance(item, int) for item in list_reaction_LinearChain)
    list_reaction_test_no_comp = []
    for i in range(0,2):
      list_reaction_test_no_comp += self.df_ReactionData_test_no_comp.iloc[:,i].tolist()
    test_no_comp = all(isinstance(item, int) for item in list_reaction_test_no_comp)
    list_reaction_test_comp = []
    for i in range(0,2):
      list_reaction_test_comp += self.df_ReactionData_test_comp.iloc[:,i].tolist()
    test_comp = all(isinstance(item, int) for item in list_reaction_test_comp)
    list_reaction_test_modifier = []
    for i in range(0,2):
      list_reaction_test_modifier += self.df_ReactionData_test_modifier.iloc[:,i].tolist()
    test_modifier = all(isinstance(item, int) for item in list_reaction_test_modifier)
    list_reaction_node_grid = []
    for i in range(0,2):
      list_reaction_node_grid += self.df_ReactionData_node_grid.iloc[:,i].tolist()
    test_node_grid = all(isinstance(item, int) for item in list_reaction_node_grid)
    list_reaction_mass_action_rxn = []
    for i in range(0,2):
      list_reaction_mass_action_rxn += self.df_ReactionData_mass_action_rxn.iloc[:,i].tolist()
    test_mass_action_rxn = all(isinstance(item, int) for item in list_reaction_mass_action_rxn)

    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)
    self.assertTrue(test_node_grid)
    self.assertTrue(test_mass_action_rxn)

  def testReaction4(self):
    # Test column 'sources' 'targets' 'modifiers' 'fill color' 'center_position' 'handles' 
    # 'arrow_head_size' 'rxn_dash'
    # of df_ReactionData are lists
    if IGNORE_TEST:
      return    
    list_reaction = []
    for i in range(3,5):
      list_reaction += self.df_ReactionData.iloc[:,i].tolist()
    for i in range(6,8):
      list_reaction += self.df_ReactionData.iloc[:,i].tolist()
    for i in range(9,11):
      list_reaction += self.df_ReactionData.iloc[:,i].tolist()
    for i in range(12,14):
      list_reaction += self.df_ReactionData.iloc[:,i].tolist()
    test = all(isinstance(item, list) for item in list_reaction)
    list_reaction_feedback = []
    for i in range(3,5):
      list_reaction_feedback += self.df_ReactionData_feedback.iloc[:,i].tolist()
    for i in range(6,8):
      list_reaction_feedback += self.df_ReactionData_feedback.iloc[:,i].tolist()
    for i in range(9,11):
      list_reaction_feedback += self.df_ReactionData_feedback.iloc[:,i].tolist()
    for i in range(12,14):
      list_reaction_feedback += self.df_ReactionData_feedback.iloc[:,i].tolist()
    test_feedback = all(isinstance(item, list) for item in list_reaction_feedback)
    list_reaction_LinearChain = []
    for i in range(3,5):
      list_reaction_LinearChain += self.df_ReactionData_LinearChain.iloc[:,i].tolist()
    for i in range(6,8):
      list_reaction_LinearChain += self.df_ReactionData_LinearChain.iloc[:,i].tolist()
    for i in range(9,11):
      list_reaction_LinearChain += self.df_ReactionData_LinearChain.iloc[:,i].tolist()
    for i in range(12,14):
      list_reaction_LinearChain += self.df_ReactionData_LinearChain.iloc[:,i].tolist()
    test_LinearChain = all(isinstance(item, list) for item in list_reaction_LinearChain)
    list_reaction_test_no_comp = []
    for i in range(3,5):
      list_reaction_test_no_comp += self.df_ReactionData_test_no_comp.iloc[:,i].tolist()
    for i in range(6,8):
      list_reaction_test_no_comp += self.df_ReactionData_test_no_comp.iloc[:,i].tolist()
    for i in range(9,11):
      list_reaction_test_no_comp += self.df_ReactionData_test_no_comp.iloc[:,i].tolist()
    for i in range(12,14):
      list_reaction_test_no_comp += self.df_ReactionData_test_no_comp.iloc[:,i].tolist()
    test_no_comp = all(isinstance(item, list) for item in list_reaction_test_no_comp)
    list_reaction_test_comp = []
    for i in range(3,5):
      list_reaction_test_comp += self.df_ReactionData_test_comp.iloc[:,i].tolist()
    for i in range(6,8):
      list_reaction_test_comp += self.df_ReactionData_test_comp.iloc[:,i].tolist()
    for i in range(9,11):
      list_reaction_test_comp += self.df_ReactionData_test_comp.iloc[:,i].tolist()
    for i in range(12,14):
      list_reaction_test_comp += self.df_ReactionData_test_comp.iloc[:,i].tolist()
    test_comp = all(isinstance(item, list) for item in list_reaction_test_comp)
    list_reaction_test_modifier = []
    for i in range(3,5):
      list_reaction_test_modifier += self.df_ReactionData_test_modifier.iloc[:,i].tolist()
    for i in range(6,8):
      list_reaction_test_modifier += self.df_ReactionData_test_modifier.iloc[:,i].tolist()
    for i in range(9,11):
      list_reaction_test_modifier += self.df_ReactionData_test_modifier.iloc[:,i].tolist()
    for i in range(12,14):
      list_reaction_test_modifier += self.df_ReactionData_test_modifier.iloc[:,i].tolist()
    test_modifier = all(isinstance(item, list) for item in list_reaction_test_modifier)
    list_reaction_node_grid = []
    for i in range(3,5):
      list_reaction_node_grid += self.df_ReactionData_node_grid.iloc[:,i].tolist()
    for i in range(6,8):
      list_reaction_node_grid += self.df_ReactionData_node_grid.iloc[:,i].tolist()
    for i in range(9,11):
      list_reaction_node_grid += self.df_ReactionData_node_grid.iloc[:,i].tolist()
    for i in range(12,14):
      list_reaction_node_grid += self.df_ReactionData_node_grid.iloc[:,i].tolist()
    test_node_grid = all(isinstance(item, list) for item in list_reaction_node_grid)
    list_reaction_mass_action_rxn = []
    for i in range(3,5):
      list_reaction_mass_action_rxn += self.df_ReactionData_mass_action_rxn.iloc[:,i].tolist()
    for i in range(6,8):
      list_reaction_mass_action_rxn += self.df_ReactionData_mass_action_rxn.iloc[:,i].tolist()
    for i in range(9,11):
      list_reaction_mass_action_rxn += self.df_ReactionData_mass_action_rxn.iloc[:,i].tolist()
    for i in range(12,14):
      list_reaction_mass_action_rxn += self.df_ReactionData_mass_action_rxn.iloc[:,i].tolist()
    test_mass_action = all(isinstance(item, list) for item in list_reaction_mass_action_rxn)
    
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)
    self.assertTrue(test_node_grid)
    self.assertTrue(test_mass_action)

  def testReaction5(self):
    # Test column 'id' 'rate_law' and 'bezier'of df_ReactionData are strings
    if IGNORE_TEST:
      return    
    list_reaction = []
    list_reaction += self.df_ReactionData.iloc[:,2].tolist()
    list_reaction += self.df_ReactionData.iloc[:,5].tolist()
    list_reaction += self.df_ReactionData.iloc[:,11].tolist()
    test = all(isinstance(item, str) for item in list_reaction)
    list_reaction_feedback = []
    list_reaction_feedback += self.df_ReactionData_feedback.iloc[:,2].tolist()
    list_reaction_feedback += self.df_ReactionData_feedback.iloc[:,5].tolist()
    list_reaction_feedback += self.df_ReactionData_feedback.iloc[:,11].tolist()
    test_feedback = all(isinstance(item, str) for item in list_reaction_feedback)
    list_reaction_LinearChain = []
    list_reaction_LinearChain += self.df_ReactionData_LinearChain.iloc[:,2].tolist()
    list_reaction_LinearChain += self.df_ReactionData_LinearChain.iloc[:,5].tolist()
    list_reaction_LinearChain += self.df_ReactionData_LinearChain.iloc[:,11].tolist()
    test_LinearChain = all(isinstance(item, str) for item in list_reaction_LinearChain)
    list_reaction_test_no_comp = []
    list_reaction_test_no_comp += self.df_ReactionData_test_no_comp.iloc[:,2].tolist()
    list_reaction_test_no_comp += self.df_ReactionData_test_no_comp.iloc[:,5].tolist()
    list_reaction_test_no_comp += self.df_ReactionData_test_no_comp.iloc[:,11].tolist()
    test_no_comp = all(isinstance(item, str) for item in list_reaction_test_no_comp)
    list_reaction_test_comp = []
    list_reaction_test_comp += self.df_ReactionData_test_comp.iloc[:,2].tolist()
    list_reaction_test_comp += self.df_ReactionData_test_comp.iloc[:,5].tolist()
    list_reaction_test_comp += self.df_ReactionData_test_comp.iloc[:,11].tolist()
    test_comp = all(isinstance(item, str) for item in list_reaction_test_comp)
    list_reaction_test_modifier = []
    list_reaction_test_modifier += self.df_ReactionData_test_modifier.iloc[:,2].tolist()
    list_reaction_test_modifier += self.df_ReactionData_test_modifier.iloc[:,5].tolist()
    list_reaction_test_modifier += self.df_ReactionData_test_modifier.iloc[:,11].tolist()
    test_modifier = all(isinstance(item, str) for item in list_reaction_test_modifier)
    list_reaction_node_grid = []
    list_reaction_node_grid += self.df_ReactionData_node_grid.iloc[:,2].tolist()
    list_reaction_node_grid += self.df_ReactionData_node_grid.iloc[:,5].tolist()
    list_reaction_node_grid += self.df_ReactionData_node_grid.iloc[:,11].tolist()
    test_node_grid = all(isinstance(item, str) for item in list_reaction_node_grid)
    list_reaction_mass_action_rxn = []
    list_reaction_mass_action_rxn += self.df_ReactionData_mass_action_rxn.iloc[:,2].tolist()
    list_reaction_mass_action_rxn += self.df_ReactionData_mass_action_rxn.iloc[:,5].tolist()
    list_reaction_mass_action_rxn += self.df_ReactionData_mass_action_rxn.iloc[:,11].tolist()
    test_mass_action_rxn = all(isinstance(item, str) for item in list_reaction_mass_action_rxn)
 

    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)
    self.assertTrue(test_node_grid)
    self.assertTrue(test_mass_action_rxn)
    

  def testReaction6(self):
    # Test column 'line_thickness' of df_ReactionData is a floating number
    if IGNORE_TEST:
      return    
    list_reaction = []
    list_reaction += self.df_ReactionData.iloc[:,8].tolist()
    test = all(isinstance(item, float) for item in list_reaction)
    list_reaction_feedback = []
    list_reaction_feedback += self.df_ReactionData_feedback.iloc[:,8].tolist()
    test_feedback = all(isinstance(item, float) for item in list_reaction_feedback)
    list_reaction_LinearChain = []
    list_reaction_LinearChain += self.df_ReactionData_LinearChain.iloc[:,8].tolist()
    test_LinearChain = all(isinstance(item, float) for item in list_reaction_LinearChain)
    list_reaction_test_no_comp = []
    list_reaction_test_no_comp += self.df_ReactionData_test_no_comp.iloc[:,8].tolist()
    test_no_comp = all(isinstance(item, float) for item in list_reaction_test_no_comp)
    list_reaction_test_comp = []
    list_reaction_test_comp += self.df_ReactionData_test_comp.iloc[:,8].tolist()
    test_comp = all(isinstance(item, float) for item in list_reaction_test_comp)
    list_reaction_test_modifier = []
    list_reaction_test_modifier += self.df_ReactionData_test_modifier.iloc[:,8].tolist()
    test_modifier = all(isinstance(item, float) for item in list_reaction_test_modifier)
    list_reaction_node_grid = []
    list_reaction_node_grid += self.df_ReactionData_node_grid.iloc[:,8].tolist()
    test_node_grid = all(isinstance(item, float) for item in list_reaction_node_grid)
    list_reaction_mass_action_rxn = []
    list_reaction_mass_action_rxn += self.df_ReactionData_mass_action_rxn.iloc[:,8].tolist()
    test_mass_action_rxn = all(isinstance(item, float) for item in list_reaction_mass_action_rxn)
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier) 
    self.assertTrue(test_node_grid)
    self.assertTrue(test_mass_action_rxn)

  def testText1(self):
    # Test all the column names
    if IGNORE_TEST:
      return    
    test_textGlyph = all(item in self.df_TextData_test_textGlyph.columns \
      for item in COLUMN_NAME_df_TextData)
    self.assertTrue(test_textGlyph)

  def testText2(self):
    # Test whether there is at least one row
    if IGNORE_TEST:
      return    
    self.assertTrue(len(self.df_TextData_test_textGlyph.index)>0) 

  def testText3(self):
    # Test column 'txt_content' and 'id 'of df_TextData are strings
    if IGNORE_TEST:
      return    
    list_text = []
    list_text += self.df_TextData_test_textGlyph[COLUMN_NAME_df_TextData[0]].tolist()
    list_text += self.df_TextData_test_textGlyph[COLUMN_NAME_df_TextData[6]].tolist()
    test_text = all(isinstance(item, str) for item in list_text)
    self.assertTrue(test_text)

  def testText4(self):
    # Test column 'txt_position', 'txt_size' and 'txt_font_color' of df_TextData are lists
    if IGNORE_TEST:
      return    
    list_text = []
    list_text += self.df_TextData_test_textGlyph[COLUMN_NAME_df_TextData[1]].tolist()
    list_text += self.df_TextData_test_textGlyph[COLUMN_NAME_df_TextData[2]].tolist()
    list_text += self.df_TextData_test_textGlyph[COLUMN_NAME_df_TextData[3]].tolist()
    test_text = all(isinstance(item, list) for item in list_text)

    self.assertTrue(test_text)

  def testText5(self):
    # Test column 'txt_line_width' and 'txt_font_size' of df_TextData are lists
    if IGNORE_TEST:
      return    
    list_text = []
    list_text += self.df_TextData_test_textGlyph[COLUMN_NAME_df_TextData[4]].tolist()
    list_text += self.df_TextData_test_textGlyph[COLUMN_NAME_df_TextData[5]].tolist()
    test_text = all(isinstance(item, float) for item in list_text)

    self.assertTrue(test_text)


  def testShape1(self):
    # Test all the column names
    if IGNORE_TEST:
      return    
    test_genGlyph = all(item in self.df_ShapeData_test_genGlyph.columns \
      for item in COLUMN_NAME_df_ShapeData)
    self.assertTrue(test_genGlyph)

  def testShape2(self):
    # Test whether there is at least one row
    if IGNORE_TEST:
      return    
    self.assertTrue(len(self.df_ShapeData_test_genGlyph.index)>0) 

  def testShape3(self):
    # Test column 'shape_name' and 'shape_type' of df_TextData are strings
    if IGNORE_TEST:
      return    
    list_shape = []
    list_shape += self.df_ShapeData_test_genGlyph[COLUMN_NAME_df_ShapeData[0]].tolist()
    list_shape += self.df_ShapeData_test_genGlyph[COLUMN_NAME_df_ShapeData[6]].tolist()
    test_shape = all(isinstance(item, str) for item in list_shape)
    self.assertTrue(test_shape)

  def testShape4(self):
    # Test column 'position', 'size', 'fill_color', 'border_color', 'shape_info' of df_ShapeData are lists
    if IGNORE_TEST:
      return    
    list_shape = []
    list_shape += self.df_ShapeData_test_genGlyph[COLUMN_NAME_df_ShapeData[1]].tolist()
    list_shape += self.df_ShapeData_test_genGlyph[COLUMN_NAME_df_ShapeData[2]].tolist()
    list_shape += self.df_ShapeData_test_genGlyph[COLUMN_NAME_df_ShapeData[3]].tolist()
    list_shape += self.df_ShapeData_test_genGlyph[COLUMN_NAME_df_ShapeData[4]].tolist()
    list_shape += self.df_ShapeData_test_genGlyph[COLUMN_NAME_df_ShapeData[7]].tolist()
    test_shape = all(isinstance(item, list) for item in list_shape)

    self.assertTrue(test_shape)

  def testShape5(self):
    # Test column 'border_width' of df_TextData are float
    if IGNORE_TEST:
      return    
    list_shape = []
    list_shape += self.df_ShapeData_test_genGlyph[COLUMN_NAME_df_ShapeData[5]].tolist()
    test_shape = all(isinstance(item, float) for item in list_shape)

    self.assertTrue(test_shape)


  def testGetCompartment(self):
    # Test all the get functions about compartment
    if IGNORE_TEST:
      return  
    self.assertTrue(self.df.getCompartmentPosition("_compartment_default_").x == [10, 10][0])
    #self.assertTrue(self.df.getCompartmentSize("_compartment_default_").x == [10000-20, 6200-20][0])
    self.assertTrue(self.df.getCompartmentSize("_compartment_default_").x == [1000-20, 1000-20][0])
    self.assertTrue(self.df.getCompartmentFillColor("_compartment_default_") == \
     [[255, 255, 255, 255], 'white', '#FFFFFFFF'])
    self.assertTrue(self.df.getCompartmentBorderColor("_compartment_default_") == \
     [[255, 255, 255, 255], 'white', '#FFFFFFFF'])
    self.assertTrue(self.df.getCompartmentBorderWidth("_compartment_default_") == 2.)
    self.assertTrue(self.df.getCompartmentTextPosition("_compartment_default_").x == 0.)
    self.assertTrue(self.df.getCompartmentTextSize("_compartment_default_").x == 0.)
    self.assertTrue(self.df.getCompartmentTextContent("_compartment_default_") == '')
    self.assertTrue(self.df.getCompartmentTextLineWidth("_compartment_default_") == 1.)
    self.assertTrue(self.df.getCompartmentTextFontSize("_compartment_default_") == 11.)
    self.assertTrue(self.df.getCompartmentTextAnchor("_compartment_default_") == 'middle')
    self.assertTrue(self.df.getCompartmentTextVAnchor("_compartment_default_") == 'middle')

  def testGetNode(self):
    # Test all the get functions about node

    if IGNORE_TEST:
      return  
    self.assertTrue(self.df.getNodeAliasNum("x_1") == 1)
    self.assertTrue(self.df.isFloatingNode("x_1") == True)
    self.assertTrue(self.df.getNodePosition("x_1").x == [413.0, 216.0][0])
    self.assertTrue(self.df.getNodeCenter("x_1").x == 438.0)
    self.assertTrue(self.df.getNodeSize("x_1").x == [50.0, 30.0][0])
    self.assertTrue(self.df.getNodeShape("x_1") == 
    ('rectangle', [[413.0, 216.0], [463.0, 216.0], [463.0, 246.0], [413.0, 246.0]]))
    self.assertTrue(self.df.getNodeTextPosition("x_1").x == [413.0, 216.0][0])
    self.assertTrue(self.df.getNodeTextSize("x_1").x == [50.0, 30.0][0])
    self.assertTrue(self.df.getNodeFillColor("x_1") == \
      [[255, 204, 153, 255], '', '#FFCC99FF'])
    self.assertTrue(self.df.getNodeBorderColor("x_1") == \
      [[255, 108, 9, 255], '', '#FF6C09FF'])
    self.assertTrue(self.df.getNodeBorderWidth("x_1") == 2.)
    self.assertTrue(self.df.getNodeTextContent("x_1") == 'x_1')
    self.assertTrue(self.df.getNodeTextFontColor("x_1") == \
      [[0, 0, 0, 255], 'black', '#000000FF'])
    self.assertTrue(self.df.getNodeTextLineWidth("x_1") == 1.)
    self.assertTrue(self.df.getNodeTextFontSize("x_1") == 11.)
    self.assertTrue(self.df.getNodeTextAnchor("x_1") == 'middle')
    self.assertTrue(self.df.getNodeTextVAnchor("x_1") == 'middle')


  def testGetReaction(self):
    # Test all the get functions about reaction

    if IGNORE_TEST:
      return


    self.assertTrue(self.df.getReactionCenterPosition("r_0").x == \
      [334.0, 231.0][0])
    self.assertTrue(self.df.getReactionBezierHandles("r_0")[0].x == \
      [[386.0, 231.0], [386.0, 231.0], [386.0, 231.0]][0][0])
    self.assertTrue(self.df.getReactionFillColor("r_0") == \
      [[91, 176, 253, 255], '', '#5BB0FDFF'])
    self.assertTrue(self.df.getReactionLineThickness("r_0") == 3.)
    self.assertTrue(self.df._isBezierReactionType("r_0") == True)
    #self.assertTrue(self.df.getReactionArrowHeadSize("r_0").x == [12., 15.][0])
    self.assertTrue(self.df.getReactionDashStyle("r_0") == [])
    self.assertTrue(self.df_lineEnding._getReactionArrowHeadPosition("path_0_re6338").x \
      == [-12.0, -6.0][0])
    self.assertTrue(self.df_lineEnding.getReactionArrowHeadSize("path_0_re6338").x \
      == [12.0, 12.0][0])
    self.assertTrue(self.df_lineEnding.getReactionArrowHeadFillColor("path_0_re6338")[0] \
      == [0, 0, 0, 255])
    self.assertTrue(self.df_lineEnding.getReactionArrowHeadShape("path_0_re6338") \
      == (['polygon'], [[[0.0, 0.0], [100.0, 50.0], [0.0, 100.0], [0.0, 0.0]]]))
    self.assertTrue(self.df_lineEnding.getReactionModifierNum("path_0_re6338") == 3)
    self.assertTrue(self.df_lineEnding._getReactionModifierHeadPosition("path_0_re6338").x 
    == [-2., 0.][0])
    self.assertTrue(self.df_lineEnding.getReactionModifierHeadSize("path_0_re6338").x 
    == [4.0, 4.0][0])
    self.assertTrue(self.df_lineEnding.getReactionModifierHeadFillColor("path_0_re6338")[0] 
    == [255, 255, 255, 255])
    self.assertTrue(self.df_lineEnding.getReactionModifierHeadShape("path_0_re6338") == 
    (['ellipse'], [[[0.0, 0.0], [100.0, 100.0]]]))


  def testSetCompartment(self):
    # Test all the set functions about compartment
    if IGNORE_TEST:
      return  

    position = [1, 0]
    size = [900, 900]
    fill_color = [255, 255, 254]
    border_color = [255, 255, 254]
    border_width = 2.
    opacity = 0.
    txt_position = [10, 10]
    txt_size = [1000, 1000]
    txt_content = 'comp'
    txt_font_color = 'red'
    txt_line_width = 10.
    txt_font_size = 10.
    txt_anchor = "start"
    txt_vanchor = 'bottom'

    self.df.setCompartmentPosition('_compartment_default_', position)
    self.df.setCompartmentSize('_compartment_default_', size)
    self.df.setCompartmentFillColor('_compartment_default_', fill_color, opacity = opacity)
    self.df.setCompartmentBorderColor('_compartment_default_', border_color)
    self.df.setCompartmentBorderWidth('_compartment_default_', border_width)
    self.df.setCompartmentTextPosition('_compartment_default_', txt_position)
    self.df.setCompartmentTextSize('_compartment_default_', txt_size)
    self.df.setCompartmentTextContent('_compartment_default_', txt_content)
    self.df.setCompartmentTextFontColor('_compartment_default_', txt_font_color)
    self.df.setCompartmentTextLineWidth('_compartment_default_', txt_line_width)
    self.df.setCompartmentTextFontSize('_compartment_default_', txt_font_size)
    self.df.setCompartmentTextAnchor('_compartment_default_', txt_anchor)
    self.df.setCompartmentTextVAnchor('_compartment_default_', txt_vanchor)

    self.assertTrue(self.df.getCompartmentPosition("_compartment_default_").x == position[0])
    self.assertTrue(self.df.getCompartmentSize("_compartment_default_").x == size[0])
    self.assertTrue(self.df.getCompartmentFillColor("_compartment_default_")[0][0:-1] == fill_color)
    self.assertTrue(self.df.getCompartmentFillColor("_compartment_default_")[0][3] == int(opacity*255/1.))
    self.assertTrue(self.df.getCompartmentBorderColor("_compartment_default_")[0][0:-1] == border_color)
    self.assertTrue(self.df.getCompartmentBorderColor("_compartment_default_")[0][3] == 255)
    self.assertTrue(self.df.getCompartmentBorderWidth("_compartment_default_") == border_width)
    self.assertTrue(self.df.getCompartmentTextPosition("_compartment_default_").x == txt_position[0])
    self.assertTrue(self.df.getCompartmentTextSize("_compartment_default_").x == txt_size[0])
    self.assertTrue(self.df.getCompartmentTextContent("_compartment_default_") == txt_content)
    self.assertTrue(self.df.getCompartmentTextFontColor("_compartment_default_")[1] == txt_font_color)
    self.assertTrue(self.df.getCompartmentTextLineWidth("_compartment_default_") == txt_line_width)
    self.assertTrue(self.df.getCompartmentTextFontSize("_compartment_default_") == txt_font_size)
    self.assertTrue(self.df.getCompartmentTextAnchor("_compartment_default_") == txt_anchor)
    self.assertTrue(self.df.getCompartmentTextVAnchor("_compartment_default_") == txt_vanchor)


  def testSetNode(self):
    # Test all the set functions about node

    if IGNORE_TEST:
      return  

    floating_node = True
    position = [412., 216.]
    position_txt_position = [413., 217.]
    size = [50., 29.]
    size_txt_size = [50., 29.]
    shapeIdx = 2
    shape = "ellipse"
    shape_name = "self_shape" 
    shape_info_polygon = [[0,0],[100,0],[0,100]]
    #shape_info_ellipse = [[[50,50],[100,100]]]
    txt_position = [412., 216.]
    txt_size = [50., 29.]
    fill_color = [255, 204, 154]
    border_color = [255, 109, 9]
    border_width = 3.
    txt_content = 'x1'
    txt_font_color = "#000000"
    txt_line_width = 1.
    txt_font_size = 12.
    txt_anchor = 'start'
    txt_vanchor = 'bottom'
    opacity = 1.
    gradient_linear_info = [[0.0, 0.0], [100.0, 100.0]]
    gradient_radial_info = [[50.0, 50.0], [50.]]
    stop_info = [[0.0, [255, 255, 255, 255]], [100.0, [0, 0, 0, 255]]]
    
    self.df.setFloatingBoundaryNode("x_1", floating_node)
    self.df.setNodePosition("x_1", position)
    self.df.setNodeSize("x_1", size)
    self.df.setNodeShape("x_1", shapeIdx)
    self.df.setNodeShape("x_1", shape)
    self.df.setNodeArbitraryPolygonShape("x_0", shape_name, shape_info_polygon)
    # self.df._setNodeArbitraryEllipseShape("x_0", shape_name, shape_info_ellipse)
    self.df.setNodeTextPosition("x_1", txt_position)
    self.df.setNodeTextSize("x_1", txt_size)
    self.df.setNodeFillColor("x_1", fill_color, opacity = opacity)
    self.df.setNodeFillLinearGradient("x_0", gradient_linear_info, stop_info)
    self.df.setNodeFillRadialGradient("x_0", gradient_radial_info, stop_info)
    self.df.setNodeBorderColor("x_1", border_color, opacity = opacity)
    self.df.setNodeBorderWidth("x_1", border_width)
    self.df.setNodeTextContent("x_1", txt_content)
    self.df.setNodeTextFontColor("x_1", txt_font_color)
    self.df.setNodeTextLineWidth("x_1", txt_line_width)
    self.df.setNodeTextFontSize("x_1", txt_font_size)
    self.df.setNodeTextAnchor("x_1", txt_anchor)
    self.df.setNodeTextVAnchor("x_1", txt_vanchor)

    self.assertTrue(self.df.isFloatingNode("x_1") == floating_node)
    self.assertTrue(self.df.getNodePosition("x_1").x == position[0])
    self.assertTrue(self.df.getNodeSize("x_1").x == size[0])
    self.assertTrue(self.df.getNodeShape("x_1")[0] == shape)
    self.assertTrue(self.df.getNodeShape("x_0")[0] == shape_name)
    self.assertTrue(self.df.getNodeTextPosition("x_1").x == txt_position[0])
    self.assertTrue(self.df.getNodeTextSize("x_1").x == txt_size[0])
    self.assertTrue(self.df.getNodeFillColor("x_1")[0][0:-1] == fill_color)
    self.assertTrue(self.df.getNodeFillColor("x_1")[0][3] == int(opacity*255/1.))
    self.assertTrue(self.df.getNodeFillColor("x_0") == 
    ['radialGradient', [[50.0, 50.0], [50.0]], [[0.0, [255, 255, 255, 255]], [100.0, [0, 0, 0, 255]]]])
    self.assertTrue(self.df.getNodeBorderColor("x_1")[0][0:-1] == border_color)
    self.assertTrue(self.df.getNodeBorderColor("x_1")[0][3] == int(opacity*255/1.))
    self.assertTrue(self.df.getNodeBorderWidth("x_1") == border_width)
    self.assertTrue(self.df.getNodeTextFontColor("x_1")[0][0:-1] == [0,0,0])
    self.assertTrue(self.df.getNodeTextFontColor("x_1")[0][3] == 255)
    self.assertTrue(self.df.getNodeTextContent("x_1") == txt_content)
    self.assertTrue(self.df.getNodeTextLineWidth("x_1") == txt_line_width)
    self.assertTrue(self.df.getNodeTextFontSize("x_1") == txt_font_size)
    self.assertTrue(self.df.getNodeTextAnchor("x_1") == txt_anchor)
    self.assertTrue(self.df.getNodeTextVAnchor("x_1") == txt_vanchor)

    self.df.setNodeAndTextPosition("x_1", position_txt_position)
    self.assertTrue(self.df.getNodePosition("x_1").x == position_txt_position[0])
    self.assertTrue(self.df.getNodeTextPosition("x_1").x == position_txt_position[0])

    self.df.setNodeAndTextSize("x_1", size_txt_size)
    self.assertTrue(self.df.getNodeSize("x_1").x == size_txt_size[0])
    self.assertTrue(self.df.getNodeTextSize("x_1").x == size_txt_size[0])

  def testSetNodeTextPosition(self):
    # Test all the set node text position functions

    if IGNORE_TEST:
      return  

    txt_position_center = [205.0, 216.0]
    txt_position_leftCenter = [155.0, 216.0]
    txt_position_rightCenter = [255.0, 216.0]
    txt_position_upperCenter = [205.0, 186.0]
    txt_position_lowerCenter = [205.0, 246.0]
    txt_position_upperLeft = [155.0, 186.0]
    txt_position_upperRight = [255.0, 186.0]
    txt_position_lowerLeft = [155.0, 246.0]
    txt_position_lowerRight = [255.0, 246.0]
    mv_position = [1., 1.]

    self.df.setNodeTextPositionCenter("x_0")
    self.assertTrue(self.df.getNodeTextPosition("x_0").x == txt_position_center[0])
    self.df.setNodeTextPositionLeftCenter("x_0")
    self.assertTrue(self.df.getNodeTextPosition("x_0").x == txt_position_leftCenter[0])
    self.df.setNodeTextPositionRightCenter("x_0")
    self.assertTrue(self.df.getNodeTextPosition("x_0").x == txt_position_rightCenter[0])
    self.df.setNodeTextPositionUpperCenter("x_0")
    self.assertTrue(self.df.getNodeTextPosition("x_0").x == txt_position_upperCenter[0])
    self.df.setNodeTextPositionLowerCenter("x_0")
    self.assertTrue(self.df.getNodeTextPosition("x_0").x == txt_position_lowerCenter[0])
    self.df.setNodeTextPositionUpperLeft("x_0")
    self.assertTrue(self.df.getNodeTextPosition("x_0").x == txt_position_upperLeft[0])
    self.df.setNodeTextPositionUpperRight("x_0")
    self.assertTrue(self.df.getNodeTextPosition("x_0").x == txt_position_upperRight[0])
    self.df.setNodeTextPositionLowerLeft("x_0")
    self.assertTrue(self.df.getNodeTextPosition("x_0").x == txt_position_lowerLeft[0])
    self.df.setNodeTextPositionLowerRight("x_0")
    self.assertTrue(self.df.getNodeTextPosition("x_0").x == txt_position_lowerRight[0])
    self.df.moveNodeTextPosition("x_0", mv_position)
    self.assertTrue(self.df.getNodeTextPosition("x_0").x == 
    txt_position_lowerRight[0] + mv_position[0])


  def testSetReaction(self):
    # Test all the set functions about reaction

    if IGNORE_TEST:
      return
    
    center_pos = [334.0, 232.0]
    handles = [[334.0, 232.0], [386.0, 231.0], [282.0, 231.0]]
    fill_color = "orange"
    opacity = 1.
    line_thickness = 2.
    bezier = False
    arrowHeadPosition = [-12.,-7.]
    arrowHeadSize = [12.,13.]
    arrowHeadFillColor = "burlywood"
    shape_type_list=['polygon']
    shape_info_list=[[[0.0, 0.0], [100.0, 60.0], [0.0, 100.0], [0.0, 0.0]]]
    rxn_dash = [5, 10]

    self.df.setReactionCenterPosition("r_0", center_pos)
    self.df.setReactionBezierHandles("r_0", handles)
    self.df.setReactionFillColor("r_0", fill_color, opacity = opacity)
    self.df.setReactionLineThickness("r_0", line_thickness)
    self.df._setBezierReactionType("r_0", bezier)
    self.df.setReactionDashStyle("r_0", rxn_dash)
    self.df_lineEnding._setReactionArrowHeadPosition("path_0_re6338", arrowHeadPosition)
    self.df_lineEnding.setReactionArrowHeadSize("path_0_re6338", arrowHeadSize)
    self.df_lineEnding.setReactionArrowHeadFillColor("path_0_re6338", arrowHeadFillColor)
    self.df_lineEnding.setReactionArrowHeadShape("path_0_re6338", 
    shape_type_list=shape_type_list, shape_info_list=shape_info_list)
    self.df_lineEnding._setReactionModifierHeadPosition("path_0_re6338", arrowHeadPosition)
    self.df_lineEnding.setReactionModifierHeadSize("path_0_re6338", arrowHeadSize)
    self.df_lineEnding.setReactionModifierHeadFillColor("path_0_re6338", arrowHeadFillColor)
    self.df_lineEnding.setReactionModifierHeadShape("path_0_re6338", 
    shape_type_list=shape_type_list, shape_info_list=shape_info_list)
    self.assertTrue(self.df.getReactionCenterPosition("r_0").x == center_pos[0])
    self.assertTrue(self.df.getReactionBezierHandles("r_0")[0].x == handles[0][0])
    self.assertTrue(self.df.getReactionFillColor("r_0")[0][0:-1] == [255, 165, 0])
    self.assertTrue(self.df.getReactionFillColor("r_0")[0][3] == int(opacity*255/1.))
    self.assertTrue(self.df.getReactionLineThickness("r_0") == line_thickness)
    self.assertTrue(self.df._isBezierReactionType("r_0") == bezier)
    self.assertTrue(self.df.getReactionDashStyle("r_0")== rxn_dash)
    self.assertTrue(self.df_lineEnding._getReactionArrowHeadPosition("path_0_re6338").x == arrowHeadPosition[0])
    self.assertTrue(self.df_lineEnding.getReactionArrowHeadSize("path_0_re6338").x == arrowHeadSize[0])
    self.assertTrue(self.df_lineEnding.getReactionArrowHeadFillColor("path_0_re6338")[1] == arrowHeadFillColor)
    self.assertTrue(self.df_lineEnding.getReactionArrowHeadShape("path_0_re6338") == (shape_type_list, shape_info_list))
    self.assertTrue(self.df_lineEnding._getReactionModifierHeadPosition("path_0_re6338").x == arrowHeadPosition[0])
    self.assertTrue(self.df_lineEnding.getReactionModifierHeadSize("path_0_re6338").x == arrowHeadSize[0])
    self.assertTrue(self.df_lineEnding.getReactionModifierHeadFillColor("path_0_re6338")[1] == arrowHeadFillColor)
    self.assertTrue(self.df_lineEnding.getReactionModifierHeadShape("path_0_re6338") == (shape_type_list, shape_info_list))


  def testSetReactionDefaultCenterAndHandlePositions(self):
    # Test the function setReactionDefaultCenterAndHandlePositions

    if IGNORE_TEST:
      return
    
    self.df.setReactionDefaultCenterAndHandlePositions("r_0")
    self.df.setReactionToStraightLine("r_0")

    self.assertTrue(self.df.getReactionCenterPosition("r_0").x == [334.0, 231.0][0])
    self.assertTrue(self.df.getReactionBezierHandles("r_0")[0].x == 
    [[334.0, 231.0], [386.0, 231.0], [282.0, 231.0]][0][0])

  def testExport(self):
    # Test the export function

    if IGNORE_TEST:
      return

    sbmlStr_layout_render = self.df.export()
    self.assertTrue(isinstance(sbmlStr_layout_render, str))

  def testGetArbitraryText(self):
    # Test all the get functions about arbitrary text

    if IGNORE_TEST:
      return  
    self.assertTrue(self.df_text.getTextContent("TextGlyph_01") == "text_content1")
    self.assertTrue(self.df_text.getTextPosition("TextGlyph_01").x == [92.0, 26.0][0])
    self.assertTrue(self.df_text.getTextSize("TextGlyph_01").x == [228.0, 24.0][0])
    self.assertTrue(self.df_text.getTextFontColor("TextGlyph_01")== [[0, 0, 0, 255], 'black', '#000000FF'])
    self.assertTrue(self.df_text.getTextLineWidth("TextGlyph_02") == 1.)
    self.assertTrue(self.df_text.getTextFontSize("TextGlyph_02") == 11.)

  def testSetArbitraryText(self):
    # Test all the set functions about arbitrary text

    if IGNORE_TEST:
      return  

    text_content = "test"
    text_position = [413., 216.]
    text_size = [413., 216.]
    text_font_color = [5,0,0]
    opacity = 1.
    text_line_width = 3.
    text_font_size = 15.
    
    self.df_text.setTextContent("TextGlyph_01", text_content)
    self.df_text.setTextPosition("TextGlyph_01", text_position)
    self.df_text.setTextSize("TextGlyph_01", text_size)
    self.df_text.setTextFontColor("TextGlyph_01", text_font_color, opacity)
    self.df_text.setTextLineWidth("TextGlyph_02", text_line_width)
    self.df_text.setTextFontSize("TextGlyph_02", text_font_size)

    self.assertTrue(self.df_text.getTextContent("TextGlyph_01") == text_content)
    self.assertTrue(self.df_text.getTextPosition("TextGlyph_01").x == text_position[0])
    self.assertTrue(self.df_text.getTextSize("TextGlyph_01").x == text_size[0])
    self.assertTrue(self.df_text.getTextFontColor("TextGlyph_01")[0] == [5, 0, 0, 255])
    self.assertTrue(self.df_text.getTextLineWidth("TextGlyph_02") == text_line_width)
    self.assertTrue(self.df_text.getTextFontSize("TextGlyph_02") == text_font_size)


  def testArbitraryText(self):
    # set reaction one by one
    if IGNORE_TEST:
      return

    txt_id = "test_id"
    txt_content = "test1"
    txt_position = [205,216]
    txt_size = [10,10]
    txt_font_color="black" 
    opacity= 1
    txt_line_width=2.
    txt_font_size=13.

    self.df_text.addText(txt_id, txt_content, txt_position, txt_size, txt_font_color, 
    opacity, txt_line_width, txt_font_size)
    self.df_text.removeText(txt_id)

    with self.assertRaises(Exception):
      self.df_text.removeText("text")

  def testGetArbitraryShape(self):
    # Test all the get functions about arbitrary shape

    if IGNORE_TEST:
      return  

    self.assertTrue(self.df_shape.getShapePosition("shape_name").x == [177., 107.][0])
    self.assertTrue(self.df_shape.getShapeSize("shape_name").x == [50., 30.][0])


  def testArbitraryShape(self):
    # set reaction one by one
    if IGNORE_TEST:
      return

    shape_name = "self_rectangle"
    position = [400,200]
    size = [100,100]
    fill_color = "red" 
    fill_opacity = 0.5
    border_color = "blue"
    border_opacity = 1.
    border_width = 3.
    shape_info = [[0,0],[100,0],[0,100]]

    self.df_shape.addRectangle(shape_name, position, size,
    fill_color, fill_opacity, border_color, border_opacity, border_width)
    self.df_shape.removeShape("shape_name")

    with self.assertRaises(Exception):
      self.df_shape.removeShape("test")

    self.df_shape.addEllipse('self_ellipse', position, size)
    self.df_shape.addPolygon('self_polygon', shape_info, position, size)

  def testNetworkFuncs(self):
    # Test the Network related function

    if IGNORE_TEST:
      return

    self.assertTrue(self.df.getNetworkTopLeftCorner().x == [205.0, 216.0][0])
    self.assertTrue(self.df.getNetworkBottomRightCorner().x == [463.0, 246.0][0])
    self.assertTrue(self.df.getNetworkSize().x == [258, 30][0])

  def testGetIds(self):
    # Test the functions for getting ids

    if IGNORE_TEST:
      return

    self.assertTrue(self.df.getCompartmentIdList() == ['_compartment_default_'])
    self.assertTrue(self.df.getNodeIdList() == ['x_1', 'x_0'])
    self.assertTrue(self.df.getReactionIdList() == ['r_0'])

    self.assertTrue(self.df_text.getTextIdList() == ["TextGlyph_01", "TextGlyph_02"])
    self.assertTrue(self.df_shape.getShapeNameList() == ['shape_name'])

  def testHasLayout(self):
    # Test the functions of hasLayout()

    if IGNORE_TEST:
      return

    self.assertTrue(self.df.hasLayout() == True)


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

  #   self.df.addText(txt_content, txt_position, txt_font_color, 
  #   opacity, txt_line_width, txt_font_size)
  #   self.df.removeText(txt_content)

  #   with self.assertRaises(Exception):
  #     self.df.removeText("text")

if __name__ == '__main__':
  unittest.main()




