submission.py generates CVC language as an input for the SAT solver STP, given an optimization goal and an S-box. 

Cipher     Name of cipher of which the S-box should be used.

bitnum     Number of bits in the given S-box

GateNum    for gate complexity, number of gates for the given S-box

AncNum     for ancilla qubit complexity, number of ancilla qubits for the given S-box

DEPTH      for depth complexity, the maximum depth of the given S-box

By modifying the above parameters, the output .cvc text is used as input to STP, returning the optimized circuit.
