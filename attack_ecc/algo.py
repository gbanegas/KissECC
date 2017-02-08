import random
from itertools import product

n = 250
N = 10
window_size = 10
v = [7951, 2968, 1367, 2894, 6069, 8988, 9499, 6365, 4547, 990, 2030]


def generate_d_candidates(difference, bit_size):
    all_combinations = []
    general_zeros = [0]*(bit_size-difference)
    for i in product([0,1], repeat=difference):
        all_combinations.append(list(i)+general_zeros)
    #print all_combinations
    return all_combinations

def xor_operation(v, d):
    l = [int(x) for x in bin(v)[2:]]
    size_d = len(d)
    complementary = [0]*(size_d-len(l))
    v_list = complementary + l
    result = []
    for j in xrange(0, size_d):
        result.append((v_list[j]+d[j]) % 2)
    #print result
    return result

#TODO Generate fake v_j
#TODO finish the xor operation
#TODO Improve the XOR operation
#TODO create argmin{S(d)}
def sum_all_ds(d_candidates):
    pairs = {}
    for d in d_candidates:
        sum_hw_d = 0
        for j in xrange(1,N):
            pre_sum = (xor_operation(v[j], d)).count(1)
            sum_hw_d = sum_hw_d + pre_sum
        pairs[sum_hw_d] = d

    return min(pairs.items(), key=lambda x: x[1])



def wide_widow_attack():
    #v = [int(10000*random.random()) for i in xrange(N)]
    #print v
    print "Starting...."
    w_l = 0
    w = window_size
    d_l = 0

    while(w < n):
        bits_size = 2**w
        d_candidates = generate_d_candidates(w-w_l, bits_size)
        w_l = w
        w = w + window_size
        d_candidate = sum_all_ds(d_candidates)
        print d_candidate



wide_widow_attack()
