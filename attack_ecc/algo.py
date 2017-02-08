from itertools import product
n = 250

window_size = 10

def generate_d_candidates(difference, bit_size):
    l =[]
    general_zeros = [0]*(bit_size-difference)
    for i in product([0,1], repeat=difference):
        l.append(list(i))

    all_combinations = []
    for w_bits_list in l:
        new_l = w_bits_list+general_zeros
        all_combinations.append(new_l)

    return all_combinations

    #print new_l




def wide_widow_attack():
    print "Starting...."
    w_l = 0
    w = window_size
    d_l = 0

    while(w < n):
        print "Interaction"
        bits_size = 2**2

        d_candidates = generate_d_candidates(w-w_l, bits_size)
        w_l = w
        w = w + window_size
        print d_candidates






wide_widow_attack()
