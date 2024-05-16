#Dynamic Sum Prop
class SegmentNode:
    left = right = None
    def __init__(self, l, r, x=0):
        self.l, self.r = l, r
        self.agg = self.val = x
        self.pend = 0
    
class SegmentTree:
    def __init__(self, l=int(-1e10), r=int(1e10)):
        self.root = SegmentNode(l, r)
    
    def __list__(self):
        st = [self.root]
        res = []
        while st:
            node = st.pop()
            if node.right:
                st.append(node.right)
            if node.left:
                st.append(node.left)
            marked = not node.left and not node.right
            if node.pend:
                self._propagate(node)
            if marked and node.val:
                if res and res[-1][0][1] == node.l and res[-1][1] == node.val:
                    res[-1][0][1] = node.r
                else:
                    res.append([[node.l, node.r], node.val])
        return res
    
    def __str__(self):
        return str(self.__list__())
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.query(key, key+1)
        l, r = key.start, key.stop
        if not l: l = 0
        if not r: r = self.root.r
        return self.query(l, r)
    
    def _refresh(self, node):
        self._propagate(node)
        l_agg, r_agg = 0, 0
        if node.left:
            self._propagate(node.left)
            l_agg = node.left.agg
        if node.right:
            self._propagate(node.right)
            r_agg = node.right.agg
        node.agg = l_agg + r_agg
    
    def _propagate(self, node):
        node.val+=node.pend
        node.agg+=node.pend*(node.r-node.l)
        if node.r-node.l>1:
            if not node.left:
                node.left = SegmentNode(node.l, node.l+(node.r-node.l)//2)
            node.left.pend+=node.pend
        if node.r-node.l>1:
            if not node.right:
                node.right = SegmentNode(node.l+(node.r-node.l)//2, node.r)
            node.right.pend+=node.pend
        node.pend = 0
        
        
    def update(self, l, r, x):
        l, r = max(l, self.root.l), min(r, self.root.r)
        st = [(self.root, 1)]
        while st:
            node, d = st.pop()
            if not d:
                self._refresh(node)
                continue
            if l<=node.l and r>=node.r:
                node.pend += x
                continue
            st.append((node, 0))
            m = node.l+(node.r-node.l)//2
            if r>m and node.r > node.l+1:
                if not node.right:
                    node.right = SegmentNode(m, node.r)
                st.append((node.right, 1))
            if l<m and node.r > node.l+1:
                if not node.left:
                    node.left = SegmentNode(node.l, m)
                st.append((node.left, 1))
        
        
    def query(self, l, r):
        st = [self.root]
        res = 0
        while st:
            node = st.pop()
            self._propagate(node)
            if l <= node.l and r >= node.r:
                res+=node.agg
                continue
            m = node.l+(node.r-node.l)//2
            if r>m and node.r > node.l+1:
                st.append(node.right)
            if l<m and node.r > node.l+1:
                st.append(node.left)
        return res
        
        
    


if __name__ == '__main__':
    import random
    import time
    testcases, operations, n = 1, 20, 1000000
    tree_time = 0
    naive_time = 0
    for t in range(testcases):
        naive_start = time.time()
        # arr = list(random.sample(range(-n, n), random.randint(n, n+5)))
        arr = [0]*n
        naive_time+=time.time()-naive_start
        tree_start = time.time()
        tree = SegmentTree()
        tree_time+=time.time()-tree_start
        for op in range(operations):
            l = random.randint(0, n-1)
            r = random.randint(l+1, n)
            l_update, r_update = l, r
            x = random.randint(-5, 5)
            tree_op_start = time.time()
            tree.update(l, r, x)
            tree_time += time.time() - tree_op_start
            naive_op_start = time.time()
            for i in range(l, r):
                arr[i]+=x
            naive_time += time.time() - naive_op_start
            l = random.randint(0, n-1)
            r = random.randint(l+1, n)
            l, r = 0, n
            tree_query_start = time.time()
            tree_val = tree[l:r]
            tree_time += time.time() - tree_query_start
            naive_query_start = time.time()
            arr_val = sum(arr[l:r])
            naive_time+=time.time()-naive_query_start
            if tree_val != arr_val:
                print(tree)
                print(arr)
                raise ValueError(f'naive and tree values are different. values: {(tree_val, arr_val)},  update: {(l_update, r_update, x)}, query: {(l, r)}')
        #     print(f'operation {op} passed!')
        # print(f'testcase {t} passed!')
            
            
    print(f'all {testcases} test cases passed!')
    print(f'{testcases*operations} total operations')
    print(f'Naive operation time: {naive_time}')
    print(f'Segment Tree operation time: {tree_time}')