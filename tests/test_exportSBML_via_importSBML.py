import unittest
import os
from SBMLDiagrams import importSBML
from SBMLDiagrams import exportSBML
import pandas as pd
from openpyxl import *

IGNORE_TEST = False

#############################
# Tests
#############################
class TestKineticLaw(unittest.TestCase):

  def setUp(self):
    
    DIR = os.path.dirname(os.path.abspath(__file__))
    TEST_FOLDER = os.path.join(DIR, "initiate_excel_files")
    xls = pd.ExcelFile(os.path.join(TEST_FOLDER, 'test.xlsx'))
    df_CompartmentData = pd.read_excel(xls, 'CompartmentData')
    df_NodeData = pd.read_excel(xls, 'NodeData')
    df_ReactionData = pd.read_excel(xls, 'ReactionData')
    # df_CompartmentData = pd.read_csv(os.path.join(TEST_FOLDER, "CompartmentData.csv")) 
    # df_NodeData = pd.read_csv(os.path.join(TEST_FOLDER, "NodeData.csv"))
    # df_ReactionData = pd.read_csv(os.path.join(TEST_FOLDER, "ReactionData.csv"))
    sbmlStr_layout_render = exportSBML.export(df_CompartmentData, df_NodeData, df_ReactionData)
    self.df_CompartmentData, self.df_NodeData, self.df_ReactionData = importSBML.load(sbmlStr_layout_render)
    
    xls_feedback = pd.ExcelFile(os.path.join(TEST_FOLDER, 'feedback.xlsx'))
    df_CompartmentData_feedback = pd.read_excel(xls_feedback, 'CompartmentData')
    df_NodeData_feedback = pd.read_excel(xls_feedback, 'NodeData')
    df_ReactionData_feedback = pd.read_excel(xls_feedback, 'ReactionData')
    sbmlStr_layout_render_feedback = exportSBML.export(df_CompartmentData_feedback, \
      df_NodeData_feedback, df_ReactionData_feedback)
    self.df_CompartmentData_feedback, self.df_NodeData_feedback, self.df_ReactionData_feedback \
       = importSBML.load(sbmlStr_layout_render_feedback)

    xls_LinearChain = pd.ExcelFile(os.path.join(TEST_FOLDER, 'LinearChain.xlsx'))
    df_CompartmentData_LinearChain = pd.read_excel(xls_LinearChain, 'CompartmentData')
    df_NodeData_LinearChain = pd.read_excel(xls_LinearChain, 'NodeData')
    df_ReactionData_LinearChain = pd.read_excel(xls_LinearChain, 'ReactionData')
    sbmlStr_layout_render_LinearChain = exportSBML.export(df_CompartmentData_LinearChain, \
      df_NodeData_LinearChain, df_ReactionData_LinearChain)
    self.df_CompartmentData_LinearChain, self.df_NodeData_LinearChain, self.df_ReactionData_LinearChain \
       = importSBML.load(sbmlStr_layout_render_LinearChain)

    xls_test_no_comp = pd.ExcelFile(os.path.join(TEST_FOLDER, 'test_no_comp.xlsx'))
    df_CompartmentData_test_no_comp = pd.read_excel(xls_test_no_comp, 'CompartmentData')
    df_NodeData_test_no_comp = pd.read_excel(xls_test_no_comp, 'NodeData')
    df_ReactionData_test_no_comp = pd.read_excel(xls_test_no_comp, 'ReactionData')
    sbmlStr_layout_render_test_no_comp = exportSBML.export(df_CompartmentData_test_no_comp, \
      df_NodeData_test_no_comp, df_ReactionData_test_no_comp)
    self.df_CompartmentData_test_no_comp, self.df_NodeData_test_no_comp, \
      self.df_ReactionData_test_no_comp = importSBML.load(sbmlStr_layout_render_test_no_comp)

    xls_test_comp = pd.ExcelFile(os.path.join(TEST_FOLDER, 'test_comp.xlsx'))
    df_CompartmentData_test_comp = pd.read_excel(xls_test_comp, 'CompartmentData')
    df_NodeData_test_comp = pd.read_excel(xls_test_comp, 'NodeData')
    df_ReactionData_test_comp = pd.read_excel(xls_test_comp, 'ReactionData')
    sbmlStr_layout_render_test_comp = exportSBML.export(df_CompartmentData_test_comp, \
      df_NodeData_test_comp, df_ReactionData_test_comp)
    self.df_CompartmentData_test_comp, self.df_NodeData_test_comp, \
      self.df_ReactionData_test_comp = importSBML.load(sbmlStr_layout_render_test_comp)

    xls_test_modifier = pd.ExcelFile(os.path.join(TEST_FOLDER, 'test_modifier.xlsx'))
    df_CompartmentData_test_modifier = pd.read_excel(xls_test_modifier, 'CompartmentData')
    df_NodeData_test_modifier = pd.read_excel(xls_test_modifier, 'NodeData')
    df_ReactionData_test_modifier = pd.read_excel(xls_test_modifier, 'ReactionData')
    sbmlStr_layout_render_test_modifier = exportSBML.export(df_CompartmentData_test_modifier, \
      df_NodeData_test_modifier, df_ReactionData_test_modifier)
    self.df_CompartmentData_test_modifier, self.df_NodeData_test_modifier, \
      self.df_ReactionData_test_modifier = importSBML.load(sbmlStr_layout_render_test_modifier)

  def testCompartment1(self):
    # Test all the column names
    if IGNORE_TEST:
      return    
    test = all(item in self.df_CompartmentData.columns \
      for item in importSBML.COLUMN_NAME_df_CompartmentData)
    test_feedback = all(item in self.df_CompartmentData_feedback.columns \
      for item in importSBML.COLUMN_NAME_df_CompartmentData)
    test_LinearChain = all(item in self.df_CompartmentData_LinearChain.columns \
      for item in importSBML.COLUMN_NAME_df_CompartmentData)
    test_no_comp = all(item in self.df_CompartmentData_test_no_comp.columns \
      for item in importSBML.COLUMN_NAME_df_CompartmentData)
    test_comp = all(item in self.df_CompartmentData_test_comp.columns \
      for item in importSBML.COLUMN_NAME_df_CompartmentData)
    test_modifier = all(item in self.df_CompartmentData_test_modifier.columns \
      for item in importSBML.COLUMN_NAME_df_CompartmentData)
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)

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

  def testCompartment3(self):
    # Test column 'net_idx' and 'idx' of df_CompartmentData are integers
    if IGNORE_TEST:
      return    
    list_compartment = []
    list_compartment += self.df_CompartmentData[importSBML.COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment += self.df_CompartmentData[importSBML.COLUMN_NAME_df_CompartmentData[1]].tolist()
    test = all(isinstance(item, int) for item in list_compartment)
    list_compartment_feedback = []
    list_compartment_feedback += self.df_CompartmentData_feedback[importSBML.COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_feedback += self.df_CompartmentData_feedback[importSBML.COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_feedback = all(isinstance(item, int) for item in list_compartment_feedback)
    list_compartment_LinearChain = []
    list_compartment_LinearChain += self.df_CompartmentData_LinearChain[importSBML.COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_LinearChain += self.df_CompartmentData_LinearChain[importSBML.COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_LinearChain = all(isinstance(item, int) for item in list_compartment_LinearChain)
    list_compartment_test_no_comp = []
    list_compartment_test_no_comp += self.df_CompartmentData_test_no_comp[importSBML.COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_test_no_comp += self.df_CompartmentData_test_no_comp[importSBML.COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_no_comp = all(isinstance(item, int) for item in list_compartment_test_no_comp)
    list_compartment_test_comp = []
    list_compartment_test_comp += self.df_CompartmentData_test_comp[importSBML.COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_test_comp += self.df_CompartmentData_test_comp[importSBML.COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_comp = all(isinstance(item, int) for item in list_compartment_test_comp)
    list_compartment_test_modifier = []
    list_compartment_test_modifier += self.df_CompartmentData_test_modifier[importSBML.COLUMN_NAME_df_CompartmentData[0]].tolist()
    list_compartment_test_modifier += self.df_CompartmentData_test_modifier[importSBML.COLUMN_NAME_df_CompartmentData[1]].tolist()
    test_modifier = all(isinstance(item, int) for item in list_compartment_test_modifier)
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)


  def testCompartment4(self):
    # Test column 'id' of df_CompartmentData is string
    if IGNORE_TEST:
      return    
    list_compartment = []
    list_compartment += self.df_CompartmentData[importSBML.COLUMN_NAME_df_CompartmentData[2]].tolist()
    test = all(isinstance(item, str) for item in list_compartment)
    list_compartment_feedback = []
    list_compartment_feedback += self.df_CompartmentData_feedback[importSBML.COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_feedback = all(isinstance(item, str) for item in list_compartment_feedback)
    list_compartment_feedback = []
    list_compartment_feedback += self.df_CompartmentData_feedback[importSBML.COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_feedback = all(isinstance(item, str) for item in list_compartment_feedback)
    list_compartment_LinearChain = []
    list_compartment_LinearChain += self.df_CompartmentData_LinearChain[importSBML.COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_LinearChain = all(isinstance(item, str) for item in list_compartment_LinearChain)
    list_compartment_test_no_comp = []
    list_compartment_test_no_comp += self.df_CompartmentData_test_no_comp[importSBML.COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_no_comp = all(isinstance(item, str) for item in list_compartment_test_no_comp)
    list_compartment_test_comp = []
    list_compartment_test_comp += self.df_CompartmentData_test_comp[importSBML.COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_comp = all(isinstance(item, str) for item in list_compartment_test_comp)
    list_compartment_test_modifier = []
    list_compartment_test_modifier += self.df_CompartmentData_test_modifier[importSBML.COLUMN_NAME_df_CompartmentData[2]].tolist()
    test_modifier = all(isinstance(item, str) for item in list_compartment_test_modifier)
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)

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
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)

  def testCompartment6(self):
    # Test column 'border width' of df_CompartmentData is a floating number
    if IGNORE_TEST:
      return    
    list_compartment = []
    list_compartment += self.df_CompartmentData[importSBML.COLUMN_NAME_df_CompartmentData[7]].tolist()
    test = all(isinstance(item, float) for item in list_compartment)
    list_compartment_feedback = []
    list_compartment_feedback += self.df_CompartmentData_feedback[importSBML.COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_feedback = all(isinstance(item, float) for item in list_compartment_feedback)
    list_compartment_LinearChain = []
    list_compartment_LinearChain += self.df_CompartmentData_LinearChain[importSBML.COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_LinearChain = all(isinstance(item, float) for item in list_compartment_LinearChain)
    list_compartment_LinearChain = []
    list_compartment_LinearChain += self.df_CompartmentData_LinearChain[importSBML.COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_LinearChain = all(isinstance(item, float) for item in list_compartment_LinearChain)
    list_compartment_test_no_comp = []
    list_compartment_test_no_comp += self.df_CompartmentData_test_no_comp[importSBML.COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_no_comp = all(isinstance(item, float) for item in list_compartment_test_no_comp)
    list_compartment_test_comp = []
    list_compartment_test_comp += self.df_CompartmentData_test_comp[importSBML.COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_comp = all(isinstance(item, float) for item in list_compartment_test_comp)
    list_compartment_test_modifier = []
    list_compartment_test_modifier += self.df_CompartmentData_test_modifier[importSBML.COLUMN_NAME_df_CompartmentData[7]].tolist()
    test_modifier = all(isinstance(item, float) for item in list_compartment_test_modifier)

    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)

  def testNode1(self):
    # Test all the column names
    if IGNORE_TEST:
      return    
    test = all(item in self.df_NodeData.columns for item in importSBML.COLUMN_NAME_df_NodeData)
    test_feedback = all(item in self.df_NodeData_feedback.columns \
      for item in importSBML.COLUMN_NAME_df_NodeData)
    test_LinearChain = all(item in self.df_NodeData_LinearChain.columns \
      for item in importSBML.COLUMN_NAME_df_NodeData)
    test_no_comp = all(item in self.df_NodeData_test_no_comp.columns \
      for item in importSBML.COLUMN_NAME_df_NodeData)
    test_comp = all(item in self.df_NodeData_test_comp.columns \
      for item in importSBML.COLUMN_NAME_df_NodeData)
    test_modifier = all(item in self.df_NodeData_test_modifier.columns \
      for item in importSBML.COLUMN_NAME_df_NodeData)
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)

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
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)


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

    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)

  def testNode5(self):
    # Test column 'id' and 'floating node' of df_NodeData is str
    if IGNORE_TEST:
      return    
    list_node = []
    list_node += self.df_NodeData[importSBML.COLUMN_NAME_df_NodeData[4]].tolist()
    list_node += self.df_NodeData[importSBML.COLUMN_NAME_df_NodeData[5]].tolist()
    test = all(isinstance(item, str) for item in list_node)
    list_node_feedback = []
    list_node_feedback += self.df_NodeData_feedback[importSBML.COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_feedback += self.df_NodeData_feedback[importSBML.COLUMN_NAME_df_NodeData[5]].tolist()
    test_feedback = all(isinstance(item, str) for item in list_node_feedback)
    list_node_LinearChain = []
    list_node_LinearChain += self.df_NodeData_LinearChain[importSBML.COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_LinearChain += self.df_NodeData_LinearChain[importSBML.COLUMN_NAME_df_NodeData[5]].tolist()
    test_LinearChain = all(isinstance(item, str) for item in list_node_LinearChain)
    list_node_test_no_comp = []
    list_node_test_no_comp += self.df_NodeData_test_no_comp[importSBML.COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_test_no_comp += self.df_NodeData_test_no_comp[importSBML.COLUMN_NAME_df_NodeData[5]].tolist()
    test_no_comp = all(isinstance(item, str) for item in list_node_test_no_comp)
    list_node_test_comp = []
    list_node_test_comp += self.df_NodeData_test_comp[importSBML.COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_test_comp += self.df_NodeData_test_comp[importSBML.COLUMN_NAME_df_NodeData[5]].tolist()
    test_comp = all(isinstance(item, str) for item in list_node_test_comp)
    list_node_test_modifier = []
    list_node_test_modifier += self.df_NodeData_test_modifier[importSBML.COLUMN_NAME_df_NodeData[4]].tolist()
    list_node_test_modifier += self.df_NodeData_test_modifier[importSBML.COLUMN_NAME_df_NodeData[5]].tolist()
    test_modifier = all(isinstance(item, str) for item in list_node_test_modifier)

    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)

  def testNode6(self):
    # Test column 'concentration', 'border width' and 'txt_line_width' of df_NodeData 
    # are floating numbers
    if IGNORE_TEST:
      return    
    list_node = []
    list_node += self.df_NodeData[importSBML.COLUMN_NAME_df_NodeData[6]].tolist()
    list_node += self.df_NodeData[importSBML.COLUMN_NAME_df_NodeData[14]].tolist()
    list_node += self.df_NodeData[importSBML.COLUMN_NAME_df_NodeData[16]].tolist()
    test = all(isinstance(item, float) for item in list_node)
    list_node_feedback = []
    list_node_feedback += self.df_NodeData_feedback[importSBML.COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_feedback += self.df_NodeData_feedback[importSBML.COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_feedback += self.df_NodeData_feedback[importSBML.COLUMN_NAME_df_NodeData[16]].tolist()
    test_feedback = all(isinstance(item, float) for item in list_node_feedback)
    list_node_LinearChain = []
    list_node_LinearChain += self.df_NodeData_LinearChain[importSBML.COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_LinearChain += self.df_NodeData_LinearChain[importSBML.COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_LinearChain += self.df_NodeData_LinearChain[importSBML.COLUMN_NAME_df_NodeData[16]].tolist()
    test_LinearChain = all(isinstance(item, float) for item in list_node_LinearChain)
    list_node_test_no_comp = []
    list_node_test_no_comp += self.df_NodeData_test_no_comp[importSBML.COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_test_no_comp += self.df_NodeData_test_no_comp[importSBML.COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_test_no_comp += self.df_NodeData_test_no_comp[importSBML.COLUMN_NAME_df_NodeData[16]].tolist()
    test_no_comp = all(isinstance(item, float) for item in list_node_test_no_comp)
    list_node_test_comp = []
    list_node_test_comp += self.df_NodeData_test_comp[importSBML.COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_test_comp += self.df_NodeData_test_comp[importSBML.COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_test_comp += self.df_NodeData_test_comp[importSBML.COLUMN_NAME_df_NodeData[16]].tolist()
    test_comp = all(isinstance(item, float) for item in list_node_test_comp)
    list_node_test_modifier = []
    list_node_test_modifier += self.df_NodeData_test_modifier[importSBML.COLUMN_NAME_df_NodeData[6]].tolist()
    list_node_test_modifier += self.df_NodeData_test_modifier[importSBML.COLUMN_NAME_df_NodeData[14]].tolist()
    list_node_test_modifier += self.df_NodeData_test_modifier[importSBML.COLUMN_NAME_df_NodeData[16]].tolist()
    test_modifier = all(isinstance(item, float) for item in list_node_test_modifier)

    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)

  def testReaction1(self):
    # Test all the column names
    if IGNORE_TEST:
      return    
    test = all(item in self.df_ReactionData.columns for item in importSBML.COLUMN_NAME_df_ReactionData)
    test_feedback = all(item in self.df_ReactionData_feedback.columns \
      for item in importSBML.COLUMN_NAME_df_ReactionData)
    test_LinearChain = all(item in self.df_ReactionData_LinearChain.columns \
      for item in importSBML.COLUMN_NAME_df_ReactionData)
    test_no_comp = all(item in self.df_ReactionData_test_no_comp.columns \
      for item in importSBML.COLUMN_NAME_df_ReactionData)
    test_comp = all(item in self.df_ReactionData_test_comp.columns \
      for item in importSBML.COLUMN_NAME_df_ReactionData)
    test_modifier = all(item in self.df_ReactionData_test_modifier.columns \
      for item in importSBML.COLUMN_NAME_df_ReactionData)
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)

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

    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)

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
    
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)

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

    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)

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
    self.assertTrue(test)
    self.assertTrue(test_feedback)
    self.assertTrue(test_LinearChain)
    self.assertTrue(test_no_comp)
    self.assertTrue(test_comp)
    self.assertTrue(test_modifier)


if __name__ == '__main__':
  unittest.main()




