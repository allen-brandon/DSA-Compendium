#Find majority element
#O(n) time, O(1) space
def find_majority(arr):
    c = 0
    for y in arr:
        if not c: x = y
        c+=((x==y)<<1)-1
    return x

# from collections import Counter
# example = [1,1,6,2,5,3,4,4,4,8,7,4,4,8,7,4,4,4,4,4,4]
# print(example)
# print(Counter(example))
# print(find_majority(example))