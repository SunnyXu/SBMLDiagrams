import unittest
import os
from SBMLDiagrams import processSBML
from SBMLDiagrams import exportSBML
import pandas as pd
from openpyxl import *

IGNORE_TEST = False

#############################
# Tests
#############################
class TestExportSBML(unittest.TestCase):
# teset exportSBML._DFToSBML() via processSBML._SBMLTODF()

  def setUp(self):
    
    DIR = os.path.dirname(os.path.abspath(__file__))
    TEST_FOLDER = os.path.join(DIR, "initiate_excel_files")
    xls = pd.ExcelFile(os.path.join(TEST_FOLDER, 'test.xlsx'))
    df_CompartmentData = pd.read_excel(xls, 'CompartmentData')
    df_NodeData = pd.read_excel(xls, 'NodeData')
    df_ReactionData = pd.read_excel(xls, 'ReactionData')
    df_TextData = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_TextData)
    # df_CompartmentData = pd.read_csv(os.path.join(TEST_FOLDER, "CompartmentData.csv")) 
    # df_NodeData = pd.read_csv(os.path.join(TEST_FOLDER, "NodeData.csv"))
    # df_ReactionData = pd.read_csv(os.path.join(TEST_FOLDER, "ReactionData.csv"))
    df = (df_CompartmentData, df_NodeData, df_ReactionData, df_TextData)
    sbmlStr_layout_render = exportSBML._DFToSBML(df)
    self.df_CompartmentData, self.df_NodeData, self.df_ReactionData, _ , _= processSBML._SBMLToDF(sbmlStr_layout_render)
    
    xls_feedback = pd.ExcelFile(os.path.join(TEST_FOLDER, 'feedback.xlsx'))
    df_CompartmentData_feedback = pd.read_excel(xls_feedback, 'CompartmentData')
    df_NodeData_feedback = pd.read_excel(xls_feedback, 'NodeData')
    df_ReactionData_feedback = pd.read_excel(xls_feedback, 'ReactionData')
    df_TextData_feedback = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_TextData)
    df_ShapeData_feedback = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_ShapeData)
    df_feedback = (df_CompartmentData_feedback, \
      df_NodeData_feedback, df_ReactionData_feedback, df_TextData_feedback, df_ShapeData_feedback)
    sbmlStr_layout_render_feedback = exportSBML._DFToSBML(df_feedback)
    self.df_CompartmentData_feedback, self.df_NodeData_feedback, self.df_ReactionData_feedback, _, _ \
       = processSBML._SBMLToDF(sbmlStr_layout_render_feedback)

    xls_LinearChain = pd.ExcelFile(os.path.join(TEST_FOLDER, 'LinearChain.xlsx'))
    df_CompartmentData_LinearChain = pd.read_excel(xls_LinearChain, 'CompartmentData')
    df_NodeData_LinearChain = pd.read_excel(xls_LinearChain, 'NodeData')
    df_ReactionData_LinearChain = pd.read_excel(xls_LinearChain, 'ReactionData')
    df_TextData_LinearChain = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_TextData)
    df_ShapeData_LinearChain = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_ShapeData)
    df_LinearChain = (df_CompartmentData_LinearChain, \
      df_NodeData_LinearChain, df_ReactionData_LinearChain, df_TextData_LinearChain, df_ShapeData_LinearChain)
    sbmlStr_layout_render_LinearChain = exportSBML._DFToSBML(df_LinearChain)
    self.df_CompartmentData_LinearChain, self.df_NodeData_LinearChain, \
    self.df_ReactionData_LinearChain, _, _ \
    = processSBML._SBMLToDF(sbmlStr_layout_render_LinearChain)

    xls_test_no_comp = pd.ExcelFile(os.path.join(TEST_FOLDER, 'test_no_comp.xlsx'))
    df_CompartmentData_test_no_comp = pd.read_excel(xls_test_no_comp, 'CompartmentData')
    df_NodeData_test_no_comp = pd.read_excel(xls_test_no_comp, 'NodeData')
    df_ReactionData_test_no_comp = pd.read_excel(xls_test_no_comp, 'ReactionData')
    df_TextData_test_no_comp = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_TextData)
    df_ShapeData_test_no_comp = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_ShapeData)
    df_test_no_comp = (df_CompartmentData_test_no_comp, \
      df_NodeData_test_no_comp, df_ReactionData_test_no_comp, df_TextData_test_no_comp, df_ShapeData_test_no_comp)
    sbmlStr_layout_render_test_no_comp = exportSBML._DFToSBML(df_test_no_comp)
    self.df_CompartmentData_test_no_comp, self.df_NodeData_test_no_comp, \
      self.df_ReactionData_test_no_comp, _, _ = processSBML._SBMLToDF(sbmlStr_layout_render_test_no_comp)

    xls_test_comp = pd.ExcelFile(os.path.join(TEST_FOLDER, 'test_comp.xlsx'))
    df_CompartmentData_test_comp = pd.read_excel(xls_test_comp, 'CompartmentData')
    df_NodeData_test_comp = pd.read_excel(xls_test_comp, 'NodeData')
    df_ReactionData_test_comp = pd.read_excel(xls_test_comp, 'ReactionData')
    df_TextData_test_comp = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_TextData)
    df_ShapeData_test_comp = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_ShapeData)
    df_test_comp = (df_CompartmentData_test_comp, \
      df_NodeData_test_comp, df_ReactionData_test_comp, df_TextData_test_comp, df_ShapeData_test_no_comp)
    sbmlStr_layout_render_test_comp = exportSBML._DFToSBML(df_test_comp)
    self.df_CompartmentData_test_comp, self.df_NodeData_test_comp, \
      self.df_ReactionData_test_comp, _, _ = processSBML._SBMLToDF(sbmlStr_layout_render_test_comp)

    xls_test_modifier = pd.ExcelFile(os.path.join(TEST_FOLDER, 'test_modifier.xlsx'))
    df_CompartmentData_test_modifier = pd.read_excel(xls_test_modifier, 'CompartmentData')
    df_NodeData_test_modifier = pd.read_excel(xls_test_modifier, 'NodeData')
    df_ReactionData_test_modifier = pd.read_excel(xls_test_modifier, 'ReactionData')
    df_TextData_test_modifier = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_TextData)
    df_ShapeData_test_modifier = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_ShapeData)
    df_test_modifier = (df_CompartmentData_test_modifier, \
      df_NodeData_test_modifier, df_ReactionData_test_modifier, df_TextData_test_modifier,
      df_ShapeData_test_modifier)
    sbmlStr_layout_render_test_modifier = exportSBML._DFToSBML(df_test_modifier)
    self.df_CompartmentData_test_modifier, self.df_NodeData_test_modifier, \
      self.df_ReactionData_test_modifier, _, _ = processSBML._SBMLToDF(sbmlStr_layout_render_test_modifier)
 
    xls_node_grid = pd.ExcelFile(os.path.join(TEST_FOLDER, 'node_grid.xlsx'))
    df_CompartmentData_node_grid = pd.read_excel(xls_node_grid, 'CompartmentData')
    df_NodeData_node_grid = pd.read_excel(xls_node_grid, 'NodeData')
    df_ReactionData_node_grid = pd.read_excel(xls_node_grid, 'ReactionData')
    df_TextData_node_grid = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_TextData)
    df_ShapeData_node_grid = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_ShapeData)
    df_node_grid = (df_CompartmentData_node_grid, \
      df_NodeData_node_grid, df_ReactionData_node_grid, df_TextData_node_grid, df_ShapeData_node_grid)
    sbmlStr_layout_render_node_grid = exportSBML._DFToSBML(df_node_grid)
    self.df_CompartmentData_node_grid, self.df_NodeData_node_grid, \
      self.df_ReactionData_node_grid, _, _ = processSBML._SBMLToDF(sbmlStr_layout_render_node_grid)

    xls_mass_action_rxn = pd.ExcelFile(os.path.join(TEST_FOLDER, 'mass_action_rxn.xlsx'))
    df_CompartmentData_mass_action_rxn = pd.read_excel(xls_mass_action_rxn, 'CompartmentData')
    df_NodeData_mass_action_rxn = pd.read_excel(xls_mass_action_rxn, 'NodeData')
    df_ReactionData_mass_action_rxn = pd.read_excel(xls_mass_action_rxn, 'ReactionData')
    df_TextData_mass_action_rxn = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_TextData)
    df_ShapeData_mass_action_rxn = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_ShapeData)
    df_mass_action_rxn = (df_CompartmentData_mass_action_rxn, \
      df_NodeData_mass_action_rxn, df_ReactionData_mass_action_rxn, df_TextData_mass_action_rxn,
      df_ShapeData_mass_action_rxn)
    sbmlStr_layout_render_mass_action_rxn = exportSBML._DFToSBML(df_mass_action_rxn)
    self.df_CompartmentData_mass_action_rxn, self.df_NodeData_mass_action_rxn, \
      self.df_ReactionData_mass_action_rxn, _, _ = processSBML._SBMLToDF(sbmlStr_layout_render_mass_action_rxn)

    xls_test_textGlyph = pd.ExcelFile(os.path.join(TEST_FOLDER, 'test_textGlyph.xlsx'))
    df_CompartmentData_test_textGlyph = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_TextData)
    df_NodeData_test_textGlyph = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_NodeData)
    df_ReactionData_test_textGlyph = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_ReactionData)
    df_TextData_test_textGlyph = pd.read_excel(xls_test_textGlyph, 'ArbitraryTextData')
    df_ShapeData_test_textGlyph = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_ShapeData)
    df_test_textGlyph = (df_CompartmentData_test_textGlyph, \
      df_NodeData_test_textGlyph, df_ReactionData_test_textGlyph, df_TextData_test_textGlyph,
      df_ShapeData_test_textGlyph)
    sbmlStr_layout_render_test_textGlyph = exportSBML._DFToSBML(df_test_textGlyph)
    _, _, _, self.df_TextData, _ = processSBML._SBMLToDF(sbmlStr_layout_render_test_textGlyph)

    xls_test_genGlyph = pd.ExcelFile(os.path.join(TEST_FOLDER, 'test_genGlyph.xlsx'))
    df_CompartmentData_test_genGlyph = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_CompartmentData)
    df_NodeData_test_genGlyph = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_NodeData)
    df_ReactionData_test_genGlyph = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_ReactionData)
    df_TextData_test_genGlyph = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_TextData)
    df_ShapeData_test_genGlyph = pd.read_excel(xls_test_genGlyph, 'ArbitraryShapeData')
    df_test_genGlyph = (df_CompartmentData_test_genGlyph, \
      df_NodeData_test_genGlyph, df_ReactionData_test_genGlyph, df_TextData_test_genGlyph,
      df_ShapeData_test_genGlyph)
    sbmlStr_layout_render_test_genGlyph = exportSBML._DFToSBML(df_test_genGlyph)
    _, _, _, _, self.df_ShapeData = processSBML._SBMLToDF(sbmlStr_layout_render_test_genGlyph)


  def testCompartment1(self):
    # Test all the column names
    if IGNORE_TEST:
      return    
    test = all(item in self.df_CompartmentData.columns \
      for item in processSBML.COLUMN_NAME_df_CompartmentData)
    test_feedback = all(item in self.df_CompartmentData_feedback.columns \
      for item in processSBML.COLUMN_NAME_df_CompartmentData)
    test_LinearChain = all(item in self.df_CompartmentData_LinearChain.columns \
      for item in processSBML.COLUMN_NAME_df_CompartmentData)
    test_no_comp = all(item in self.df_CompartmentData_test_no_comp.columns \
      for item in processSBML.COLUMN_NAME_df_CompartmentData)
    test_comp = all(item in self.df_CompartmentData_test_comp.columns \
      for item in processSBML.COLUMN_NAME_df_CompartmentData)
    test_modifier = all(item in self.df_CompartmentData_test_modifier.columns \
      for item in processSBML.COLUMN_NAME_df_CompartmentData)
    test_node_grid = all(item in self.df_CompartmentData_node_grid.columns \
      for item in processSBML.COLUMN_NAME_df_CompartmentData)
    test_mass_action_rxn = all(item in self.df_CompartmentData_mass_action_rxn.columns \
      for item in processSBML.COLUMN_NAME_df_CompartmentData)
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
    list_compartment += self.df_CompartmentData[processSBML.COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment += self.df_CompartmentData[processSBML.COLUMN_NAME_df_CompartmentData[1]].tolist()
    test = all(isinstance(item, int) for item in list_compartment)
    list_compartment_feedback = []
    list_compartment_feedback += self.df_CompartmentData_feedback[processSBML.COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_feedback += self.df_CompartmentData_feedback[processSBML.COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_feedback = all(isinstance(item, int) for item in list_compartment_feedback)
    list_compartment_LinearChain = []
    list_compartment_LinearChain += self.df_CompartmentData_LinearChain[processSBML.COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_LinearChain += self.df_CompartmentData_LinearChain[processSBML.COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_LinearChain = all(isinstance(item, int) for item in list_compartment_LinearChain)
    list_compartment_test_no_comp = []
    list_compartment_test_no_comp += self.df_CompartmentData_test_no_comp[processSBML.COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_test_no_comp += self.df_CompartmentData_test_no_comp[processSBML.COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_no_comp = all(isinstance(item, int) for item in list_compartment_test_no_comp)
    list_compartment_test_comp = []
    list_compartment_test_comp += self.df_CompartmentData_test_comp[processSBML.COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_test_comp += self.df_CompartmentData_test_comp[processSBML.COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_comp = all(isinstance(item, int) for item in list_compartment_test_comp)
    list_compartment_test_modifier = []
    list_compartment_test_modifier += self.df_CompartmentData_test_modifier[processSBML.COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_test_modifier += self.df_CompartmentData_test_modifier[processSBML.COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_modifier = all(isinstance(item, int) for item in list_compartment_test_modifier)
    list_compartment_node_grid = []
    list_compartment_node_grid += self.df_CompartmentData_node_grid[processSBML.COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_node_grid += self.df_CompartmentData_node_grid[processSBML.COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_node_grid = all(isinstance(item, int) for item in list_compartment_node_grid)
    list_compartment_mass_action_rxn = []
    list_compartment_mass_action_rxn += self.df_CompartmentData_mass_action_rxn[processSBML.COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_mass_action_rxn += self.df_CompartmentData_mass_action_rxn[processSBML.COLUMN_NAME_df_CompartmentData[1]].tolist()
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
    list_compartment += self.df_CompartmentData[processSBML.COLUMN_NAME_df_CompartmentData[2]].tolist()
    test = all(isinstance(item, str) for item in list_compartment)
    list_compartment_feedback = []
    list_compartment_feedback += self.df_CompartmentData_feedback[processSBML.COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_feedback = all(isinstance(item, str) for item in list_compartment_feedback)
    list_compartment_feedback = []
    list_compartment_feedback += self.df_CompartmentData_feedback[processSBML.COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_feedback = all(isinstance(item, str) for item in list_compartment_feedback)
    list_compartment_LinearChain = []
    list_compartment_LinearChain += self.df_CompartmentData_LinearChain[processSBML.COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_LinearChain = all(isinstance(item, str) for item in list_compartment_LinearChain)
    list_compartment_test_no_comp = []
    list_compartment_test_no_comp += self.df_CompartmentData_test_no_comp[processSBML.COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_no_comp = all(isinstance(item, str) for item in list_compartment_test_no_comp)
    list_compartment_test_comp = []
    list_compartment_test_comp += self.df_CompartmentData_test_comp[processSBML.COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_comp = all(isinstance(item, str) for item in list_compartment_test_comp)
    list_compartment_test_modifier = []
    list_compartment_test_modifier += self.df_CompartmentData_test_modifier[processSBML.COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_modifier = all(isinstance(item, str) for item in list_compartment_test_modifier)
    list_compartment_node_grid = []
    list_compartment_node_grid += self.df_CompartmentData_node_grid[processSBML.COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_node_grid = all(isinstance(item, str) for item in list_compartment_node_grid)
    list_compartment_mass_action_rxn = []
    list_compartment_mass_action_rxn += self.df_CompartmentData_mass_action_rxn[processSBML.COLUMN_NAME_df_CompartmentData[2]].tolist()
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
    list_compartment += self.df_CompartmentData[processSBML.COLUMN_NAME_df_CompartmentData[7]].tolist()
    test = all(isinstance(item, float) for item in list_compartment)
    list_compartment_feedback = []
    list_compartment_feedback += self.df_CompartmentData_feedback[processSBML.COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_feedback = all(isinstance(item, float) for item in list_compartment_feedback)
    list_compartment_LinearChain = []
    list_compartment_LinearChain += self.df_CompartmentData_LinearChain[processSBML.COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_LinearChain = all(isinstance(item, float) for item in list_compartment_LinearChain)
    list_compartment_LinearChain = []
    list_compartment_LinearChain += self.df_CompartmentData_LinearChain[processSBML.COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_LinearChain = all(isinstance(item, float) for item in list_compartment_LinearChain)
    list_compartment_test_no_comp = []
    list_compartment_test_no_comp += self.df_CompartmentData_test_no_comp[processSBML.COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_no_comp = all(isinstance(item, float) for item in list_compartment_test_no_comp)
    list_compartment_test_comp = []
    list_compartment_test_comp += self.df_CompartmentData_test_comp[processSBML.COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_comp = all(isinstance(item, float) for item in list_compartment_test_comp)
    list_compartment_test_modifier = []
    list_compartment_test_modifier += self.df_CompartmentData_test_modifier[processSBML.COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_modifier = all(isinstance(item, float) for item in list_compartment_test_modifier)
    list_compartment_node_grid = []
    list_compartment_node_grid += self.df_CompartmentData_node_grid[processSBML.COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_node_grid = all(isinstance(item, float) for item in list_compartment_node_grid)
    list_compartment_mass_action_rxn = []
    list_compartment_mass_action_rxn += self.df_CompartmentData_mass_action_rxn[processSBML.COLUMN_NAME_df_CompartmentData[7]].tolist()
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
    test = all(item in self.df_NodeData.columns for item in processSBML.COLUMN_NAME_df_NodeData)
    test_feedback = all(item in self.df_NodeData_feedback.columns \
      for item in processSBML.COLUMN_NAME_df_NodeData)
    test_LinearChain = all(item in self.df_NodeData_LinearChain.columns \
      for item in processSBML.COLUMN_NAME_df_NodeData)
    test_no_comp = all(item in self.df_NodeData_test_no_comp.columns \
      for item in processSBML.COLUMN_NAME_df_NodeData)
    test_comp = all(item in self.df_NodeData_test_comp.columns \
      for item in processSBML.COLUMN_NAME_df_NodeData)
    test_modifier = all(item in self.df_NodeData_test_modifier.columns \
      for item in processSBML.COLUMN_NAME_df_NodeData)
    test_node_grid = all(item in self.df_NodeData_node_grid.columns \
      for item in processSBML.COLUMN_NAME_df_NodeData)
    test_mass_action_rxn = all(item in self.df_NodeData_mass_action_rxn.columns \
      for item in processSBML.COLUMN_NAME_df_NodeData)
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
    test_mass_action_rxn = all(isinstance(item, list) for item in list_node_mass_action_rxn)

    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)
    self.assertTrue(test_node_grid)
    self.assertTrue(test_mass_action_rxn)

  def testNode5(self):
    # Test column 'id' and 'floating node' of df_NodeData is str
    if IGNORE_TEST:
      return    
    list_node = []
    list_node += self.df_NodeData[processSBML.COLUMN_NAME_df_NodeData[4]].tolist()
    list_node += self.df_NodeData[processSBML.COLUMN_NAME_df_NodeData[5]].tolist()
    test = all(isinstance(item, str) for item in list_node)
    list_node_feedback = []
    list_node_feedback += self.df_NodeData_feedback[processSBML.COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_feedback += self.df_NodeData_feedback[processSBML.COLUMN_NAME_df_NodeData[5]].tolist()
    test_feedback = all(isinstance(item, str) for item in list_node_feedback)
    list_node_LinearChain = []
    list_node_LinearChain += self.df_NodeData_LinearChain[processSBML.COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_LinearChain += self.df_NodeData_LinearChain[processSBML.COLUMN_NAME_df_NodeData[5]].tolist()
    test_LinearChain = all(isinstance(item, str) for item in list_node_LinearChain)
    list_node_test_no_comp = []
    list_node_test_no_comp += self.df_NodeData_test_no_comp[processSBML.COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_test_no_comp += self.df_NodeData_test_no_comp[processSBML.COLUMN_NAME_df_NodeData[5]].tolist()
    test_no_comp = all(isinstance(item, str) for item in list_node_test_no_comp)
    list_node_test_comp = []
    list_node_test_comp += self.df_NodeData_test_comp[processSBML.COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_test_comp += self.df_NodeData_test_comp[processSBML.COLUMN_NAME_df_NodeData[5]].tolist()
    test_comp = all(isinstance(item, str) for item in list_node_test_comp)
    list_node_test_modifier = []
    list_node_test_modifier += self.df_NodeData_test_modifier[processSBML.COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_test_modifier += self.df_NodeData_test_modifier[processSBML.COLUMN_NAME_df_NodeData[5]].tolist()
    test_modifier = all(isinstance(item, str) for item in list_node_test_modifier)
    list_node_node_grid = []
    list_node_node_grid += self.df_NodeData_node_grid[processSBML.COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_node_grid += self.df_NodeData_node_grid[processSBML.COLUMN_NAME_df_NodeData[5]].tolist()
    test_node_grid = all(isinstance(item, str) for item in list_node_node_grid)
    list_node_mass_action_rxn = []
    list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn[processSBML.COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn[processSBML.COLUMN_NAME_df_NodeData[5]].tolist()
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
    # Test column 'concentration', 'border width', 'txt_line_width', 'txt_font_size' of df_NodeData 
    # are floating numbers
    if IGNORE_TEST:
      return    
    list_node = []
    list_node += self.df_NodeData[processSBML.COLUMN_NAME_df_NodeData[6]].tolist()
    list_node += self.df_NodeData[processSBML.COLUMN_NAME_df_NodeData[14]].tolist()
    list_node += self.df_NodeData[processSBML.COLUMN_NAME_df_NodeData[16]].tolist()
    list_node += self.df_NodeData[processSBML.COLUMN_NAME_df_NodeData[17]].tolist()
    test = all(isinstance(item, float) for item in list_node)
    list_node_feedback = []
    list_node_feedback += self.df_NodeData_feedback[processSBML.COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_feedback += self.df_NodeData_feedback[processSBML.COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_feedback += self.df_NodeData_feedback[processSBML.COLUMN_NAME_df_NodeData[16]].tolist()
    list_node_feedback += self.df_NodeData_feedback[processSBML.COLUMN_NAME_df_NodeData[17]].tolist()
    test_feedback = all(isinstance(item, float) for item in list_node_feedback)
    list_node_LinearChain = []
    list_node_LinearChain += self.df_NodeData_LinearChain[processSBML.COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_LinearChain += self.df_NodeData_LinearChain[processSBML.COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_LinearChain += self.df_NodeData_LinearChain[processSBML.COLUMN_NAME_df_NodeData[16]].tolist()
    list_node_LinearChain += self.df_NodeData_LinearChain[processSBML.COLUMN_NAME_df_NodeData[17]].tolist()
    test_LinearChain = all(isinstance(item, float) for item in list_node_LinearChain)
    list_node_test_no_comp = []
    list_node_test_no_comp += self.df_NodeData_test_no_comp[processSBML.COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_test_no_comp += self.df_NodeData_test_no_comp[processSBML.COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_test_no_comp += self.df_NodeData_test_no_comp[processSBML.COLUMN_NAME_df_NodeData[16]].tolist()
    list_node_test_no_comp += self.df_NodeData_test_no_comp[processSBML.COLUMN_NAME_df_NodeData[17]].tolist()
    test_no_comp = all(isinstance(item, float) for item in list_node_test_no_comp)
    list_node_test_comp = []
    list_node_test_comp += self.df_NodeData_test_comp[processSBML.COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_test_comp += self.df_NodeData_test_comp[processSBML.COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_test_comp += self.df_NodeData_test_comp[processSBML.COLUMN_NAME_df_NodeData[16]].tolist()
    list_node_test_comp += self.df_NodeData_test_comp[processSBML.COLUMN_NAME_df_NodeData[17]].tolist()
    test_comp = all(isinstance(item, float) for item in list_node_test_comp)
    list_node_test_modifier = []
    list_node_test_modifier += self.df_NodeData_test_modifier[processSBML.COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_test_modifier += self.df_NodeData_test_modifier[processSBML.COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_test_modifier += self.df_NodeData_test_modifier[processSBML.COLUMN_NAME_df_NodeData[16]].tolist()
    list_node_test_modifier += self.df_NodeData_test_modifier[processSBML.COLUMN_NAME_df_NodeData[17]].tolist()
    test_modifier = all(isinstance(item, float) for item in list_node_test_modifier)
    list_node_node_grid = []
    list_node_node_grid += self.df_NodeData_node_grid[processSBML.COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_node_grid += self.df_NodeData_node_grid[processSBML.COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_node_grid += self.df_NodeData_node_grid[processSBML.COLUMN_NAME_df_NodeData[16]].tolist()
    list_node_node_grid += self.df_NodeData_node_grid[processSBML.COLUMN_NAME_df_NodeData[17]].tolist()
    test_node_grid = all(isinstance(item, float) for item in list_node_node_grid)
    list_node_mass_action_rxn = []
    list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn[processSBML.COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn[processSBML.COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn[processSBML.COLUMN_NAME_df_NodeData[16]].tolist()
    list_node_mass_action_rxn += self.df_NodeData_mass_action_rxn[processSBML.COLUMN_NAME_df_NodeData[17]].tolist()
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
    test = all(item in self.df_ReactionData.columns for item in processSBML.COLUMN_NAME_df_ReactionData)
    test_feedback = all(item in self.df_ReactionData_feedback.columns \
      for item in processSBML.COLUMN_NAME_df_ReactionData)
    test_LinearChain = all(item in self.df_ReactionData_LinearChain.columns \
      for item in processSBML.COLUMN_NAME_df_ReactionData)
    test_no_comp = all(item in self.df_ReactionData_test_no_comp.columns \
      for item in processSBML.COLUMN_NAME_df_ReactionData)
    test_comp = all(item in self.df_ReactionData_test_comp.columns \
      for item in processSBML.COLUMN_NAME_df_ReactionData)
    test_modifier = all(item in self.df_ReactionData_test_modifier.columns \
      for item in processSBML.COLUMN_NAME_df_ReactionData)
    test_node_grid = all(item in self.df_ReactionData_node_grid.columns \
      for item in processSBML.COLUMN_NAME_df_ReactionData)
    test_mass_action_rxn = all(item in self.df_ReactionData_mass_action_rxn.columns \
      for item in processSBML.COLUMN_NAME_df_ReactionData)
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
    #only grid of nodes, there are no reactions in the network
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
    test_textGlyph = all(item in self.df_TextData.columns \
      for item in processSBML.COLUMN_NAME_df_TextData)
    self.assertTrue(test_textGlyph)

  def testText2(self):
    # Test whether there is at least one row
    if IGNORE_TEST:
      return    
    self.assertTrue(len(self.df_TextData.index)>0) 

  def testText3(self):
    # Test column 'txt_content' of df_TextData are strings
    if IGNORE_TEST:
      return    
    list_text = []
    list_text += self.df_TextData[processSBML.COLUMN_NAME_df_TextData[0]].tolist()
    test_text = all(isinstance(item, str) for item in list_text)
    self.assertTrue(test_text)

  def testText4(self):
    # Test column 'txt_position', 'txt_size' and 'txt_font_color' of df_TextData are lists
    if IGNORE_TEST:
      return    
    list_text = []
    list_text += self.df_TextData[processSBML.COLUMN_NAME_df_TextData[1]].tolist()
    list_text += self.df_TextData[processSBML.COLUMN_NAME_df_TextData[2]].tolist()
    list_text += self.df_TextData[processSBML.COLUMN_NAME_df_TextData[3]].tolist()
    test_text = all(isinstance(item, list) for item in list_text)

    self.assertTrue(test_text)

  def testText5(self):
    # Test column 'txt_line_width' and 'txt_font_size' of df_TextData are float
    if IGNORE_TEST:
      return    
    list_text = []
    list_text += self.df_TextData[processSBML.COLUMN_NAME_df_TextData[4]].tolist()
    list_text += self.df_TextData[processSBML.COLUMN_NAME_df_TextData[5]].tolist()
    test_text = all(isinstance(item, float) for item in list_text)

    self.assertTrue(test_text)

  def testShape1(self):
    # Test all the column names
    if IGNORE_TEST:
      return    
    test_genGlyph = all(item in self.df_ShapeData.columns \
      for item in processSBML.COLUMN_NAME_df_ShapeData)
    self.assertTrue(test_genGlyph)

  def testShape2(self):
    # Test whether there is at least one row
    if IGNORE_TEST:
      return    
    self.assertTrue(len(self.df_ShapeData.index)>0) 

  def testShape3(self):
    # Test column 'shape_name' and 'shape_type' of df_TextData are strings
    if IGNORE_TEST:
      return    
    list_shape = []
    list_shape += self.df_ShapeData[processSBML.COLUMN_NAME_df_ShapeData[0]].tolist()
    list_shape += self.df_ShapeData[processSBML.COLUMN_NAME_df_ShapeData[6]].tolist()
    test_shape = all(isinstance(item, str) for item in list_shape)
    self.assertTrue(test_shape)

  def testShape4(self):
    # Test column 'position', 'size', 'fill_color', 'border_color', 'shape_info' of df_ShapeData are lists
    if IGNORE_TEST:
      return    
    list_shape = []
    list_shape += self.df_ShapeData[processSBML.COLUMN_NAME_df_ShapeData[1]].tolist()
    list_shape += self.df_ShapeData[processSBML.COLUMN_NAME_df_ShapeData[2]].tolist()
    list_shape += self.df_ShapeData[processSBML.COLUMN_NAME_df_ShapeData[3]].tolist()
    list_shape += self.df_ShapeData[processSBML.COLUMN_NAME_df_ShapeData[4]].tolist()
    list_shape += self.df_ShapeData[processSBML.COLUMN_NAME_df_ShapeData[7]].tolist()
    test_shape = all(isinstance(item, list) for item in list_shape)

    self.assertTrue(test_shape)

  def testShape5(self):
    # Test column 'border_width' of df_TextData are float
    if IGNORE_TEST:
      return    
    list_shape = []
    list_shape += self.df_ShapeData[processSBML.COLUMN_NAME_df_ShapeData[5]].tolist()
    test_shape = all(isinstance(item, float) for item in list_shape)

    self.assertTrue(test_shape)


if __name__ == '__main__':
  unittest.main()




