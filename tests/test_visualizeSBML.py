import unittest
import os
from SBMLDiagrams import processSBML
from SBMLDiagrams import visualizeSBML
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

  def plotInvalidStr(self):
    # system exit if plot an invalid string
    if IGNORE_TEST:
      return    
    with self.assertRaises(SystemExit):
         visualizeSBML.plot("adb")

if __name__ == '__main__':
  unittest.main()
  