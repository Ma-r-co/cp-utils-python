N = 1  # 頂点の数
M = 1  # 辺の数

edge = [(1, 2, 11), (2, 3, 2)]  # 辺 (始点、終点、コスト)

path = [float('inf')] * N  # 頂点0からのコスト
path[0] = 0


# N - 1回更新を行う
# O(NM)
for i in range(N - 1):
    for j in range(M):
        a, b, c = edge[j]
        path[b] = min(path[b], path[a] + c)
