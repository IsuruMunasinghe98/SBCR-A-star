import heapq
from .common import Cell

def find_dijkstra(grid, src, dest):
    ROW = len(grid)
    COL = len(grid[0]) if ROW > 0 else 0
    path = []

    def is_valid(row, col):
        return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

    def is_unblocked(grid, row, col):
        return grid[row][col] == 1

    def is_destination(row, col, dest):
        return row == dest[0] and col == dest[1]

    def trace_path(cell_details, dest):
        nonlocal path
        row = dest[0]
        col = dest[1]

        while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
            path.append((row, col))
            temp_row = cell_details[row][col].parent_i
            temp_col = cell_details[row][col].parent_j
            row = temp_row
            col = temp_col

        path.append((row, col))
        path.reverse()
        return path

    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
        print("Source or destination is invalid")
        return []

    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("Source or the destination is blocked")
        return []

    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
        return [src]

    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    i = src[0]
    j = src[1]
    cell_details[i][j].distance = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    found_dest = False
    result_path = []

    while open_list:
        p = heapq.heappop(open_list)

        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        if is_destination(i, j, dest):
            print("The destination cell is found")
            result_path = trace_path(cell_details, dest)
            found_dest = True
            return result_path

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                new_distance = cell_details[i][j].distance + 1.0

                if cell_details[new_i][new_j].distance == float('inf') or cell_details[new_i][new_j].distance > new_distance:
                    heapq.heappush(open_list, (new_distance, new_i, new_j))
                    cell_details[new_i][new_j].distance = new_distance
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j

    if not found_dest:
        print("Failed to find the destination cell")
    return []
