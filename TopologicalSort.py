class TopologicalSort():
    """グラフをトポロジカル・ソートするためのクラス

    Methods:
        solve_dfs(): DFSによりトポロジカルソートを行い、ソートされた頂点のリストを返す
        solve_bfs(): BFSによりトポロジカルソートを行う、ソートされた頂点のリストを返す
    """

    def __init__(self, N: int, edge: list):
        """
        Args:
            N (int): 頂点の数
            edge (list): 有向辺の隣接リスト. len(edge) == N
        """
        self.N = N
        self.edge = edge

    def solve_dfs(self):
        """
        Returns:
            bool: グラフがループかどうか
            list: トポロジカル・ソートされた頂点のリスト
        """
        import sys
        sys.setrecursionlimit(10 ** 6)
        N = self.N
        path = self.path = [0] * N
        ret = self.ret = [] * N
        isLoop = False
        for i in range(N):
            if path[i] == 0:
                path[i] = 1
                isLoop |= self._dfs(i)
        ret.reverse()
        return isLoop, ret

    def _dfs(self, v):
        edge, path, ret = self.edge, self.path, self.ret
        isLoop = False
        for nv in edge[v]:
            if path[nv] == 0:
                path[nv] = 1
                isLoop |= self._dfs(nv)
            elif path[nv] == 1:
                isLoop = True
        ret.append(v)
        path[v] = 2
        return isLoop

    def solve_bfs(self):
        """
        Returns:
            bool: グラフがループかどうか
            list: トポロジカル・ソートされた頂点のリスト
        """
        from collections import deque
        N, edge = self.N, self.edge
        ret = self.ret = []
        rank = [0] * N
        for i in range(N):
            for j in edge[i]:
                rank[j] += 1
        q = deque(i for i in range(N) if rank[i] == 0)
        while q:
            v = q.popleft()
            ret.append(v)
            for nv in edge[v]:
                rank[nv] -= 1
                if rank[nv] == 0:
                    q.append(nv)
        isLoop = len(ret) != N
        return isLoop, ret


def validate():
    """ABC139-E
    https://atcoder.jp/contests/abc139/tasks/abc139_e
    """
    def match(i, j, N):
        if i > j:
            i, j = j, i
        return i * N + j

    N = int(input())
    M = N ** 2
    edge = [[] for _ in range(M)]
    for i in range(N):
        A = list(map(lambda x: int(x) - 1, input().split()))
        for j in range(N - 2):
            s, t = match(i, A[j], N), match(i, A[j + 1], N)
            edge[s].append(t)

    ts = TopologicalSort(M, edge)
    isLoop, order = ts.solve_bfs()
    # isLoop, order = ts.solve_dfs()
    if isLoop:
        print(-1)
    else:
        idx = [0] * M
        for i, v in enumerate(order):
            idx[v] = i
        dp = [1] * len(order)
        for i in range(len(order)):
            here = dp[i]
            v = order[i]
            for nv in edge[v]:
                j = idx[nv]
                dp[j] = max(dp[j], here + 1)
        print(max(dp))


validate()
