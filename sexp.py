"""
    sexp
    ~~~~

    Implementation of a simpler subset of rivest's sexps,
    but only supports strings in 'verbatim' form, and assumes
    that the transport form is the same as canonical form,
    with some relaxations allowed.
"""


class SExpError(ValueError):
    pass


def loads(s):
    """
    Deserializes the sexp string `s`.
    """
    S = []
    S.append(S)
    i = 0
    N = len(s)
    while i < N:
        # skip forward until we can find meaningful data
        while s[i] == ' ':
            i += 1
            if i == N:
                raise SExpError
        ch = s[i]

        if ch == ')':
            r = S.pop()
            S[-1].append(r)
            i += 1
            continue

        if ch == '(':
            S.append([])
            i += 1
            continue

        length = ch
        while True:
            i += 1
            if i == N:
                raise SExpError
            if s[i] == ':':
                break
            length += s[i]
        length = int(length)
        assert i + length < N
        data = ""
        for _ in range(length):
            i += 1
            data += s[i]
        S[-1].append(data)
        i += 1
    return S.pop()


def _idump(d):
    if isinstance(d, (list, tuple)):
        yield '('
        for item in d:
            yield from _idump(item)
        yield ')'
        return
    yield str(len(d))
    yield ':'
    yield d


def dumps(d):
    """
    Converts a structure `d` into an sexp string.
    """
    return "".join(_idump(d))
