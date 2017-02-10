import random
from itertools import product

n = 50
N = 500
d = 983737618
q = 2**252 + 27742317777372353535851937790883648493
window_size = 10
r = []
v = []
alpha = []

def int_to_bin(number):
    return [int(x) for x in bin(number)[2:]]

def bin_to_int(bit_list):
    output = 0
    for bit in bit_list:
        output = output * 2 + bit
    return output

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

def xor_operation(v, d):
    result = v ^ d
    return result

def sum_all_ds(d_candidates, interval, mod_value):
    pairs = {}
    for d in d_candidates:
        sum_hw_d = 0
        for j in xrange(1,N):
            d_prime = bin_to_int(d)+(alpha[j]*q) % mod_value
            v_j = v[j] % mod_value
            pre_sum = int_to_bin(xor_operation(v_j, d_prime))[-interval:].count(1)
            sum_hw_d = sum_hw_d + pre_sum
        try:
            #print pairs[sum_hw_d]
            if pairs[sum_hw_d] <> None:
                val = pairs[sum_hw_d]
                if val.count(1) > d.count(1):
                    pairs[sum_hw_d] = d
        except Exception as e:
            pairs[sum_hw_d] = d


    return min(pairs.keys()) , pairs



def wide_widow_attack():
    generate_r_js()
    generate_alpha_js()
    generate_v_values()
    print "d = ",  int_to_bin(d), " len: ", len(int_to_bin(d))
    print "Starting...."
    window_size = 10
    w_prime = 0
    w = window_size
    d_prime = 0

#TODO: Change to least significant bits
#TODO: The HW will be "form w' to w"
    difference = w - w_prime
    variations = []
    for i in product([0,1], repeat=difference):
        variations.append(list(i))
    while (w < n):
        print "w: ", w
        print "w_prime: ", w_prime
        mod_value = 2**w
        d_prime = d_prime % mod_value
        d_prime_bin = int_to_bin(d_prime)
        to_iterate = []
        for variation in variations:
            to_iterate.append(variation+d_prime_bin)
        sum_d , d_candidate = sum_all_ds(to_iterate, w, mod_value)
        d_prime = bin_to_int(d_candidate[sum_d])
        print "sum: ", sum_d, " d_candidate = ", int_to_bin(d_prime)
        w_prime = w
        w = w + window_size
    print "Finished."



wide_widow_attack()

#lista = [1,2,3,4,5,6,7,8]
#print lista[3:5]
#print lista[-2]
