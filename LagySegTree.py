# operator.add(a, b)
# operator.mul(a, b)

"""
https://komiyam.hatenadiary.org/entry/20131202/1385992406
大雑把に言って、平衡二分探索木からinsert,delete,split,mergeなどができないよう制限したのがsegment treeで、
segment treeの区間[L,R)に対するクエリをL=0に制限したのがbinary indexed treeだと見なすことができます。

Lazyの実装はここを参考
https://tjkendev.github.io/procon-library/python/range_query/rmq_ruq_segment_tree_lp.html
"""


class LazySegmentTree():
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
        LV = (len(A) - 1).bit_length()
        n = 2 ** LV
        self.__LV = LV
        self.__n = n
        self.__dot = dot
        self.__e = e
        self.__node = [e] * (2 * n)
        self.__lazy = [None] * (2 * n)
        for i in range(len(A)):
            self.__node[i + n] = A[i]
        for i in range(n - 1, 0, -1):
            self.__node[i] = self.__dot(self.__node[2 * i], self.__node[2 * i + 1])

    def gindex(self, l, r):
        L = (l + self.__n) >> 1
        R = (r + self.__n) >> 1
        lc = 0 if l & 1 else (L & -L).bit_length()
        rc = 0 if r & 1 else (R & -R).bit_length()
        for i in range(self.__LV):
            if rc <= i:
                yield R
            if L < R and lc <= i:
                yield L
            L >>= 1; R >>= 1

    def propagates(self, *ids):
        lazy = self.__lazy
        node = self.__node
        for i in reversed(ids):
            v = lazy[i]
            if v is None:
                continue
            lazy[2 * i] = node[2 * i] = lazy[2 * i + 1] = node[2 * i + 1] = v
            lazy[i] = None

    def update(self, l, r, x):
        """
        区間[l, r)をxで更新
        """
        # i += self.__n
        # node = self.__node
        # node[i] = c
        # while i > 0:
        #     i //= 2
        #     node[i] = self.__dot(node[2 * i], node[2 * i + 1])
        *ids, = self.gindex(l, r)
        self.propagates(*ids)

        L = l + self.__n; R = r + self.__n
        lazy = self.__lazy
        node = self.__node
        while L < R:
            if R & 1:
                R -= 1
                lazy[R] = node[R] = x
            if L & 1:
                lazy[L] = node[L] = x
                L += 1
            L >>= 1; R >>= 1
        for i in ids:
            node[i] = self.__dot(node[2 * i], node[2 * i + 1])

    def get(self, l, r):
        self.propagates(*self.gindex(l, r))
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


# http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DSL_2_A
def AOJ_DSL_2_A():
    n, q = map(int, input().split())
    e = (1 << 31) - 1
    A = [e] * n
    seg = LazySegmentTree(A, min, e)

    for i in range(q):
        t, x, y = map(int, input().split())
        if t == 0:
            seg.update(x, x + 1, y)
        else:
            print(seg.get(x, y + 1))


# http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DSL_2_B
def AOJ_DSL_2_B():
    from operator import add
    import sys
    n, q = map(int, input().split())
    e = 0
    A = [e] * n
    seg = LazySegmentTree(A, add, e)

    query = sys.stdin.readlines()
    for i in range(q):
        t, x, y = map(int, query[i].split())
        x -= 1
        if t == 0:
            A[x] += y
            seg.update(x, x + 1, A[x])
        else:
            y -= 1
            print(seg.get(x, y + 1))


def ABC125_C():
    from fractions import gcd
    N = int(input())
    A = list(map(int, input().split()))

    seg = LazySegmentTree(A, gcd, 0)
    ans = 0
    for i in range(N):
        ans = max(ans, gcd(seg.get(0, i), seg.get(i + 1, N)))
    print(ans)


# AOJ_DSL_2_A()
AOJ_DSL_2_B()
# ABC125_C()
