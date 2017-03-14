import threading

q = 2**252 + 27742317777372353535851937790883648493

def int_to_bin(number):
    return [int(x) for x in bin(number)[2:]]

def bin_to_int(bit_list):
    output = 0
    for bit in bit_list:
        output = output * 2 + bit
    return output

def xor_operation(v, d):
    result = v ^ d
    return result

def getalpha(v,j):
    return v[j]-v[0]

class ThreadSum(threading.Thread):

    def __init__(self, threadID, d_list, v_list, alpha_list, N, mod_value, interval):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.d_candidates = d_list
        self.v = v_list
        self.alpha = alpha_list
        self.N = N
        self.mod_value = mod_value
        self.key = 0
        self.d = []
        self.interval = interval

    def run(self):
        pairs = {}
        for d in self.d_candidates:
            sum_hw_d = 0
            for j in xrange(1,self.N):
                d_prime = bin_to_int(d)+(getalpha(self.v,j)) % self.mod_value
                v_j = self.v[j] % self.mod_value
                pre_sum = int_to_bin(xor_operation(v_j, d_prime))[-self.interval:].count(1)
                sum_hw_d = sum_hw_d + pre_sum
            try:
                if pairs[sum_hw_d] <> None:
                    val = pairs[sum_hw_d]
                    if val.count(1) > d.count(1):
                        pairs[sum_hw_d] = d
            except Exception as e:
                pairs[sum_hw_d] = d

        self.key = min(pairs.keys())
        self.d = pairs[self.key]

    def return_result(self):
        return self.key, self.d

    def clean(self):
        del self.v
        del self.alpha
        del self.d
        del self.key
        self.run = False
