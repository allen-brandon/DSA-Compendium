_mod = 344555666677777
_base = 37
_inv = pow(_base, _mod-2, _mod)
_p_pref, _inv_pref = [1], [1]
class PrefixHash:
    #Input a string encoded as an array (e.g. numbers bounded from 0-26)
    #Initialization is O(n)
    def __init__(self, arr):
        self.mod = _mod
        self.pref = pref = [0]
        hsh = 0
        for i, x in enumerate(arr):
            #Extend global modular prefix if needed
            if len(_p_pref) <= i+1:
                _p_pref.append((_p_pref[-1]*_base)%_mod)
                _inv_pref.append((_inv_pref[-1]*_inv)%_mod)
            hsh = (hsh+x*_p_pref[i+1])%_mod
            pref.append(hsh)
    #Obtain the hash of a substring [l, ... r] in O(1)
    #Inclusive of l and r
    def query(self, l, r):
        return (self.pref[r+1]-self.pref[l])*_inv_pref[l]%self.mod
    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return self.query(idx.start, idx.stop-1)
        return self.query(idx, idx)