"""Golden Master solver outputs — captured from Green runtime (2026-05-29).

Do not edit by hand; regenerate by re-running the capture script against
``SolvePartialGrid``, ``BoundaryResolver``, and ``ResponseFormatter``.
"""

from typing import Final, TypedDict

from tests.fixtures.error_catalog import ERROR_CATALOG
from tests.fixtures.grids import (
    GRID_CORNER_BLANK_0_0,
    GRID_MISSING_15_16,
    GRID_MISSING_3_7,
    GRID_PUZZLE_SECOND_TRIAL,
    GRID_UNSOLVABLE,
    VALID_GRID_TWO_BLANKS,
)


class BoundarySuccessRecord(TypedDict):
    """Serialized Boundary success response."""

    kind: str
    result: list[int]


class BoundaryErrorRecord(TypedDict):
    """Serialized Boundary error response."""

    kind: str
    code: str
    message: str


class GoldenMasterSuccess(TypedDict):
    """Golden Master record for a solvable fixture."""

    ac_ids: list[str]
    test_ids: list[str]
    domain_result: list[int]
    formatted: str
    boundary: BoundarySuccessRecord


class GoldenMasterFailure(TypedDict):
    """Golden Master record for an unsolvable fixture."""

    ac_ids: list[str]
    test_ids: list[str]
    domain_exception: str
    boundary: BoundaryErrorRecord


GoldenMasterRecord = GoldenMasterSuccess | GoldenMasterFailure

_DOMAIN_UNSOLVABLE_MESSAGE: Final[str] = ERROR_CATALOG["DOMAIN_UNSOLVABLE"]

GOLDEN_MASTER_GRIDS: Final[dict[str, list[list[int]]]] = {
    "VALID_GRID_TWO_BLANKS": VALID_GRID_TWO_BLANKS,
    "GRID_PUZZLE_SECOND_TRIAL": GRID_PUZZLE_SECOND_TRIAL,
    "GRID_CORNER_BLANK_0_0": GRID_CORNER_BLANK_0_0,
    "GRID_MISSING_15_16": GRID_MISSING_15_16,
    "GRID_MISSING_3_7": GRID_MISSING_3_7,
    "GRID_UNSOLVABLE": GRID_UNSOLVABLE,
}

GOLDEN_MASTER_SOLVER_OUTPUTS: Final[dict[str, GoldenMasterRecord]] = {
    "VALID_GRID_TWO_BLANKS": {
        "ac_ids": ["AC-US-05-06", "OC-1", "OC-2", "OC-3", "OC-4", "OC-5", "OC-6"],
        "test_ids": ["DT-05", "IT-01", "RG-US-05"],
        "domain_result": [2, 3, 7, 4, 4, 16],
        "formatted": "OK [2,3,7,4,4,16]",
        "boundary": {"kind": "success", "result": [2, 3, 7, 4, 4, 16]},
    },
    "GRID_PUZZLE_SECOND_TRIAL": {
        "ac_ids": ["AC-US-05-04", "IT-02"],
        "test_ids": ["IT-02", "AC-US-05-04"],
        "domain_result": [2, 3, 7, 3, 1, 3],
        "formatted": "OK [2,3,7,3,1,3]",
        "boundary": {"kind": "success", "result": [2, 3, 7, 3, 1, 3]},
    },
    "GRID_CORNER_BLANK_0_0": {
        "ac_ids": ["AC-US-05-08", "SV-04"],
        "test_ids": ["DT-05", "AC-US-05-08"],
        "domain_result": [1, 1, 1, 4, 4, 16],
        "formatted": "OK [1,1,1,4,4,16]",
        "boundary": {"kind": "success", "result": [1, 1, 1, 4, 4, 16]},
    },
    "GRID_MISSING_15_16": {
        "ac_ids": ["AC-US-05-11"],
        "test_ids": ["AC-US-05-11"],
        "domain_result": [1, 2, 15, 4, 4, 16],
        "formatted": "OK [1,2,15,4,4,16]",
        "boundary": {"kind": "success", "result": [1, 2, 15, 4, 4, 16]},
    },
    "GRID_MISSING_3_7": {
        "ac_ids": ["AC-US-05-10", "EC-5"],
        "test_ids": ["GM-GRID_MISSING_3_7"],
        "domain_exception": "UnsolvableGrid",
        "boundary": {
            "kind": "error",
            "code": "DOMAIN_UNSOLVABLE",
            "message": _DOMAIN_UNSOLVABLE_MESSAGE,
        },
    },
    "GRID_UNSOLVABLE": {
        "ac_ids": ["AC-US-05-10", "EC-5", "IT-06"],
        "test_ids": ["IT-06", "RG-US-05", "DT-05"],
        "domain_exception": "UnsolvableGrid",
        "boundary": {
            "kind": "error",
            "code": "DOMAIN_UNSOLVABLE",
            "message": _DOMAIN_UNSOLVABLE_MESSAGE,
        },
    },
}
