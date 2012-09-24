import hashlib


def hexdigest(strings):
    m = hashlib.md5()
    for s in strings:
        m.update(s)
    return m.hexdigest()
