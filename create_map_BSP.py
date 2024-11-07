import random


class Leaf:
    MIN_LEAF_SIZE = 6  # 最小の分割サイズ

    def __init__(self, x: int, y: int, width: int, height: int):
        # Leafの初期化を行う
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left_child = None  # 左の子ノード
        self.right_child = None  # 右の子ノード
        self.room = None  # このLeaf内での部屋
        self.halls = []  # 他のLeafと接続するための通路

    def split(self) -> bool:
        # Leafを二つの子ノードに分割するためのもの
        if self.left_child or self.right_child:
            return False

        # 分割方向の決定(垂直or水平)
        split_horizontally = random.random() > 0.5
        if self.width > self.height and self.width / self.height >= 1.25:
            split_horizontally = False  # 垂直に分割
        elif self.width > self.height and self.width / self.height >= 1.25:
            split_horizontally = True  # 水平に分割

        # 分割が可能かどうかの判定
        max_size = (
            self.height if split_horizontally else self.width) - self.MIN_LEAF_SIZE
        if max_size <= self.MIN_LEAF_SIZE:
            return False

        split = random.randint(self.MIN_LEAF_SIZE, max_size)  # 分割する位置の決定

        # 分割方向決定後、子ノードの作成
        if split_horizontally:
            self.left_child = Leaf(self.x, self.y, self.width, split)
            self.right_child = Leaf(
                self.x, self.y + split, self.width, self.height - split)
        else:
            self.left_child = Leaf(self.x, self.y, split, self.height)
            self.right_child = Leaf(
                self.x + split, self.y, self.width - split, self.height)

        return True  # 分割に成功

    def create_rooms(self):
        if self.left_child is not None or self.right_child is not None:
            if self.left_child is not None or self.right_child is not None:
                if self.left_child is not None:
                    self.left_child.create_rooms()
                if self.right_child is not None:
                    self.right_child.create_rooms()
            else:
                room_width = random.randint(3, self.width - 2)
                room_height = random.randint(3, self.height - 2)
                room_x = random.randint(1, self.width - room_width - 1)
                room_y = random.randint(1, self.width - room_width - 1)
                self.room = (self.x + room_x, self.y +
                             room_y, room_width, room_height)


# ダンジョン生成の開始
MAX_LEAF_SIZE = 20
_leafs = []  # Leafのリスト

# _sprMapの幅と高さを仮定
spr_map_width = 30  # 例: マップの幅
spr_map_height = 30  # 例: マップの高さ

# ルートとなるLeafを作成し、_leafsリストに追加
root = Leaf(0, 0, spr_map_width, spr_map_height)
_leafs.append(root)

did_split = True

# すべてのLeafが分割できなくなるまで繰り返し
while did_split:
    did_split = False
    for l in _leafs[:]:  # リストのコピーを使用して分割中にループを安全に行う
        if l.left_child is None and l.right_child is None:  # すでに分割されていないLeafである場合
            # Leafが大きすぎるか、ランダムに75%の確率で分割
            if l.width > MAX_LEAF_SIZE or l.height > MAX_LEAF_SIZE or random.random() > 0.25:
                if l.split():  # Leafを分割
                    # 分割が成功した場合、子Leafをリストに追加
                    _leafs.append(l.left_child)
                    _leafs.append(l.right_child)
                    did_split = True


root.create_rooms()
