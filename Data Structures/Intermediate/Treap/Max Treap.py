# This code implements an (implicit) treap with max queries
# Full propagation functionality
from functools import partial
import math
import random
import operator
class Treap:
    size = 1
    pend = 0
    left = right = None
    def __init__(self, val):
        if hasattr(val, '__iter__') and not isinstance(val, tuple): #Remove if you're making Treaps of iterables (?)
            raise TypeError("Iterable given as Treap node's value. You likely meant to call Treap.from_iterable")
        self.max = self.val = val #Created by Brandon Allen
        self.weight = random.randint(1, int(1e9))
        
    #Instanced Methods
    
    # Convert this to a list
    def __list__(self):
        Treap._propagate(self)
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
        if isinstance(iter, int): iter = range(iter)
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
        if node:
            return node.max
        return -math.inf
    
    @staticmethod
    def _refresh(node):
        '''Update a node's size to be correct (private)'''
        if node:
            node.size = Treap.count(node.left) + 1 + Treap.count(node.right)
            node.max = max(Treap.aggr(node.left), node.val, Treap.aggr(node.right))
    
    @staticmethod
    def _propagate(node):
        '''Apply a node's pending updates to its value and children (private)'''
        if not node: return
        node.val+=node.pend
        node.max+=node.pend
        if node.left: node.left.pend+=node.pend
        if node.right: node.right.pend+=node.pend
        node.pend=0
    
    @staticmethod
    def split(node, x):
        '''Split a Treap into two, < and >= x'''
        Treap._propagate(node)
        if not node:
            return (None, None)
        if Treap.count(node.left)<=x:
            left, right = Treap.split(node.right, x-Treap.count(node.left)-1)
            node.right = left #Created by Brandon Allen
            Treap._refresh(node)
            return (node, right)
        else:
            left, right = Treap.split(node.left, x)
            node.left = right
            Treap._refresh(node)
            return (left, node)
    
    @staticmethod
    def merge(l, r):
        '''Merge two Treaps into one'''
        Treap._propagate(r)
        Treap._propagate(l)
        if not l: return r
        if not r: return l
        if l.weight<r.weight:
            l.right = Treap.merge(l.right, r)
            res = l #Created by Brandon Allen
        else: 
            r.left = Treap.merge(l, r.left)
            res = r
        Treap._refresh(res)
        return res
        
    @staticmethod
    def query(node, l=-int(1e9), r=int(1e9)):
        '''Find a prefix maximum in a range'''
        Treap._propagate(node)
        if not node: return -math.inf
        l, r = max(l, 0), min(r, node.size-1)
        if (l, r) == (0, node.size-1): return node.max
        lpop = Treap.count(node.left)
        left = Treap.query(node.left, l, r) if l<lpop else -math.inf
        mid = node.val if l<=lpop<=r else -math.inf# l and r are 0-indexed; lpop is "1-indexed" (e.g. size)
        right = Treap.query(node.right, l-1-lpop, r-1-lpop) if r>lpop else -math.inf
        Treap._refresh(node)
        return max(left, mid, right)
    
    @staticmethod
    def update(node, x, l=-int(1e9), r=int(1e9)):
        '''Add a number to an index or range of indices'''
        if not node: return
        l, r = max(l, 0), min(r, node.size-1)
        if (l, r) == (0, node.size-1):
            node.pend+=x
            return
        lpop = Treap.count(node.left)#1 indexed
        if l<=lpop<=r:
            node.val+=x
        if l<lpop:# Created by Brandon Allen
            Treap.update(node.left, x, l, r)
        if r>lpop:
            Treap.update(node.right, x, l-1-lpop, r-1-lpop)
        Treap._refresh(node)
    
if __name__ == "__main__":
    for _ in range(1000):
        treap = Treap.from_iterable([random.randint(-100, 100) for _ in range(100)])
        if Treap.query(treap) != max(list(treap)):
            raise ValueError("Something went wrong when initializing the treap")
        
        l = random.randint(0, 99)
        r = random.randint(l, 99)
        if Treap.query(treap, l, r) != max(list(treap)[l:r+1]):
            raise ValueError("Something went wrong with query before changes")
        
        x = random.randint(-100, 100)
        Treap.update(treap, x, l, r)
        if Treap.query(treap, l, r) != max(list(treap)[l:r+1]):
            raise ValueError("Something went wrong with query after range update")
        
        idx = random.randint(0, 100)
        left, right = Treap.split(treap, idx)
        treap = Treap.merge(right, left)
        if Treap.query(treap, l, r) != max(list(treap)[l:r+1]):
            raise ValueError("Something went wrong with query after structural change")
    
    print("All tests passed!")