"""
# 最小共通祖先 (Least Common Ancestor)

## 参考
https://ikatakos.com/pot/programming_algorithm/graph_theory/lowest_common_ancestor

## 考え方
求め方は複数のアルゴリズム・実装が知られているが、本プログラムでは Euler Tour + RMQ を使用する.
- Euler Tour + Range Minimum Query
- ダブリング
- Schieber-Vishkin algorithm

## 計算量
前処理 NlogN, クエリ logN

## 前提
RMQ部分はSegmentTreeを用いる
"""


class SegmentTree():
    def __init__(self, A, dot, e):
        n = 2 ** (len(A) - 1).bit_length()
        self.__n = n
        self.__dot = dot
        self.__e = e
        self.__node = [e] * (2 * n)
        for i in range(len(A)):
            self.__node[i + n] = A[i]
        for i in range(n - 1, 0, -1):
            self.__node[i] = self.__dot(self.__node[2 * i], self.__node[2 * i + 1])

    def get(self, l, r):
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


class LCA():
    import sys
    sys.setrecursionlimit(10 ** 6)
    
    def __init__(self, edge):
        """
        edge[頂点][移動可能な別頂点]の配列からLCAを求める.
            - eular_tour[i] = (d, v)
                i番目に通りかかる頂点の（深さ, 頂点番号）
            - first_appear[v] = i
                頂点vがeular_tour上で初めて現れるindex
        こうすると、頂点aとbのLCAは、以下で求められる。
            - それぞれが eular_tour 上ではじめて現れるindex pa,pb を取得する
                - pa < pb と仮定する
            - euler_tour上で、区間 [pa,pb] 内から、depthが最小となる頂点を取得する
            - そいつがLCAである（このような頂点はただ1つ存在する）
        """
        self.edge = edge
        self.N = len(edge)
        self.eular_tour = []
        self.first_appear = [None] * self.N
        self.rank = [-1] * self.N
        self.__dfs(0, 0)
        self.__construct_segtree(self.eular_tour, min, (self.N, self.N))
    
    def __dfs(self, d, v):
        self.rank[v] = d
        self.first_appear[v] = len(self.eular_tour)
        self.eular_tour.append((d, v))
        for nv in self.edge[v]:
            if self.rank[nv] < 0:
                self.__dfs(d + 1, nv)
                self.eular_tour.append((d, v))

    def __construct_segtree(self, E, dot, e):
        self.st = SegmentTree(E, dot, e)
    
    def get_lca(self, i, j):
        """頂点i, jのLCAおよびその深さを返す
        return d, v
         - d: 深さ, v: LCA
        """
        l = self.first_appear[i]
        r = self.first_appear[j]
        if l > r:
            l, r = r, l
        d, v = self.st.get(l, r + 1)
        return d, v

    def get_distance(self, i, j):
        """頂点i, j間の距離を返す
        return l
        """
        d, v = self.get_lca(i, j)
        di = self.rank[i]
        dj = self.rank[j]
        distance = abs(d - di) + abs(d - dj)
        return distance


def solve():
    """
    Verify: https://atcoder.jp/contests/abc014/tasks/abc014_4
    """
    N = int(input())
    edge = [[] for _ in range(N)]
    for _ in range(N - 1):
        x, y = map(int, input().split())
        edge[x - 1].append(y - 1)
        edge[y - 1].append(x - 1)
    Q = int(input())
    query = [tuple(map(lambda x: int(x) - 1, input().split())) for _ in range(Q)]

    lca = LCA(edge)
    for a, b in query:
        l = lca.get_distance(a, b)
        print(l + 1)


if __name__ == '__main__':
    solve()
