#SEG TREE (Implicit No Prop)
        
class SegmentTree:
    def __init__(self, input_arr):
        self.n = n = len(input_arr)
        self.arr = arr = [None]*(n*2)
        self.pop = pop = [0]*(n*2)
        self.acc = acc = [0]*(n*2)
        st = [(0, n, 1, 0)]
        while st:
            l, r, d, i = st.pop()
            if l == r: continue
            if not d:
                self._refresh(i)
                continue
            else:
                m = l+(r-l)//2
                arr[i] = input_arr[m]
                st.append((l, r, 0, i))
                st.append((m+1, r, 1, i*2+2))
                st.append((l, m, 1, i*2+1))
    
    def __str__(self):
        arr = self.arr
        st = [(0, 1)]
        res = []
        while st:
            i, d = st.pop()
            if d:
                if i*2+2<self.n*2 and self.arr[i*2+2] is not None: st.append((i*2+2, 1))
                st.append((i, 0))
                if i*2+1<self.n*2 and self.arr[i*2+1] is not None: st.append((i*2+1, 1))
            else:
                res.append((arr[i]))
        return str(res)
                
    def update(self, i, val):
        arr, pop, acc = self.arr, self.pop, self.acc
        st = [(0, i, 1)]
        while st:
            u, i, d = st.pop()
            if not d:
                self._refresh(u)
                continue
            l_pop = self._count(u*2+1)
            st.append((u, i, 0))
            if i == l_pop:
                arr[u] += val
                continue
            elif i > l_pop:
                st.append((u*2+2, i-l_pop-1, 1))
            elif i < l_pop:
                st.append((u*2+1, i, 1))
            
    
    def query(self, l, r):
        arr, pop, acc = self.arr, self.pop, self.acc
        res = 0 #Identity element
        st = [(0, l, r)]
        while st:
            i, l, r = st.pop()
            l = max(l, 0)
            r = min(r, pop[i])
            if not l and r == pop[i]:
                res += acc[i]
                continue
            l_pop = self._count(i*2+1)
            res += arr[i]*(l<=l_pop)*(r>l_pop)
            if r > l_pop+1:
                st.append((i*2+2, l-l_pop-1, r-l_pop-1))
            if l < l_pop:
                st.append((i*2+1, l, r))
        return res

    
    def _refresh(self, i):
        self.acc[i] = self._aggr(i*2+1)+self.arr[i]+self._aggr(i*2+2)
        self.pop[i] = self._count(i*2+1)+1+self._count(i*2+2)
        
    def _aggr(self, i):
        if i<self.n*2 and self.arr[i] is not None:
            return self.acc[i]
        else:
            return 0
    
    def _count(self, i):
        return self.pop[i] if i<self.n*2 and self.arr[i] is not None else 0

    
    

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