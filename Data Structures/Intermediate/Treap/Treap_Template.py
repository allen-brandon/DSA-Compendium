import random
class TreapNode:
    size = 1
    left = right = None
    def __init__(self, val):
        self.weight = random.randint(1, int(1e9))
        self.val = val

class Treap:
    root = None
    def __init__(self, seq=(), node=None):
        for x in seq:
            self.add(x)
            
    def count(self, node):
        return node.size if node else 0
    
    def update(self, node):
        if node: node.size = self.count(node.left)+self.count(node.right)+1
        
    def split(self, x, node="undefined"):
        if node == "undefined":
            return self.split(x, self.root)
        if not node:
            return (None, None)
        if self.count(node.left)<x:
            left, right = self.split(x-self.count(node)-1, node.right)
            node.right = left
            self.update(node)
            return (node, right)
        else:
            left, right = self.split(x, node.left)
            node.left = right
            self.update(node)
            return (left, node)
        
    def merge(self, l, r):
        if not l:
            self.update(r)
            return r
        if not r:
            self.update(l)
            return l
        if l.weight<r.weight:
            print("test")
            l.right = self.merge(l.right, r)
            self.update(r)
            return l
        else:
            print("test")
            r.left = self.merge(l, r.left)
            self.update(l)
            return r
        
    def add(self, x):
        node = TreapNode(x)
        self.root = self.merge(self.root, node)
    
    def __str__(self):
        res = []
        self.inord_print(res, self.root)
        return str(res)
        
    def inord_print(self, res, node):
        if not node: return
        self.inord_print(res, node.left)
        res.append(node.val)
        self.inord_print(res, node.right)
    
    
if __name__ == "__main__":
    treap = Treap([1,2,3,4,5])
    print(treap)
    left, right = treap.split(3)
    print((left, right))
    test = Treap()