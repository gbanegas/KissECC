import collections
from ecc import EC
from edwards_curve import EdwardsCurve

Coord = collections.namedtuple("Coord", ["x", "y"])

if __name__ == "__main__":
    # Toy examples
    ec = EC(1, 18, 19)
    ed = EdwardsCurve(ec, 1, 18, 19)
    p1 = Coord(2,1)
    p2 = Coord(1,0)
    p3 = ed.add(p1,p2)
    print p3
