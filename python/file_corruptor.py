from math import ceil
from random import randint, randbytes


def corrupt(fn: str, amt: float):
    data = b""
    with open(fn, "rb") as fd:
        data = fd.read()
    filesize = len(data)

    fn_new = fn + ".bin"
    try:
        open(fn_new)
    except FileNotFoundError:
        bmode = "xb"
    else:
        bmode = "wb"
    with open(fn_new, bmode) as fd:
        fd.write(b"")

    to_corrupt = ceil(filesize * amt / 100)
    mcrlen = ceil(to_corrupt / 2)
    corrupted = 0
    data_list = list(data)
    while corrupted < to_corrupt:
        i = randint(0, filesize - 1)
        l = randint(1, mcrlen)
        if l + i > filesize - 1:
            l = 1
        d = randbytes(l)
        for j in range(l):
            c = randint(0, 3)
            p = i + j
            if c == 0:
                data_list[p] = max(data_list[p] - ceil(d[j] / 4), 32)
            if c == 1 or c == 2 or c == 3:
                data_list[p] = min((data_list[p] * 5), 255)
            if c == 3:
                data_list[p] = 255 - data_list[p]
        corrupted += l

    with open(fn_new, "wb") as fd:
        fd.write(bytes(data_list))


if __name__ == "__main__":
    fn = input("What file would you like to corrupt?")
    amt = float(input("How much corruption do you want? (in percent, e.g. 1.23)"))
    corrupt(fn, amt / 100)
