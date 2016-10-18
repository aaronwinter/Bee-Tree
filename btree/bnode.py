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
    def _search(self, key):
        if key in self.keys:
            return True
        elif self.isLeaf:
            return False
        else:
            index = self._get_index(key)
            return self.pointers[index]._search(key)

