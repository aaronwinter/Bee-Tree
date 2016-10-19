class Node(object):
    def __init__(self, order, parent=None, isRoot=False):
        self.order = order
        self.parent = parent
        self.isRoot = isRoot
        self.pointers = []
        self.keys = []
        self.count = 0
        self.isLeaf = True

    @staticmethod
    def _split_keys(arr):
        lHalf = arr[:len(arr)/2]
        rHalf = arr[len(arr)/2+1:]
        median = arr[len(arr)/2]
        return (lHalf, median, rHalf)

    @staticmethod
    def _split_pointers(arr):
        return (arr[:len(arr)/2], arr[len(arr)/2:])
    
    def _is_full(self):
       return len(self.keys) == 2 * self.order - 1

    def _is_half_full(self):
       return len(self.keys) == (2 * self.order - 1)/2
    
    def _is_overflowing(self):
        return len(self.keys) >= self.order

    def _is_underflowing(self):
        return len(self.keys) <= (self.order/2 - 1)

    def _get_index(self, k):
        index = 0
        for index, v in enumerate(self.keys):
            if k < v: break

        if index == (len(self.keys) - 1) and k > self.keys[-1]:
            return index + 1
        else:
            return index
    
    def _get_index_pointer(self, target):
        index = 0
        for index, ptr in enumerate(self.pointers):
            if target == ptr:
                return index
        return -1
    
    def _replace_key(self, k, new_k):
        arr = self.keys
        for i, v in enumerate(arr):
            if v == k:
                arr[i] = new_k
                break
        return arr
    def _insert_nonfull(self, key):
        index = self._get_index(key)

        if self.isLeaf is True:
            self.keys.insert(index, key)
            self.count += 1
        else:
            nextNode = self.pointers[index]
            if nextNode._is_full():
                self._split_child(self.pointers[index])
                self.isLeaf = False
                if key > self.keys[index]: index += 1
            self.pointers[index]._insert_nonfull(key)

    def _insert(self, key):
        if self._is_full():
            root = self
            newNode = Node(self.order, parent=None, isRoot=True)
            newNode.isLeaf = False
            newNode.count = 0
            newNode.pointers.append(root)

            self = newNode
            root.parent = self
            root.isRoot = False
            self._split_child(root)
            self._insert_nonfull(key)
            return self
        else:
            self._insert_nonfull(key)
            return self

    def _search(self, key):
        if key in self.keys:
            return True
        elif self.isLeaf:
            return False
        else:
            index = self._get_index(key)
            return self.pointers[index]._search(key)

