"""
    netstrings
    ~~~~~~~~~~

    Simple implementation of djb's tiny netstrings
    (https://cr.yp.to/proto/netstrings.txt) spec.
    Can work with non-ASCII data, but the headers
    are still in ASCII.
"""


def loadb(b):
    """
    Retrieve a byte string from nestring `b`.
    """
    i = 0
    l = ''
    # get length
    while True:
        ch = b[i]
        i += 1
        if ch == 58:  # ch == ':'
            break
        elif 48 <= ch <= 57:  # '0' <= ch <= '9'
            l += chr(ch)
        else:
            raise ValueError("expected 0-9 or : in header")
    if len(l) == 0:
        raise ValueError("emtpy header")
    # i == length of header
    # b = [...] (length i) + [...] (length l) + "," (1)
    length = int(l)
    if len(b) - i - 1 != length:
        raise ValueError("payload length doesn't match declared length")
    return b[i:-1]


def dumpb(b):
    """
    Convert byte string `b` to a nestring.
    """
    return b''.join([
            str(len(b)).encode('ascii'),
            b':',
            b,
            b',',
        ])
