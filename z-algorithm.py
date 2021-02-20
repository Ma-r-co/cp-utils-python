S = 'strangeorange'


def z_algo(S):
    '''
    文字列が与えられた時、各 i について「S と S[i:|S|-1] の最長共通接頭辞の長さ」を記録した配列 A を O(|S|) で構築するアルゴリズムです。

    ex)
    aaabaaaab
    921034210

    ex) 文字列TのなかにパターンSが存在するかどうか？
    P = 'aab'
    T = 'baabaa'
    S = P+'$'+T
    z_array_for_S = [x, 1, 0, 0, 0, 3, 1, 0, 2, 1]
    # 3 が存在するためこの部分でPに一致している
    '''
    N = len(S)

    A = [0] * N
    A[0] = N
    i = 1
    j = 0

    while i < N:
        while i + j < N and S[j] == S[i + j]:
            j += 1
        if not j:
            i += 1
            continue
        A[i] = j
        k = 1
        while N - i > k < j - A[k]:
            A[i + k] = A[k]
            k += 1
        i += k
        j -= k
    return A


for i in range(len(S)):
    print("{}: {}".format(S[i:], z_algo(S[i:])))
