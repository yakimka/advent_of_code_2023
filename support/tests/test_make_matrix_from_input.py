import pytest

from support import make_matrix_from_input


@pytest.mark.parametrize(
    "input_s",
    [
        ".#.\n###",
        "\n.#.\n###",
        ".#.\n###\n",
        "\n.#.\n###\n",
        "\n\n.#.\n###\n\n",
    ],
)
def test_make_string_matrix_from_input(input_s) -> None:
    result = make_matrix_from_input(input_s)
    matrix, width, height = result

    assert matrix == [[".", "#", "."], ["#", "#", "#"]]
    assert width == 3
    assert height == 2


@pytest.mark.parametrize(
    "input_s,expected",
    [
        ("1 2\n22 33\n4 78", [[1, 2], [22, 33], [4, 78]]),
    ],
)
def test_make_int_matrix_from_input(input_s, expected) -> None:
    result = make_matrix_from_input(input_s, split_by=" ", cast_func=int)

    assert result == (expected, 2, 3)
