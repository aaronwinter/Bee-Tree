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

    def _split_child(self, fullChild):
        lHalf, median, rHalf = Node._split_keys(fullChild.keys)

        leftChild = Node(self.order, self)
        leftChild.isLeaf = fullChild.isLeaf

        leftChild.keys = lHalf
        fullChild.keys = rHalf
        leftChild.count = len(leftChild.keys)
        fullChild.count = len(fullChild.keys)

        if fullChild.isLeaf is False:
            pLeft, pRight = Node._split_pointers(fullChild.pointers)
            leftChild.pointers = pLeft
            fullChild.pointers = pRight

        index = self._get_index(median)
        if index == len(self.keys):
            self.keys.append(median)
            self.pointers.insert(index, leftChild)
        else:
            self.keys.insert(index, median)
            self.pointers.insert(index, leftChild)
        self.count += 1

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

    def _adjust_overflowing(self, leftN=None, rightN=None, index_ptr=0):
        if leftN is not None and leftN._is_full():
            self._get_left_sib(index_ptr)._redistribute('->')
        elif rightN is not None and rightN._is_full():
            self._get_right_sib(index_ptr)._redistribute('<-')
        else:
            self.parent._split_child(self)
            self.parent._adjust()
    
    def _adjust_underflowing(self, leftN=None, rightN=None, index_ptr=0):
        if leftN is not None and len(leftN.keys) > (self.order - 1):
            self._get_left_sib(index_ptr)._redistribute('->')
            return
        elif rightN is not None and len(rightN.keys) > (self.order - 1):
            self._get_right_sib(index_ptr)._redistribute('<-')
            return
        elif self.isRoot is True:
            if len(self.pointers) == 1:
                self.keys = self.pointers[0].keys
                self.pointers = self.pointers[0].pointers
                return
        else:
            if rightN is not None:
                self._merge(self._get_right_sib(index_ptr))
                return
            else:
                self._merge(self._get_left_sib(index_ptr))
                return
        return

                
    def _adjust(self):
        overflowing = self._is_overflowing()
        underflowing = self._is_underflowing()
        index_ptr = self.parent._get_index_pointer(self)
        left_sib_exist = self._has_left_sib(index_ptr)
        right_sib_exist = self._has_right_sib(index_ptr)
        leftN = self._get_left_sib(index_ptr) if left_sib_exist else None
        rightN = self._get_right_sib(index_ptr) if right_sib_exist else None

        if overflowing is True:
            self._adjust_overflowing(leftN, rightN, index_ptr)
        elif underflowing is True:
            self._adjust_underflowing(leftN, rightN, index_ptr)
        else:
            return
           
    def _delete(self, key):
        if key in self.keys and self.isLeaf is True:
            self.keys.remove(key)
            self._adjust()
        elif key in self.keys and self.isLeaf is False:
            index = self._get_index(key)
            smallestNode = self.pointers[index+1]._get_leftmost_leaf()
            smallestKey = smallestNode.keys[0]
            self._replace_key(key, smallestKey)
            self.pointers[index+1]._get_leftmost_leaf()._adjust()
        else:
            index = self._get_index(key)
            return self.pointers[index]._delete(key)
