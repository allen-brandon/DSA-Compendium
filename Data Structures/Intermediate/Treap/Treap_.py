import random
class Treap:
    size = 1
    left = right = None
    def __init__(self, val):
        if hasattr(val, '__iter__') and not isinstance(val, tuple): #Remove if you're making Treaps of iterables (?)
            raise TypeError("Iterable given as Treap node's value. You likely meant to call Treap.from_iterable")
        self.aggregate = self.val = val #Created by Brandon Allen
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
    
    # Update a node's size to be correct (private)
    @staticmethod
    def _update(node):
        if node: node.size = Treap.count(node.left)+Treap.count(node.right)+1
    
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
        
if __name__ == "__main__":
    treap = Treap.from_iterable(range(10))
    print(treap)
    left, right = Treap.split(treap, 5)
    print(left, right)
    treap = Treap.merge(right, left)
    print(treap)
    left, right = Treap.split(treap, 5)
    treap = Treap.merge(right, left)
    print(treap)