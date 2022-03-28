import unittest
import os
from SBMLDiagrams import processSBML
from SBMLDiagrams import visualizeSBML
import SBMLDiagrams
#from pandas.testing import assert_frame_equal

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
    self.sbmlStr_test = f_test.read()
    f_test.close()
    TEST_PATH_LinearChain = os.path.join(TEST_FOLDER, "LinearChain.xml")
    f_LinearChain = open(TEST_PATH_LinearChain, 'r')
    self.sbmlStr_LinearChain = f_LinearChain.read()
    f_LinearChain.close()
    TEST_PATH_test_textGlyph = os.path.join(TEST_FOLDER, "test_textGlyph.xml")
    f_test_textGlyph = open(TEST_PATH_test_textGlyph, 'r')
    self.sbmlStr_test_textGlyph = f_test_textGlyph.read()
    f_test_textGlyph.close()
    TEST_PATH_test_genGlyph = os.path.join(TEST_FOLDER, "test_genGlyph.xml")
    f_test_genGlyph = open(TEST_PATH_test_genGlyph, 'r')
    self.sbmlStr_test_genGlyph = f_test_genGlyph.read()
    f_test_genGlyph.close()

  def test(self):
    # Test the functions related to network positions and size

    if IGNORE_TEST:
      return

    self.assertTrue(visualizeSBML._getNetworkTopLeftCorner(self.sbmlStr_test) == [205.0, 216.0])
    self.assertTrue(visualizeSBML._getNetworkBottomRightCorner(self.sbmlStr_test) == [463.0, 246.0])
    self.assertTrue(visualizeSBML._getNetworkSize(self.sbmlStr_test) == [258, 30])
    #boundary nodes from LinearChain.xml
    self.assertTrue(visualizeSBML._getNetworkTopLeftCorner(self.sbmlStr_LinearChain) == [40.0, 109.0])
    self.assertTrue(visualizeSBML._getNetworkBottomRightCorner(self.sbmlStr_LinearChain) == [702.0, 149.0])
    #text from test_textGlyph.xml
    self.assertTrue(visualizeSBML._getNetworkTopLeftCorner(self.sbmlStr_test_textGlyph) == [92.0, 26.0])
    self.assertTrue(visualizeSBML._getNetworkBottomRightCorner(self.sbmlStr_test_textGlyph) == [320.0, 194.0])
    #text from test_genGlyph.xml
    self.assertTrue(visualizeSBML._getNetworkTopLeftCorner(self.sbmlStr_test_genGlyph) == [177.0, 107.0])
    self.assertTrue(visualizeSBML._getNetworkBottomRightCorner(self.sbmlStr_test_genGlyph) == [227.0, 137.0])


  # def plotInvalidStr(self):
  #   # system exit if plot an invalid string
  #   if IGNORE_TEST:
  #     return    
  #   with self.assertRaises(SystemExit):
  #        visualizeSBML.draw("adb")


if __name__ == '__main__':
  unittest.main()
  