import collections

class Solution1:
    def getFood(self, grid):
        m, n = len(grid), len(grid[0])

        def _is_valid(x, y):
            return 0 <= x < m and 0 <= y < n

        def neighbors(x1, y1):
            return [(x2, y2) for (x2, y2) in [(x1 - 1, y1), (x1 + 1, y1), (x1, y1 - 1), (x1, y1 + 1)]
                    if _is_valid(x2, y2)]

        start = (-1, -1)
        end = set()
        visited = set()

        for i in range(m):
            for j in range(n):
                if grid[i][j] == "*":
                    start = (i, j)
                if grid[i][j] == "#":
                    end.add((i, j))
                if grid[i][j] == "X":
                    visited.add((i, j))

        ans = 0
        queue = collections.deque([start])
        while queue:
            for _ in range(len(queue)):
                i1, j1 = queue.popleft()
                if (i1, j1) in end:
                    return ans
                for (i2, j2) in neighbors(i1, j1):
                    if (i2, j2) not in visited:
                        visited.add((i2, j2))
                        queue.append((i2, j2))
            ans += 1
        return -1


class Solution2:
    def getFood(self, grid):
        m, n = len(grid), len(grid[0])
        queue = []
        for i in range(m):
            for j in range(n):
                if grid[i][j] == "*":
                    queue.append((i, j))
                    grid[i][j] = 'X'
                    break
        # print(q)

        distance = 0
        while queue:
            print queue
            for _ in range(len(queue)):
                cur_x, cur_y = queue.pop(0)
                # print 'x1, y1:',x1, y1
                for nb_x, nb_y in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    # print 'x2,y2:',x2,y2
                    nb_x += cur_x
                    nb_y += cur_y
                    # print x2,y2
                    if nb_x < 0 or nb_x >= m or nb_y < 0 or nb_y >= n or grid[nb_x][nb_y] == "X":
                        continue
                    if grid[nb_x][nb_y] == "#":
                        return distance + 1
                    grid[nb_x][nb_y] = 'X'
                    queue.append((nb_x, nb_y))
                    # print q
            distance += 1
        return -1
grid = [
["X","X","X","X","X","X","X","X"],
["X","*","O","X","O","#","O","X"],
["X","O","O","X","O","O","X","X"],
["X","O","O","O","O","#","O","X"],
["X","X","X","X","X","X","X","X"]]

# s1=Solution1()
# print s1.getFood(grid)

s2=Solution2()
print s2.getFood(grid)

# print '****'
# for x in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#     print 'x2,y2:', x

def manhattan_dis(loc1, loc2):
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

x1 = (1,1)
x2 = (2,2)
# print(manhattan_dis(x1,x2))


def initMatrix1(x_len, y_len):
    m = []
    for x in range(0, x_len):
        line = []
        for y in range(0, y_len):
            line.append(0)
        m.append(line)
    return m

def initMatrix2(x_len, y_len):
    return [[0] * y_len for _ in range(x_len)]

def initMatrix3(x_len,y_len):
    return [(x,y) for x in range(x_len) for y in range(y_len)]
# print initMatrix1(4,5)
print "***"

all_loc = initMatrix3(20,11)
available_loc = [ i for i in all_loc if i not in [(0,0)]]
# print all_loc
# print available_loc

getAdjacent = ('West','East')

WALLS

# def ts(location, direction):
#     x = location[0]
#     y = location[1]
#
#     s = {'West': [x - 1, y],
#          'East': [x + 1, y],
#          'South': [x, y - 1],
#          'North': [x, y + 1]}
#
#     adj = list(getAdjacent(direction))
#     # [adj.remove(v) for v in adj if (s[v]['x'], s[v]['y'] in self.WALLS)]
#     [adj.remove(v) for v in adj if (s[v][0], s[v][1] is not in (0,0)]
#
#     move_info = [{'dir': direction,'p': 1.0 - (0.1 * len(adj)),'x': s[direction][0],'y': s[direction][1]}]
#
#     for k in adj: move_info.append({
#         'dir': k,
#         'p': 0.1,
#         'x': s[k]['x'],
#         'y': s[k]['y']})
#
#     return move_info

s = {'West': [x - 1, y],
    'East':  [x + 1, y],
    'South': [x, y - 1],
    'North': [x, y + 1]}

