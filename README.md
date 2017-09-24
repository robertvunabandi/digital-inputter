# README

DigitalInputter helps with simple logic computations.

Given a raw input, such as `(!A)^(B\*X)`, this will output the expression. For instance, given input `[0,0,0]`, the output here would be `1`.

This can work for any arbitrary length input with maximum 26 inputs (26 letters, one shouldn't need that much anyway). One can also print a table. Gor the input given above, the table output would be:

| A B X | OUT |
| ----- | --- |
| 0 0 0 | 1 |
| 0 0 1 | 1 |
| 0 1 0 | 1 |
| 0 1 1 | 0 |
| 1 0 0 | 0 |
| 1 0 1 | 0 |
| 1 1 0 | 0 |
| 1 1 1 | 1 | 

## Details

The class DigitalInputer takes in as input a Raw expression, as detailed below. That expression would be the entry point for this class. 

### Naming convention

- ASA: replaces "as stated above". This is to make it apparent that we're referencing a variable in this naming convention.
- Value: Alphabetical letter
- Expression: Either a Value ASA or a parsed valued array, such as `[33, 'A']` or `[42, 'A', 'B']` `(NOT A)` and `(A AND B)` respectively.
- Raw: The single string that represents a boolean logic expression that is to be parsed into an Expression ASA. For example, `A*(B*(!C))`.
- Parsed Expression: An expression that is parsed as specified by the Expression.parse. For instance, `A*B` is parsed into `[42, 'A', 'B']`, which is the Parsed Expression for that Raw.
- Letter: A letter of the alphabet
- Operators: Boolean operators. `*` for `AND`, `+` for `OR`, `!` for `NOT`.

### The Raw ASA string has to follow some guidelines

- (1) It has to be written in the form `LOLOLOLOL` without spaces, where `L` is either a Letter or another Raw enclosed in parentheses and where `O` is an operator (@). For example, `A*(B*(!C))`.
- (2) All of the `O` have to be the same, or else it will raise a SyntaxError. Remember, it's recursive, so for any `L`, all of the `O` have to be the same still but they can be different than the main `O`. 
- (3) Following from (2), in order to write a NOT expression, it needs to always be enclosed in Parenthesis unless it's the global thing to be NOTed. For instance, `!A` (global) or `A+(!(A+B))` (not global).
- (4) Some advanced operations require only 2 `L`'s: those are `IFF` and `IMPLIES` operations.
- (@) an exception to this rule is the `NOT` operator `!` as shown in the given example.

### Symbols to operation

- `!` means `NOT`
- `$` means `NOR`
- `&` means `NAND`
- `*` means `AND`
- `+` means `OR`
- `>` means `IMPLIES`
- `^` means `XOR`
- `|` means `IFF`
