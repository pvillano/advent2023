NEWS_XY = ((0, 1), (1, 0), (-1, 0), (0, -1))
NEWS_RC = ((-1, 0), (0, 1), (0, -1), (1, 0))


def transpose(iterable):
    iterable = list(iterable)
    assert len(set(map(len, iterable))) == 1
    return list(zip(*iterable))


def rotate_clockwise(grid):
    return transpose(reversed(grid))


def rotate_counterclockwise(grid):
    return reversed(transpose(grid))
