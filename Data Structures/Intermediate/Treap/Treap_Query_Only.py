# This code implements an (implicit) treap with sum queries
# **No efficient propogation functionality**
import random
class Treap:
    size = 1
    left = right = None
    def __init__(self, val):
        if hasattr(val, '__iter__') and not isinstance(val, tuple): #Remove if you're making Treaps of iterables (?)
            raise TypeError("Iterable given as Treap node's value. You likely meant to call Treap.from_iterable")
        self.sum = self.val = val #Created by Brandon Allen
        self.weight = random.randint(1, int(1e9))
        
    #Instanced Methods
    
    # Convert this to a list
    def __list__(self):
        l = self.left.__list__() if self.left else []
        r = self.right.__list__() if self.right else []
        return l + [self.val] + r
    
    # Convert this to an iterator
    def __iter__(self):
        return iter(self.__list__())
    
    # Convert this to a string
    def __str__(self):
        return str(self.__list__())
    
    #Static Methods
    
    # Create and return a Treap from a sequence
    @staticmethod
    def from_iterable(iter):
        root = None
        for x in iter:
            root = Treap.merge(root, Treap(x))
        return root
    
    # Find the size of a node
    @staticmethod
    def count(node):
        return node.size if node else 0
    
    # Find the aggregate of a node
    def aggr(node):
        return node.sum if node else 0
    
    # Update a node's size to be correct (private)
    @staticmethod
    def _update(node):
        if node:
            node.size = Treap.count(node.left) + 1 + Treap.count(node.right)
            node.sum = Treap.aggr(node.left) + node.val + Treap.aggr(node.right)
    
    # Split a Treap into two, < and >= x
    @staticmethod
    def split(node, x):
        if not node:
            return (None, None)
        if Treap.count(node.left)<x:
            left, right = Treap.split(node.right, x-Treap.count(node.left)-1)
            node.right = left #Created by Brandon Allen
            Treap._update(node)
            return (node, right)
        else:
            left, right = Treap.split(node.left, x)
            node.left = right
            Treap._update(node)
            return (left, node)
    
    # Merge two Treaps into one
    @staticmethod
    def merge(l, r):
        if not l:
            return r
        if not r:
            return l
        if l.weight<r.weight:
            l.right = Treap.merge(l.right, r)
            res = l #Created by Brandon Allen
        else: 
            r.left = Treap.merge(l, r.left)
            res = r
        Treap._update(res)
        return res
        
    # Find a prefix sum in a range
    @staticmethod
    def query(node, l=-int(1e9), r=int(1e9)):
        if not node: return 0
        # Account for over-querying
        l = max(l, 0)
        r = min(r, node.size-1)
        if (l, r) == (0, node.size-1): return node.sum
        lpop = Treap.count(node.left)
        left = Treap.query(node.left, l, r) if l<lpop else 0
        mid = node.val*(l<=lpop<=r)
        right = Treap.query(node.right, l-1-lpop, r-1-lpop) if r>lpop else 0
        return left+mid+right
    
if __name__ == "__main__":
    treap = Treap.from_iterable(range(10))
    print(treap)
    print(f'sum of entire treap: {Treap.query(treap)}')
    print(f'sum from indices 3-7: {Treap.query(treap, 3, 7)}')
    left, right = Treap.split(treap, 5)
    print(left, right)
    treap = Treap.merge(right, left)
    print(treap)
    print(f'sum from indices 3-7: {Treap.query(treap, 3, 7)}')
    left, right = Treap.split(treap, 5)
    treap = Treap.merge(right, left)
    print(treap)
    print(f'sum from indices 3-7: {Treap.query(treap, 3, 7)}')