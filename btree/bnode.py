class Node(object):
    def __init__(self, order, parent=None, isRoot=False):
        self.order = order
        self.parent = parent
        self.isRoot = isRoot
        self.pointers = []
        self.keys = []
        self.count = 0
        self.isLeaf = True

    def _search(self, key):
        if key in self.keys:
            return True
        elif self.isLeaf:
            return False
        else:
            index = self._get_index(key)
            return self.pointers[index]._search(key)

