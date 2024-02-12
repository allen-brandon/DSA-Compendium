import random as rd
class TreapNode:
    #BASIC TREAP
    def __init__(self, value=None, priority=None, parent=None, hash=None):
        self.val = value
        self.priority = priority
        self.parent = parent
        self.right = self.left = None
        if hash: __hash__ = hash
        if priority is None: self.priority = self.__hash__(value)
        if value is not None: self.add(value, priority)

        #Index in inorder traversal
        self.idx=0
        if parent:
            self._rotate()
        

    def __hash__(self, key):
        return rd.randint(-int(1e9+7), int(1e9+7))
    
    #Check if a value is present
    def __contains__(self, value):
        if self.value == value:
            return 1
        if self.value > value and self.left:
            return self.left.__contains__(value)
        elif self.right: return self.right.__contains__(value)
        return 0
        

    #Add a value
    def add(self, value, priority=None):
        if hasattr(value, '__iter__'):
            #O(nlogn) solution
            for x in value: self.add(value, priority)
            return
        if value in self: return
        if priority == None: priority = self.__hash__(value)
        if self.val is None:
            self.val = value
            self.priority = priority
            return

        if value >= self.val:
            if self.right:
                self.right.add(value, priority)
            else:
                self.right = TreapNode(value, priority, parent=self)
        else:
            if self.left:
                self.left.add(value, priority)
            else:
                self.left = TreapNode(value, priority, parent=self)




    #Remove a value
    #    Does nothing if value isn't present
    def remove(self, value):
        if value not in self: return

    #Find index of a value
    #    Raise ValueError if not present
    def index(self, value):
        pass

    #Remove (and return) value by index
    #    Raise IndexError if not in bounds
    def pop(self, idx):
        pass

    #Remove elements with values between l and r
    def erase(self, l, r):
        pass

    #Return index of first value >= target
    def bisect_left(self, target):
        pass
    
    #Return index of first value > target
    def bisect_right(self, target):
        pass

    ###      Private Methods      ###

    #Swap nodes to maintain heap invariant
    def _rotate(self):
        arr = self.arr
        #Rotate Right if par.left
        if node == par*2+1:
            #node -> parent
            #parent -> parent.right
            #
            pass
        #Rotate Left if par.right
        else:
            pass

    