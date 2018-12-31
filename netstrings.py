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
    l = 0
    while True:
        ch = b[i]
        if 48 <= ch <= 57:  # '0' <= ch <= '9'
            l *= 10
            l += (ch - 48)
            i += 1
        elif ch == 58:  # ch == ':'
            break
        else:
            raise ValueError("expected 0-9 or : in header")
    if i + l + 2 != len(b):
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
