"""Build OC-1~6 solution vectors from domain placement results."""


def to_solution_vector(
    first_blank: tuple[int, int],
    second_blank: tuple[int, int],
    first_number: int,
    second_number: int,
) -> list[int]:
    """Return ``[r1, c1, n1, r2, c2, n2]`` using 1-indexed coordinates."""
    return [
        first_blank[0] + 1,
        first_blank[1] + 1,
        first_number,
        second_blank[0] + 1,
        second_blank[1] + 1,
        second_number,
    ]
