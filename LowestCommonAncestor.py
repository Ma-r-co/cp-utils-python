"""
# 最小共通祖先 (Lowest Common Ancestor)

## 参考
https://ikatakos.com/pot/programming_algorithm/graph_theory/lowest_common_ancestor
https://ei1333.github.io/luzhiled/snippets/tree/doubling-lowest-common-ancestor.html

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


class EulerTourLowestCommonAncestor():
    """Calculates LCA by Euler Tour

    Methods:
        get_lca(i, j)      : Returns LCA and its depth
        get_distance(i, j) : Returns distance btwn i <> j

    Notes:
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
    # import sys
    # sys.setrecursionlimit(10 ** 6)

    def __init__(self, edge, root):
        self.edge: list = edge
        self.N: int = len(edge)
        self.root: int = root
        self.eular_tour: list = []
        self.first_appear: list = [-1] * self.N
        self.rank: list = [-1] * self.N
        self.__go_eular_tour(root)
        # self.__go_eular_tour_dfs(0, root)
        self.__construct_segtree(self.eular_tour, min, (self.N, self.N))

    def __go_eular_tour(self, root):
        self.parent: list = [-1] * self.N
        # self.child: list = [[] for _ in range(self.N)]
        self.parent[root] = root
        self.rank[root] = 0
        q = [root]
        while q:
            v = q.pop()
            d = self.rank[v]
            if self.first_appear[v] == -1:
                if v != root:
                    q.append(self.parent[v])
                self.first_appear[v] = len(self.eular_tour)
                for nv in self.edge[v]:
                    if self.rank[nv] < 0:
                        self.parent[nv] = v
                        # self.child[v].append(nv)
                        self.rank[nv] = d + 1
                        q.append(nv)
            self.eular_tour.append((d, v))

    def __go_eular_tour_dfs(self, d, v):
        # self.parent: list = [-1] * self.N
        # self.child: list = [[] for _ in range(self.N)]
        self.rank[v] = d
        self.first_appear[v] = len(self.eular_tour)
        self.eular_tour.append((d, v))
        for nv in self.edge[v]:
            if self.rank[nv] < 0:
                # self.parent[nv] = v
                # self.child[v].append(nv)
                self.__go_eular_tour_dfs(d + 1, nv)
                self.eular_tour.append((d, v))

    def __construct_segtree(self, E, dot, e):
        self.st = SegmentTree(E, dot, e)

    def get_lca(self, i: int, j: int):
        """Returns LCA and its rank

        Args:
            i (int): Vertex
            j (int): Vertex

        Returns:
            int: LCA
            int: Rank of LCA
        """
        l = self.first_appear[i]
        r = self.first_appear[j]
        if l > r:
            l, r = r, l
        d, v = self.st.get(l, r + 1)
        return v, d

    def get_distance(self, i: int, j: int):
        """Returns distance btwn i <> j

        Args:
            i (int): vertex
            j (int): vertex

        Returns:
            int: Distance btwn i <> j
        """
        v, d = self.get_lca(i, j)
        di = self.rank[i]
        dj = self.rank[j]
        distance = abs(d - di) + abs(d - dj)
        return distance


def solve():
    from random import randint
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

    root = randint(0, N - 1)
    lca = EulerTourLowestCommonAncestor(edge, root)
    for a, b in query:
        l = lca.get_distance(a, b)
        print(l + 1)


if __name__ == '__main__':
    solve()
