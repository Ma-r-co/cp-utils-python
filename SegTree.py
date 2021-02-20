# operator.add(a, b)
# operator.mul(a, b)

"""
https://komiyam.hatenadiary.org/entry/20131202/1385992406
大雑把に言って、平衡二分探索木からinsert,delete,split,mergeなどができないよう制限したのがsegment treeで、
segment treeの区間[L,R)に対するクエリをL=0に制限したのがbinary indexed treeだと見なすことができます。
"""
"""
N = 2 のときは使えない！！
get(x, N + 1)の処理で index out of range エラーとなる(ABC047-D) ??
"""


class SegmentTree():
    """
    update, get を提供するSegmentTree

    Attributes
    ----------
    __n : int
        葉の数。2 ^ i - 1
    __dot :
        Segment function
    __e: int
        単位元
    __node: list
        Segment Tree
    """

    def __init__(self, A, dot, e):
        """
        Parameters
        ----------
        A : list
            対象の配列
        dot :
            Segment function
        e : int
            単位元
        """
        n = 2 ** (len(A) - 1).bit_length()
        self.__n = n
        self.__dot = dot
        self.__e = e
        self.__node = [e] * (2 * n)
        for i in range(len(A)):
            self.__node[i + n] = A[i]
        for i in range(n - 1, 0, -1):
            self.__node[i] = self.__dot(self.__node[2 * i], self.__node[2 * i + 1])

    def update(self, i, c):
        i += self.__n
        node = self.__node
        if node[i] == c:
            return
        node[i] = c
        while i > 1:
            i //= 2
            node[i] = self.__dot(node[2 * i], node[2 * i + 1])

    def get(self, l, r):
        """
        区間[l, r)での値を返す. 0-index.
        """
        vl, vr = self.__e, self.__e
        l += self.__n
        r += self.__n
        while (l < r):
            if l & 1:
                vl = self.__dot(vl, self.__node[l])
                l += 1
            l //= 2
            if r & 1:
                r -= 1
                vr = self.__dot(vr, self.__node[r])
            r //= 2
        return self.__dot(vl, vr)

    def node(self, i):
        '''node[i]を返す(0-index)
        '''
        return self.__node[i + self.__n]


# http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DSL_2_A
def AOJ_DSL_2_A():
    n, q = map(int, input().split())
    e = (1 << 31) - 1
    A = [e] * n
    seg = SegmentTree(A, min, e)

    for i in range(q):
        t, x, y = map(int, input().split())
        if t == 0:
            seg.update(x, y)
        else:
            print(seg.get(x, y + 1))


# http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DSL_2_B
def AOJ_DSL_2_B():
    from operator import add
    import sys
    n, q = map(int, input().split())
    e = 0
    A = [e] * n
    seg = SegmentTree(A, add, e)

    query = sys.stdin.readlines()
    for i in range(q):
        t, x, y = map(int, query[i].split())
        x -= 1
        if t == 0:
            A[x] += y
            seg.update(x, A[x])
        else:
            y -= 1
            print(seg.get(x, y + 1))


def ABC125_C():
    from fractions import gcd
    N = int(input())
    A = list(map(int, input().split()))

    seg = SegmentTree(A, gcd, 0)
    ans = 0
    for i in range(N):
        ans = max(ans, gcd(seg.get(0, i), seg.get(i + 1, N)))
    print(ans)


# AOJ_DSL_2_A()
AOJ_DSL_2_B()
# ABC125_C()
