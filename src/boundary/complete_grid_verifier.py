"""Boundary verification for complete 4×4 magic squares."""

from dataclasses import dataclass

from src.boundary.domain_exception_mapping import boundary_error_code_for
from src.boundary.error_catalog import ERROR_CATALOG
from src.boundary.grid_validation import COMPLETE_GRID_POLICY, GridStructureValidator
from src.domain.constants import MAGIC_CONSTANT
from src.domain.magic_square_judge import MagicSquareJudge


@dataclass(frozen=True, slots=True)
class VerifySuccess:
    """Complete grid passed structural checks; includes magic verdict."""

    is_magic: bool
    magic_constant: int


@dataclass(frozen=True, slots=True)
class VerifyError:
    """Verification could not run because input violates Boundary contract."""

    code: str
    message: str


class CompleteGridVerifier:
    """Validate a filled grid and delegate magic-square judgment to Domain."""

    def __init__(self, judge: MagicSquareJudge | None = None) -> None:
        self._judge = judge if judge is not None else MagicSquareJudge()
        self._structure_validator = GridStructureValidator(COMPLETE_GRID_POLICY)

    def verify(self, grid: object) -> VerifySuccess | VerifyError:
        """Return whether a complete grid is a magic square, or a contract error."""
        structure_error = self._structure_validator.validate(grid)
        if structure_error is not None:
            return self._error(structure_error)

        assert isinstance(grid, list)
        typed_grid: list[list[int]] = grid

        try:
            is_magic = self._judge.is_magic(typed_grid)
        except Exception as exc:
            error_code = boundary_error_code_for(exc)
            if error_code is None:
                raise
            return self._error(error_code)

        return VerifySuccess(is_magic=is_magic, magic_constant=MAGIC_CONSTANT)

    def _error(self, code: str) -> VerifyError:
        return VerifyError(code=code, message=ERROR_CATALOG[code])
