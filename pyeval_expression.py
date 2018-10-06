"""
Expression - defines an infix expression

Uses Operand to break the infix expression down, and
outputs an RPN string using the shunting yard approach
"""

from pyeval_operator import Operator

class Expression():
    """ Defines the expression."""

    # The operator_stack variable uses standard Python lists to implement
    # a simple stack. As operators are parsed from the string,
    # they are appended to the stack. As the input string is processed, the
    # grows as needed. In the end, it should be empty.

    operator_stack = []             # Holds the current stack of operators

    # Store the string, and where we are in our parsing run.
    expr_string = ""
    output_string = ""
    current_position = 0

    # Have we evaluated this expressions yet?
    evaluated = False

    def __init__(self, expression_string):
        """ Create a new expression."""
        # Add '$' as an end of line marker
        self.expr_string = expression_string + "$"
        self.current_position = 0
        self.output_string = ""

        # Clear the stack
        self.operator_stack.clear()

        # Reset the evaluated flag
        self.evaluated = False

    def result(self):
        """
        Returns the result of the evaluation.
        If the expression is not yet evaluated, we attempt to parse the expression
          If this is unsuccessful, we raise a ValueError exception.
        Else we return the output string
        """
        if not self.evaluated:
            self.parse()
            if not self.evaluated:
                raise ValueError
        return self.output_string

    def parse(self):
        """ Parses the current infix expression, and return the RPN version."""

        # If we've already evaluated, just return the result
        if self.evaluated:
            return self.output_string

        # Let's start evaluating
        # First, are we expecting a operand or an operator?
        # We always start with an operand
        expecting_operand = True

        # Get the current character to inspect
        current_char = self.expr_string[self.current_position]

        # Loop until we're past the end of the string
        while self.current_position < len(self.expr_string) and current_char != "$":

            # Store the operand in the current_token string
            current_token = ""

            if expecting_operand:
                # First, we need to check for a leading '-' or '+' sign
                if current_char == "-" or current_char == "+":
                    current_token += current_char
                    self.current_position += 1
                    current_char = self.expr_string[self.current_position]

                # Now we loop for as long as we have numbers
                while current_char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    current_token += current_char
                    self.current_position += 1
                    current_char = self.expr_string[self.current_position]
                    
                # We should have a number now - add it to the output string, space delimited
                self.output_string += current_token + " "

                # And after every operand, we need to look for an operator
                expecting_operand = False
            
            else:
                # Here, we just need a single operator, so
                # Get that operator, validate it, then
                # Create a new operator object
                if current_char not in ["+", "-", "*", "/", "%", "^"]:
                    raise SyntaxError

                current_operator = Operator(current_char)

                # Now comes the shunting yard part
                # - If the operator stack is empty, push the current operator
                # - Else
                #   - While the top of stack operator is higher precedence
                #     - Pop it and output it.
                #   - Push the current operator

                if len(self.operator_stack) == 0:
                    self.operator_stack.append(current_operator)

                else:
                    top_operator = self.operator_stack[len(self.operator_stack)-1]
                    while len(self.operator_stack)>0 and top_operator.precedence > current_operator.precedence:
                        self.output_string += top_operator.op_string + " "
                        self.operator_stack.pop()
                        if len(self.operator_stack)>0:
                            top_operator = self.operator_stack[len(self.operator_stack)-1]

                    self.operator_stack.append(current_operator)

                # Get the next character
                self.current_position += 1
                current_char = self.expr_string[self.current_position]

                # After every operator, look for an operand
                expecting_operand = True

        # At this point, we're done with the string, so we just need to pop
        # the remaining operators off the stack

        while len(self.operator_stack) > 0:
            top_operator = self.operator_stack.pop()
            self.output_string += top_operator.op_string + " "

        self.evaluated = True
        return self.output_string
        