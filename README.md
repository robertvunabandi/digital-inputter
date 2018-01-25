# README

`DigitalInputter` helps with simple logic computations.

Given a raw input, such as `(!A)^(B*X)`, this will output the expression. For instance, given input `[0,0,0]`, the output here would be `1`.

This can work for any arbitrary length input with maximum 26 inputs (26 letters, one shouldn't need that much anyway). One can also print a table. For the input given above, the table output would be:

| A | B | X | OUT |
| - | - | - | --- |
| 0 | 0 | 0 |  1  |
| 0 | 0 | 1 |  1  |
| 0 | 1 | 0 |  1  |
| 0 | 1 | 1 |  0  |
| 1 | 0 | 0 |  0  |
| 1 | 0 | 1 |  0  |
| 1 | 1 | 0 |  0  |
| 1 | 1 | 1 |  1  | 

## Details

The class `DigitalInputer` takes in as input a `Raw` expression, as detailed below. That expression would be the entry point for this class. 

### Naming convention

- **`ASA`**: stands for "as stated above". This is to make it apparent that we're referencing a variable in this naming convention.
- **`Value`**: Just an **UPPERCASED** alphabetical letter. Values have to be uppercased, otherwise it'd cause an error.
- **`Expression`**: Either a Value **`ASA`** or a parsed valued array, such as `[33, 'A']` or `[42, 'A', 'B']` **`(NOT A)`** and **`(A AND B)`** respectively.
- **`Raw`**: The single string that represents a boolean logic expression that is to be parsed into an `Expression` **`ASA`**. For example, `A*(B*(!C))`.
- **`Parsed Expression`**: An `Expression` that is parsed as specified by the `Expression.parse` variable in the class `Expression`. For instance, `A*B` would be parsed into `[42, 'A', 'B']`, which is the `Parsed Expression` for that `Raw`.
- **`Letter`**: A letter of the alphabet
- **`Operators`**: Boolean operators. `*` for **`AND`**, `+` for **`OR`**, `!` for **`NOT`**.

### The Raw **`ASA`** string has to follow some guidelines

- (1) It has to be written in the form `LOLOLOLOL` without spaces, where `L` is either a Letter or another Raw enclosed in parentheses and where `O` is an operator (**see `@` below**). For example, `A*(B*(!C))`. 
- The fact that there is no space in between letters in the expression `LOLOLOLOL` is to say that a space will cause an Exception to occur.
- (2) All of the `O` have to be the same, or else it will raise a SyntaxError. Remember, it's recursive, so for any `L`, all of the `O` have to be the same still but they can be different than the main `O`. 
- (3) Following from (2), in order to write a NOT expression, it needs to always be enclosed in Parenthesis unless it's the global thing to be NOTed. For instance, `!A` (global) or `A+(!(A+B))` (not global).
- (4) Some advanced operations require only 2 `L`'s: those are `IFF` and `IMPLIES` operations.
- (**`@`**) an exception to this rule is the **`NOT`** operator `!` as shown in the given example.

### Examples

`DigitalInputer` offers four main method:
- `get_output(input_array)`: Returns the output for a given set of inputs.
- `print_output_table()`: Prints the table returned by `get_output_table_print_ready()` below.
- `get_output_table_print_ready()`: Returns a table showing all the different combinations of inputs and their outputs, which can be stored in a variable.
- `get_table_output_dictionary()`: Gets a dictionary showing all the different combinations of inputs and their outputs via keys as tuples of input and values as outputs of those inputs.

Here's a simple example for `A OR B`:
```python
from DigitalInputer import DigitalInputer
A = DigitalInputer("A+B")  # A OR B
print(A.get_output([0,0])) # 0, the first argument in the array is for A
print(A.get_output([0,1])) # 1
print(A.get_output([1,0])) # 1
print(A.get_output([1,1])) # 1
```

The input of the array with the method `get_output` are alphabetical no matter what:
```python
B = DigitalInputer("B+(A*B)") # B OR (A AND B)
print(A.get_output([0,0])) # 0, the first argument in the array is for A
print(A.get_output([0,1])) # 1
print(A.get_output([1,0])) # 0
print(A.get_output([1,1])) # 1

```

You can also see tables with their values with the method `print_output_table`:
```python
B = DigitalInputer("B+(A*B)") # B OR (A AND B)
B.print_output_table()
"""
prints the following:
A B | OUT
0 0 | 0
0 1 | 1
1 0 | 0
1 1 | 1
"""
```

You can even get the table as a string with `get_output_table_print_ready`:
```python
B = DigitalInputer("B+(A*B)") # B OR (A AND B)
string_table = B.get_output_table_print_ready()
print(string_table)
"""
prints the following:
A B | OUT
0 0 | 0
0 1 | 1
1 0 | 0
1 1 | 1
"""
```

What if you want to save it in a different format? You can get a python `dictionary` with the method `print_output_table`:

```python
B = DigitalInputer("B+(A*B)") # B OR (A AND B)
print(B.print_output_table()) # {(0, 1): 1, (1, 0): 0, (0, 0): 0, (1, 1): 1}
```

### Operation Symbols 

- `!` means **`NOT`**
- `$` means **`NOR`**
- `&` means **`NAND`**
- `*` means **`AND`**
- `+` means **`OR`**
- `>` means **`IMPLIES`**
- `^` means **`XOR`**
- `|` means **`IFF`**
