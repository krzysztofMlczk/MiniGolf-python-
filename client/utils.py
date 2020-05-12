def flipy(y):
    """Converting pymunk coordinates to pygame"""
    return -y + 900


def sign(x):
    """Getting plus or minus sign of given value"""
    return 1 if x >= 0 else -1
