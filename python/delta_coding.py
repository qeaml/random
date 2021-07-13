def delta_encode(i):
    out = []
    last = 0
    for v in i:
        out += [-(last-v)]
        last = v
    return out
    
def delta_decode(i):
    out = []
    last = 0
    for v in i:
        out += [last+v]
        last += v
    return out

if __name__ == '__main__':
    l = [10,13,10,6,7,8]
    encoded = delta_encode(l)
    decoded = delta_decode(encoded)
    print(encoded, decoded)