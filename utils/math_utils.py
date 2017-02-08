
class MathUtil(object):

    @staticmethod
    def sqrt(n, q):
        """sqrt on PN modulo: returns two numbers or exception if not exist
        >>> assert (sqrt(n, q)[0] ** 2) % q == n
        >>> assert (sqrt(n, q)[1] ** 2) % q == n
        """
        assert n < q
        for i in range(1, q):
            if i * i % q == n:
                return (i, q - i)
            pass
        raise Exception("sqrt not found")
