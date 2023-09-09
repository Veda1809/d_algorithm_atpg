from itertools import product

# Define a function for simulating the circuit
def simulate_circuit(circuit, inputs):
    values = {}
    for gate in circuit:
        if gate[0] == 'input':
            values[gate[1]] = inputs[gate[1]]
        elif gate[0] == 'and':
            values[gate[3]] = values[gate[1]] & values[gate[2]]
        elif gate[0] == 'or':
            values[gate[3]] = values[gate[1]] | values[gate[2]]
        elif gate[0] == 'not':
            values[gate[2]] = not values[gate[1]]
        elif gate[0] == 'xor':
            values[gate[3]] = values[gate[1]] ^ values[gate[2]]
        elif gate[0] == 'nand':
            values[gate[3]] = not (values[gate[1]] & values[gate[2]])
        elif gate[0] == 'nor':
            values[gate[3]] = not (values[gate[1]] | values[gate[2]])
        elif gate[0] == 'xnor':
            values[gate[3]] = not (values[gate[1]] ^ values[gate[2]])
    return values

# Define the D algorithm for ATPG
def d_algorithm(circuit, fault, initial_tests):
    """
    Performs the D-algorithm for combinational ATPG to generate test vectors for fault detection.
    """
    stack = []
    stack.extend(initial_tests)
    values = simulate_circuit(circuit, initial_tests[0])
    all_test_vectors = []
    while stack:
        test = stack.pop()
        fault_sim = simulate_circuit(circuit, test)

        if fault_sim[fault[0]] != fault[1]:
            # Fault is detected, add the test pattern to the list of all test vectors
            all_test_vectors.append(test)
        else:
            # Propagate the fault to the primary inputs
            for gate in circuit:
                if gate[0] == 'input' and fault[0] in gate[1]:
                    if fault_sim[gate[1]] != fault[1]:
                        # Propagate the fault to the input
                        new_test = test.copy()
                        new_test[gate[1]] = fault[1]
                        stack.append(new_test)

    if not all_test_vectors:
        # No test vectors detected the fault, return None
        return None

    # Return all test vectors that detected the fault
    return all_test_vectors

# Example usage
circuit = [('input', 'a'), ('input', 'b'), ('input', 'c'), ('and', 'a', 'b', 'g1'), ('or', 'a', 'g1', 'g2'), ('not', 'g2', 'g3'), ('xor', 'b', 'c', 'g4'), ('nand', 'a', 'c', 'g5'), ('nor', 'b', 'g3', 'g6'), ('xnor', 'g4', 'g5', 'g7')] 

fault = ('g7', False) # Updated fault position to gate 'g7' with value False

inputs = ['a', 'b', 'c'] # List of all input names
initial_tests = [dict(zip(inputs, t)) for t in product([False, True], repeat=len(inputs))] # All possible combinations of inputs

test_vectors = d_algorithm(circuit, fault, initial_tests)
if test_vectors is None:
    print("Fault is undetected.")
else:
    print("Test vectors for fault detection:")
    for test_vector in test_vectors:
        print(test_vector)
