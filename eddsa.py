import hashlib
from twistedcurves import TwistedEC
from utils.converter import Converter
from utils.bitop import BitOp
from utils.inversion import Inverse
from exceptions_ecc.signatureerror import SignatureError

BITS_SIZE = 256

def hash_function(m):
    # Accept both str and bytes. If str, encode using UTF-8.
    if isinstance(m, str):
        m = m.encode('utf-8')
    return hashlib.sha512(m).digest()


class EdDSA(object):

    def __init__(self, ed):
        """Creating the EdDSA with an instance of TwistedEC"""
        assert isinstance(ed, TwistedEC)
        self.ed = ed
        By = 4 * Inverse().inv(5, self.ed.q)
        Bx = self.ed.xrecover(By)
        self.B = [Bx % self.ed.q, By % self.ed.q]

    def publickey(self, privkey):
        h = hash_function(privkey)
        a = 2 ** (BITS_SIZE - 2) + sum(2 ** i * BitOp().bit(h, i) for i in range(3, BITS_SIZE - 2))
        A = self.ed.scalar_multiplication(self.B, a)
        return Converter().byteToHex(self.__encodepoint(A))

    def sign(self, hashval, privkey, pub):
        # Ensure hashval is a bytes object.
        if isinstance(hashval, str):
            hashval = hashval.encode('utf-8')

        h = hash_function(privkey)
        pub_key = Converter().hexToByte(pub)
        a = 2 ** (BITS_SIZE - 2) + sum(2 ** i * BitOp().bit(h, i) for i in range(3, BITS_SIZE - 2))
        # Now h[...] is bytes and hashval is bytes, so concatenation works.
        r = self.__hint(h[BITS_SIZE // 8: BITS_SIZE // 4] + hashval)
        R = self.ed.scalar_multiplication(self.B, r)
        S = (r + self.__hint(self.__encodepoint(R) + pub_key + hashval) * a) % self.ed.l
        encoded = self.__encodepoint(R) + self.__encodeint(S)
        return encoded, Converter().byteToHex(encoded)

    def validate(self, signature, message, publickey):
        # Ensure message is in bytes if it's a string.
        if isinstance(message, str):
            message = message.encode('utf-8')

        pub_k = Converter().hexToByte(publickey)
        sign = signature
        if len(sign) != BITS_SIZE // 4:
            raise Exception("signature length is wrong")
        if len(pub_k) != BITS_SIZE // 8:
            raise Exception("public-key length is wrong")
        R = self.__decodepoint(sign[0: BITS_SIZE // 8])
        A = self.__decodepoint(pub_k)
        S = self.__decodeint(sign[BITS_SIZE // 8: BITS_SIZE // 4])
        h = self.__hint(self.__encodepoint(R) + pub_k + message)
        vef = self.ed.scalar_multiplication(self.B, S)
        sig = self.ed.edwards(R, self.ed.scalar_multiplication(A, h))
        if vef != sig:
            raise SignatureError(vef, sig)
        else:
            return True, "Valid"

    def validate_point(self, p):
        return self.ed.is_valid(p)

    def __hint(self, m):
        h = hash_function(m)
        return sum(2 ** i * BitOp().bit(h, i) for i in range(2 * BITS_SIZE))

    def __decodeint(self, s):
        return sum(2 ** i * BitOp().bit(s, i) for i in range(BITS_SIZE))

    def __decodepoint(self, s):
        y = sum(2 ** i * BitOp().bit(s, i) for i in range(BITS_SIZE - 1))
        x = self.ed.xrecover(y)
        if (x & 1) != BitOp().bit(s, BITS_SIZE - 1):
            x = self.ed.q - x
        P = [x, y]
        if not self.validate_point(P):
            raise Exception("decoding point that is not on curve")
        return P

    def __encodeint(self, y):
        bits = [(y >> i) & 1 for i in range(BITS_SIZE)]
        return bytes([sum(bits[i * 8 + j] << j for j in range(8)) for i in range(BITS_SIZE // 8)])

    def __encodepoint(self, P):
        x = P[0]
        y = P[1]
        bits = [(y >> i) & 1 for i in range(BITS_SIZE - 1)] + [x & 1]
        return bytes([sum(bits[i * 8 + j] << j for j in range(8)) for i in range(BITS_SIZE // 8)])
