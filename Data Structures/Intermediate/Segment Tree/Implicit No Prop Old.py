#SEG TREE (Implicit No Prop)
        
class SegmentTree:
    def __init__(self, input_arr):
        n = 1<<(len(input_arr).bit_length()-1)
        if n < len(input_arr): n<<=1
        self.n = n
        self.arr = arr =[-inf]*n + input_arr + [-inf]*(n-len(input_arr))
        for i in range(n-1,0,-1):
            arr[i] = max(arr[i*2], arr[i*2+1])
    
    def __list__(self):
        return self.arr
    def __str__(self):
        return str(self.__list__())
    def update(self, i, val):
        st = []
        u, bit = 1, self.n>>1
        while bit:
            st.append(u)
            u*=2
            u+=bool(bit&i)
            bit>>=1
        self.arr[u] = val
        while st:
            u = st.pop()
            self.arr[u]=max(self.arr[u*2], self.arr[u*2+1])
            
            
    def query(self, l, r):
        res = -inf
        st = [(1, l, r, self.n)]
        while st:
            u, l, r, n = st.pop()
            l = max(l, 0)
            r = min(r, n)
            if r-l==n:
                res = max(res, self.arr[u])
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
    testcases, operations, n = 1, 50, 1000000
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
            tree_val = tree.query(l, r)
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