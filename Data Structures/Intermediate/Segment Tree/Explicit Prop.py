#SEG TREE (Prop)
class SegmentNode:
    def __init__(self, v=0):
        self.pop = 1
        self.pend = 0
        self.val = self.sum = v
        self.left = self.right = None
        
class SegmentTree:
    def __init__(self, arr):
        n = len(arr)
        node_arr = [None]*n
        st = [(0, n, None)]
        while st:
            l, r, node = st.pop()
            if l == r: continue
            if node:
                m = l+(r-l)//2
                if m>l: node.left = node_arr[l+(m-l)//2]
                if r>m+1: node.right = node_arr[m+1+(r-m-1)//2]
                self._refresh(node)
                continue
            else:
                m = l+(r-l)//2
                node = SegmentNode(arr[m])
                node_arr[m]=node
                st.append((l, r, node))
                st.append((m+1, r, None))
                st.append((l, m, None))
        self.root = node
    
    def __str__(self):
        st = [(self.root, 1)]
        res = []
        while st:
            node, d = st.pop()
            self._propagate(node)
            if d:
                if u.right: st.append((node.right, 1))
                st.append((node, 0))
                if u.left: st.append((node.left, 1))
            else:
                res.append((node.val))
        return str(res)
                
    def update(self, l, r, val):
        st = [(self.root, l, r, 1)]
        while st:
            node, l, r, d = st.pop()
            if not d:
                self._refresh(node)
                continue
            l = max(l, 0)
            r = min(r, node.pop)
            if not l and r == node.pop:
                node.pend+=val
                continue
            l_pop = self._count(node.left)
            if l<=l_pop and r>l_pop:
                node.val+=val
            st.append((node, l, r, 0))
            if r > l_pop+1:
                st.append((node.right, l-l_pop-1, r-l_pop-1, 1))
            if l < l_pop:
                st.append((node.left, l, r, 1))
            
    
    def query(self, l, r):
        res = 0 #Identity element
        st = [(self.root, l, r)]
        while st:
            node, l, r = st.pop()
            self._propagate(node)
            l = max(l, 0)
            r = min(r, node.pop)
            if not l and r == node.pop:
                res += node.sum
                continue
            l_pop = self._count(node.left)
            res += node.val*(l<=l_pop)*(r>l_pop)
            if r > l_pop+1:
                st.append((node.right, l-l_pop-1, r-l_pop-1))
            if l < l_pop:
                st.append((node.left, l, r))
        return res

    
    def _refresh(self, node):
        self._propagate(node)
        node.sum = self._aggr(node.left)+node.val+self._aggr(node.right)
        node.pop = self._count(node.left)+1+self._count(node.right)
        
    def _propagate(self, node):
        node.val += node.pend
        node.sum += node.pend*node.pop
        if node.left: node.left.pend+=node.pend
        if node.right: node.right.pend+=node.pend
        node.pend = 0
        
    def _aggr(self, node):
        if node: self._propagate(node)
        return node.sum if node else 0
    
    def _count(self, node):
        return node.pop if node else 0

    
    

if __name__ == '__main__':
    import random
    import time
    testcases, operations, n = 100, 100, 5000
    tree_time = 0
    naive_time = 0
    for t in range(testcases):
        naive_start = time.time()
        arr = list(random.sample(range(-n, n), random.randint(n, n+5)))
        naive_time+=time.time()-naive_start
        n = len(arr)
        tree_start = time.time()
        tree = SegmentTree(arr)
        tree_time+=time.time()-tree_start
        for op in range(operations):
            l = random.randint(0, n-1)
            r = random.randint(l+1, n)
            x = random.randint(-100, 100)
            tree_op_start = time.time()
            tree.update(l, r, x)
            tree_time += time.time() - tree_op_start
            naive_op_start = time.time()
            for i in range(l, r):
                arr[i]+=x
            naive_time += time.time() - naive_op_start
            l = random.randint(0, n-1)
            r = random.randint(l+1, n)
            tree_query_start = time.time()
            tree_val = tree.query(l, r)
            tree_time += time.time() - tree_query_start
            naive_query_start = time.time()
            arr_val = sum(arr[l:r])
            if tree_val != arr_val:
                raise ValueError(f'naive and tree values are different. values: {(tree_val, arr_val)},  update: {(i, x)}, query: {(l, r)}')
            
            
    print(f'all {testcases} test cases passed!')
    print(f'{testcases*operations} total operations')
    print(f'Naive operation time: {naive_time}')
    print(f'Segment Tree operation time: {tree_time}')