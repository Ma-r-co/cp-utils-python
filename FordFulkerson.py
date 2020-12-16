class FordFulkerson():
    '''
    フローネットワークにおける最大フローを求めるアルゴリズム
    '''
    def __init__(self, N: int, E: list):
        '''
        N: 頂点の数
        E: 有向辺のリスト, (from, to, capacity)

        G: 有向グラフの隣接リスト表現, (to, capacity, rev)
            ※rev: 逆辺が保存されているG[to]での番地
        '''
        self.N = N
        self.G = [[] for _ in range(self.N)]
        for f, t, c in E:
            # from から to への容量 cap の辺とその逆辺をグラフ G に追加する．
            # 辺 e の逆辺は G[e.to] の rev 番目に追加される．
            # G[e.to][e.rev] = 辺 e の逆辺.
            self.G[f].append([t, c, len(self.G[t])])
            self.G[t].append([f, 0, len(self.G[f]) - 1])

    def flow_dfs(self, s, g, mincap):
        '''
        s から g へのパスを DFS で探し，そのパスに流せる最大流量を返す．
        mincap = 通った辺の中の最少容量
        '''
        if s == g:
            return mincap
        self.used[s] = 1
        for i, (to, cap, rev) in enumerate(self.G[s]):
            if self.used[to] == 0 and cap > 0:
                d = self.flow_dfs(to, g, min(mincap, cap))
                if d > 0:
                    self.G[s][i][1] -= d
                    self.G[to][rev][1] += d
                    return d
        return 0

    def solve_max_flow(self, s, t):
        '''s(source)からt(sink)への最大フローを算出する
        '''
        flow = 0
        INF = float('inf')
        while True:
            self.used = [0] * self.N
            f = self.flow_dfs(s, t, INF)
            if f == 0:
                return flow
            flow += f
