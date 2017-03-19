import random, math
import time
from itertools import product

R = 32
N = 1000
#d = 13393249480990767973698914121061987209673507827659760595482620214891467806973397091277092174
d = 1233932494 #31 bits
#d = 23393249481
#d = 133932494809907679736989141210619872096735078276597605954826202148555332 #237 bits
q = 2**252 + 27742317777372353535851937790883648493
#q = 2**32
window_size = 10
RANDOMIZED_BITS = 0
r = []
v = []
alpha = []
n = 0
def getalpha(v,j):
    return v[j]-v[0]

def int_to_bin(number):
    return [int(x) for x in bin(number)[2:]]

def bin_to_int(bit_list):
    output = 0
    for bit in bit_list:
        output = output * 2 + bit
    return output

def generate_v():
    value = d + (r[0]*q)
    #print (r[0]*q), " , ",int_to_bin((r[0]*q))
    v.append(value)
    for i in xrange(1, N):
        value = d + (r[i]*q)
        v.append(value)

def  generate_alpha_js():
    for i in xrange(1, N+1):
        al = r[i] - r[0]
        alpha.append(int(math.fabs(al)))

def  generate_r_js():
    for i in xrange(0, N+1):
        a = random.getrandbits(R)
        r.append(int(math.fabs(a)))

def xor_operation(v, d):
    result = v ^ d
    return result

def sum_all_ds(d_candidates, w, w_prime, mod_value):
    pairs = {}
    for d in d_candidates:
        #print "d_candidate: ", d
        sum_hw_d = 0
        for j in xrange(1,N):
            d_prime = (bin_to_int(d)+(getalpha(v,j))) % mod_value
            v_j = v[j] % mod_value
            #change here to get now "W - W_prime"
            temp_xor = int_to_bin(xor_operation(v_j, d_prime))
            temp = temp_xor[:(w-w_prime)]
            #print "Xor: ", temp_xor
            #print "Temp: ", temp
            pre_sum = temp.count(1)
            #print "HW: ", pre_sum
            #time.sleep(0.5)
            sum_hw_d = sum_hw_d + pre_sum
        try:
            if pairs[sum_hw_d] <> None:
                val = pairs[sum_hw_d]
                pairs[sum_hw_d].append(d)
        except Exception as e:
            pairs[sum_hw_d] = [d]


    return min(pairs.keys()) , pairs[min(pairs.keys())]

def check_result(d_candidates):
    for d_prime in d_candidates:
        if bin_to_int(d_prime) == d:
            return True, d_prime
    return False, None

def wide_widow_attack():
    generate_r_js()
    generate_alpha_js()
    generate_v()
    print "d = ",  int_to_bin(d), " len: ", len(int_to_bin(d)), " d ", d
    print "Starting...."
    w_prime = 0
    w = window_size
    #d_prime = [0]
    d_candidate = []
    difference = w - w_prime
    variations = []
    for i in product([0,1], repeat=difference):
        variations.append(list(i))
    n = len(int_to_bin(v[0]))
    while (w < (n)):
        print "w: ", w
        print "w_prime: ", w_prime
        mod_value = 2**w
        to_iterate = []
        for d_prime in d_candidate:
            for variation in variations:
                to_iterate.append(variation+d_prime)
        sum_d , d_candidate = sum_all_ds(to_iterate, w, w_prime, mod_value)
        print "sum: ", sum_d, " d_candidate = ", d_candidate
        print "sum: ", sum_d, " d_candidate = ", d_candidate[0], " d_ca = ", bin_to_int(d_candidate[0])
        #time.sleep(5)
        w_prime = w
        w = w + window_size

        check, result_d = check_result(d_candidate)
        if check:
            w = w+n
            print "FOUND KEY."
            print result_d


    #if (d == bin_to_int(d_prime)):
    #    print "FOUND KEY."
    #else:
    #    print "SORRY"
    print "Finished."



wide_widow_attack()

#lista = [1,2,3,4,5,6,7,8]
#print lista[3:5]
#print lista[-2]
