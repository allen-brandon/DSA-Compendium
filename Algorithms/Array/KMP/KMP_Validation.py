from random import randint
from string import ascii_lowercase

#Longest-Prefix-Suffix Array
#lps[i]: longest prefix of s that is a suffix of s[:i]
def create_lps(s):
    n = len(s)
    lps = [0]*n
    for i in range(1, n):
        j = i-1
        while j != lps[j] and s[i] != s[lps[j]]:
            j = max(0, lps[j]-1)
        if s[i] == s[lps[j]]:
            lps[i] = lps[j]+1
    return lps

#KMP
#kmp[i]: the substring s[i:i+len(w)] == w
def create_kmp(s, w):
    m, n = len(s), len(w)
    matches = [0]*m
    if n>m: return matches
    lps = create_lps(w)
    j = 0
    for i in range(m):
        if s[i] == w[j]:
            j+=1
            if j == n:
                #match found
                matches[i+1-j]=1
                j = lps[j-1]
        else:
            j = max(0, lps[j]-1)
    return matches

def brute_force(s, w):
    m, n = len(s), len(w)
    matches = [0]*m
    if n>m: return matches
    for i in range(m+1-n):
        if s[i:i+n] == w:
            matches[i] = 1
    return matches

#Will take ~4 seconds
for test in range(100):
    w = "".join([ascii_lowercase[randint(0, 25)] for _ in range((test//300)+1)])
    s = "".join([ascii_lowercase[randint(0, 25)] for _ in range(100000)])
    kmp = create_kmp(s, w)
    null = brute_force(s, w)
    if kmp != null:
        #This will never print
        print("something went wrong")
#All occurrences match