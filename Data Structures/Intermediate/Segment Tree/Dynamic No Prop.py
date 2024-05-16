#Dynamic Sum No Prop
#Right bound exclusive
class SegmentNode:
    left = right = None
    def __init__(self, l, r, x=0):
        self.l, self.r = l, r
        self.agg = self.val = x
    
class SegmentTree:
    def __init__(self, l=int(-1e10), r=int(1e10)):
        self.root = SegmentNode(l, r)
    
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
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.query(key, key+1)
        l, r = key.start, key.stop
        if not l: l = 0
        if not r: r = self.root.r
        return self.query(l, r)
    
    def _refresh(self, node):
        l_agg = node.left.agg if node.left else 0
        r_agg = node.right.agg if node.right else 0
        node.agg = l_agg + node.val + r_agg
        
    def update(self, i, x):
        st = [(self.root, 1)]
        while st:
            node, d = st.pop()
            if not d:
                self._refresh(node)
                continue
            if node.l == i and node.r == i+1:
                node.val += x
                node.agg += x
                continue
            m = node.l+(node.r-node.l)//2
            st.append((node, 0))
            if i>=m:
                if not node.right:
                    node.right = SegmentNode(node.l+(node.r-node.l)//2, node.r)
                st.append((node.right, 1))
            else:
                if not node.left:
                    node.left = SegmentNode(node.l, node.l+(node.r-node.l)//2)
                st.append((node.left, 1))
        
        
    def query(self, l, r):
        st = [self.root]
        res = 0
        while st:
            node = st.pop()
            if l <= node.l and r >= node.r:
                res+=node.agg
                continue
            m = node.l+(node.r-node.l)//2
            if r>m:
                if not node.right:
                    node.right = SegmentNode(node.l+(node.r-node.l)//2, node.r)
                st.append(node.right)
            if l<m:
                if not node.left:
                    node.left = SegmentNode(node.l, node.l+(node.r-node.l)//2)
                st.append(node.left)
        return res
        

if __name__ == '__main__':
    import random
    import time
    testcases, operations, n = 100, 500, 1000
    tree_time = 0
    naive_time = 0
    for t in range(testcases):
        naive_start = time.time()
        # arr = list(random.sample(range(-n, n), random.randint(n, n+5)))
        arr = [0]*(n+5)
        naive_time+=time.time()-naive_start
        n = len(arr)
        tree_start = time.time()
        tree = SegmentTree()
        tree_time+=time.time()-tree_start
        for op in range(operations):
            i = random.randint(0, n-1)
            i_update = i
            x = random.randint(-5, 5)
            tree_op_start = time.time()
            tree.update(i, x)
            tree_time += time.time() - tree_op_start
            naive_op_start = time.time()
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
                raise ValueError(f'naive and tree values are different. values: {(tree_val, arr_val)},  update: {(i_update, x)}, query: {(l, r)}')
        #     print(f'operation {op} passed!')
        # print(f'testcase {t} passed!')
            
            
    print(f'all {testcases} test cases passed!')
    print(f'{testcases*operations} total operations')
    print(f'Naive operation time: {naive_time}')
    print(f'Segment Tree operation time: {tree_time}')