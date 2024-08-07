#### Hack Protection ####
# Heavily inspired by Alex Wice's RabinKarp class implementation
class PrefixHash:
    #Input a string encoded as an array (e.g. numbers bounded from 0-26)
    #Initialization is O(n)
    def __init__(self, arr):
        self.mod = mod = 455666777788888999999
        self.base = base = 37
        self.inv = inv = pow(base, mod-2, mod)
        self.pref = pref = [0]
        self.invpref = invpref = [1]
        pwr, invpwr = 1, 1
        hsh = 0
        for x in arr:
            hsh = (hsh+x*pwr)%mod
            pwr = (pwr*base)%mod
            invpwr = (invpwr*inv)%mod
            pref.append(hsh)
            invpref.append(invpwr)
    #Obtain the hash of a substring [l, ... r] in O(1)
    #Inclusive of l and r
    def query(self, l, r):
        return (self.pref[r+1]-self.pref[l])*self.invpref[l]%self.mod

### Notes ###
# 

#### No Hack Protection ####
# # Heavily inspired by Alex Wice's RabinKarp class implementation
# class PrefixHash:
#     #Input a string encoded as an array (e.g. numbers bounded from 0-26)
#     #Initialization is O(n)
#     def __init__(self, arr):
#         self.mod = mod = 455666777788888999999
#         self.base = base = 37
#         self.inv = inv = pow(base, mod-2, mod)
#         self.pref = pref = [0]
#         self.invpref = invpref = [1]
#         pwr, invpwr = 1, 1
#         hsh = 0
#         for x in arr:
#             hsh = (hsh+x*pwr)%mod
#             pwr = (pwr*base)%mod
#             invpwr = (invpwr*inv)%mod
#             pref.append(hsh)
#             invpref.append(invpwr)
#     #Obtain the hash of a substring [l, ... r] in O(1)
#     #Inclusive of l and r
#     def query(self, l, r):
#         return (self.pref[r+1]-self.pref[l])*self.invpref[l]%self.mod