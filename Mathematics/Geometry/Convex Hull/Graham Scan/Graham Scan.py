import numpy
import math
from functools import partial

#Doesn't Include Colinear Points
class GrahamScan:
    def __init__(self, points=None):
        if points:
            self.hull = self.scan(points)
        
    def scan(self, points):
        slope = lambda x1, y1, x2, y2: (y2-y1)/(x2-x1) if x1!=x2 else math.inf
        dist = lambda x1, y1, x2, y2: round(math.sqrt((x2-x1)**2+(y2-y1)**2), 5)
        angle = lambda x1, y1, x2, y2, x3, y3: numpy.cross([x2-x1, y2-y1], [x3-x1, y3-y1])
        first = min(points, key=lambda p: [p[1],p[0]])
        points.remove(first)
        if not points:
            self.hull = [first]
            return [first]
        polar_sort = lambda first, point: (slope(*first, *point)<0, slope(*first, *point), dist(*first, *point))
        points.sort(key=partial(polar_sort, first))
        points.append(first)
        st = [first]
        for tree in points:
            while len(st)>1 and angle(*st[-2], *st[-1], *tree)<=0:
                st.pop()
            st.append(tree)
        self.hull = st[1:]
        return st[1:]

### Testing ###
gc = GrahamScan()
test1 = [[0,2],[0,4],[0,5],[0,9],[2,1],[2,2],[2,3],[2,5],[3,1],[3,2],[3,6],[3,9],[4,2],[4,5],[5,8],[5,9],[6,3],[7,9],[8,1],[8,2],[8,5],[8,7],[9,0],[9,1],[9,6]]
print(gc.scan(test1))
test2 = [[3,0],[4,0],[5,0],[6,1],[7,2],[7,3],[7,4],[6,5],[5,5],[4,5],[3,5],[2,5],[1,4],[1,3],[1,2],[2,1],[4,2],[0,3]]
print(gc.scan(test2))
test3 = [[0,0],[0,1],[0,2],[1,2],[2,2],[3,2],[3,1],[3,0],[2,0],[1,0],[1,1],[3,3]]
print(gc.scan(test3))
test4 = [[0,2],[0,1],[0,0],[1,0],[2,0],[1,1]]
print(gc.scan(test4))