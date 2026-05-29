"""Boundary resolver — validate input and delegate to Domain."""

from dataclasses import dataclass

from src.boundary.domain_exception_mapping import boundary_error_code_for
from src.boundary.error_catalog import ERROR_CATALOG
from src.boundary.input_validator import InputValidator
from src.domain.solve_partial_grid import SolvePartialGrid


@dataclass(frozen=True, slots=True)
class BoundarySuccess:
    """Successful Boundary resolution carrying the Domain result vector."""

    result: list[int]


@dataclass(frozen=True, slots=True)
class BoundaryError:
    """Boundary or Domain failure with a fixed error contract."""

    code: str
    message: str


class BoundaryResolver:
    """Orchestrate validation and Domain execution at the system edge."""

    def __init__(self) -> None:
        self._validator = InputValidator()
        self._use_case = SolvePartialGrid()

    def solve(self, grid: object) -> BoundarySuccess | BoundaryError:
        """Validate *grid* and return either a success vector or an error."""
        validation_error = self._validator.validate(grid)
        if validation_error is not None:
            return BoundaryError(
                code=validation_error.code,
                message=validation_error.message,
            )

        assert isinstance(grid, list)

        try:
            result = self._use_case.execute(grid)
        except Exception as exc:
            error_code = boundary_error_code_for(exc)
            if error_code is None:
                raise
            return BoundaryError(
                code=error_code,
                message=ERROR_CATALOG[error_code],
            )

        return BoundarySuccess(result=result)
