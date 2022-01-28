import unittest
import os
from SBMLDiagrams.processSBML import *
from SBMLDiagrams.processSBML import _SBMLToDF

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
    self.df_CompartmentData, self.df_NodeData, self.df_ReactionData = _SBMLToDF(sbmlStr_test)
    self.df_CompartmentData_feedback, self.df_NodeData_feedback, self.df_ReactionData_feedback = \
      _SBMLToDF(sbmlStr_feedback)
    self.df_CompartmentData_LinearChain, self.df_NodeData_LinearChain, self.df_ReactionData_LinearChain = \
      _SBMLToDF(sbmlStr_LinearChain)
    self.df_CompartmentData_test_no_comp, self.df_NodeData_test_no_comp, self.df_ReactionData_test_no_comp = \
      _SBMLToDF(sbmlStr_test_no_comp)
    self.df_CompartmentData_test_comp, self.df_NodeData_test_comp, self.df_ReactionData_test_comp = \
      _SBMLToDF(sbmlStr_test_comp)
    self.df_CompartmentData_test_modifier, self.df_NodeData_test_modifier, self.df_ReactionData_test_modifier = \
      _SBMLToDF(sbmlStr_test_modifier)
    self.df_CompartmentData_node_grid, self.df_NodeData_node_grid, self.df_ReactionData_node_grid = \
      _SBMLToDF(sbmlStr_node_grid)
    self.df_CompartmentData_mass_action_rxn, self.df_NodeData_mass_action_rxn, self.df_ReactionData_mass_action_rxn = \
      _SBMLToDF(sbmlStr_mass_action_rxn)
    self.df = load(sbmlStr_test)

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
    # Test column 'id' and 'floating node' of df_NodeData is str
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
    # Test column 'concentration', 'border width' and 'txt_line_width' of df_NodeData 
    # are floating numbers
    if IGNORE_TEST:
      return    
    list_node = []
    list_node += self.df_NodeData[COLUMN_NAME_df_NodeData[6]].tolist()
    list_node += self.df_NodeData[COLUMN_NAME_df_NodeData[14]].tolist()
    list_node += self.df_NodeData[COLUMN_NAME_df_NodeData[16]].tolist()
    test = all(isinstance(item, float) for item in list_node)
    list_node_feedback = []
    list_node_feedback += self.df_NodeData_feedback[COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_feedback += self.df_NodeData_feedback[COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_feedback += self.df_NodeData_feedback[COLUMN_NAME_df_NodeData[16]].tolist()
    test_feedback = all(isinstance(item, float) for item in list_node_feedback)
    list_node_LinearChain = []
    list_node_LinearChain += self.df_NodeData_LinearChain[COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_LinearChain += self.df_NodeData_LinearChain[COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_LinearChain += self.df_NodeData_LinearChain[COLUMN_NAME_df_NodeData[16]].tolist()
    test_LinearChain = all(isinstance(item, float) for item in list_node_LinearChain)
    list_node_test_no_comp = []
    list_node_test_no_comp += self.df_NodeData_test_no_comp[COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_test_no_comp += self.df_NodeData_test_no_comp[COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_test_no_comp += self.df_NodeData_test_no_comp[COLUMN_NAME_df_NodeData[16]].tolist()
    test_no_comp = all(isinstance(item, float) for item in list_node_test_no_comp)
    list_node_test_comp = []
    list_node_test_comp += self.df_NodeData_test_comp[COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_test_comp += self.df_NodeData_test_comp[COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_test_comp += self.df_NodeData_test_comp[COLUMN_NAME_df_NodeData[16]].tolist()
    test_comp = all(isinstance(item, float) for item in list_node_test_comp)
    list_node_test_modifier = []
    list_node_test_modifier += self.df_NodeData_test_modifier[COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_test_modifier += self.df_NodeData_test_modifier[COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_test_modifier += self.df_NodeData_test_modifier[COLUMN_NAME_df_NodeData[16]].tolist()
    test_modifier = all(isinstance(item, float) for item in list_node_test_modifier)
    list_node_node_grid = []
    list_node_node_grid += self.df_NodeData_node_grid[COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_node_grid += self.df_NodeData_node_grid[COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_node_grid += self.df_NodeData_node_grid[COLUMN_NAME_df_NodeData[16]].tolist()
    test_node_grid = all(isinstance(item, float) for item in list_node_node_grid)
    list_node_mass_action_rxn = []
    list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn[COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn[COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn[COLUMN_NAME_df_NodeData[16]].tolist()
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
    test = all(isinstance(item, list) for item in list_reaction)
    list_reaction_feedback = []
    for i in range(3,5):
      list_reaction_feedback += self.df_ReactionData_feedback.iloc[:,i].tolist()
    for i in range(6,8):
      list_reaction_feedback += self.df_ReactionData_feedback.iloc[:,i].tolist()
    for i in range(9,11):
      list_reaction_feedback += self.df_ReactionData_feedback.iloc[:,i].tolist()
    test_feedback = all(isinstance(item, list) for item in list_reaction_feedback)
    list_reaction_LinearChain = []
    for i in range(3,5):
      list_reaction_LinearChain += self.df_ReactionData_LinearChain.iloc[:,i].tolist()
    for i in range(6,8):
      list_reaction_LinearChain += self.df_ReactionData_LinearChain.iloc[:,i].tolist()
    for i in range(9,11):
      list_reaction_LinearChain += self.df_ReactionData_LinearChain.iloc[:,i].tolist()
    test_LinearChain = all(isinstance(item, list) for item in list_reaction_LinearChain)
    list_reaction_test_no_comp = []
    for i in range(3,5):
      list_reaction_test_no_comp += self.df_ReactionData_test_no_comp.iloc[:,i].tolist()
    for i in range(6,8):
      list_reaction_test_no_comp += self.df_ReactionData_test_no_comp.iloc[:,i].tolist()
    for i in range(9,11):
      list_reaction_test_no_comp += self.df_ReactionData_test_no_comp.iloc[:,i].tolist()
    test_no_comp = all(isinstance(item, list) for item in list_reaction_test_no_comp)
    list_reaction_test_comp = []
    for i in range(3,5):
      list_reaction_test_comp += self.df_ReactionData_test_comp.iloc[:,i].tolist()
    for i in range(6,8):
      list_reaction_test_comp += self.df_ReactionData_test_comp.iloc[:,i].tolist()
    for i in range(9,11):
      list_reaction_test_comp += self.df_ReactionData_test_comp.iloc[:,i].tolist()
    test_comp = all(isinstance(item, list) for item in list_reaction_test_comp)
    list_reaction_test_modifier = []
    for i in range(3,5):
      list_reaction_test_modifier += self.df_ReactionData_test_modifier.iloc[:,i].tolist()
    for i in range(6,8):
      list_reaction_test_modifier += self.df_ReactionData_test_modifier.iloc[:,i].tolist()
    for i in range(9,11):
      list_reaction_test_modifier += self.df_ReactionData_test_modifier.iloc[:,i].tolist()
    test_modifier = all(isinstance(item, list) for item in list_reaction_test_modifier)
    list_reaction_node_grid = []
    for i in range(3,5):
      list_reaction_node_grid += self.df_ReactionData_node_grid.iloc[:,i].tolist()
    for i in range(6,8):
      list_reaction_node_grid += self.df_ReactionData_node_grid.iloc[:,i].tolist()
    for i in range(9,11):
      list_reaction_node_grid += self.df_ReactionData_node_grid.iloc[:,i].tolist()
    test_node_grid = all(isinstance(item, list) for item in list_reaction_node_grid)
    list_reaction_mass_action_rxn = []
    for i in range(3,5):
      list_reaction_mass_action_rxn += self.df_ReactionData_mass_action_rxn.iloc[:,i].tolist()
    for i in range(6,8):
      list_reaction_mass_action_rxn += self.df_ReactionData_mass_action_rxn.iloc[:,i].tolist()
    for i in range(9,11):
      list_reaction_mass_action_rxn += self.df_ReactionData_mass_action_rxn.iloc[:,i].tolist()
    test_mass_action_rxn = all(isinstance(item, list) for item in list_reaction_mass_action_rxn)
    
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)
    self.assertTrue(test_node_grid)
    self.assertTrue(test_mass_action_rxn)

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

  def testGetCompartment(self):
    # Test all the get functions about compartment
    if IGNORE_TEST:
      return  
    self.assertTrue(self.df.getCompartmentPosition("_compartment_default_")[0] == [0, 0])
    self.assertTrue(self.df.getCompartmentSize("_compartment_default_")[0] == [3900, 2400])
    self.assertTrue(self.df.getCompartmentFillColor("_compartment_default_")[0] == \
      [[255, 255, 255, 255], 'White', '#FFFFFFFF'])
    self.assertTrue(self.df.getCompartmentBorderColor("_compartment_default_")[0] == \
      [[255, 255, 255, 255], 'White', '#FFFFFFFF'])
    self.assertTrue(self.df.getCompartmentBorderWidth("_compartment_default_")[0] == 2.)

  def testGetNode(self):
    # Test all the get functions about node

    if IGNORE_TEST:
      return  
    self.assertTrue(self.df.isFloatingNode("x_1")[0] == True)
    self.assertTrue(self.df.getNodePosition("x_1")[0] == [413.0, 216.0])
    self.assertTrue(self.df.getNodeSize("x_1")[0] == [50.0, 30.0])
    self.assertTrue(self.df.getNodeShape("x_1")[0] == (1, 'reactangle'))
    self.assertTrue(self.df.getNodeTextPosition("x_1")[0] == [413.0, 216.0])
    self.assertTrue(self.df.getNodeTextSize("x_1")[0] == [50.0, 30.0])
    self.assertTrue(self.df.getNodeFillColor("x_1")[0] == \
      [[255, 204, 153, 255], '', '#FFCC99FF'])
    self.assertTrue(self.df.getNodeBorderColor("x_1")[0] == \
      [[255, 108, 9, 255], '', '#FF6C09FF'])
    self.assertTrue(self.df.getNodeBorderWidth("x_1")[0] == 2.)
    self.assertTrue(self.df.getNodeTextFontColor("x_1")[0] == \
      [[0, 0, 0, 255], 'Black', '#000000FF'])
    self.assertTrue(self.df.getNodeTextLineWidth("x_1")[0] == 1.)


  def testGetReaction(self):
    # Test all the get functions about reaction

    if IGNORE_TEST:
      return


    self.assertTrue(self.df.getReactionCenterPosition("r_0")[0] == \
      [334.0, 231.0])
    # self.assertTrue(self.df.getReactionHandlePositions("r_0")[0] == \
      # [[334.0, 231.0], [386.0, 231.0], [282.0, 231.0]])
    self.assertTrue(self.df.getReactionHandlePositions("r_0")[0] == \
      [[386.0, 231.0], [386.0, 231.0], [386.0, 231.0]])
    self.assertTrue(self.df.getReactionFillColor("r_0")[0] == \
      [[91, 176, 253, 255], '', '#5BB0FDFF'])
    self.assertTrue(self.df.getReactionLineThickness("r_0")[0] == 3.)
    self.assertTrue(self.df.isBezierReactionType("r_0")[0] == True)

  def testSetCompartment(self):
    # Test all the get functions about compartment
    if IGNORE_TEST:
      return  

    position = [1, 0]
    size = [900, 900]
    fill_color = [255, 255, 254]
    border_color = [255, 255, 254]
    border_width = 2.
    opacity = 0.

    self.df.setCompartmentPosition('_compartment_default_', position)
    self.df.setCompartmentSize('_compartment_default_', size)
    self.df.setCompartmentFillColor('_compartment_default_', fill_color, opacity = opacity)
    self.df.setCompartmentBorderColor('_compartment_default_', border_color)
    self.df.setCompartmentBorderWidth('_compartment_default_', border_width)

    self.assertTrue(self.df.getCompartmentPosition("_compartment_default_")[0] == position)
    self.assertTrue(self.df.getCompartmentSize("_compartment_default_")[0] == size)
    self.assertTrue(self.df.getCompartmentFillColor("_compartment_default_")[0][0][0:-1] == fill_color)
    self.assertTrue(self.df.getCompartmentFillColor("_compartment_default_")[0][0][3] == int(opacity*255/1.))
    self.assertTrue(self.df.getCompartmentBorderColor("_compartment_default_")[0][0][0:-1] == border_color)
    self.assertTrue(self.df.getCompartmentBorderColor("_compartment_default_")[0][0][3] == 255)
    self.assertTrue(self.df.getCompartmentBorderWidth("_compartment_default_")[0] == border_width)

  def testSetNode(self):
    # Test all the get functions about node

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
    txt_font_color = "#000000"
    txt_line_width = 1.
    opacity = 1.
    
    self.df.setFloatingBoundaryNode("x_1", floating_node)
    self.df.setNodePosition("x_1", position)
    self.df.setNodeSize("x_1", size)
    self.df.setNodeShapeIdx("x_1", shapeIdx)
    self.df.setNodeTextPosition("x_1", txt_position)
    self.df.setNodeTextSize("x_1", txt_size)
    self.df.setNodeFillColor("x_1", fill_color, opacity = opacity)
    self.df.setNodeBorderColor("x_1", border_color, opacity = opacity)
    self.df.setNodeBorderWidth("x_1", border_width)
    self.df.setNodeTextFontColor("x_1", txt_font_color)
    self.df.setNodeTextLineWidth("x_1", txt_line_width)

    self.assertTrue(self.df.isFloatingNode("x_1")[0] == floating_node)
    self.assertTrue(self.df.getNodePosition("x_1")[0] == position)
    self.assertTrue(self.df.getNodeSize("x_1")[0] == size)
    self.assertTrue(self.df.getNodeShape("x_1")[0][0] == shapeIdx)
    self.assertTrue(self.df.getNodeTextPosition("x_1")[0] == txt_position)
    self.assertTrue(self.df.getNodeTextSize("x_1")[0] == txt_size)
    self.assertTrue(self.df.getNodeFillColor("x_1")[0][0][0:-1] == fill_color)
    self.assertTrue(self.df.getNodeFillColor("x_1")[0][0][3] == int(opacity*255/1.))
    self.assertTrue(self.df.getNodeBorderColor("x_1")[0][0][0:-1] == border_color)
    self.assertTrue(self.df.getNodeBorderColor("x_1")[0][0][3] == int(opacity*255/1.))
    self.assertTrue(self.df.getNodeBorderWidth("x_1")[0] == border_width)
    self.assertTrue(self.df.getNodeTextFontColor("x_1")[0][0][0:-1] == [0,0,0])
    self.assertTrue(self.df.getNodeTextFontColor("x_1")[0][0][3] == 255)
    self.assertTrue(self.df.getNodeTextLineWidth("x_1")[0] == txt_line_width)


  def testSetReaction(self):
    # Test all the get functions about reaction

    if IGNORE_TEST:
      return
    
    center_pos = [334.0, 232.0]
    handles = [[334.0, 232.0], [386.0, 231.0], [282.0, 231.0]]
    fill_color = "orange"
    opacity = 0.5
    line_thickness = 2.
    bezier = False

    self.df.setReactionCenterPosition("r_0", center_pos)
    self.df.setReactionHandlePositions("r_0", handles)
    self.df.setReactionFillColor("r_0", fill_color, opacity = opacity)
    self.df.setReactionLineThickness("r_0", line_thickness)
    self.df.setBezierReactionType("r_0", bezier)

    self.assertTrue(self.df.getReactionCenterPosition("r_0")[0] == center_pos)
    self.assertTrue(self.df.getReactionHandlePositions("r_0")[0] == handles)
    self.assertTrue(self.df.getReactionFillColor("r_0")[0][0][0:-1] == [255, 165, 0])
    self.assertTrue(self.df.getReactionFillColor("r_0")[0][0][3] == int(opacity*255/1.))
    self.assertTrue(self.df.getReactionLineThickness("r_0")[0] == line_thickness)
    self.assertTrue(self.df.isBezierReactionType("r_0")[0] == bezier)

  def testExport(self):
    # Test the export function

    if IGNORE_TEST:
      return

    sbmlStr_layout_render = self.df.export()
    self.assertTrue(isinstance(sbmlStr_layout_render, str))


if __name__ == '__main__':
  unittest.main()




