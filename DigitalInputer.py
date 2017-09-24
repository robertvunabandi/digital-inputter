from Expression import ExpressionAsserter, Expression
from BasicOperation import InputAsserter, BasicOperation, AdvancedOperation

class DigitalInputer:
    """
    Given a raw expression (as defined in Expression.py),
    this class will help getting outputs from that 
    the parsed Expression returned from Expression class
    in Expression.py. 

    For syntax on how to write raw expressions, please see
    Expression.py. This supports AdvancedOperator syntax
    as well; see BasicOperation.py or ExpressionAsserter.py
    for more information.

    Useful methods:
    - getOutput(input_array): given an input array, this
        returns the output of the given raw expression. 
    - getOuputTablePrintReady(): this returns a string
        containing an output table with every possible
        inputs in a clearly defined setup with headers
        containing the input Values (as defined is 
        Expression.py) and "OUT" (short for output). 
    - getTableOutputDictionary(): returns a dictionary
        mapping tuples of inputs to an output. Similar
        to the table, except one can get certain values
        directly from this dictionary.
    - printOutputTable(): prints the output table received
        from getOuputTablePrintReady()
    """

    def __init__(self, raw):
        """
        All that is needed for the initialization
        is a raw expression. This raw expression
        is an expression as defined in Expression.py
        """
        self.expression = Expression(raw)
    
    def getOutput(self, array):
        """
        Given an input as an array (for example, "[0,1]"), 
        this  returns whatever the output needs to be. The 
        order of inputs is given in Alphabetical order. 
        For instance, if given input "[0,0,1]" for 
        variables are "B, H, E", the first 0 would be 
        mapped to "B", the second 0 would be mapped to
        "E", and 1 would be mapped to "H".
        
        This is a design decision that is more convenient
        in place of defining an obscure logic to the 
        mapping of the variables in the expression.
        """
        self.__assertArrayLengthIsValid(array)
        return self.__solveOutputForInput(array, self.expression.parsed)

    def __solveOutputForInput(self, input_array, parsed_expression):
        """
        Given an input_array, this will given an output
        based on the parsed expression
        """
        operation = self.__getOperation(parsed_expression)
        inputs = self.__getDigitalInputs(input_array, parsed_expression)
        return AdvancedOperation.getOutput(operation, inputs)

    def __getOperation(self, parsed_expression):
        """
        Returns the operation of a parsed Expression,
        which is always in the first index of the
        Expression
        """
        return parsed_expression[0]
    
    def __getDigitalInputs(self, input_array, parsed_expression):
        """ 
        returns an array containing 0's and 1's based on
        the input_array and parsed expression. 

        If parsed_expression is [33, "A"] and input_array
        is [0], then it'll return [0]. The not operation
        (33) is to be done elsewhere, not here.
        """
        inputs = []
        # ignore the operator, which is always the first element
        for expr in parsed_expression[1:]: 
            if (DigitalInputer.__isValue(expr)):
                # map the expression to the actual value
                inputs.append(self.__mapToDigitalInput(input_array, expr))
            else:
                # solve for the given expression
                inputs.append(self.__solveOutputForInput(input_array, expr))
        return inputs

    @staticmethod
    def __isValue(expression):
        """
        Checks whether the given expression is a
        Value (an alphabetical letter) ASA or an 
        Expression ASA
        """
        return type(expression) != list

    def __mapToDigitalInput(self, input_array, expr):
        """
        Maps a digital value, say "A", to an input
        value.
        """
        index = self.expression.varsSorted.index(expr)
        return input_array[index]

    def __assertArrayLengthIsValid(self, array):
        """
        The length of this array must be equal to
        self.expresssion.varCount
        """
        msg =  "The length of the array must equal the number of variables in the expression"
        assert len(array) == self.expression.varCount, msg

    def getTableOutputDictionary(self):
        """
        Returns a dictionary mapping tuples of inputs
        (e.g.: (0,0,1)) to digital value outputs. 
        
        For some reason, the order in which they come
        is shuffle, but that's okay.
        """
        array_inputs_list = DigitalInputer.__getArrayInputsList(self.expression.varCount)
        dic = {}
        for array_input in array_inputs_list:
            dic[tuple(array_input)] = self.getOutput(array_input)
        return dic

    @staticmethod
    def __getArrayInputsList(count):
        """
        Given a count, say N, this will return an array
        of binary digits ranging from 0 to 2^N - 1. For
        example, if count = 2, then the output will be
        [[0,0], [0,1], [1,0], [1,1]]
        """
        array_inputs_list = []
        max_number = 2**(count)
        for number in range(max_number):
            array_inputs_list.append(DigitalInputer.__arrayFromBinary(bin(number), count))
        return array_inputs_list

    @staticmethod
    def __arrayFromBinary(binary_number, var_count):
        """
        Given a binary number "0bxx...x", this returns
        the array [x, x, x, ..., x] where each x in
        an integer that is either 1 or 0
        """
        attempt = [int(IN) for IN in binary_number[2:]]
        while (len(attempt)) < var_count:
            # the length needs to be as long as var_count
            # so if it's not, insert, at index 0, a 0
            attempt.insert(0, 0)
        return attempt

    def getOuputTablePrintReady(self):
        """
        Returns a string containing the output table
        with the given inputs and "OUT" as headers
        and every possible combination of outputs for
        the given inputs
        """
        array_inputs_list = DigitalInputer.__getArrayInputsList(self.expression.varCount)
        string = "\n" + DigitalInputer.__printOutputTableLine(self.expression.varsSorted, "OUT")
        for array_input in array_inputs_list:
            string += "\n" + DigitalInputer.__printOutputTableLine(array_input, self.getOutput(array_input))
        return string

    @staticmethod
    def __printOutputTableLine(expression_values, output):
        """
        Returns a string containing the line, as needed,
        for the output table. expression_values should 
        have the length of self.expression.varCount and
        is an array of either alphabetical letters or
        digital input values output is either a string 
        or an integer
        """
        string = ""
        for expr in expression_values:
            string += str(expr) + " "
        string += "| " + str(output)
        return string

    def printOutputTable(self):
        """
        Prints the output table
        """
        print(self.getOuputTablePrintReady())
        
