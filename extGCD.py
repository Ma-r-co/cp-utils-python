import typing


def extGCD(a: int, b: int) -> typing.Tuple[int, int, int]:
    '''ax + by = gcd(a, b) を満たす整数解x, yを求める

    Returns:
        gcd(a, b), x, y

    Reference:
        https://qiita.com/akebono-san/items/f00c0db99342a8d68e5d
    '''

    x, y, u, v = 1, 0, 0, 1  # 単位行列
    p, q = a, b
    while q:
        k = p // q
        x -= k * u
        y -= k * v
        x, u = u, x
        y, v = v, y
        p, q = q, p % q
    return x * a + y * b, x, y


def inv_mod(a: int, m: int) -> int:
    '''法 m の元での a の逆元を求める

    Constraints:
        m と a は互いに素

    Returns:
        x (int): 法 m の元での a の逆元
        ※ m と a が互いに素でない場合は-1を返す

    Notes:
        ax = 1 (mod m)
        ax = 1 + -qm  (整数q)
        ax + mq = 1  -> (x, q)の解をextGCDで求める
    '''
    d, x, q = extGCD(a, m)
    x %= m
    if x < 0:
        x -= m
    return x if d == 1 or d == -1 else -1


def _crt_pair(b1: int, m1: int, b2: int, m2: int) -> typing.Tuple[int, int]:
    """以下の連立合同式を満たす最小の非負整数 r を求める
        r = b1 (mod m1)
        r = b2 (mod m2)

    Args:
        b1 (int): r = b1 (mod m1)
        m1 (int):
        b2 (int): r = b2 (mod m2)
        m2 (int):

    Returns:
        typing.Tuple[int, int]: R, M (0 <= R < M, M = gcd(m1, m2))を返す。解が存在しないとき(0, -1)を返す。

    Notes:
        > m1x + m2y = d  (d = gcd(m1, m2)) を満たすx, yを求める
        > r = b1 + m1 * x * ((b2 - b1) // d)
        > (b2 - b1) % d != 0 のとき解は存在しない

    """
    d, x, y = extGCD(m1, m2)
    if (b2 - b1) % d != 0:
        R, M = 0, -1
    else:
        c = (b2 - b1) // d
        M = (m1 * m2) // d
        R = (m1 * x * c + b1) % M
    return R, M


def crt(b: typing.List[int], m: typing.List[int]) -> typing.Tuple[int, int]:
    """連立合同式を満たす最小の非負整数 r を求める
        r = b1 (mod m1)
        r = b2 (mod m2)
        ...
        r = bn (mod mn)

    Args:
        b (typing.List[int]): r = bi (mod mi)
        m (typing.List[int]): r = bi (mod mi)

    Returns:
        typing.Tuple[int, int]: R, M (0 <= R < M, M = gcd(m1, m2))を返す。解が存在しないとき(0, -1)を返す。

    Reference:
        https://qiita.com/drken/items/ae02240cd1f8edfc86fd#%E5%95%8F%E9%A1%8C-2yukicoder-0187-%E4%B8%AD%E8%8F%AF%E9%A2%A8-hard

    Notes:
        > R = 0 (mod 1) (-> 任意の整数) を初期値として、順に_crt_pairを適用していく
    """
    N = len(b)
    assert len(m) == N, '!Size of arguments b and m must be equal!'

    R, M = 0, 1
    for i in range(N):
        R, M = _crt_pair(R, M, b[i], m[i])
        if M == -1:
            break
    return R, M


'''
[ABC186 - E]
ax + by = c の一般解
 x = b't + c'x'
 y = -a't + c'y'
 (a' = a // d,
  b' = b // d,
  c' = c // d,
  x', y': ax + by = gcd(a, b) の解の一つ)
'''


def validate_inv_mod():
    '''ABC186-E
    https://atcoder.jp/contests/abc186/tasks/abc186_e
    '''
    from math import gcd
    T = int(input())
    query = [tuple(map(int, input().split())) for _ in range(T)]
    for N, S, K in query:
        d = gcd(N, gcd(S, K))
        A, B, M = K // d, S // d, N // d
        x = inv_mod(A, M)
        if x == -1:
            print(-1)
        else:
            print((-B * x) % M)


def validate_crt():
    '''ABC193-E
    https://atcoder.jp/contests/abc193/tasks/abc193_e
    '''
    INF = (1 << 64)
    T = int(input())
    case = [tuple(map(int, input().split())) for _ in range(T)]
    for X, Y, P, Q in case:
        Z = 2 * (X + Y)
        R = P + Q
        ans = INF
        for i in range(X, X + Y):
            for j in range(P, P + Q):
                r, m = crt([i, j], [Z, R])
                if m >= 0:
                    ans = min(ans, r)
        print(ans if ans < INF else 'infinity')


def validate_crt_2():
    """yukicoder No.186
    https://yukicoder.me/problems/no/186
    """
    X = [0] * 3
    Y = [0] * 3
    for i in range(3):
        X[i], Y[i] = map(int, input().split())
    r, m = crt(X, Y)
    if m == -1:
        print(-1)
    else:
        print(r if r > 0 else m)


# validate_inv_mod()
# validate_crt()
validate_crt_2()
