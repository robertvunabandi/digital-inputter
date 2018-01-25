from BasicOperation import AdvancedOperation


class ExpressionAsserter:
	"""
	This class has 2 objectives:
	- assert that a given expression is a valid logic operation
		through method assert_raw_is_valid()
	- offers methods that can be used to check things about
		boolean logic expression
	"""

	# the following 2 methods are needed to complete
	# assertions is_in_alphabet() and is_operator().
	@staticmethod
	def get_operators():
		# symbols for operators
		# ! means NOT, $ means NOR,  & means NAND, * means AND, + means OR, > means IMPLIES, ^ means XOR, | means IFF
		return {"!": 33, "$": 36, "&": 38, "*": 42, "+": 43, ">": 62, "^": 94, "|": 124}

	@staticmethod
	def get_alphabet():
		# uppercase alphabet
		return {chr(i): i for i in range(65, 91)}

	OPERATORS = get_operators.__func__()
	ALPHABET = get_alphabet.__func__()

	@staticmethod
	def assert_raw_is_valid(raw):
		RANGE = range(0, len(raw))
		# checks that the string parameter given is valid
		assert type(raw) == str, "raw must be a string"

		# check that the characters given are valid
		def character_error_for_character(char):
			return "one of the characters in the raw string was invalid. Received: " + str(char)

		for i in RANGE:
			char = raw[i]
			assert ExpressionAsserter.is_valid_raw_character(char), character_error_for_character(char)

		# assert the parenthesis count
		ExpressionAsserter.assert_parentheses_count(raw)

	@staticmethod
	def is_valid_raw_character(char):
		result = ExpressionAsserter.is_in_alphabet(char)
		result = result or ExpressionAsserter.is_operator(char)
		result = result or ExpressionAsserter.is_blank_space(char)
		result = result or ExpressionAsserter.is_opening_parenthesis(char)
		result = result or ExpressionAsserter.is_closing_parenthesis(char)
		return result

	@staticmethod
	def is_in_alphabet(char):
		return ExpressionAsserter.ALPHABET.get(char, -1) != -1

	@staticmethod
	def is_operator(char):
		return ExpressionAsserter.OPERATORS.get(char, -1) != -1

	@staticmethod
	def is_blank_space(char):
		return ord(char) == 32

	@staticmethod
	def is_opening_parenthesis(char):
		return ord(char) == 40

	@staticmethod
	def is_closing_parenthesis(char):
		return ord(char) == 41

	@staticmethod
	def assert_parentheses_count(raw):
		count = ExpressionAsserter.__get_delta_parentheses(raw)
		assert count == 0, "Parentheses do not match"

	@staticmethod
	def __get_delta_parentheses(raw):
		count = 0
		for index in range(0, len(raw)):
			char = raw[index]
			count = count + ExpressionAsserter.get_delta_character_for_parenthesis(char)
			ExpressionAsserter.__assert_count_parenthesis_is_nonnegative(count)
		return count

	@staticmethod
	def get_delta_character_for_parenthesis(char):
		if ExpressionAsserter.is_opening_parenthesis(char):
			return 1
		if ExpressionAsserter.is_closing_parenthesis(char):
			return -1
		return 0

	@staticmethod
	def __assert_count_parenthesis_is_nonnegative(count):
		assert count > -1, "parenthesis count was negative. It should never be."

	@staticmethod
	def is_OR_operator(char):
		return ord(char) == 43

	@staticmethod
	def is_AND_operator(char):
		return ord(char) == 42

	@staticmethod
	def is_NOT_operator(char):
		return ord(char) == 33
