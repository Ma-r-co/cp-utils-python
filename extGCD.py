def extGCD(a, b):
    '''
    ax + by = gcd(a, b) を満たす整数解x, yを求める
    返り値: gcd(a, b), x, y
    '''
    if b == 0:
        d = abs(a)
        x, y = (1, 0) if a >= 0 else (-1, 0)
    else:
        d, s, t = extGCD(b, a % b)
        x = t
        y = s - (a // b) * t
    return d, x, y


def inv_mod(a, m):
    '''
    法 m の元での a の逆元を求める

    ax = 1 (mod m)
    ax - 1 = qm  (整数q)
    ax - mq = 1  -> (x, q)の解をextGCDで求める
    '''
    from math import gcd
    if gcd(a, m) != 1:
        raise Exception
    else:
        d, x, q = extGCD(a, -m)
    return x


'''
[ABC186 - E]
ax + by = c の一般解
 x = b't + x'
 y = -a't + y'
 (a' = a // d,
  b' = b // d,
  x', y': ax + by = gcd(a, b) の解の一つ)
'''

print(extGCD(111, 30))
print(inv_mod(3, 10))
