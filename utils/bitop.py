
class BitOp(object):
    """
    Class to operate with bits
    """
    @staticmethod
    def bit(h,i):
      return (ord(h[i/8]) >> (i%8)) & 1
