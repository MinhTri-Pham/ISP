from ex1 import query_pred
from phe import paillier

NUM_WEIGHTS = 10
# Get bias term by feeding zero input vector
bias_input_vec = [0] * NUM_WEIGHTS
bias = query_pred(bias_input_vec)
weights = [] 
# Get weight w_i by feeding input with 1 in position i and zero everywhere else
for i in range(NUM_WEIGHTS):
    weight_input_vec = [0] * NUM_WEIGHTS
    weight_input_vec[i] = 1
    weights.append(query_pred(weight_input_vec) - bias)
# Validate
input_vector = [0.48555949, 0.29289251, 0.63463107,
                    0.41933057, 0.78672205, 0.58910837,
                    0.00739207, 0.31390802, 0.37037496,
                    0.3375726]

true_prediction = query_pred(input_vector)    
my_prediction = sum(v[0] * v[1] for i in zip(weights, input_vector)) + bias
print(true_prediction)
print(my_prediction)
assert 2**(-16) > abs(true_prediction - my_prediction)    
