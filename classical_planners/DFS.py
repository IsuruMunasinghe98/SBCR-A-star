from .common import Point

def find_path_dfs_2d_array(mat, src: Point, dest: Point):
    ROW = len(mat)
    COL = len(mat[0]) if ROW > 0 else 0

    def isValid(row: int, col: int):
        return 0 <= row < ROW and 0 <= col < COL

    rowNum = [-1, 0, 0, 1]
    colNum = [0, -1, 1, 0]

    if not isValid(src.x, src.y) or not isValid(dest.x, dest.y) or mat[src.x][src.y] != 1 or mat[dest.x][dest.y] != 1:
        return []

    visited = [[False for _ in range(COL)] for _ in range(ROW)]
    path_found_list = []

    def DFS(current: Point, target: Point, visited_grid, path):
        nonlocal ROW, COL, path_found_list
        if not isValid(current.x, current.y) or mat[current.x][current.y] != 1 or visited_grid[current.x][current.y]:
            return False

        visited_grid[current.x][current.y] = True
        path.append([current.x, current.y])  # Append as a list [row, column]

        if current.x == target.x and current.y == target.y:
            path_found_list.extend(path)
            return True

        for i in range(4):
            next_row, next_col = current.x + rowNum[i], current.y + colNum[i]
            next_point = Point(next_row, next_col)
            if DFS(next_point, target, visited_grid, path):
                return True

        path.pop()
        return False

    DFS(src, dest, visited, [])
    return path_found_list
