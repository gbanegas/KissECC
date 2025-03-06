class Converter(object):
    """
    Class to convert bytes to Hex and vice versa.
    It is easier for a human to read hexadecimal.
    """
    @staticmethod
    def byteToHex(byteStr):
        """
        Convert a bytes object to its hex string representation, e.g. for output.
        """
        # Iterating over a bytes object yields integers.
        return ' '.join(["%02X" % b for b in byteStr])

    @staticmethod
    def hexToByte(hexStr):
        """
        Convert a string of hex byte values into a bytes object.
        The Hex Byte values may or may not be space separated.
        """
        # Remove any spaces
        hexStr = ''.join(hexStr.split(" "))
        return bytes.fromhex(hexStr)
