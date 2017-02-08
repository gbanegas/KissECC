from itertools import product
n = 250

window_size = 10

def generate_d_candidates(difference):
    for i in product([0,1], repeat=difference):
        print i
    new_l = l+bin_list
    #print new_l




def wide_widow_attack():
    print "Starting...."
    w_l = 0
    w = window_size
    d_l = 0
    while(w > n):
        d_candidates = generate_d_candidates(w-w_l)
        w_l = w
        w = w + window_size





wide_widow_attack()
