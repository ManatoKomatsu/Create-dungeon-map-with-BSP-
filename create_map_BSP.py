import random


class Leef:
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
