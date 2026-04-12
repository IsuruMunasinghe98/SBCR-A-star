class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.distance = float('inf')
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0.0

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class queueNode:
    def __init__(self, pt: Point, dist: int, path: list):
        self.pt = pt
        self.dist = dist
        self.path = path
