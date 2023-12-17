import pytest

from support import num_of_prev_coords

MAX_BOUNDS = (5, 10)


@pytest.mark.parametrize(
    "coords,direction,max_bounds,expected",
    [
        ((0, 0), "up", MAX_BOUNDS, 0),
        ((0, 0), "left", MAX_BOUNDS, 0),
        ((0, 0), "down", MAX_BOUNDS, 5),
        ((0, 0), "right", MAX_BOUNDS, 10),
        ((0, 1), "up", MAX_BOUNDS, 0),
        ((0, 1), "left", MAX_BOUNDS, 1),
        ((0, 1), "down", MAX_BOUNDS, 5),
        ((0, 1), "right", MAX_BOUNDS, 9),
        ((0, 9), "up", MAX_BOUNDS, 0),
        ((0, 9), "left", MAX_BOUNDS, 9),
        ((0, 9), "down", MAX_BOUNDS, 5),
        ((0, 9), "right", MAX_BOUNDS, 1),
        ((1, 0), "up", MAX_BOUNDS, 1),
        ((1, 0), "left", MAX_BOUNDS, 0),
        ((1, 0), "down", MAX_BOUNDS, 4),
        ((1, 0), "right", MAX_BOUNDS, 10),
        ((1, 1), "up", MAX_BOUNDS, 1),
        ((1, 1), "left", MAX_BOUNDS, 1),
        ((1, 1), "down", MAX_BOUNDS, 4),
        ((1, 1), "right", MAX_BOUNDS, 9),
        ((1, 9), "up", MAX_BOUNDS, 1),
        ((1, 9), "left", MAX_BOUNDS, 9),
        ((1, 9), "down", MAX_BOUNDS, 4),
        ((1, 9), "right", MAX_BOUNDS, 1),
        ((4, 0), "up", MAX_BOUNDS, 4),
        ((4, 0), "left", MAX_BOUNDS, 0),
        ((4, 0), "down", MAX_BOUNDS, 1),
        ((4, 0), "right", MAX_BOUNDS, 10),
        ((4, 1), "up", MAX_BOUNDS, 4),
        ((4, 1), "left", MAX_BOUNDS, 1),
        ((4, 1), "down", MAX_BOUNDS, 1),
        ((4, 1), "right", MAX_BOUNDS, 9),
        ((4, 9), "up", MAX_BOUNDS, 4),
    ],
)
def test_num_of_prev_coords(coords, direction, max_bounds, expected):
    m, n = coords

    result = num_of_prev_coords(m, n, direction, max_bounds=max_bounds)

    assert result == expected
