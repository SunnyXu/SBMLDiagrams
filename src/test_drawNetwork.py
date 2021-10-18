import drawNetwork
import unittest

IGNORE_TEST = False

#############################
# Tests
#############################
class TestKineticLaw(unittest.TestCase):

  def setUp(self):
    initial_model_indx = 5
    final_model_indx = 6
    self.test = 1

  def testClassification1(self):
    # Test all the column names
    if IGNORE_TEST:
      return    
    self.assertTrue(self.test == 1)

  def testClassification2(self):
    # Test whether there is at least one row
    if IGNORE_TEST:
      return    
    self.assertFalse(self.test == 2)

if __name__ == '__main__':
  unittest.main()




