def VLoSPS(grid, path):
    if not path:
        return []

    integer_path = []
    for point in path:
        if isinstance(point, (list, tuple)):
            x = int(round(point[0]))
            y = int(round(point[1]))
            # x = point[0]
            # y = point[1]
            integer_path.append((x, y))

    if len(integer_path) < 3:
        return integer_path

    simplified_path = [integer_path[0]]
    current_index = 0

    while current_index < len(integer_path) - 1:
        farthest = current_index + 1
        for j in range(len(integer_path) - 1, current_index, -1):
            p1 = integer_path[current_index]
            p2 = integer_path[j]
            visible = False

            if p1 == p2:
                visible = True
            elif p1[0] == p2[0]:
                y1, y2 = min(p1[1], p2[1]), max(p1[1], p2[1])
                visible = True
                for y in range(y1, y2 + 1):
                    if not (0 <= p1[0] < len(grid)) or not (0 <= y < len(grid[0])) or grid[p1[0]][y] != 1:
                        visible = False
                        break
            elif p1[1] == p2[1]:
                x1, x2 = min(p1[0], p2[0]), max(p1[0], p2[0])
                visible = True
                for x in range(x1, x2 + 1):
                    if not (0 <= x < len(grid)) or not (0 <= p1[1] < len(grid[0])) or grid[x][p1[1]] != 1:
                        visible = False
                        break

            if visible:
                farthest = j
                break

        simplified_path.append(integer_path[farthest])
        current_index = farthest

    return simplified_path
