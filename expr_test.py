'''
Test cases for PyEval

Jon Fincher, July 2018
'''
import unittest
from pyeval_expression import Expression

class TestPyEval(unittest.TestCase):

    '''
    test_positive_operand_expression - tests a correct result from a single positive operand expression
    '''
    def test_positive_operand_expression(self):
        expr = Expression("53")
        self.assertEqual("53 ", expr.result(), "ERROR: Positive operand")

    '''
    test_negative_operand_expression - tests a correct result from a single negative operand expression
    '''
    def test_negative_operand_expression(self):
        expr = Expression("-53")
        self.assertEqual("-53 ", expr.result(), "ERROR: Negative operand")

    '''
    test_double_term_expression - tests a correct result from a set of double term expressions
    '''
    def test_double_term_expression(self):
        expr = Expression("53+2")
        self.assertEqual("53 2 + ", expr.result(), "ERROR: Double positive term expression")
        expr = Expression("-53+2")
        self.assertEqual("-53 2 + ", expr.result(), "ERROR: Negative/positive term expression")
        expr = Expression("53+-2")
        self.assertEqual("53 -2 + ", expr.result(), "ERROR: Positive/negative term expression")
        expr = Expression("-53+-2")
        self.assertEqual("-53 -2 + ", expr.result(), "ERROR: Double negative term expression")

    '''
    test_double_term_operands - tests a correct result from a set of operands
    '''
    def test_double_term_operands(self):
        expr = Expression("53+2")
        self.assertEqual("53 2 + ", expr.result(), "ERROR: Additive expression")
        expr = Expression("53-2")
        self.assertEqual("53 2 - ", expr.result(), "ERROR: Subtrative expression")
        expr = Expression("53*2")
        self.assertEqual("53 2 * ", expr.result(), "ERROR: Multiplicative expression")
        expr = Expression("53/2")
        self.assertEqual("53 2 / ", expr.result(), "ERROR: Divide expression")

    '''
    test_triple_term_expression - tests a correct result from a set of triple term expressions
    '''
    def test_triple_term_expression(self):
        expr = Expression("53+2+37")
        self.assertEqual("53 2 37 + + ", expr.result(), "ERROR: Add/Add expression")
        expr = Expression("53+2*37")
        self.assertEqual("53 2 37 * + ", expr.result(), "ERROR: Add/Multiply expression")
        expr = Expression("53*2+37")
        self.assertEqual("53 2 * 37 + ", expr.result(), "ERROR: Multiply/Add expression")
        expr = Expression("53*2*37")
        self.assertEqual("53 2 37 * * ", expr.result(), "ERROR: Multiply/Multiply expression")

    '''
    test_whitespace_expression - tests a correct result from a variety of whitespace
    '''
    def test_whitespace_expression(self):
        expr = Expression("53+2+37")
        self.assertEqual("53 2 37 + + ", expr.result(), "ERROR: No whitespace expression")
        expr = Expression("53 + 2 + 37")
        self.assertEqual("53 2 37 + + ", expr.result(), "ERROR: Infixed whitespace expression")
        expr = Expression(" 53+2+37 ")
        self.assertEqual("53 2 37 + + ", expr.result(), "ERROR: Pre/post-fixed whitespace expression")
        expr = Expression(" 53 + 2 + 37 ")
        self.assertEqual("53 2 37 + + ", expr.result(), "ERROR: Pre/post/in-fixed whitespace expression")
        expr = Expression("  53  +  2  +  37  ")
        self.assertEqual("53 2 37 + + ", expr.result(), "ERROR: Multiple whitespace expression")
        # This test should throw an exception - spaces in between operands should give an error
        with self.assertRaises(SyntaxError):
            expr = Expression("  53  +  -  2  +  37  ")
            expr.parse()

