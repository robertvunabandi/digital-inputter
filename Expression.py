from ExpressionAsserter import ExpressionAsserter


class Expression:
	"""
	This class takes in a boolean logic expression, and creates
	a parsed expression that will be used to generate outputs.

	Naming convention:
	- ASA: replaces "as stated above". This is to make it apparent
		that we're referencing a variable in this naming convention.
	- Value: Alphabetical letter
	- Expression: Either a Value ASA or a parsed valued array, such
		as [33, 'A'] or [42, 'A', 'B'] (not A) and (A and B)
		respectively
	- Raw: The single string that represents a boolean logic
		expression that is to be parsed into an Expression ASA. For
		example, "A*(B*(!C))"
	- Parsed Expression: An expression that is parsed as specified by
		the Expression.parse. For instance, "A*B" is parsed into
		[42, 'A', 'B'], which is the Parsed Expression for that Raw
	- Letter: A letter of the alphabet
	- Operators: Boolean operators. * for AND, + for OR, ! for NOT.

	The Raw ASA string has to follow some guidelines:
	- (1) It has to be written in the form "LOLOLOLOL" without spaces,
		where L is either a Letter or another Raw enclosed in
		parentheses and where O is an operator (*). For example,
		"A*(B*(!C))".
	- (2) All of the O have to be the same, or else it will raise a
		SyntaxError. Remember, it's recursive, so for any L, all
		of the O have to be the same still but they can be different
		than the main O.
	- (3) Following from (2), in order to write a NOT expression, it
		needs to always be enclosed in Parenthesis unless it's the
		global thing to be NOTed. For instance, "!A" (global )or
		"A+(!(A+B))" (not global)
	- (4) Some advanced operations require only 2 L's: those are
		IFF and IMPLIES operations.
	- (*) an exception to this rule is the NOT operator "!" as shown
		in the given example

	Symbols to operation (ignore the " \ ", it's used to escape some
		character for pydoc in Visual Studio Code):
	- \! means NOT
	- $ means NOR
	- & means NAND
	- \* means AND
	- \+ means OR
	- \> means IMPLIES
	- ^ means XOR
	- | means IFF
	"""

	def __init__(self, raw):
		# raw: [String] has the form "(A*B)+!(AC+B)"
		self.LRANGE = range(0, len(raw))
		# run assertion to make sure parameter given is ok
		ExpressionAsserter.assert_raw_is_valid(raw)
		# initialize raw string and variables
		self.raw = raw
		# add the list of variables
		self.vars = {}
		self.extract_variables()
		self.varsSorted = sorted([value for value in self.vars.keys()])
		# create the parsed expression
		self.parsed = None
		self.__create_parsed_expression()

		self.varCount = len(self.vars.keys())

	def extract_variables(self):
		for index in self.LRANGE:
			char = self.__get_char_at(index)
			self.__add_variable_if_valid(char, index)

	def __add_variable_if_valid(self, char, index):
		if (ExpressionAsserter.is_in_alphabet(char)):
			self.__add_variable_position(char, index)

	def __get_char_at(self, index):
		return self.raw[index]

	def __add_variable_position(self, char, index):
		try:
			self.vars[char].append(index)
		except:
			self.vars[char] = [index]

	def __create_parsed_expression(self):
		# initialize and compute parsed
		self.parsed = Expression.__get_next_expression(self.raw)

	# This functions is a recursive one that returns a
	# parsed expression from the substring. It's the main
	# thing that Expression does.
	@staticmethod
	def __get_next_expression(raw_substring):
		L, index = len(raw_substring), 0
		# expression stack is an array containing the expressions
		# operator is the operation for this set of expressions in
		# the stack
		expression_stack, operation = [], None
		while index < L:
			# do something with the indexes
			char = raw_substring[index]
			if (ExpressionAsserter.is_in_alphabet(char)):
				# add this character into the expression_stack
				expression_stack.append(char)
			elif (ExpressionAsserter.is_opening_parenthesis(char)):
				# find the closing index and get the substring,
				# from which we find the parsed expression
				closing_index = Expression.find_closing_parenthesis_from(raw_substring, index)
				sub_raw_substring = raw_substring[index + 1:closing_index]
				# append the expression in the parentheses to the stack
				expression_stack.append(Expression.__get_next_expression(sub_raw_substring))
				# set the index to the closing parenthesis
				index = closing_index
			elif (ExpressionAsserter.is_operator(char)):
				# set the operation if we find the operation
				# there should be only one, so this method raises
				# an error in case the operation is already set
				operation = Expression.__get_operation(operation, char)
			# increase the index at the end or set it
			# to the end parenthesis index
			index = index + 1

		# make sure this operation follows the guidelines as stated above
		Expression.__assert_operation_is_valid(operation, expression_stack, raw_substring)

		# return an array containing at the first index the operation
		# and at the rest elements are the expressions for this operation
		result = [operation]
		result.extend(expression_stack)
		return result

	@staticmethod
	def __get_operation(operation, char, raw=None):
		if ord(char) == operation:
			return operation
		if (operation != None):
			Expression.__raise_syntax_operation_error(raw)
		return ord(char)

	@staticmethod
	def __raise_syntax_operation_error(raw=None):
		raw_string = " "
		if (raw != None):
			raw_string = " (" + str(raw) + ") "
		msg = 'Two operations in the same scope. Raw given' + raw_string + 'must be invalid.'
		raise SyntaxError(msg)

	@staticmethod
	def __assert_operation_is_valid(operation, expression_stack, raw_substring):
		# the operation cannot be None
		assert operation != None, 'Operation is None. Raw given (' + raw_substring + ') must be invalid.'
		# Raise a SyntaxError in case the ! operation has more
		# than 2 Expression or Value to be NOTed
		Expression.__assert_NOT_operation_case(operation, expression_stack, raw_substring)
		# Raise a SyntaxError in case the * or + operation is
		# done on only 1 Expression or Value
		Expression.__assert_other_operations_case(operation, expression_stack, raw_substring)

	@staticmethod
	def __assert_NOT_operation_case(operation, expression_stack, raw_substring):
		is_stack_length_valid_for_NOT = len(expression_stack) > 1
		is_NOT_operation = operation == ord("!")
		if is_stack_length_valid_for_NOT and is_NOT_operation:
			Expression.__raise_syntax_NOT_operation_error(raw_substring)

	@staticmethod
	def __raise_syntax_NOT_operation_error(_raw=None):
		raw_string = raw_substring = " " if (_raw == None) else " (" + str(_raw) + ") "
		msg = 'The not operation had 2 or more Expression. It should only have 1. Raw given' + raw_string + 'must be invalid.'
		raise SyntaxError(msg)

	@staticmethod
	def __assert_other_operations_case(operation, expression_stack, raw_substring):
		is_stack_length_valid_for_AND_or_OR = len(expression_stack) < 2
		is_AND_or_OR_operation = (operation == ord("*")) or (operation == ord("+"))
		if is_stack_length_valid_for_AND_or_OR and is_AND_or_OR_operation:
			Expression.__raise_syntax_other_operations_error(raw_substring)

	@staticmethod
	def __raise_syntax_other_operations_error(_raw=None):
		raw_string = raw_substring = " " if (_raw == None) else " (" + str(_raw) + ") "
		msg = 'The operation had only 1 or less Expressions. It should only more than 1. Raw given' + raw_string + 'must be invalid.'
		raise SyntaxError(msg)

	# this method returns the closing parenthesis of a given expression
	# throws IndexError or AssertionError
	@staticmethod
	def find_closing_parenthesis_from(raw_substring, index):
		count, current_index, opening = 1, index, raw_substring[index]

		error_string = "Character at index " + str(index)
		error_string += " must be an opening parenthesis. Received: " + str(opening)
		assert ExpressionAsserter.is_opening_parenthesis(opening), error_string

		while (count > 0):
			current_index += 1
			char = raw_substring[current_index]
			count = count + ExpressionAsserter.get_delta_character_for_parenthesis(char)

		return current_index

	def __str__(self):
		return str(self.raw)

	def __repr__(self):
		return str(self.raw)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.raw == other.raw
		return False

	def __ne__(self, other):
		return not self.__eq__(other)


"""
Example representations for expresion.parsed

EXAMPLE 1:
raw: "(A*B)+C"
parsed: [43, [42, 'A', 'B'], 'C']

EXAMPLE 2:
raw: "(!A)+C+(B*(!C))"
parsed: [43, [33, 'A'], 'C', [42, 'B', [33, 'C']]]

This will be a lot easier to compute for specific inputs, say "0,0,1"
"""
