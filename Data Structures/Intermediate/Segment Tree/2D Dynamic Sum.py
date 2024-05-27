class SubNode:
    left = right = None
    def __init__(self, l, r, x=0):
        self.l, self.r = l, r
        self.val = x
        
class SubTree:
    def __init__(self, l=int(-1e10), r=int(1e10)):
        self.root = SubNode(l, r)
        
    def __list__(self):
        st = [self.root]
        res = []
        while st:
            node = st.pop()
            if not node.left and not node.right:
                res.append(node.val)
            if node.left:
                st.append(node.left)
            if node.right:
                st.append(node.right)
        return res
    
    def __str__(self):
        return str(self.__list__())
    
    def update(self, i, x):
        st = [self.root]
        while st:
            node = st.pop()
            node.val+=x
            if node.l == i and node.r == i+1:
                continue
            m = node.l+(node.r-node.l)//2
            if i>=m:
                if not node.right:
                    node.right = SubNode(m, node.r)
                st.append(node.right)
            else:
                if not node.left:
                    node.left = SubNode(node.l, m)
                st.append(node.left)
                
    def query(self, l, r):
        st = [self.root]
        res = 0
        while st:
            node = st.pop()
            if l <= node.l and r >= node.r:
                res+=node.val
                continue
            m = node.l+(node.r-node.l)//2
            if r>m:
                if not node.right:
                    node.right = SubNode(m, node.r)
                st.append(node.right)
            if l<m:
                if not node.left:
                    node.left = SubNode(node.l,m)
                st.append(node.left)
        return res
        
class SegmentNode:
    left = right = None
    def __init__(self, x1=-int(1e10), x2=int(1e10), y1=-int(1e10), y2=int(1e10)):
        self.x1 = x1
        self.x2 = x2
        self.tree = SubTree(y1, y2)
    
class SegmentTree:
    def __init__(self, x1=-int(1e10), x2=int(1e10), y1=-int(1e10), y2=int(1e10)):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.root = SegmentNode(x1, x2, y1, y2)
        
    def __list__(self):
        st = [self.root]
        res = []
        while st:
            node = st.pop()
            if not node.left and not node.right:
                res.append(node.tree.__list__())
            if node.left:
                st.append(node.left)
            if node.right:
                st.append(node.right)
        return res
    
    def __str__(self):
        return str(self.__list__())
        
    def update(self, x, y, val):
        st = [self.root]
        while st:
            node = st.pop()
            node.tree.update(y, val)
            if node.x1 == x and node.x2 == x+1:
                continue
            m = node.x1+(node.x2-node.x1)//2
            if x>=m:
                if not node.right:
                    node.right = SegmentNode(m, node.x2, self.y1, self.y2)
                st.append(node.right)
            else:
                if not node.left:
                    node.left = SegmentNode(node.x1, m, self.y1, self.y2)
                st.append(node.left) 
                
    def query(self, x1, x2, y1, y2):
        st = [self.root]
        res = 0
        while st:
            node = st.pop()
            if x1<=node.x1 and x2>=node.x2:
                res+=node.tree.query(y1, y2)
                continue
            m = node.x1+(node.x2-node.x1)//2
            if x2>m:
                if not node.right:
                    node.right = SegmentNode(m, node.x2, self.y1, self.y2)
                st.append(node.right)
            if x1<m:
                if not node.left:
                    node.left = SegmentNode(node.x1, m, self.y1, self.y2)
                st.append(node.left)    
            
        return res
    
    
if __name__ == '__main__':
    testcases, operations, m, n = 10000, 100, 3, 3
    import random
    for t in range(testcases):
        arr = [[0]*n for _ in range(m)]
        tree = SegmentTree(0, m, 0, n)
        for op in range(operations):
            x_update = random.randint(0, m-1)
            y_update = random.randint(0, n-1)
            val = random.randint(-100, 100)
            tree.update(x_update, y_update, val)
            arr[x_update][y_update] += val
            
            x1_query = random.randint(0, m-1)
            x2_query = random.randint(x1_query+1, m)
            y1_query = random.randint(0, n-1)
            y2_query = random.randint(y1_query+1, n)
            
            tree_val = tree.query(x1_query, x2_query, y1_query, y2_query)
            arr_val = 0
            for i in range(x1_query, x2_query):
                for j in range(y1_query, y2_query):
                    arr_val += arr[i][j]
            
            if tree_val != arr_val:
                for row in arr: print(row)
                print()
                for row in tree.__list__():
                    print(row)
                raise ValueError(f'Values are different. values: {tree_val, arr_val}, update: {(x_update, y_update, val)}, query: {(x1_query, x2_query, y1_query, y2_query)}')
            # print(f'operation {op} passed!')
        # print(f'testcase {t} passed!')
            
            
    print(f'all {testcases} test cases passed!')
    print(f'{testcases*operations} total operations')
    # print(f'Naive operation time: {naive_time}')
    # print(f'Segment Tree operation time: {tree_time}')
        