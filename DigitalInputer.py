from Expression import Expression
from BasicOperation import AdvancedOperation


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
	- get_output(input_array): given an input array, this
		returns the output of the given raw expression.
	- get_output_table_print_ready(): this returns a string
		containing an output table with every possible
		inputs in a clearly defined setup with headers
		containing the input Values (as defined is
		Expression.py) and "OUT" (short for output).
	- get_table_output_dictionary(): returns a dictionary
		mapping tuples of inputs to an output. Similar
		to the table, except one can get certain values
		directly from this dictionary.
	- print_output_table(): prints the output table received
		from get_output_table_print_ready()
	"""

	def __init__(self, raw):
		"""
		All that is needed for the initialization
		is a raw expression. This raw expression
		is an expression as defined in Expression.py
		"""
		self.expression = Expression(raw)

	def get_output(self, array):
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
		self.__assert_array_length_is_valid(array)
		return self.__solve_output_for_input(array, self.expression.parsed)

	def __solve_output_for_input(self, input_array, parsed_expression):
		"""
		Given an input_array, this will given an output
		based on the parsed expression
		"""
		operation = DigitalInputer.__get_operation(parsed_expression)
		inputs = self.__get_digital_inputs(input_array, parsed_expression)
		return AdvancedOperation.getOutput(operation, inputs)

	@staticmethod
	def __get_operation(parsed_expression):
		"""
		Returns the operation of a parsed Expression,
		which is always in the first index of the
		Expression
		"""
		return parsed_expression[0]

	def __get_digital_inputs(self, input_array, parsed_expression):
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
			if DigitalInputer.__is_value(expr):
				# map the expression to the actual value
				inputs.append(self.__map_to_digital_input(input_array, expr))
			else:
				# solve for the given expression
				inputs.append(self.__solve_output_for_input(input_array, expr))
		return inputs

	@staticmethod
	def __is_value(expression):
		"""
		Checks whether the given expression is a
		Value (an alphabetical letter) ASA or an
		Expression ASA
		"""
		return type(expression) != list

	def __map_to_digital_input(self, input_array, expr):
		"""
		Maps a digital value, say "A", to an input
		value.
		"""
		index = self.expression.varsSorted.index(expr)
		return input_array[index]

	def __assert_array_length_is_valid(self, array):
		"""
		The length of this array must be equal to
		self.expression.varCount
		"""
		msg = "The length of the array must equal the number of variables in the expression"
		assert len(array) == self.expression.varCount, msg

	def get_table_output_dictionary(self):
		"""
		Returns a dictionary mapping tuples of inputs
		(e.g.: (0,0,1)) to digital value outputs.

		For some reason, the order in which they come
		is shuffle, but that's okay.
		"""
		array_inputs_list = DigitalInputer.__get_array_inputs_list(self.expression.varCount)
		dic = {}
		for array_input in array_inputs_list:
			dic[tuple(array_input)] = self.get_output(array_input)
		return dic

	@staticmethod
	def __get_array_inputs_list(count):
		"""
		Given a count, say N, this will return an array
		of binary digits ranging from 0 to 2^N - 1. For
		example, if count = 2, then the output will be
		[[0,0], [0,1], [1,0], [1,1]]
		"""
		array_inputs_list = []
		max_number = 2 ** count
		for number in range(max_number):
			array_inputs_list.append(DigitalInputer.__array_from_binary(bin(number), count))
		return array_inputs_list

	@staticmethod
	def __array_from_binary(binary_number, var_count):
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

	def get_output_table_print_ready(self):
		"""
		Returns a string containing the output table
		with the given inputs and "OUT" as headers
		and every possible combination of outputs for
		the given inputs
		"""
		array_inputs_list = DigitalInputer.__get_array_inputs_list(self.expression.varCount)
		string = "\n" + DigitalInputer.__print_output_table_line(self.expression.varsSorted, "OUT")
		for array_input in array_inputs_list:
			string += "\n" + DigitalInputer.__print_output_table_line(array_input, self.get_output(array_input))
		return string

	@staticmethod
	def __print_output_table_line(expression_values, output):
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

	def print_output_table(self):
		"""
		Prints the output table
		"""
		print(self.get_output_table_print_ready())

	def __str__(self):
		return str(self.expression.raw)

	def __repr__(self):
		return str(self.expression.raw)

	def __eq__(self, other):
		if type(other) == str:
			# assumes that other is just a string of raw
			# and self with the DigitalInputer of other
			return self == DigitalInputer(other)
		if isinstance(other, self.__class__):
			# we need to compare both outputs and string raw
			return self.__are_raw_equal(other) or self.__are_outputs_equal(other)
		return False

	def __are_raw_equal(self, other):
		return self.expression.raw == other.expression.raw

	def __are_outputs_equal(self, other):
		# pre-compute the dictionaries because they
		# may take a long time to compute
		other_output = other.get_table_output_dictionary()
		other_output_keys = other_output.keys()
		self_output = self.get_table_output_dictionary()

		for key in other_output_keys:
			# try/except KeyError because if other has
			# more or less variables than A, so its
			# inputs tuples will definitely not be part
			# of the dictionary from self
			try:
				if self_output[key] != other_output[key]:
					return False
			except KeyError:
				return False
		return True

	def __ne__(self, other):
		return not self.__eq__(other)
