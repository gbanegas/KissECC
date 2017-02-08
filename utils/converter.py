
class Converter(object):
    """
    Class to convert byte to Hex and vice versa.
    It is easier for a human "read" hexadecimal.
    """
    @staticmethod
    def byteToHex(byteStr ):
        """
        Convert a byte string to it's hex string representation e.g. for output.
        """
        return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()

    @staticmethod
    def hexToByte(hexStr ):
        """
        Convert a string hex byte values into a byte string. The Hex Byte values may
        or may not be space separated.
        """
        bytes = []

        hexStr = ''.join( hexStr.split(" ") )

        for i in range(0, len(hexStr), 2):
            bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

        return ''.join( bytes )
