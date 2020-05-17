screen_size = None


def flip_coords(point):
    """Converting pymunk coordinates to pygame"""
    return point[0], -point[1] + screen_size[1]


def sign(x):
    """Getting plus or minus sign of given value"""
    return 1 if x >= 0 else -1
