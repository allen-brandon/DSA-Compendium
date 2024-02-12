#Search for local maximum/minimum of a unimodal object
def tsearch(arr):
    n = len(arr)
    l, r = 0, len(arr)
    while r-l>2:
        m1, m2 = l+(r-l)//3, r-(r-l)//3
        # print(m1, m2)
        if arr[m1]<=arr[m2]:
            l = m1
        if arr[m1]>=arr[m2]:
            r = m2
    return max(range(l, r+1), key=arr.__getitem__)