import time

from AuxTables import s_boxes_tables
from RNGvideo.rng import get_seed_from_pixel


def string_to_bit_conv(text):
    _list = []
    [_list.extend(list(map(int, list(evaluate(char, 8))))) for char in text]

    return _list


def bits_to_string_conv(_list):
    return ''.join([chr(int(y, 2)) for y in [''.join([str(x) for x in _bytes]) for _bytes in split(_list, 8)]])


def evaluate(value, size):
    binvalue = bin(value)[2:] if isinstance(value, int) else bin(ord(value))[2:]
    if len(binvalue) > size:
        raise Exception("binary value larger than the expected size")
    while len(binvalue) < size:
        binvalue = "0" + binvalue
    return binvalue


def split(to_split, size):
    return [to_split[i:i + size] for i in range(0, len(to_split), size)]


def substitute(right_expanded):
    subblocks = split(right_expanded, 6)
    result = []
    for i in enumerate(subblocks):
        row = int(str(i[1][0]) + str(i[1][5]), 2)  # not mathematical way in case of 01, 02 etc. vals.
        column = int(''.join([str(x) for x in i[1][1:][:-1]]), 2)
        val = s_boxes_tables[i[0]][row][column]
        result.extend([int(x) for x in evaluate(val, 4)])

    return result


# permute and expand are the same, twice declared so code remains clear
def permute(block, table):
    return [block[x - 1] for x in table]


def expand(block, table):
    return [block[x - 1] for x in table]


def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]


def shift(left, right, _shift):
    return left[_shift:] + left[:_shift], right[_shift:] + right[:_shift]


def depadd(data):
    return data[:-ord(data[-1])]


def padd(data):
    pad_len = 8 - (len(data) % 8)
    return pad_len * chr(pad_len)


def get_key(video, rng, primes, w, h):
    video.set(1, time.time() * 1000 % video.get(7))
    res, frame = video.read()
    seed = get_seed_from_pixel(frame=frame, w=w, h=h)

    while True:
        key = str(rng.single(primes=primes, pixel_seed=seed, rnd_range=99999999))
        if len(key) == 8:
            break

    return key
