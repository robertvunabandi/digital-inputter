from DigitalInputer import DigitalInputer

a = DigitalInputer("(!A)^(B*X)")
print(a.get_output_table_print_ready())

"""
The operation given above is NOT(A) XOR (B AND X)

Prints the following ouput:
A B X | OUT
0 0 0 | 1
0 0 1 | 1
0 1 0 | 1
0 1 1 | 0
1 0 0 | 0
1 0 1 | 0
1 1 0 | 0
1 1 1 | 1
"""

A = DigitalInputer("(!A)*(!B)")
B = DigitalInputer("!(A+B)")
C = "!(A+B)"
print(A == B) # True
print(A == C) # True
print(B == C) # True
