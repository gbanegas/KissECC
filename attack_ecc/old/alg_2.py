import random
from itertools import product
from collections import defaultdict

n = 40
N = 10
window_size = 10
v = []
def int_to_bin(number):
    return [int(x) for x in bin(number)[2:]]

def bin_to_int(bit_list):
    output = 0
    for bit in bit_list:
        output = output * 2 + bit
    return output

def generate_d_candidates(difference, w, w_l):
    all_combinations = []
    l_zeros = [0]*(n-w)
    h_zeros = [0]*(w_l)

    for i in product([0,1], repeat=difference):
        comb = h_zeros+list(i)+l_zeros
        #print comb
        all_combinations.append(comb)
    return all_combinations

def xor_operation(v, d):
    #l = [int(x) for x in bin(v)[2:]]
    size_d = len(d)
    complementary = [0]*(size_d-len(v))
    v_list = complementary + v
    result = []
    for j in xrange(0, size_d):
        result.append((v_list[j]+d[j]) % 2)
    #print result
    return result

#TODO create argmin{S(d)}
def sum_all_ds(d_candidates, interval):
    pairs = defaultdict()
    for d in d_candidates:
        sum_hw_d = 0
        for j in xrange(1,N):
            print  (xor_operation(v[j], d))[-interval:]
            pre_sum = (xor_operation(v[j], d))[-interval:].count(1)
            sum_hw_d = sum_hw_d + pre_sum
        #print sum_hw_d, " ", d
        pairs[sum_hw_d] = d
    #print pairs.keys()
    key = min(pairs.keys())
    print "Min key: ", key, " value: ", pairs[key]
    return key



def wide_widow_attack():
    for i in xrange(0, N):
        a = random.getrandbits(n)
        v.append(int_to_bin(a))
    print "Starting...."
    w_l = 0
    w = window_size
    d_l = 0
    bits_size = 2**w

    while(w < n):
        print "Interaction"
        print "w_l ", w_l, " w ", w
        d_candidates = generate_d_candidates(window_size,w,w_l)
        d_candidate = sum_all_ds(d_candidates,w-w_l)
        w_l = w
        w = w + window_size

        #print d_candidate

    print "Finished."



wide_widow_attack()
