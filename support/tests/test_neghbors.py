from functools import partial

import pytest

from support import (
    filter_neighbors,
    neighbors_cross,
    neighbors_cross_diag,
    neighbors_diag,
)


@pytest.mark.parametrize(
    "coords,filter_gen,expected",
    [
        ((0, 0), None, [(0, -1), (-1, 0), (1, 0), (0, 1)]),
        ((0, 0), partial(filter_neighbors, max_bounds=(0, 0)), []),
        ((1, 1), None, [(1, 0), (0, 1), (2, 1), (1, 2)]),
        ((1, 1), partial(filter_neighbors, max_bounds=(1, 1)), [(1, 0), (0, 1)]),
    ],
)
def test_neighbors_cross(coords, filter_gen, expected):
    x, y = coords

    result = neighbors_cross(x, y, filter_gen=filter_gen)

    assert list(result) == expected


@pytest.mark.parametrize(
    "coords,filter_gen,expected",
    [
        ((0, 0), None, [(-1, -1), (1, -1), (-1, 1), (1, 1)]),
        ((0, 0), partial(filter_neighbors, max_bounds=(0, 0)), []),
        ((1, 1), None, [(0, 0), (2, 0), (0, 2), (2, 2)]),
        ((1, 1), partial(filter_neighbors, max_bounds=(1, 1)), [(0, 0)]),
    ],
)
def test_neighbors_diag(coords, filter_gen, expected):
    x, y = coords

    result = neighbors_diag(x, y, filter_gen=filter_gen)

    assert list(result) == expected


@pytest.mark.parametrize(
    "coords,filter_gen,expected",
    [
        (
            (0, 0),
            None,
            [(0, -1), (-1, 0), (1, 0), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)],
        ),
        ((0, 0), partial(filter_neighbors, max_bounds=(0, 0)), []),
        (
            (1, 1),
            None,
            [(1, 0), (0, 1), (2, 1), (1, 2), (0, 0), (2, 0), (0, 2), (2, 2)],
        ),
        (
            (1, 1),
            partial(filter_neighbors, max_bounds=(1, 1)),
            [(1, 0), (0, 1), (0, 0)],
        ),
    ],
)
def test_neighbors_cross_diag(coords, filter_gen, expected):
    x, y = coords

    result = neighbors_cross_diag(x, y, filter_gen=filter_gen)

    assert list(result) == expected
