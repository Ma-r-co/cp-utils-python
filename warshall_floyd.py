# dp[i][j] は辺(i, j)のコスト

N = 10  # Nodes
INF = 10 ** 6

dp = [[INF] * N for _ in range(N)]
for i in range(N):
    dp[i][i] = 0

for k in range(N):
    for i in range(N):
        for j in range(N):
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])
