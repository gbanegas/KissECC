from ecc import EC
from df import DiffieHellman
from elgamal import ElGamal
from dsa import DSA

if __name__ == "__main__":
    # shared elliptic curve system of examples
    ec = EC(1, 18, 19)


    g, _ = ec.at(7)
    print ec.order(g)
    assert ec.order(g) <= ec.q

    # ElGamal enc/dec usage
    eg = ElGamal(ec, g)
    # mapping value to ec point
    # "masking": value k to point ec.mul(g, k)
    # ("imbedding" on proper n:use a point of x as 0 <= n*v <= x < n*(v+1) < q)
    mapping = [ec.mul(g, i) for i in range(eg.n)]
    plain = mapping[7]

    priv = 5
    pub = eg.gen(priv)

    cipher = eg.enc(plain, pub, 15)
    decoded = eg.dec(cipher, priv)
    assert decoded == plain
    assert cipher != pub


    # ECDH usage
    dh = DiffieHellman(ec, g)

    apriv = 11
    apub = dh.gen(apriv)

    bpriv = 3
    bpub = dh.gen(bpriv)

    cpriv = 7
    cpub = dh.gen(cpriv)
    # same secret on each pair
    assert dh.secret(apriv, bpub) == dh.secret(bpriv, apub)
    assert dh.secret(apriv, cpub) == dh.secret(cpriv, apub)
    assert dh.secret(bpriv, cpub) == dh.secret(cpriv, bpub)

    # not same secret on other pair
    assert dh.secret(apriv, cpub) != dh.secret(apriv, bpub)
    assert dh.secret(bpriv, apub) != dh.secret(bpriv, cpub)
    assert dh.secret(cpriv, bpub) != dh.secret(cpriv, apub)


    # ECDSA usage
    dsa = DSA(ec, g)

    priv = 11
    pub = eg.gen(priv)
    hashval = 128
    r = 7

    sig = dsa.sign(hashval, priv, r)
    assert dsa.validate(hashval, sig, pub)
    print "OI"
    pass
