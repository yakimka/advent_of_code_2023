import pytest

import support as sup


@pytest.fixture()
def matrix():
    return [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]


@pytest.fixture()
def graph(matrix):
    neighbors_cross = sup.max_bounds_closure(sup.neighbors_cross, matrix)

    return {
        (m, n): {(n_m, n_n): matrix[n_m][n_n] for n_m, n_n in neighbors_cross(m, n)}
        for m in range(len(matrix))
        for n in range(len(matrix[0]))
    }


def test_dijkstra(graph) -> None:
    source = (0, 0)

    result_dist, result_prev = sup.dijkstra(graph, source)

    assert result_dist == {
        (0, 0): 0,
        (0, 1): 2,
        (0, 2): 5,
        (1, 0): 4,
        (1, 1): 7,
        (1, 2): 11,
        (2, 0): 11,
        (2, 1): 15,
        (2, 2): 20,
    }
    assert result_prev == {
        (0, 0): None,
        (0, 1): (0, 0),
        (0, 2): (0, 1),
        (1, 0): (0, 0),
        (1, 1): (0, 1),
        (1, 2): (0, 2),
        (2, 0): (1, 0),
        (2, 1): (1, 1),
        (2, 2): (1, 2),
    }
