"""
    bencoding
    ~~~~~~~~~

    Implementation of the bencoding exchange format found in
    BitTorrent (http://www.bittorrent.org/beps/bep_0003.html#bencoding).
"""


class BEncodingError(ValueError):
    pass


EOS = object()  # end of sequence


def _loadi(it, expecting_eos=False):
    ch = next(it, None)
    if ch is None:
        raise BEncodingError("no data")

    # outside of list and dictionary mode we don't generally
    # expect the data to contain an unmarked "e".
    if ch == 'e' and expecting_eos:
        return EOS

    # list or dictionary
    # 'l' <items> 'e' or 'd' <items> 'e'
    if ch == 'l' or ch == 'd':
        data = []
        while True:
            item = _loadi(it, expecting_eos=True)
            if item is EOS:
                break
            data.append(item)
        if ch == 'd':
            rv = {}
            for i in range(len(data) // 2):
                key = data[2*i]
                val = data[2*i+1]
                # should this really be done?
                if isinstance(key, list):
                    key = tuple(key)
                rv[key] = val
            return rv
        return data

    # integer
    # 'i' <data:int> 'e'
    if ch == 'i':
        b = ""
        while True:
            c = next(it, None)
            if c == 'e':
                break
            b += c
        try:
            return int(b)
        except ValueError:
            raise BEncodingError("invalid integer")

    # string
    # <length:int> ':' <data[length]>
    if ch.isalnum():
        l = ch  # length buffer
        while True:
            c = next(it, None)
            if c == ':':
                break
            l += c
        try:
            l = int(l)
        except ValueError:
            raise BEncodingError("invalid string length")
        try:
            return "".join(next(it, None) for _ in range(l))
        except TypeError:
            raise BEncodingError("length > available data")

    raise BEncodingError("unexpected data")


def _idump(d):
    if isinstance(d, dict):
        yield 'd'
        for key in sorted(d):
            yield from _idump(key)
            yield from _idump(d[key])
        yield 'e'

    elif isinstance(d, (list, tuple)):
        yield 'l'
        for item in d:
            yield from _idump(item)
        yield 'e'

    elif isinstance(d, int):
        yield 'i'
        yield str(d)
        yield 'e'

    elif isinstance(d, str):
        yield str(len(d))
        yield ':'
        yield d

    else:
        raise BEncodingError("invalid data")


def loads(s):
    """
    Convert from a bencoded string `s` into a python object.
    """
    return _loadi(iter(s))


def dumps(d):
    """
    Returns the bencoding for some python object `d`.
    """
    return "".join(_idump(d))
