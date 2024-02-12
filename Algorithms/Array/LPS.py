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

s = "abbababbbab"
print(list(s))
print(create_lps(s))