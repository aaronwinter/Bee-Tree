class BTree(object):
    def __init__(self, order):
        self.order = order
        self.root = Node(order, parent=None, isRoot=True)
        return

