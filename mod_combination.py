MOD = 10 ** 9 + 7


def modFact(n):
    global MOD
    if n == 1:
        return 1
    else:
        return (n * modFact(n - 1)) % MOD


def modInvFact(n):
    global MOD
    ans = 1
    for i in range(1, n + 1):
        ans *= pow(i, MOD - 2, MOD)
        ans %= MOD
    return ans


def modCombi(n, r):
    global MOD
    if r == 0:
        return 1
    else:
        N = modFact(n)
        NR = modInvFact(n - r)
        R = modInvFact(r)
    return (N * R * NR) % MOD


# -----------
MOD = 10 ** 9 + 7


def prepare(n):
    global MOD
    modFacts = [0] * (n + 1)
    modFacts[0] = 1
    for i in range(n):
        modFacts[i + 1] = (modFacts[i] * (i + 1)) % MOD

    invs = [1] * (n + 1)
    invs[n] = pow(modFacts[n], MOD - 2, MOD)
    for i in range(n, 1, -1):
        invs[i - 1] = (invs[i] * i) % MOD

    return modFacts, invs


def comb(n, r):
    global MOD, modFacts, invs
    return (modFacts[n] * invs[n - r] * invs[r]) % MOD


def perm(n, r):
    global MOD, modFacts, invs
    return (modFacts[n] * invs[n - r]) % MOD
