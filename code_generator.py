from qutils import alphabet, numbers
from random import randint as r

a = alphabet + numbers
c = lambda l : ''.join([a[r(0, len(a)-1)] for x in range(1, l)])

__all__ = ['c']