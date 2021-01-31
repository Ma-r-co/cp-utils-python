def check_segment_intersection(A1, A2, B1, B2):
    ''' 線分A1A2と線分B1B2が交わるかどうか判定する
    (ABC016-D)
    '''
    ax1, ay1 = A1
    ax2, ay2 = A2
    bx1, by1 = B1
    bx2, by2 = B2
    L1 = (ay1 - ay2) * (bx1 - ax1) - (ax1 - ax2) * (by1 - ay1)
    L2 = (ay1 - ay2) * (bx2 - ax1) - (ax1 - ax2) * (by2 - ay1)
    R1 = (by1 - by2) * (ax1 - bx1) - (bx1 - bx2) * (ay1 - by1)
    R2 = (by1 - by2) * (ax2 - bx1) - (bx1 - bx2) * (ay2 - by1)
    return L1 * L2 <= 0 and R1 * R2 <= 0


def mul(S, sizeS, T, sizeT):
    ''' 行列積 S @ T を計算する
    S, T: 1次元行列
    sizeS, sizeT = [row, col]: row行, col列

    Sc == Tr 必須

    返値 = [Sr, Tc]の1次元行列
    '''
    Sr, Sc, Tr, Tc = *sizeS, *sizeT
    N = Sr * Tc
    ret = [0] * (N)
    for i in range(N):
        x, y = divmod(i, Tc)
        L = S[Sc * x: Sc * (x + 1)]
        R = [T[Tc * j + y] for j in range(Tr)]
        tmp = sum(a * b for a, b in zip(L, R))
        ret[i] = tmp
    return ret


A = (-1, 0, 5, 0, 1, 0, 0, 0, 1)
B = (3, 10, 1)
tmp = mul(A, (3, 3), B, (3, 1))
print(tmp)

'''
# θ度回転
    cosθ -sinθ
    sinθ cosθ

# 90度回転
    0 -1
    1 0
# 180度回転
    -1 0
    0  -1
# 270度回転
    0  1
    -1 0
# x軸反転 (y = 0 反転)
    1  0
    0 -1
# y軸反転 (x = 0 反転)
    -1 0
    0  1
# x = p 反転
    -1 0 2p | x
    0  1  0 | y
    0  0  1 | 1
# y = p 反転
    1  0  0 | x
    0 -1 2p | y
    0  0  1 | 1
'''
