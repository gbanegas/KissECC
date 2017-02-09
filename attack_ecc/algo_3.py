import random
from itertools import product

from thread_sum import ThreadSum

n = 250
N = 1200
q = 2**255 - 19
window_size = 10
v = []
alpha = []

def generate_v_values():
    for i in xrange(0, N):
        a = random.getrandbits(n)
        v.append(int_to_bin(a))

def  generate_alpha_j():
    for i in xrange(0, N):
        a = random.getrandbits(n)
        alpha.append(a)


def int_to_bin(number):
    return [int(x) for x in bin(number)[2:]]

def bin_to_int(bit_list):
    output = 0
    for bit in bit_list:
        output = output * 2 + bit
    return output

def generate_d_candidates(difference):
    all_combinations = []
    general_zeros = [0]*(n-difference)
    for i in product([0,1], repeat=difference):
        all_combinations.append(list(i)+general_zeros)
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
def sum_all_ds(d_candidates, interval, mod_value):
    pairs = {}
    number_of_threads = 4
    ds = zip(*[iter(d_candidates)]*number_of_threads)
    threads = []
    for i in xrange(0, number_of_threads):
        threads.append(ThreadSum(i, ds[i],v,alpha,N, mod_value, interval))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    for t in threads:
        key, d = t.return_result()
        pairs[key] = d

    print key
    print pairs.keys()
    return min(pairs.keys()) , pairs



def wide_widow_attack():
    generate_v_values()
    generate_alpha_j()
    print "Starting...."
    w_l = 0
    w = window_size
    d_l = 0


    while(w < n):
        print "Interaction"
        print "w_l ", w_l, " w ", w
        mod_value = 2**w
        d_candidates = generate_d_candidates(w-w_l)
        sum_d , d_candidate = sum_all_ds(d_candidates,w-w_l, mod_value)

        w_l = w
        w = w + window_size

        #print d_candidate

    print "Finished."



wide_widow_attack()
