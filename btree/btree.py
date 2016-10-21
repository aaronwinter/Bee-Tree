from bnode import Node


class BTree(object):
    def __init__(self, order):
        self.order = order
        self.root = Node(order, parent=None, isRoot=True)
        return

    def insert(self, key):
        self.root = self.root._insert(key)
        return

    def search(self, key):
        return self.root._search(key)

    def delete(self, key):
        self.root._delete(key)
        return

    def preorder(self):
        self.root._preorder()
        return
