from collections import Counter


# 素因数分解: Counter({prime: count})
def factorization(n):
    from collections import Counter
    arr = Counter()
    temp = n
    for i in range(2, int(-(-n**0.5 // 1)) + 1):
        if temp % i == 0:
            cnt = 0
            while temp % i == 0:
                cnt += 1
                temp //= i
            arr[i] = cnt

    if temp != 1:
        arr[temp] = 1

    if len(arr.keys()) == 0 and n != 1:
        arr[n] = 1

    return arr


# print(factorization(32400))


def prime_factor_table(n):
    table = [0] * (n + 1)

    for i in range(2, n + 1):
        if table[i] == 0:
            for j in range(i + i, n + 1, i):
                table[j] = i

    return table


def prime_factor(n, prime_factor_table):
    prime_count = Counter()

    while prime_factor_table[n] != 0:
        prime_count[prime_factor_table[n]] += 1
        n //= prime_factor_table[n]
    prime_count[n] += 1

    return prime_count


# すべての約数 (1含む)
def f1(n):
    divs = []
    for i in range(1, int(n ** 0.5) + 1):  # range(n, int(n ** 0.5) - 1, -1)とすると非常に遅い！！
        if n % i == 0:
            divs.append(i)
            j = n // i
            if i != j:
                divs.append(j)
    return divs


# エラトステネスの篩
# def sieve(n):
#     is_prime = [1 for _ in range(n + 1)]
#     is_prime[0] = 0
#     is_prime[1] = 0

#     for i in range(2, n + 1):
#         if is_prime[i]:
#             j = i + i
#             while j <= n:
#                 is_prime[j] = 0
#                 j += i

#     return is_prime
def create_sieve(n):
    sieve = [0] * (n + 1)

    for i in range(2, n + 1):
        if sieve[i] == 0:
            j = i ** 2
            while j <= n:
                sieve[j] = i
                j += i

    return sieve


# 高速素因数分解: Counter({prime: count})
def fast_factorization(n, sieve):
    from collections import Counter
    arr = Counter()
    while n > 1:
        p = sieve[n]
        if p == 0:
            arr[n] += 1
            break
        else:
            arr[p] += 1
            n //= p
    return arr
