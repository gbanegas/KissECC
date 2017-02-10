import random
from itertools import product

from thread_sum import ThreadSum


n = 30
N = 2**(n/2)
d = 429496 + 123
q = 2**252 + 27742317777372353535851937790883648493
window_size = 5
r = []
v = []
alpha = []

def generate_v_values():
    for i in xrange(0, N):
        value = d + (alpha[i]*q)
        v.append(value)

def  generate_alpha_js():
    for i in xrange(1, N+1):
        al = r[i] - r[0]
        alpha.append(al)

def  generate_r_js():
    for i in xrange(0, N+1):
        a = random.getrandbits(n)
        r.append(a)

def resize_lists(v,d):
    if len(v) > len(d):
        diff = len(v)-len(d)
        plus = [0]*diff
        d = plus + d
    elif len(d) > len(v):
        diff = len(d)-len(v)
        plus = [0]*diff
        v = plus + v
    return v, d

def int_to_bin(number):
    return [int(x) for x in bin(number)[2:]]

def bin_to_int(bit_list):
    output = 0
    for bit in bit_list:
        output = output * 2 + bit
    return output

def generate_d_candidates(difference, size):
    all_combinations = []
    general_zeros = [0]*(size-difference)
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
    generate_r_js()
    generate_alpha_js()
    generate_v_values()
    print "d = ",  int_to_bin(d)
    print "Starting...."
    w_l = 0
    w = window_size
    d_l = 0


    while(w < n):
        print "Interaction"
        print "w_l ", w_l, " w ", w
        mod_value = 2**w
        d_candidates = generate_d_candidates(w-w_l, w)
        sum_d , d_candidate = sum_all_ds(d_candidates,w-w_l, mod_value)
        d_prime = bin_to_int(d_candidate[sum_d]) % mod_value
        print "sum: ", sum_d, " d_candidate = ", int_to_bin(d_prime)
        w_l = w
        w = w + window_size

        #print d_candidate

    print "Finished."



wide_widow_attack()
