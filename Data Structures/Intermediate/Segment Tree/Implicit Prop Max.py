#SEG TREE (Implicit Prop, Max Query)
from math import inf
class SegmentTree:
    def __init__(self, input_arr):
        n = 1<<(len(input_arr).bit_length()-1)
        if n < len(input_arr): n<<=1
        self.n = n
        self.arr = [-inf]*n + input_arr + [-inf]*(n-len(input_arr))
        self.pend = [0]*(n*2)
        for i in range(n-1,0,-1):
            self.arr[i] = max(self.arr[i*2], self.arr[i*2+1])
            
    def flush_pending(self):
        n = self.n
        for i in range(n):
            self.pend[i*2]+=self.pend[i]
            self.pend[i*2+1]+=self.pend[i]
        for i in range(n, n*2):
            self.arr[i]+=self.pend[i]
        self.pend = [0]*(n*2)
        for i in range(n-1, 0, -1):
            self.arr[i] = max(self.arr[i*2], self.arr[i*2+1])
            
    __list__ = lambda self: self.flush_pending() or self.arr[-self.n:]
    __str__ = lambda self: str(self.__list__())
    
    def update(self, l, r, x):
        st = [(1, l, r, self.n, 1)]
        while st:
            u, l, r, n, d = st.pop()
            l = max(0, l)
            r = min(n, r)
            if r-l==n:
                self.pend[u]+=x
                continue
            if not d:
                self.arr[u] = max(self.arr[u*2]+self.pend[u*2], self.arr[u*2+1]+self.pend[u*2+1])
                continue
            st.append((u, l, r, n, 0))
            n//=2
            if l<n:
                st.append((u*2, l, r, n, 1))
            if r>n:
                st.append((u*2+1, l-n, r-n, n, 1))
            
        
    def query(self, l, r):
        res = -inf
        st = [(1, l, r, self.n)]
        while st:
            u, l, r, n = st.pop()
            self.arr[u]+=self.pend[u]
            if n != 1:
                self.pend[u*2]+=self.pend[u]
                self.pend[u*2+1]+=self.pend[u]
            self.pend[u]=0
            l = max(0, l)
            r = min(n, r)
            if r-l==n:
                res= max(res, self.arr[u])
                continue
            n//=2
            if l<n:
                st.append((u*2, l, r, n))
            if r>n:
                st.append((u*2+1, l-n, r-n, n))
        return res

if __name__ == '__main__':
    import random
    import time
    testcases, operations, m = 10, 10, 100000
    tree_time = 0
    naive_time = 0
    for t in range(testcases):
        naive_start = time.time()
        arr = list(random.sample(range(-m, m), random.randint(m, m+5)))
        naive_time+=time.time()-naive_start
        n = len(arr)
        tree_start = time.time()
        tree = SegmentTree(arr)
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
            tree_query_start = time.time()
            tree_val = tree.query(l, r)
            tree_time += time.time() - tree_query_start
            naive_query_start = time.time()
            arr_val = max(arr[l:r])
            naive_time+=time.time()-naive_query_start
            if tree_val != arr_val:
                # print(tree.arr)
                # print(tree.pend)
                print(tree)
                print(arr)
                raise ValueError(f'naive and tree values are different. values: {(tree_val, arr_val)},  update: {(l_update, r_update, x)}, query: {(l, r)}')
        #     print(f'operation {op} passed!')
        # print(f'testcase {t} passed!')
            
            
    print(f'all {testcases} test cases passed!')
    print(f'{testcases*operations} total operations')
    print(f'Naive operation time: {naive_time}')
    print(f'Segment Tree operation time: {tree_time}')
