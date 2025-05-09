#Abstract Segment Tree
from operator import lt, le
class SegmentTree:
    def __init__(self, a, S, S_id, op, F, F_id, mapping, compose, S_inv=lambda x:x):
        self.n = n = 1<<(len(a).bit_length())-(len(a).bit_count()==1)
        self.arr = arr = [S_id]*n+[*map(S, a)]+[S_id]*(n-len(a))
        self.pend = pend = [F_id]*(n*2)
        self.op, self.mapping, self.compose = op, mapping, compose
        self.S_id, self.F_id, self.S_inv = S_id, F_id, S_inv
        for i in range(n-1,0,-1):
            arr[i]=op(arr[i*2], arr[i*2+1])
    def __str__(self):
        return str(list(self))
    def __iter__(self):
        self.flush_pending()
        return (self.S_inv(self.arr[i]) for i in range(self.n,self.n<<1))
    def flush_pending(self):
        [*map(self.prop, range(self.n*2))]     
    def prop(self, i):
        if self.pend[i] == self.F_id: return
        self.arr[i] = self.mapping(self.pend[i], self.arr[i])
        if i<self.n:
            self.pend[i*2] = self.compose(self.pend[i], self.pend[i*2])
            self.pend[i*2+1] = self.compose(self.pend[i], self.pend[i*2+1])
        self.pend[i]=self.F_id
        
    def update(self, l, r, x):
        '''update f(x, arr[l:r])'''
        n, arr, pend = self.n, self.arr, self.pend
        mapping, compose = self.mapping, self.compose
        l+=n
        r+=n
        l_copy = l
        r_inclusive=r-1
        for i in range(l.bit_length(), 0, -1):
            self.prop(l>>i)
            self.prop(r_inclusive>>i)
        while l<r:
            if l&1:
                self.pend[l]=compose(x, self.pend[l])
                l+=1
            if r&1:
                r-=1
                self.pend[r]=compose(x, self.pend[r])
            l>>=1
            r>>=1
        l, r = l_copy>>1, r_inclusive>>1
        while l:
            arr[l] = self.op(mapping(pend[l*2], arr[l*2]), mapping(pend[l*2+1], arr[l*2+1]))
            arr[r] = self.op(mapping(pend[r*2], arr[r*2]), mapping(pend[r*2+1], arr[r*2+1]))
            l>>=1
            r>>=1

    def query(self, l, r):
        '''op(arr[l:r])'''
        n, arr, pend = self.n, self.arr, self.pend
        op, mapping, compose = self.op, self.mapping, self.compose
        l, r = l+n, r+n
        r_inclusive = r-1
        res = self.S_id
        for i in range(l.bit_length(), 0, -1):
            self.prop(l>>i)
            self.prop(r_inclusive>>i)
        while l<r:
            if l&1:
                res = self.op(res, mapping(self.pend[l], self.arr[l]))
                l+=1
            if r&1:
                r-=1
                res = self.op(res, mapping(self.pend[r], self.arr[r]))
            l>>=1
            r>>=1
        return self.S_inv(res)
    
    
    def bisect_left(self, x, cmp=lt):
        '''Insertion Point for x in prefix (op must have prefix monotonicity)'''
        n, arr, pend = self.n, self.arr, self.pend
        mapping, compose = self.mapping, self.compose
        i = 1
        while i<n:
            self.prop(i)
            i<<=1
            if cmp(mapping(pend[i], arr[i]), x): i+=1
        self.prop(i)
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
# mod = 998244353
# S = lambda x: (x%mod, 1)
# S_id = (0,0)
# op = lambda l, r: ((l[0]+r[0])%mod, l[1]+r[1])
# F = lambda x, y: (x, y)
# F_id = (1, 0)
# mapping = lambda f, s: ((f[0]*s[0]+f[1]*s[1])%mod, s[1])
# compose = lambda f1, f2: ((f1[0]*f2[0])%mod, (f1[0]*f2[1]+f1[1])%mod)
# S_inv = lambda x: x[0]

# st = SegmentTree(a, S, S_id, op, F, F_id, mapping, compose)