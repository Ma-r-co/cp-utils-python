def solve(n):
    pass


# [ok, ng) - Maximum
# (ng, ok] - Minimum
# ok が 最終的な答え
ok = 0
ng = 0
while abs(ok - ng) > 1:
    mid = (ok + ng) // 2
    if solve(mid):
        ok = mid
    else:
        ng = mid
