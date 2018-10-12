"""
    tcs
    ~~~

    Type safe, straightforward implementation of Tagged Canonical S-Exps
    (https://gist.github.com/rain-1/a253e47b939fc0769524d8716541c96e).
    Note that Python does not support char or atom types, but this
    implementation preserves the type information, i.e.:

        loads(dumps(loads(x))) == x

    For all valid TCS tuples x.
"""


class TCSError(ValueError):
    pass


class Atom(str):
    def __repr__(self):
        return "Atom(%s)" % (str.__repr__(self))


class Char(str):
    def __repr__(self):
        return "Char(%s)" % (str.__repr__(self))


def _iload(it):
    ch = next(it)
    if ch == ".":
        return (
            _iload(it),
            _iload(it),
            )
    # get the length of the content
    length = ""
    while True:
        char = next(it)
        if char == ":":
            break
        length += char
    length = int(length)
    data = "".join(next(it) for _ in range(length))
    # now parse according to tag
    if ch == "A": return Atom(data)
    if ch == "S": return data
    if ch == "N": return int(data)
    if ch == "C": assert length == 1, "data has length 1"; return Char(data)
    if ch == "Z": assert length == 0, "data has length 0"; return None
    if ch == "B": assert data in "tf", "data is one of 't' or 'f'"; return data == "t"
    raise TCSError("invalid tag")


def _idump(xs):
    if isinstance(xs, tuple):
        yield "."
        yield from _idump(xs[0])
        yield from _idump(xs[1])
        return
    tag = (
        "A" if isinstance(xs, Atom) else  # more specific types before more general ones,
        "C" if isinstance(xs, Char) else  # since Char and Atom are both subclasses of str
        "S" if isinstance(xs, str) else
        "B" if isinstance(xs, bool) else  # bool before int because isinstance(False, int) == True
        "N" if isinstance(xs, int) else
        "Z"
        )
    content = (
        xs if tag in "ACS" else
        str(xs) if tag == "N" else
        ("t" if xs else "f") if tag == "B" else
        ""
        )
    yield tag
    yield str(len(content))
    yield ":"
    yield content


def loads(s):
    """
    Load a python object from some tcs `s`.
    """
    try:
        return _iload(iter(s))
    except AssertionError as exc:
        raise TCSError(exc.args[0])

def dumps(d):
    """
    Convert `d` into some tcs `s`.
    """
    return "".join(_idump(d))
