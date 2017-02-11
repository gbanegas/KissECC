import random
from itertools import product

from thread_sum import ThreadSum



n = 50
N = 500
d = 83737618
q = 2**252 + 27742317777372353535851937790883648493
window_size = 10
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


def int_to_bin(number):
    return [int(x) for x in bin(number)[2:]]

def bin_to_int(bit_list):
    output = 0
    for bit in bit_list:
        output = output * 2 + bit
    return output


def sum_all_ds(d_candidates, interval, mod_value):
    pairs = {}
    number_of_threads = 4
    ds = zip(*[iter(d_candidates)]*number_of_threads)
    threads = []
    for i in xrange(0, number_of_threads):
        threads.append(ThreadSum(i, ds[i], v, alpha, N, mod_value, interval))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    for t in threads:
        key, d = t.return_result()
        try:
            if pairs[key] <> None:
                val = pairs[key]
                if val.count(1) > d.count(1):
                    pairs[key] = d
        except Exception as e:
            pairs[key] = d

    print key
    print pairs.keys()
    return min(pairs.keys()) , pairs



def wide_widow_attack():
    generate_r_js()
    generate_alpha_js()
    generate_v_values()
    print "d = ",  int_to_bin(d), " len: ", len(int_to_bin(d))
    print "Starting...."
    w_prime = 0
    w = window_size
    d_prime = 0
    variations = []
    for i in product([0,1], repeat=window_size):
        variations.append(list(i))


    while(w < n):
        print "w: ", w
        print "w_prime: ", w_prime
        mod_value = 2**w
        d_prime = d_prime % mod_value
        d_prime_bin = int_to_bin(d_prime)
        to_iterate = []
        for variation in variations:
            to_iterate.append(variation+d_prime_bin)
        sum_d , d_candidate = sum_all_ds(to_iterate, w, mod_value)
        d_prime = bin_to_int(d_candidate[sum_d]) % mod_value
        print "sum: ", sum_d, " d_candidate = ", int_to_bin(d_prime)
        w_l = w
        w = w + window_size

    print "Finished."



wide_widow_attack()
