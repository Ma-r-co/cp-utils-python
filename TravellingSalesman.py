class TravellingSalesman():
    '''
    巡回セールスマン問題を解くクラス

    solve_roundtrip(start)：
        startから出発してすべての都市を周りstartに帰ってくるまでの最小コスト
    solve_oneway(start):
        startから出発してすべての都市を周るまでの最小コスト
    '''

    def __init__(self, N: int, dist: list):
        '''
        N: 都市の数
        dist[i][j]: 都市i-->都市jのコスト
        '''
        self.N: int = N
        self.dist: list = dist
        self.oneway_answer: list = [-1] * N
        self.roundtrip_answer: list = [-1] * N

    def solve_oneway(self, start: int):
        if self.oneway_answer[start] == -1:
            self._solve_oneway()
        return self.oneway_answer[start]

    def _solve_oneway(self):
        INF = float('inf')
        N = self.N
        dp = [[INF] * (1 << N) for _ in range(N)]
        # dp[i][S]: 現在都市iにいて残り都市S(0:未訪問, 1:訪問済)をすべて周るときの最小コスト
        dist = self.dist
        for i in range(N):
            dp[i][-1] = 0
        for S in range((1 << N) - 1, -1, -1):
            nxt = [j for j in range(N) if (S >> j) & 1]
            for i in range(N):
                here = dp[i][S]
                for j in nxt:
                    nS = S & ~(1 << j)
                    dp[j][nS] = min(dp[j][nS], here + dist[j][i])  # 注意: j -> i へ移動すると考える
        for i in range(N):
            self.oneway_answer[i] = dp[i][0]

    def solve_roundtrip(self, start: int):
        if self.roundtrip_answer[start] == -1:
            self._solve_roundtrip(start)
        return self.roundtrip_answer[start]

    def _solve_roundtrip(self, start: int):
        INF = float('inf')
        N = self.N
        dp = [[INF] * (1 << N) for _ in range(N)]
        # dp[i][S]: 現在都市iにいて残り都市S(0:未訪問, 1:訪問済)をすべて周ってstartに帰るときの最小コスト
        dist = self.dist
        for i in range(N):
            dp[i][-1] = dist[i][start]
        for S in range((1 << N) - 1, -1, -1):
            nxt = [j for j in range(N) if (S >> j) & 1]
            for i in range(N):
                here = dp[i][S]
                for j in nxt:
                    nS = S & ~(1 << j)
                    dp[j][nS] = min(dp[j][nS], here + dist[j][i])  # 注意: j -> i へ移動すると考える
        self.roundtrip_answer[start] = dp[start][0]


# -------------------------------------------------------------------
'''
Validation - solve_oneway
ABC190-E
'''


def solve_ABC190_E():
    import sys
    from collections import deque
    import random
    random.seed()

    N, M = map(int, input().split())
    order = [i for i in range(N)]
    random.shuffle(order)
    cond = [tuple(map(lambda x: order[int(x) - 1], sys.stdin.readline().split())) for _ in range(M)]
    edge = [[] for _ in range(N)]
    for a, b in cond:
        edge[a].append(b)
        edge[b].append(a)
    K = int(input())
    C = list(map(lambda x: order[int(x) - 1], input().split()))

    Cidx = {}  # 頂点Ci の配列C内でのindexを返す
    for i, c in enumerate(C):
        Cidx[c] = i

    # まずは頂点Ci <> Cj の2点間距離を全て求める。
    # 各頂点からBFSを実施する
    INF = float('inf')
    dist = [[INF] * K for _ in range(K)]  # dist[i][j]: Ci<>Cjの距離
    for i, c in enumerate(C):
        path = [-1] * N
        q = deque()
        q.append((0, c))
        while q:
            s, v = q.popleft()
            if path[v] == -1:
                path[v] = s
                if v in Cidx:
                    dist[i][Cidx[v]] = dist[Cidx[v]][i] = s
                ns = s + 1
                for nv in edge[v]:
                    q.append((ns, nv))

    ts = TravellingSalesman(K, dist)
    cnt = INF
    for i in random.sample(range(K), K):
        cnt = min(cnt, ts.solve_oneway(i))
    ans = cnt + 1 if cnt < (1 << 64) else -1
    print(ans)


# -------------------------------------------------------------------
'''
Validation - solve_roundtrip
ABC180-E
'''


def solve_ABC180_E():
    import random
    random.seed()

    def calc_dist(S, G):
        a, b, c = S
        p, q, r = G
        return abs(p - a) + abs(q - b) + max(0, r - c)

    N = int(input())
    city0 = tuple(map(int, input().split()))
    city = [tuple(map(int, input().split())) for _ in range(N - 1)]
    idx = random.randint(0, N - 1)
    random.shuffle(city)
    city.insert(idx, city0)

    dist = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            dist[i][j] = calc_dist(city[i], city[j])

    ts = TravellingSalesman(N, dist)

    print(ts.solve_roundtrip(idx))


# -------------------------------------------------------------------
solve_ABC190_E()
# solve_ABC180_E()
