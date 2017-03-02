import random
import math
from itertools import product
from itertools import chain
from thread_sum import ThreadSum


q = 2**252 + 27742317777372353535851937790883648493
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

def groupsof(n, xs):
    if len(xs) < n:
        return [xs]
    else:
        return chain([xs[0:n]], groupsof(n, xs[n:]))


class WindowAttack(object):
    def generate_v_values(self, d, N):
        for i in xrange(0, N):
            value = d + (alpha[i]*q)
            v.append(value)

    def  generate_alpha_js(self, N):
        for i in xrange(1, N+1):
            al = r[i] - r[0]
            alpha.append(int(math.fabs(al)))

    def  generate_r_js(self, n, N):
        for i in xrange(0, N+1):
            a = random.getrandbits(n)
            r.append(int(math.fabs(a)))

    def bit_flip_random(self, bit_list, randomized_bits):
        bit_list_t = bit_list[:]
        pos_list = []
        if len(bit_list) < randomized_bits:
            raise Exception("Randomized bigger then d+(a*r)")
            print "Lenght: ", len(bit_list)
        for i in xrange(0, randomized_bits):
            pos_bit_to_flip = random.randint(0, len(bit_list)-1)
            while(pos_bit_to_flip in pos_list):
                pos_bit_to_flip = random.randint(0, len(bit_list)-1)
            pos_list.append(pos_bit_to_flip)
            if bit_list_t[pos_bit_to_flip] == 1:
                bit_list_t[pos_bit_to_flip] = 0
            else:
                bit_list_t[pos_bit_to_flip] = 1

        return bit_list_t

    def generate_v_values_with_bit_flip(self, d, N, randomized_bits):
        for i in xrange(0, N):
            value = d + (alpha[i]*q)
            bit_list = int_to_bin(value)
            #print len(bit_list)
            bit_list_flipped = self.bit_flip_random(bit_list, randomized_bits)
            value_flipped = bin_to_int(bit_list_flipped)
            v.append(value_flipped)



    def sum_all_ds(self, d_candidates, interval, mod_value, N):
        pairs = {}
        number_of_threads = 4
        ds = list(groupsof(len(d_candidates)/number_of_threads, d_candidates))
        #ds = zip(*[iter(d_candidates)]*number_of_threads)
        threads = []
        #print "DS: ", len(ds)
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

        #print pairs

        #print key
        #print pairs.keys()
        return min(pairs.keys()) , pairs


    def test_d(self, d, to_test):
        """ Function to test the candidate to d. In our case, it is a comparasion
        with the original d. However, in a real case could be the ciphered text with the original
        and the candidate"""
        return (d==to_test)

    def wide_widow_attack(self, d, window_size = 10, n = 512, N = 200, randomized_bits = 30):
        self.generate_r_js(n, N)
        self.generate_alpha_js(N)
        self.generate_v_values_with_bit_flip(d, N, randomized_bits)
        print "d = ",  int_to_bin(d), " len: ", len(int_to_bin(d))
        print "Starting...."
        w_prime = 0
        w = window_size
        d_prime = 0
        variations = []
        for i in product([0,1], repeat=window_size):
            variations.append(list(i))

        while(w < (n + window_size + window_size)):
            print "w: ", w
            print "w_prime: ", w_prime
            mod_value = 2**w
            d_prime = d_prime % mod_value
            d_prime_bin = int_to_bin(d_prime)
            to_iterate = []
            for variation in variations:
                to_iterate.append(variation+d_prime_bin)
            sum_d , d_candidate = self.sum_all_ds(to_iterate, w, mod_value, N)
            d_prime = bin_to_int(d_candidate[sum_d])
            print "sum: ", sum_d, " d_candidate = ", int_to_bin(d_prime)
            w_prime = w
            w = w + window_size

            if self.test_d(d, d_prime):
                w = w+n

        if (d == d_prime):
            print "FOUND KEY."
        else:
            print "SORRY"
        print "Finished."
