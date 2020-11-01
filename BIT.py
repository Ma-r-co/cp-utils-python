class BinaryIndexedTree():
    '''
    1-indexed
    '''
    def __init__(self, A):
        self.__n = len(A)
        self.__node = [0] * (self.__n + 1)
        self.__data = [0] * (self.__n + 1)

        S = [0] * (self.__n + 1)
        for i in range(self.__n):
            S[i + 1] = S[i] + A[i]

        for i in range(1, self.__n + 1):
            self.__data[i] = A[i - 1]
            self.__node[i] = S[i] - S[i - (i & -i)]

    def add(self, i, v):
        self.__data[i] += v
        while i <= self.__n:
            self.__node[i] += v
            i += i & -i

    def sum(self, i):
        ''' [1, i]の和
        '''
        rst = 0
        while i > 0:
            rst += self.__node[i]
            i -= i & -i
        return rst
    
    def get(self, i, j):
        '''[i, j]の和
        '''
        if i == j:
            return self.__data[i]
        else:
            return self.sum(j) - self.sum(i - 1)
