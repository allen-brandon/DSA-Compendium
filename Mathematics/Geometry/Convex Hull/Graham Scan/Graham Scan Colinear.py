# import numpy
# import math
# from functools import partial

# #Includes Colinear Points
# class GrahamScan:
#     def __init__(self, points=None):
#         if points:
#             self.hull = self.scan(points)
        
#     def scan(self, points):
#         slope = lambda x1, y1, x2, y2: (y2-y1)/(x2-x1) if x1!=x2 else math.inf
#         dist = lambda x1, y1, x2, y2: round(math.sqrt((x2-x1)**2+(y2-y1)**2), 5)
#         angle = lambda x1, y1, x2, y2, x3, y3: numpy.cross([x2-x1, y2-y1], [x3-x1, y3-y1])
#         slopekey = lambda first, point: (slope(*first, *point)<0, slope(*first, *point))
#         first = min(points, key=lambda p: [p[1],p[0]])
#         points.remove(first)
#         if not points:
#             self.hull = [first]
#             return [first]
#         second = min(points, key=partial(slopekey, first))
#         polar_sort = lambda first, point: (slope(*first, *point)<0, slope(*first, *point), (dist(*first, *point)*((slopekey(first, second)==slopekey(first, point))*2-1)))
#         points.sort(key=partial(polar_sort, first))
#         points.append(first)
#         st = [first]
#         for tree in points:
#             while len(st)>1 and angle(*st[-2], *st[-1], *tree)<0:
#                 st.pop()
#             st.append(tree)
#         self.hull = st[1:]
#         return st[1:]
    
#CSES: Convex Hull
# from numpy import cross
from math import inf
import sys
input = sys.stdin.readline
pr = sys.stdout.write
class GrahamScan:
    
    def __init__(self, a=None):
        if a:
            self.hull = self.scan(a)
    
    def scan(self, a):
        #utility functions
        slope = lambda x0, y0, x1, y1: (y1-y0)/(x1-x0) if x0!=x1 else inf
        #if no numpy:
        cross = lambda v0, v1: v0[0]*v1[1]-v1[0]*v0[1]
        concave = lambda x0, y0, x1, y1, x2, y2: cross([x1-x0,y1-y0],[x2-x0,y2-y0])<0
        dist = lambda x1, y1, x2, y2: round((x2-x1)**2+(y2-y1)**2**(1/2), 5)
        
        #polar sort
        first = min(a, key=lambda p: [p[1],p[0]])
        a.remove(first)
        second = min(a, key = lambda p: (slope(*first, *p)<0, slope(*first, *p)))
        polar_key = lambda p: (slope(*first, *p)<0, slope(*first, *p), dist(*first, *p) if slope(*first, *p) == slope(*first, *second) else -dist(*first, *p))
        a.sort(key=polar_key)
        
        #build hull
        st = [first]
        for p in a:
            while len(st)>1 and concave(*st[-2],*st[-1],*p):
                st.pop()
            st.append(p)
        self.hull = st
        return st
k = int(input())
a = []
for _ in range(k):
    a.append([*map(int, input().split())])
gc = GrahamScan(a)
pr(str(len(gc.hull)) + '\n')
for x, y in gc.hull:
    pr(str(x) + ' ' + str(y) + '\n')

### Testing ###
# gc = GrahamScan()
# test1 = [[0,2],[0,4],[0,5],[0,9],[2,1],[2,2],[2,3],[2,5],[3,1],[3,2],[3,6],[3,9],[4,2],[4,5],[5,8],[5,9],[6,3],[7,9],[8,1],[8,2],[8,5],[8,7],[9,0],[9,1],[9,6]]
# print(gc.scan(test1))
# test2 = [[3,0],[4,0],[5,0],[6,1],[7,2],[7,3],[7,4],[6,5],[5,5],[4,5],[3,5],[2,5],[1,4],[1,3],[1,2],[2,1],[4,2],[0,3]]
# print(gc.scan(test2))
# test3 = [[0,0],[0,1],[0,2],[1,2],[2,2],[3,2],[3,1],[3,0],[2,0],[1,0],[1,1],[3,3]]
# print(gc.scan(test3))
# test4 = [[0,2],[0,1],[0,0],[1,0],[2,0],[1,1]]
# print(gc.scan(test4))