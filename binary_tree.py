class Node: # ノードの型
    def __init__(self, height, key, x):
        self.height = height # そのノードを根とする部分木の高さ
        self.key    = key    # そのノードのキー
        self.value  = x      # そのノードの値
        self.lst    = None   # 左部分木
        self.rst    = None   # 右部分木

# 部分木 t の高さを返す
def height(t): return 0 if t is None else t.height

# 左右の部分木の高さの差を返す。左が高いと正、右が高いと負
def bias(t): return height(t.lst) - height(t.rst)

# 左右の部分木の高さから、その木の高さを計算して修正する
def modHeight(t): t.height = 1 + max(height(t.lst), height(t.rst))

def rotateL(v): # ２分探索木 v の左回転。回転した木を返す
    u = v.rst; t2 = u.lst
    u.lst = v; v.rst = t2
    modHeight(u.lst)
    modHeight(u)
    return u
def rotateR(u): # ２分探索木 u の右回転。回転した木を返す
    v = u.lst; t2 = v.rst
    v.rst = u; u.lst = t2
    modHeight(v.rst)
    modHeight(v)
    return v
def rotateLR(t): # ２分探索木 t の二重回転(左回転 -> 右回転)。回転した木を返す
    t.lst = rotateL(t.lst)
    return rotateR(t)
def rotateRL(t): # ２分探索木 t の二重回転(右回転 -> 左回転)。回転した木を返す
    t.rst = rotateR(t.rst)
    return rotateL(t)

###############################################################################
# AVL木マップクラス
###############################################################################

class AVLMap:
    def __init__(self):
        self.root   = None  # AVL木の根。Node 型
        self.change = False # 修正が必要かを示すフラグ(True:必要, False:不要)
        self.lmax   = None  # 左部分木のキーの最大値
        self.value  = None  # lmax に対応する値

    ###########################################################################
    # バランス回復
    ###########################################################################

    # 挿入時の修正(balanceLi:左部分木への挿入, balanceRi:右部分木への挿入)
    def balanceLi(self, t): return self.balanceL(t)
    def balanceRi(self, t): return self.balanceR(t)

    # 削除時の修正(balanceLd:左部分木での削除, balanceRd:右部分木での削除)
    def balanceLd(self, t): return self.balanceR(t)
    def balanceRd(self, t): return self.balanceL(t)

    # 部分木 t のバランスを回復して戻り値で返す
    # 左部分木への挿入に伴うAVL木の修正
    # 右部分木での削除に伴うAVL木の修正
    def balanceL(self, t):
        if not self.change: return t
        h = height(t)
        if bias(t) == 2:
            if bias(t.lst) >= 0:
                t = rotateR(t)
            else:
                t = rotateLR(t)
        else: modHeight(t)
        self.change = (h != height(t))
        return t

    # 部分木 t のバランスを回復して戻り値で返す
    # 右部分木への挿入に伴うAVL木の修正
    # 左部分木での削除に伴うAVL木の修正
    def balanceR(self, t):
        if not self.change: return t
        h = height(t)
        if bias(t) == -2:
            if bias(t.rst) <= 0:
                t = rotateL(t)
            else:
                t = rotateRL(t)
        else: modHeight(t)
        self.change = (h != height(t))
        return t

    ###########################################################################
    # insert(挿入)
    ###########################################################################

    # エントリー(key, x のペア)を挿入する
    def insert(self, key, x): self.root = self.insert_sub(self.root, key, x)

    def insert_sub(self, t, key, x):
        if t is None:
            self.change = True
            return Node(1, key, x)
        elif key < t.key:
            t.lst = self.insert_sub(t.lst, key, x)
            return self.balanceLi(t)
        elif key > t.key:
            t.rst = self.insert_sub(t.rst, key, x)
            return self.balanceRi(t)
        else:
            self.change = False
            t.value = x
            return t

    ###########################################################################
    # delete(削除)
    ###########################################################################

    # key で指すエントリー(ノード)を削除する
    def delete(self, key): self.root = self.delete_sub(self.root, key)

    def delete_sub(self, t, key):
        if t is None:
            self.change = False
            return None
        elif key < t.key:
            t.lst = self.delete_sub(t.lst, key)
            return self.balanceLd(t)
        elif key > t.key:
            t.rst = self.delete_sub(t.rst, key)
            return self.balanceRd(t)
        else:
            if t.lst is None:
                self.change = True
                return t.rst # 右部分木を昇格させる
            else:
                t.lst = self.delete_max(t.lst) # 左部分木の最大値を削除する
                t.key = self.lmax # 左部分木の削除した最大値で置き換える
                t.value = self.value
                return self.balanceLd(t)

    # 部分木 t の最大値のノードを削除する
    # 戻り値は削除により修正された部分木
    # 削除した最大値を lmax に保存する
    def delete_max(self, t):
        if t.rst is not None:
            t.rst = self.delete_max(t.rst)
            return self.balanceRd(t)
        else:
            self.change = True
            self.lmax = t.key # 部分木のキーの最大値を保存
            self.value = t.value
            return t.lst # 左部分木を昇格させる

    ###########################################################################
    # member(検索)等
    ###########################################################################

    # キーの検索。ヒットすれば True、しなければ False
    def member(self, key):
        t = self.root
        while t is not None:
            if key < t.key:
                t = t.lst
            elif key > t.key:
                t = t.rst
            else:
                return True
        return False

    # キーから値を得る。キーがヒットしない場合は None を返す
    def lookup(self, key):
        t = self.root
        while t is not None:
            if key < t.key:
                t = t.lst
            elif key > t.key:
                t = t.rst
            else:
                return t.value
        return None

    # マップが空なら True、空でないなら False
    def isEmpty(self): return self.root is None

    # マップを空にする
    def clear(self): self.root = None

    # キーのリスト
    def keys(self): return keys_sub(self.root)

    # 値のリスト
    def values(self): return values_sub(self.root)

    # エントリーのリスト
    def items(self): return items_sub(self.root)

    # マップのサイズ
    def size(self): return len(self.keys())

    def __contains__(self, key): self.member(key)
    def __getitem__(self, key): return self.lookup(key)
    def __setitem__(self, key, x): return self.insert(key, x)
    def __delitem__(self, key): self.delete(key)
    def __bool__(self): return not self.isEmpty()
    def __len__(self): return self.size()
    def __iter__(self): return iter(self.keys())



###########################################################################
class Node:
    """
    https://qiita.com/amb_00/items/ee26260fa186a5c728a0

    print("\n(6の)次節点")
    print(r.search(6).successor())  # 7

    print("\n(6の)前節点")
    print(r.search(6).predecessor())  # 4

    """

    def __init__(self, key, parent=None, left=None, right=None):
        self.key = key
        self.p = parent
        self.left = left
        self.right = right

    def __repr__(self):
        return 'Node(%s)' % repr(self.key)

    # 探索
    def search(self, k):
        if self is None or k == self.key:
            return self
        if k < self.key:
            return self.left.search(k)
        else:
            return self.right.search(k)

    # 最小値
    def minimum(self):
        while self.left:
            self = self.left
        return self

    # 最大値
    def maximum(self):
        while self.right:
            self = self.right
        return self

    # 次節点
    def successor(self):
        if self.right:
            return self.right.minimum()
        y = self.p
        while y and self == y.right:
            self = y
            y = y.p
        return y

    # 前節点
    def predecessor(self):
        if self.left:
            return self.left.maximum()
        y = self.p
        while y and self == y.left:
            self = y
            y = y.p
        return y

    # 二分探索木のルートを返すメソッド
    def root(self):
        while self.p:
            self = self.p
        return self

    # 挿入
    def insert(self, value):
        z = Node(value)
        y = None
        self = self.root()
        while self:
            y = self
            if z.key < self.key:
                self = self.left
            else:
                self = self.right
        z.p = y
        if y is None:
            pass
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

    # 節点(自分)を削除して、子の節点に差し替えるメソッド(deleteメソッドの一部)
    def transparent(self, v):  # selfは削除される節点、vは差し替える節点
        if self.p is None:
            pass
        elif self == self.p.left:  # 節点が親の左部分木に属する場合
            self.p.left = v
        else:  # 節点が親の右部分木に属する場合
            self.p.right = v
        if v:
            v.p = self.p

    # 削除
    def delete(self):
        if self.left is None:  # 右の子のみを持つ場合
            y = self.right
            self.transparent(y)
        elif self.right is None:  # 左の子のみを持つ場合
            y = self.left
            self.transparent(y)
        else:  # 子を二つ持つ場合
            y = self.right.minimum()
            if y.p != self:
                y.transparent(y.right)
                y.right = self.right
                y.right.p = y
            self.transparent(y)
            y.left = self.left
            y.left.p = y
        return y.root()  # 新しく構成した二分木を返す


def main():
    # データセット
    r = Node(15)
    x1 = Node(6, r)
    x2 = Node(18, r)
    x3 = Node(3, x1)
    x4 = Node(7, x1)
    x5 = Node(17, x2)
    x6 = Node(20, x2)
    x7 = Node(2, x3)
    x8 = Node(4, x3)
    x9 = Node(13, x4)
    x10 = Node(9, x9)

    # 後からleft,rightを代入
    r.left, r.right = x1, x2
    x1.left, x1.right = x3, x4
    x2.left, x2.right = x5, x6
    x3.left, x3.right = x7, x8
    x4.right = x9
    x9.left = x10

    print("探索")
    print(r.search(13))  # 13

    print("\n最小値")
    print(r.minimum())  # 2

    print("\n最大値")
    print(r.maximum())  # 20

    print("\n(6の)次節点")
    print(r.search(6).successor())  # 7

    print("\n(6の)前節点")
    print(r.search(6).predecessor())  # 4

    print("\n挿入")
    r.insert(10)  # 10を挿入
    print(r.search(10))  # 確認

    print("\n削除")
    # 子が一つの場合
    print("zが右の子のみをもつ場合")
    print("before:{}".format(r.left.right))
    r = r.search(7).delete()
    print("after:{}".format(r.left.right))

    # 子が二つの場合
    print("\nzが子を二つもつ場合")
    print("before:{}".format(r.left))
    r = r.search(6).delete()
    print("after:{}".format(r.left))

    # ルートの場合
    print("\nzがルートの場合")
    print("before:{}".format(r))
    r = r.delete()
    print("after:{}".format(r))


if __name__ == '__main__':
    main()
