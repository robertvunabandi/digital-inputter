class InputAsserter:
	"""
	Asserts whether an array of inputs or an input is valid
	"""

	@staticmethod
	def __error_message(_in):
		"""
		Specific error message for when the input is invalid
		"""
		return "input must be 1 or 0. Received: " + str(_in)

	@staticmethod
	def assert_input(IN):
		"""
		Checks whether one input is valid
		"""
		assert type(IN) == int, "Argument given must be an integer"
		assert IN == 0 or IN == 1, InputAsserter.__error_message(IN)

	@staticmethod
	def assert_inputs(INS):
		"""
		Checks whether each element in an array of input is valid
		"""
		assert type(INS) == list, "Inputs must be a list"
		for IN in INS:
			InputAsserter.assert_input(IN)

	@staticmethod
	def assert_single_input(INS):
		"""
		Checks whether the length of the array is 1
		"""
		InputAsserter.assert_inputs(INS)
		assert len(INS) == 1, "Inputs list must be of length 1"

	@staticmethod
	def assert_double_input(INS):
		"""
		Checks whether the length of the array is 2
		"""
		InputAsserter.assert_inputs(INS)
		assert len(INS) == 2, "Inputs list must be of length 2"

	@staticmethod
	def assert_array_is_valid(array):
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
		InputAsserter.assert_single_input(IN)
		return 1 - IN[0]

	@staticmethod
	def OR(array):
		"""
		OR logic operator: 0,0 => 0, 0,1 => 1, 1,0 => 1, 1,1 => 1
		"""
		InputAsserter.assert_array_is_valid(array)
		for IN in array:
			InputAsserter.assert_input(IN)
			if IN == 1:
				return 1
		return 0

	@staticmethod
	def AND(array):
		"""
		AND logic operator: 0,0 => 0, 0,1 => 0, 1,0 => 0, 1,1 => 1
		"""
		InputAsserter.assert_array_is_valid(array)
		for IN in array:
			InputAsserter.assert_input(IN)
			if IN == 0:
				return 0
		return 1

	@staticmethod
	def get_output(operation, inputs):
		"""
		Given an operation code (33, 42, 43), this will
		give an output. The input is a list of 1s and 0s
		"""
		if BasicOperation.__is_NOT_operation(operation):
			return BasicOperation.NOT(inputs)
		if BasicOperation.__is_OR_operation(operation):
			return BasicOperation.OR(inputs)
		if BasicOperation.__is_AND_operation(operation):
			return BasicOperation.AND(inputs)
		raise NotImplementedError('Operation given (' + str(operation) + ') is not a BasicOperation')

	@staticmethod
	def __is_NOT_operation(operation):
		return operation == ord(BasicOperation.SYMBOLS["NOT"])

	@staticmethod
	def __is_OR_operation(operation):
		return operation == ord(BasicOperation.SYMBOLS["OR"])

	@staticmethod
	def __is_AND_operation(operation):
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
		InputAsserter.assert_array_is_valid(array)
		InputAsserter.assert_inputs(array)
		return sum(array) % 2

	@staticmethod
	def IMPLIES(array):
		"""
		IMPLIES logic operator: 0,0 => 1, 0,1 => 0, 1,0 => 1, 1,1 => 1
		"""
		InputAsserter.assert_double_input(array)
		if (array[0] == 0) and (array[1] == 1):
			return 0
		return 1

	@staticmethod
	def IFF(array):
		"""
		IFF logic operator: 0,0 => 1, 0,1 => 0, 1,0 => 0, 1,1 => 1
		"""
		InputAsserter.assert_double_input(array)
		if (array[0] == array[1]):
			return 1
		return 0

	@staticmethod
	def get_output(operation, inputs):
		"""
		Given an operation code (33, 42, 43), this will
		give an output. The input is a list of 1s and 0s
		"""
		if AdvancedOperation.__is_NOT_operation(operation):
			return BasicOperation.NOT(inputs)
		if AdvancedOperation.__is_OR_operation(operation):
			return BasicOperation.OR(inputs)
		if AdvancedOperation.__is_AND_operation(operation):
			return BasicOperation.AND(inputs)
		if AdvancedOperation.__is_NOR_operation(operation):
			return AdvancedOperation.NOR(inputs)
		if AdvancedOperation.__is_NAND_operation(operation):
			return AdvancedOperation.NAND(inputs)
		if AdvancedOperation.__is_XOR_operation(operation):
			return AdvancedOperation.XOR(inputs)
		if AdvancedOperation.__is_IMPLIES_operation(operation):
			return AdvancedOperation.IMPLIES(inputs)
		if AdvancedOperation.__is_IFF_operation(operation):
			return AdvancedOperation.IFF(inputs)
		raise NotImplementedError('Operation is not a valid AdvancedOperation')

	@staticmethod
	def __is_NOT_operation(operation):
		return operation == ord(BasicOperation.SYMBOLS["NOT"])

	@staticmethod
	def __is_OR_operation(operation):
		return operation == ord(BasicOperation.SYMBOLS["OR"])

	@staticmethod
	def __is_AND_operation(operation):
		return operation == ord(BasicOperation.SYMBOLS["AND"])

	@staticmethod
	def __is_NOR_operation(operation):
		return operation == ord(AdvancedOperation.SYMBOLS["NOR"])

	@staticmethod
	def __is_NAND_operation(operation):
		return operation == ord(AdvancedOperation.SYMBOLS["NAND"])

	@staticmethod
	def __is_XOR_operation(operation):
		return operation == ord(AdvancedOperation.SYMBOLS["XOR"])

	@staticmethod
	def __is_IMPLIES_operation(operation):
		return operation == ord(AdvancedOperation.SYMBOLS["IMPLIES"])

	@staticmethod
	def __is_IFF_operation(operation):
		return operation == ord(AdvancedOperation.SYMBOLS["IFF"])
