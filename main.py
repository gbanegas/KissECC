import collections
import math
from edwards_curve import EdwardsCurve
from twistedcurves import TwistedEC
from eddsa import EdDSA
from elgamal import ElGamal
from utils.inversion import Inverse


if __name__ == "__main__":
    # Toy examples wih ed25519
    a = -1
    q = 2**255 - 19
    d = -121665 * Inverse().inv(121666, q)
    l = 2**252 + 27742317777372353535851937790883648493
    print "Strarting...."
    et = TwistedEC(a, d, q, l)
    edsa = EdDSA(et)
    priv = "gustavo"
    print "Using private key: ", priv
    pubk = edsa.publickey(priv)
    print "Public key generated: ", pubk
    text_to_sign = "Dance Like No One's Watching Encrypt Like Everyone Is"
    print "Signing: ", text_to_sign
    signature, _ = edsa.sign(text_to_sign, priv, pubk)
    print "Signature: ", _
    valid, _ = edsa.validate(signature, text_to_sign, pubk)
    print _
    print "Finished."
