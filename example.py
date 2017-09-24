from DigitalInputer import DigitalInputer

a = DigitalInputer("(!A)^(B*X)")
print(a.getOuputTablePrintReady())

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

