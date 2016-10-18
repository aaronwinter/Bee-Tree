class Node(object):
    def __init__(self, order, parent=None, isRoot=False):
        self.order = order
        self.parent = parent
        self.isRoot = isRoot
        self.pointers = []
        self.keys = []
        self.count = 0
        self.isLeaf = True

