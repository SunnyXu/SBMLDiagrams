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
    sbmlStr_test = f_test.read()
    f_test.close()

    self.df = processSBML._SBMLToDF(sbmlStr_test)

  def plotInvalidStr(self):
    # system exit if plot an invalid string
    if IGNORE_TEST:
      return    
    with self.assertRaises(SystemExit):
         visualizeSBML.plot("adb")

if __name__ == '__main__':
  unittest.main()
  