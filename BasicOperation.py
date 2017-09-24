class InputAsserter:
    """
    Asserts whether an array of inputs or an input is valid
    """
    @staticmethod
    def __errorMessage(_in):
        """
        Specific error message for when the input is invalid
        """
        return "input must be 1 or 0. Received: " + str(_in)

    
    @staticmethod
    def assertInput(IN):
        """
        Checks whether one input is valid
        """
        assert type(IN) == int, "Argument given must be an integer"
        assert IN == 0 or IN == 1, InputAsserter.__errorMessage(IN)
    
    @staticmethod
    def assertInputs(INS):
        """
        Checks whether each element in an array of input is valid
        """
        assert type(INS) == list, "Inputs must be a list"
        for IN in INS:
            InputAsserter.assertInput(IN)
        
    @staticmethod
    def assertSingleInput(INS):
        """
        Checks whether the length of the array is 1
        """
        InputAsserter.assertInputs(INS)
        assert len(INS) == 1, "Inputs list must be of length 1"

    @staticmethod
    def assertDoubleInput(INS):
        """
        Checks whether the length of the array is 2
        """
        InputAsserter.assertInputs(INS)
        assert len(INS) == 2, "Inputs list must be of length 2"

    @staticmethod
    def assertArrayIsValid(array):
        """
        Checks whether the array is an array and has length > 1
        """
        assert type(array) == list, "Argument given must be a list"
        assert len(array) > 1, "Length of array given was less than 2"
  
class BasicOperation:
    """
    Has the basic logic operators OR, AND, and NAND
    """

    SYMBOLS = {"OR": "+", "AND": "*", "NOT": "!"}

    @staticmethod
    def NOT(IN):
        """
        NOT logic operator: 0 => 1, 1 => 0
        """
        InputAsserter.assertSingleInput(IN)
        return 1 - IN[0]

    @staticmethod
    def OR(array):
        """
        OR logic operator: 0,0 => 0, 0,1 => 1, 1,0 => 1, 1,1 => 1
        """
        InputAsserter.assertArrayIsValid(array)
        for IN in array:
            InputAsserter.assertInput(IN)
            if IN == 1:
                return 1
        return 0

    @staticmethod
    def AND(array):
        """
        AND logic operator: 0,0 => 0, 0,1 => 0, 1,0 => 0, 1,1 => 1
        """
        InputAsserter.assertArrayIsValid(array)
        for IN in array:
            InputAsserter.assertInput(IN)
            if IN == 0:
                return 0
        return 1

    @staticmethod
    def getOutput(operation, inputs):
        """
        Given an operation code (33, 42, 43), this will
        give an output. The input is a list of 1s and 0s
        """
        if BasicOperation.__isNOTOperation(operation):
            return BasicOperation.NOT(inputs)
        if BasicOperation.__isOROperation(operation):
            return BasicOperation.OR(inputs)
        if BasicOperation.__isANDOperation(operation):
            return BasicOperation.AND(inputs)
        raise NotImplementedError('Operation given (' + str(operation)+ ') is not a BasicOperation')

    @staticmethod
    def __isNOTOperation(operation):
        return operation == ord(BasicOperation.SYMBOLS["NOT"])
    
    @staticmethod
    def __isOROperation(operation):
        return operation == ord(BasicOperation.SYMBOLS["OR"])
    
    @staticmethod
    def __isANDOperation(operation):
        return operation == ord(BasicOperation.SYMBOLS["AND"])

class AdvancedOperation(BasicOperation):
    """
    Has, in addition to basic logic operations 
    OR, AND, and NOT: NOR, NAND, XOR, IMPLIES, and IFF.
    """

    SYMBOLS = {"OR": "+", "AND": "*", "NOT": "!", "XOR": "^", "NOR": "$", "NAND": "&", "IMPLIES": ">", "IFF": "|"}

    @staticmethod
    def NOR(array):
        """
        NOR logic operator: 0,0 => 1, 0,1 => 0, 1,0 => 0, 1,1 => 0
        """
        return BasicOperation.NOT([BasicOperation.OR(array)])

    @staticmethod
    def NAND(array):
        """
        NAND logic operator: 0,0 => 1, 0,1 => 1, 1,0 => 1, 1,1 => 0
        """
        return BasicOperation.NOT([BasicOperation.AND(array)])

    @staticmethod
    def XOR(array):
        """
        XOR (Exclusive-OR) logic operator: 0,0 => 0, 0,1 => 1, 1,0 => 1, 1,1 => 0
        """
        InputAsserter.assertArrayIsValid(array)
        InputAsserter.assertInputs(array)
        return sum(array) % 2

    @staticmethod
    def IMPLIES(array):
        """
        IMPLIES logic operator: 0,0 => 1, 0,1 => 0, 1,0 => 1, 1,1 => 1
        """
        InputAsserter.assertDoubleInput(array)
        if (array[0] == 0) and (array[1] == 1):
            return 0
        return 1

    @staticmethod
    def IFF(array):
        """
        IFF logic operator: 0,0 => 1, 0,1 => 0, 1,0 => 0, 1,1 => 1
        """
        InputAsserter.assertDoubleInput(array)
        if (array[0] == array[1]):
            return 1
        return 0

    @staticmethod
    def getOutput(operation, inputs):
        """
        Given an operation code (33, 42, 43), this will
        give an output. The input is a list of 1s and 0s
        """
        if AdvancedOperation.__isNOTOperation(operation):
            return BasicOperation.NOT(inputs)
        if AdvancedOperation.__isOROperation(operation):
            return BasicOperation.OR(inputs)
        if AdvancedOperation.__isANDOperation(operation):
            return BasicOperation.AND(inputs)
        if AdvancedOperation.__isNOROperation(operation):
            return AdvancedOperation.NOR(inputs)
        if AdvancedOperation.__isNANDOperation(operation):
            return AdvancedOperation.NAND(inputs)
        if AdvancedOperation.__isXOROperation(operation):
            return AdvancedOperation.XOR(inputs)
        if AdvancedOperation.__isIMPLIESOperation(operation):
            return AdvancedOperation.IMPLIES(inputs)
        if AdvancedOperation.__isIFFOperation(operation):
            return AdvancedOperation.IFF(inputs)
        raise NotImplementedError('Operation is not a valid AdvancedOperation')
    
    @staticmethod
    def __isNOTOperation(operation):
        return operation == ord(BasicOperation.SYMBOLS["NOT"])
    
    @staticmethod
    def __isOROperation(operation):
        return operation == ord(BasicOperation.SYMBOLS["OR"])
    
    @staticmethod
    def __isANDOperation(operation):
        return operation == ord(BasicOperation.SYMBOLS["AND"])

    @staticmethod
    def __isNOROperation(operation):
        return operation == ord(AdvancedOperation.SYMBOLS["NOR"])

    @staticmethod
    def __isNANDOperation(operation):
        return operation == ord(AdvancedOperation.SYMBOLS["NAND"])

    @staticmethod
    def __isXOROperation(operation):
        return operation == ord(AdvancedOperation.SYMBOLS["XOR"])

    @staticmethod
    def __isIMPLIESOperation(operation):
        return operation == ord(AdvancedOperation.SYMBOLS["IMPLIES"])

    @staticmethod
    def __isIFFOperation(operation):
        return operation == ord(AdvancedOperation.SYMBOLS["IFF"])