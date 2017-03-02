import random, math
from itertools import product

n = 1024
N = 100
#d = 1123983737618
#d = 265463185775234288092201526257649332892133932494809907679736989141210619872096735078276597605954826202148
d = 13393249480990767973698914121061987209673507827659760595482620214891467806973397091277092174174393961305025200909026701058146674630543302845868229392185528
q = 2**252 + 27742317777372353535851937790883648493
window_size = 10
RANDOMIZED_BITS = 512
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



def bit_flip_random(bit_list):
    bit_list_t = bit_list[:]
    for i in xrange(0, RANDOMIZED_BITS):
        pos_bit_to_flip = random.randint(0, len(bit_list)-1)
        if bit_list_t[pos_bit_to_flip] == 1:
            bit_list_t[pos_bit_to_flip] = 0
        else:
            bit_list_t[pos_bit_to_flip] = 1

    return bit_list_t



def generate_v_values_with_bit_flip():
    for i in xrange(0, N):
        value = d + (alpha[i]*q)
        bit_list = int_to_bin(value)
        #print len(bit_list)
        bit_list_flipped = bit_flip_random(bit_list)
        value_flipped = bin_to_int(bit_list_flipped)
        v.append(value_flipped)

def  generate_alpha_js():
    for i in xrange(1, N+1):
        al = r[i] - r[0]
        alpha.append(int(math.fabs(al)))

def  generate_r_js():
    for i in xrange(0, N+1):
        a = random.getrandbits(n)
        r.append(int(math.fabs(a)))

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
            if pairs[sum_hw_d] <> None:
                val = pairs[sum_hw_d]
                if val.count(1) > d.count(1):
                    pairs[sum_hw_d] = d
        except Exception as e:
            pairs[sum_hw_d] = d


    return min(pairs.keys()) , pairs

def test_d(to_test):
    """ Function to test the candidate to d. In our case, it is a comparasion
    with the original d. However, in a real case could be the ciphered text with the original
    and the candidate"""
    return (d==to_test)


def wide_widow_attack():
    generate_r_js()
    generate_alpha_js()
    generate_v_values_with_bit_flip()
    print "d = ",  int_to_bin(d), " len: ", len(int_to_bin(d))
    print "Starting...."
    window_size = 10
    w_prime = 0
    w = window_size
    d_prime = 0
    difference = w - w_prime
    variations = []
    first_pass = True
    for i in product([0,1], repeat=difference):
        variations.append(list(i))

    while (w < (n + window_size + window_size)):
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

        if test_d(d_prime):
            w = w+n

    if (d == d_prime):
        print "FOUND KEY."
    else:
        print "SORRY"
    print "Finished."



wide_widow_attack()

#lista = [1,2,3,4,5,6,7,8]
#print lista[3:5]
#print lista[-2]
