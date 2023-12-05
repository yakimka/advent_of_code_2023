import pytest

from support import neighbors_cross, neighbors_cross_diag, neighbors_diag


@pytest.mark.parametrize(
    "coords,max_bounds,expected",
    [
        ((0, 0), None, [(1, 0), (0, 1)]),
        ((0, 0), (0, 0), []),
        ((1, 1), None, [(1, 0), (0, 1), (2, 1), (1, 2)]),
        ((1, 1), (1, 1), [(1, 0), (0, 1)]),
    ],
)
def test_neighbors_cross(coords, max_bounds, expected):
    x, y = coords

    result = neighbors_cross(x, y, max_bounds=max_bounds)

    assert list(result) == expected


@pytest.mark.parametrize(
    "coords,max_bounds,expected",
    [
        ((0, 0), None, [(1, 1)]),
        ((0, 0), (0, 0), []),
        ((1, 1), None, [(0, 0), (2, 0), (0, 2), (2, 2)]),
        ((1, 1), (1, 1), [(0, 0)]),
    ],
)
def test_neighbors_diag(coords, max_bounds, expected):
    x, y = coords

    result = neighbors_diag(x, y, max_bounds=max_bounds)

    assert list(result) == expected


@pytest.mark.parametrize(
    "coords,max_bounds,expected",
    [
        ((0, 0), None, [(1, 0), (0, 1), (1, 1)]),
        ((0, 0), (0, 0), []),
        (
            (1, 1),
            None,
            [(1, 0), (0, 1), (2, 1), (1, 2), (0, 0), (2, 0), (0, 2), (2, 2)],
        ),
        ((1, 1), (1, 1), [(1, 0), (0, 1), (0, 0)]),
    ],
)
def test_neighbors_cross_diag(coords, max_bounds, expected):
    x, y = coords

    result = neighbors_cross_diag(x, y, max_bounds=max_bounds)

    assert list(result) == expected
