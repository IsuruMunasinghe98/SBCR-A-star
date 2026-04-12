from collections import deque
from .common import Point, queueNode

def find_shortest_path_bfs(mat, src: Point, dest: Point):
    ROW = len(mat)
    COL = len(mat[0]) if ROW > 0 else 0

    def isValid(row: int, col: int):
        return 0 <= row < ROW and 0 <= col < COL

    rowNum = [-1, 0, 0, 1]
    colNum = [0, -1, 1, 0]

    if not isValid(src.x, src.y) or not isValid(dest.x, dest.y) or mat[src.x][src.y] != 1 or mat[dest.x][dest.y] != 1:
        return -1, []

    visited = [[False for _ in range(COL)] for _ in range(ROW)]
    visited[src.x][src.y] = True

    q = deque()
    q.append(queueNode(src, 0, [(src.x, src.y)]))

    while q:
        curr = q.popleft()
        pt = curr.pt

        if pt.x == dest.x and pt.y == dest.y:
            return curr.dist, curr.path

        for i in range(4):
            row, col = pt.x + rowNum[i], pt.y + colNum[i]
            if isValid(row, col) and mat[row][col] == 1 and not visited[row][col]:
                visited[row][col] = True
                q.append(queueNode(Point(row, col), curr.dist + 1, curr.path + [(row, col)]))

    return -1, []
