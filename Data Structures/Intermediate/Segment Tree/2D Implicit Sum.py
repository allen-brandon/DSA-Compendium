#SEG TREE (Implicit No Prop)
        
class SubTree:
    def __init__(self, input_arr):
        n = 1<<(len(input_arr).bit_length()-1)
        if n < len(input_arr): n<<=1
        self.n = n
        self.arr = arr =[0]*n + input_arr + [0]*(n-len(input_arr))
        for i in range(n-1,0,-1):
            arr[i] = arr[i*2]+arr[i*2+1]
    
    def __list__(self):
        return self.arr
    def __str__(self):
        return str(self.__list__())
    def update(self, i, val):
        u, bit = 1, self.n>>1
        while bit:
            self.arr[u]+=val
            u*=2
            u+=bool(bit&i)
            bit>>=1
        self.arr[u]+=val
            
            
    def query(self, l, r):
        res = 0
        st = [(1, l, r, self.n)]
        while st:
            u, l, r, n = st.pop()
            l = max(l, 0)
            r = min(r, n)
            if r-l==n:
                res+=self.arr[u]
                continue
            n//=2
            if l<n:
                st.append((u*2, l, r, n))
            if r>n:
                st.append((u*2+1, l-n, r-n, n))
        return res

class SegmentTree:
    def __init__(self, input_arr):
        m = 1<<(len(input_arr).bit_length()-1)
        if m < len(input_arr): m<<=1
        self.m = m
        n = 1<<(len(input_arr[0]).bit_length()-1)
        if n < len(input_arr[0]): n<<=1
        self.n = n
        self.arr = arr =[None]*m + [SubTree(row) for row in input_arr] + [None]*(m-len(input_arr))
        
        for i in range(m-1,0,-1):
            l, r = self.arr[i*2], self.arr[i*2+1]
            arr[i] = SubTree([(l.arr[i] if l else 0)+(r.arr[i] if r else 0) for i in range(n, n*2)])
    
    def __list__(self):
        return list(map(lambda t: t.arr if t else [], self.arr))
    
    def __str__(self):
        return str(self.__list__())
    
    def update(self, x, y, val):
        u, bit = 1, self.m>>1
        while bit:
            self.arr[u].update(y, val)
            u*=2
            u+=bool(bit&x)
            bit>>=1
        self.arr[u].update(y, val)
            
            
    def query(self, x1, x2, y1, y2):
        res = 0
        st = [(1, x1, x2, self.m)]
        while st:
            u, x1, x2, m = st.pop()
            x1 = max(x1, 0)
            x2 = min(x2, m)
            if x2-x1==m:
                res+=self.arr[u].query(y1, y2)
                continue
            m//=2
            if x1<m:
                st.append((u*2, x1, x2, m))
            if x2>m:
                st.append((u*2+1, x1-m, x2-m, m))
        return res

if __name__ == '__main__':
    testcases, operations, m, n = 10, 10, 300, 300
    import random
    for t in range(testcases):
        arr = [[random.randint(0, n) for _ in range(n)] for _ in range(m)]
        tree = SegmentTree(arr)
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
        