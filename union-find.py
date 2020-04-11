# http://b1u3.hateblo.jp/entry/2019/11/19/192551


class UnionFind():
    def __init__(self, n):
        self.parents = [-1] * n

    def find(self, x):
        if self.parents[x] < 0:
            return x
        else:
            self.parents[x] = self.find(self.parents[x])
            return self.parents[x]

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return

        if self.parents[x] > self.parents[y]:
            x, y = y, x

        self.parents[x] += self.parents[y]
        self.parents[y] = x


class WeightedUnionFind():
    def __init__(self, n):
        self.parents = [-1] * n
        self.par_weight = [0] * n

    def find(self, x):
        if self.parents[x] < 0:
            return x
        else:
            root = self.find(self.parents[x])
            self.par_weight[x] += self.par_weight[self.parents[x]]
            self.parents[x] = root
            return self.parents[x]

    def union(self, x, y, w):
        w = w + self.weight(x) - self.weight(y)
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return

        if self.parents[x] > self.parents[y]:
            self.parents[y] += self.parents[x]
            self.parents[x] = y
            self.par_weight[x] = -w
        else:
            self.parents[x] += self.parents[y]
            self.parents[y] = x
            self.par_weight[y] = w

    def weight(self, x):
        if self.parents[x] < 0:
            return 0
        else:
            return self.par_weight[x] + self.weight(self.parents[x])

    def diff(self, x, y):
        if self.find(x) != self.find(y):
            raise Exception('"{}" belongs to a different tree from "{}"'.format(x, y))
        return self.weight(y) - self.weight(x)


ufb = WeightedUnionFind(4)
print(ufb.parents)
print(ufb.par_weight)
print('')
ufb.union(1 - 1, 2 - 1, -3)
print(ufb.parents)
print(ufb.par_weight)
print('')
ufb.union(3 - 1, 4 - 1, 2)
print(ufb.parents)
print(ufb.par_weight)
print('')
ufb.union(0, 2, 4)
print(ufb.parents)
print(ufb.par_weight)
print('')
# ufb.union(1, 2)
# print(ufb.parents)
# print('')
# ufb.union(0, 4)
# print(ufb.parents)
