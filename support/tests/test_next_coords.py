import pytest

from support import max_bounds_closure, neighbors_cross, next_coords


@pytest.fixture()
def matrix():
    return [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
    ]


@pytest.mark.parametrize(
    "coords,direction,expected",
    [
        ((0, 0), "up", None),
        ((0, 0), "down", (1, 0)),
        ((0, 0), "left", None),
        ((0, 0), "right", (0, 1)),
        ((0, 1), "up", None),
        ((0, 1), "down", (1, 1)),
        ((0, 1), "left", (0, 0)),
        ((0, 1), "right", (0, 2)),
        ((0, 4), "up", None),
        ((0, 4), "down", (1, 4)),
        ((0, 4), "left", (0, 3)),
        ((0, 4), "right", None),
        ((1, 0), "up", (0, 0)),
        ((1, 0), "down", (2, 0)),
        ((1, 0), "left", None),
        ((1, 0), "right", (1, 1)),
        ((1, 1), "up", (0, 1)),
        ((1, 1), "down", (2, 1)),
        ((1, 1), "left", (1, 0)),
        ((1, 1), "right", (1, 2)),
        ((1, 4), "up", (0, 4)),
        ((1, 4), "down", (2, 4)),
        ((1, 4), "left", (1, 3)),
        ((1, 4), "right", None),
        ((3, 0), "up", (2, 0)),
        ((3, 0), "down", None),
        ((3, 0), "left", None),
        ((3, 0), "right", (3, 1)),
        ((3, 1), "up", (2, 1)),
        ((3, 1), "down", None),
        ((3, 1), "left", (3, 0)),
        ((3, 1), "right", (3, 2)),
        ((3, 4), "up", (2, 4)),
        ((3, 4), "down", None),
    ],
)
def test_next_coords(matrix, coords, direction, expected):
    m, n = coords
    next_coords_func = max_bounds_closure(next_coords, matrix)

    result = next_coords_func(m, n, direction)

    assert result == expected


def test_max_bounds_closure_with_generator(matrix):
    neighbors_cross_func = max_bounds_closure(neighbors_cross, matrix)

    result = neighbors_cross_func(1, 3)

    assert list(result) == [(1, 2), (0, 3), (2, 3), (1, 4)]
