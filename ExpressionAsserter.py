from BasicOperation import AdvancedOperation

class ExpressionAsserter:
    """
    This class has 2 objectives:
    - assert that a given expression is a valid logic operation
        through method assertRawIsValid()
    - offers methods that can be used to check things about
        boolean logic expression
    """

    # the following 2 methods are needed to complete
    # assertions isInAlphabet() and isOperator().
    @staticmethod
    def getOperators():
        # symbols for operators
        # ! means NOT, $ means NOR,  & means NAND, * means AND, + means OR, > means IMPLIES, ^ means XOR, | means IFF
        return {"!": 33, "$": 36, "&": 38, "*": 42, "+": 43, ">": 62, "^": 94, "|": 124}

    @staticmethod
    def getAlphabet():
        # uppercase alphabet
        return {chr(i): i for i in range(65, 91)} 

    OPERATORS = getOperators.__func__()
    ALPHABET = getAlphabet.__func__()

    @staticmethod
    def assertRawIsValid(raw):
        RANGE = range(0, len(raw))
        # checks that the string parameter given is valid
        assert type(raw) == str, "raw must be a string"
       
        # check that the characters given are valid
        def characterErrorForCharacter(char):
            return "one of the characters in the raw string was invalid. Received: " + str(char)

        for i in RANGE:
            char = raw[i]
            assert ExpressionAsserter.isValidRawCharacter(char), characterErrorForCharacter(char)

        # assert the parenthesis count
        ExpressionAsserter.assertParenthesesCount(raw)

    @staticmethod
    def isValidRawCharacter(char):
        result = ExpressionAsserter.isInAlphabet(char)
        result = result or ExpressionAsserter.isOperator(char)
        result = result or ExpressionAsserter.isBlankSpace(char)
        result = result or ExpressionAsserter.isOpeningParenthesis(char)
        result = result or ExpressionAsserter.isClosingParenthesis(char)
        return result


    @staticmethod
    def isInAlphabet(char):
        return ExpressionAsserter.ALPHABET.get(char, -1) != -1
   
    @staticmethod
    def isOperator(char):
        return ExpressionAsserter.OPERATORS.get(char, -1) != -1

    @staticmethod
    def isBlankSpace(char):
        return ord(char) == 32

    @staticmethod
    def isOpeningParenthesis(char):
        return ord(char) == 40

    @staticmethod
    def isClosingParenthesis(char):
        return ord(char) == 41

    @staticmethod
    def assertParenthesesCount(raw):
        count = ExpressionAsserter.__getDeltaParentheses(raw)
        assert count == 0, "Parentheses do not match"

    @staticmethod
    def __getDeltaParentheses(raw):
        count = 0
        for index in range(0, len(raw)):
            char = raw[index]
            count = count + ExpressionAsserter.getDeltaCharacterForParenthesis(char)
            ExpressionAsserter.__assertCountParenthesisIsNonnegative(count)
        return count

    @staticmethod
    def getDeltaCharacterForParenthesis(char):
        if ExpressionAsserter.isOpeningParenthesis(char):
            return 1
        if ExpressionAsserter.isClosingParenthesis(char):
            return -1
        return 0

    @staticmethod
    def __assertCountParenthesisIsNonnegative(count):
        assert count > -1, "parenthesis count was negative. It should never be."

    @staticmethod
    def isOROperator(char):
        return ord(char) == 43 

    @staticmethod
    def isANDOperator(char):
        return ord(char) == 42

    @staticmethod
    def isNOTOperator(char):
        return ord(char) == 33