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

