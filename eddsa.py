import hashlib, collections
from twistedcurves import TwistedEC
from exceptions_ecc.signatureerror import SignatureError

b = 256
l = 2**252 + 27742317777372353535851937790883648493
def hash_function(m):
    return hashlib.sha512(m).digest()

def bit(h,i):
  return (ord(h[i/8]) >> (i%8)) & 1

def inv(x, q):
  return power_mod(x,q-2,q)

def power_mod(b,e,m):
    if e == 0: return 1
    t = power_mod(b,e/2,m)**2 % m
    if e & 1: t = (t*b) % m
    return t


def ByteToHex( byteStr ):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """
    return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()

#-------------------------------------------------------------------------------

def HexToByte( hexStr ):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    bytes = []

    hexStr = ''.join( hexStr.split(" ") )

    for i in range(0, len(hexStr), 2):
        bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

    return ''.join( bytes )


class EdDSA(object):

    def __init__(self, ed):
        """ Creating the EdDSA with a instace of TwistedEC"""
        assert isinstance(ed, TwistedEC)
        self.ed = ed
        By = 4 * inv(5, self.ed.q)
        Bx = self.ed.xrecover(By)
        self.B = Coord(Bx % self.ed.q, By % self.ed.q)

    def publickey(self, privkey):
        h = hash_function(privkey)
        a = 2**(b-2) + sum(2**i * bit(h,i) for i in range(3,b-2))
        A = self.ed.scalar_multiplication(self.B,a)
        return ByteToHex(self.encodepoint(A))

    def sign(self, hashval, privkey, pub):
        h = hash_function(privkey)
        pub_key = HexToByte(pub)
        a = 2**(b-2) + sum(2**i * bit(h,i) for i in range(3,b-2))
        r = self.__hint__(''.join([h[i] for i in range(b/8,b/4)]) + hashval)
        R = self.ed.scalar_multiplication(self.B,r)
        S = (r + self.__hint__(self.encodepoint(R) + pub_key + hashval) * a) % l
        return self.encodepoint(R) + self.encodeint(S), ByteToHex(self.encodepoint(R) + self.encodeint(S))

    def validate_point(self, p):
        return self.ed.is_valid(p)

    def __hint__(self, m):
        h = hash_function(m)
        return sum(2**i * bit(h,i) for i in range(2*b))

    def __decodeint__(self, s):
        return sum(2**i * bit(s,i) for i in range(0,b))

    def __decodepoint__(self, s):
        y = sum(2**i * bit(s,i) for i in range(0,b-1))
        x = self.ed.xrecover(y)
        if x & 1 != bit(s,b-1): x = self.ed.q-x
        P = Coord(x,y)
        if not self.validate_point(P): raise Exception("decoding point that is not on curve")
        return P

    def encodeint(self, y):
        bits = [(y >> i) & 1 for i in range(b)]
        return ''.join([chr(sum([bits[i * 8 + j] << j for j in range(8)])) for i in range(b/8)])

    def encodepoint(self, P):
        x = P[0]
        y = P[1]
        bits = [(y >> i) & 1 for i in range(b - 1)] + [x & 1]
        return ''.join([chr(sum([bits[i * 8 + j] << j for j in range(8)])) for i in range(b/8)])

    def validate(self, signature, message, publickey):
        pub_k = HexToByte(publickey)
        sign = signature
        if len(sign) != b/4: raise Exception("signature length is wrong")
        if len(pub_k) != b/8: raise Exception("public-key length is wrong")
        R = self.__decodepoint__(sign[0:b/8])
        A = self.__decodepoint__(pub_k)
        S = self.__decodeint__(sign[b/8:b/4])
        h = self.__hint__(self.encodepoint(R) + pub_k + message)
        vef = self.ed.scalar_multiplication(self.B,S)
        sig = self.ed.edwards(R,self.ed.scalar_multiplication(A,h))
        if vef != sig:
            raise SignatureError(vef, sig)
        else:
            return True, "Valid"
