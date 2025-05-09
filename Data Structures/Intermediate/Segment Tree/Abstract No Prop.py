#Abstract Segment Tree
from operator import lt, le
class SegmentTree:
    def __init__(self, a, S, S_id, op, F, F_id, mapping, compose, S_inv=lambda x:x):
        #smallest pow of 2 >= len(a)
        self.n = n = 1<<(len(a).bit_length())-(len(a).bit_count()==1)
        self.arr = arr = [S_id]*n+[*map(S, a)]+[S_id]*(n-len(a))
        self.op, self.mapping = op, mapping
        self.S_id, self.S_inv = S_id, S_inv
        for i in range(n-1,0,-1):
            arr[i]=op(arr[i*2], arr[i*2+1])
    def __str__(self):
        return str(list(self))
    def __iter__(self):
        return (self.S_inv(self.arr[i]) for i in range(self.n,self.n<<1))   
        
    def update(self, i, x):
        '''update f(x, arr[l:r])'''
        n, arr, mapping = self.n, self.arr, self.mapping
        i+=n
        arr[i] = mapping(x, arr[i])
        while i:
            i>>=1
            arr[i] = self.op(arr[i*2], arr[i*2+1])

    def query(self, l, r):
        '''op(arr[l:r])'''
        n, arr = self.n, self.arr
        op, mapping = self.op, self.mapping
        l, r = l+n, r+n
        r_inclusive = r-1
        res = self.S_id
        while l<r:
            if l&1:
                res = self.op(res, arr[l])
                l+=1
            if r&1:
                r-=1
                res = self.op(res, arr[l])
            l>>=1
            r>>=1
        return self.S_inv(res)
    
    
    def bisect_left(self, x, cmp=lt):
        '''Insertion Point for x in prefix (op must have prefix monotonicity)'''
        n, arr, mapping = self.n, self.arr, self.mapping
        i = 1
        while i<n:
            i<<=1
            if cmp(arr[i], x): i+=1
        return n if cmp(arr[i], x) else i-n
    
    def bisect_right(self, x, cmp=le):
        return self.bisect_left(x, cmp)
    
    
#Preset structs

#op: max, map: set
# S = lambda x: x
# S_id = -inf
# S_inv = lambda x: x
# op = max
# F = int
# F_id = None
# mapping = lambda f, s: s if f is None else f
# compose = lambda f1, f2: f2 if f1 is None else f1        

#op: sum, map: add (elements are val + subtree pop)
# S = lambda x: (x,1)
# S_id = (0,0)
# S_inv = lambda x: x[0]
# op = lambda l, r: (l[0]+r[0], l[1]+r[1])
# F = int
# F_id = 0
# mapping = lambda f, s: [s[0]+f*s[1], s[1]]
# compose = add

#op: sum%998244353 map: affine (elements are val + subtree pop)
mod = 998244353
S = lambda x: (x%mod, 1)
S_id = (0,0)
op = lambda l, r: ((l[0]+r[0])%mod, l[1]+r[1])
F = lambda x, y: (x, y)
F_id = (1, 0)
mapping = lambda f, s: ((f[0]*s[0]+f[1]*s[1])%mod, s[1])
compose = lambda f1, f2: ((f1[0]*f2[0])%mod, (f1[0]*f2[1]+f1[1])%mod)
S_inv = lambda x: x[0]

import sys
print = lambda x: sys.stdout.write(str(x)+'\n')
inp = sys.stdin.read().split('\n')
n, q = map(int, inp[0].split())
a = [*map(int, inp[1].split())]
st = SegmentTree(a, S, S_id, op, F, F_id, mapping, compose, S_inv)
for i in range(q):
    query = [*map(int, inp[i+2].split())]
    if query[0]:
        l, r = query[1:]
        print(st.query(l, r))
    else:
        l, r, b, c = query[1:]
        st.update(l, r, (b, c))