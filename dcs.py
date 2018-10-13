"""
    dcs
    ~~~

    Straightforward implementation of Dotted Canonical S-Exps
    (https://gist.github.com/rain-1/a253e47b939fc0769524d8716541c96e).
"""


def _iload(it):
    ch = next(it)
    if ch == ".":
        return (
            _iload(it),
            _iload(it),
            )
    # get the length of the content
    length = ch
    while True:
        char = next(it)
        if char == ":":
            break
        length += char
    length = int(length)
    data = "".join(next(it) for _ in range(length))
    return data


def _idump(xs):
    if isinstance(xs, tuple):
        yield "."
        yield from _idump(xs[0])
        yield from _idump(xs[1])
        return
    yield str(len(xs))
    yield ":"
    yield xs


def loads(s):
    """
    Load a python object from some tcs `s`.
    """
    return _iload(iter(s))

def dumps(d):
    """
    Convert `d` into some tcs `s`.
    """
    return "".join(_idump(d))
