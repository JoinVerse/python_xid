# All credit to github.com/rs
# almost a direct copy of https://github.com/rs/Xid
# Changes to make more pythonic as needed.

import os
from datetime import datetime
import threading

import base32hex

# MyPy imports
try:
    from typing import List
except:
    pass  # ignore, we do not need the typing module

# Some Constants
trimLen = 20
encodedLen = 24
rawLen = 12
precision = 1000000000


class InvalidVid(Exception):
    pass


def rand_int():
    # type: () -> int
    buf = str(os.urandom(6))
    buford = list(map(ord, buf))
    return buford[0] << 40 | buford[1] << 32 | buford[2] << 24 | buford[3] << 16 | buford[4] << 8 | buford[5]


def generate_next_id():
    id = rand_int()
    lock = threading.Lock()

    while True:
        lock.acquire()
        new_id = id + 1
        id += 1
        lock.release()
        yield new_id


objectIDGenerator = generate_next_id()


def generate_new_vid():
    # type: () -> List[int]
    now = int(datetime.now().timestamp() * precision)
    id = [0] * rawLen

    id[0] = (now >> 56) & 0xff
    id[1] = (now >> 48) & 0xff
    id[2] = (now >> 40) & 0xff
    id[3] = (now >> 32) & 0xff
    id[4] = (now >> 24) & 0xff
    id[5] = (now >> 16) & 0xff

    i = next(objectIDGenerator)

    id[6] = (i >> 40) & 0xff
    id[7] = (i >> 32) & 0xff
    id[8] = (i >> 24) & 0xff
    id[9] = (i >> 16) & 0xff
    id[10] = (i >> 8) & 0xff
    id[11] = i & 0xff

    return id


class Vid(object):
    def __init__(self, id=None):
        # type: (List[int]) -> None
        if id is None:
            id = generate_new_vid()
        self.value = id

    def counter(self):
        # type: () -> int
        return (self.value[6] << 40 |
                self.value[7] << 32 |
                self.value[8] << 24 |
                self.value[9] << 16 |
                self.value[10] << 8 |
                self.value[11])

    def datetime(self):
        return datetime.fromtimestamp(self.time())

    def time(self):
        # type: () -> float
        return (self.value[0] << 56 |
                self.value[1] << 48 |
                self.value[2] << 40 |
                self.value[3] << 32 |
                self.value[4] << 24 |
                self.value[5] << 16) / precision

    def string(self):
        # type: () -> str
        byte_value = self.bytes()
        return base32hex.b32encode(byte_value).lower()[:trimLen]

    def bytes(self):
        # type: () -> str
        return ''.join(map(chr, self.value))

    def __repr__(self):
        return "<Vid '%s'>" % self.__str__()

    def __str__(self):
        return self.string()

    def __lt__(self, arg):
        # type: (Vid) -> bool
        return self.string() < arg.string()

    def __gt__(self, arg):
        # type: (Vid) -> bool
        return self.string() > arg.string()

    @classmethod
    def from_string(cls, s):
        # type: (str) -> Vid
        val = base32hex.b32decode(s.upper())
        value_check = [0 <= x <= 255 for x in val]

        if not all(value_check):
            raise InvalidVid(s)

        return cls(val)
