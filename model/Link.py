class Link:
    def __init__(self, x1, y1, z1, x2, y2, z2, is_door, is_open, is_sentinel, is_ladder):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.is_door = is_door
        self.is_open = is_open
        self.is_sentinel = is_sentinel
        self.is_ladder = is_ladder
