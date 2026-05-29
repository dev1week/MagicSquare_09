"""PyQt6 main window for Magic Square solve and verify."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.boundary.complete_grid_verifier import (
    CompleteGridVerifier,
    VerifyError,
    VerifySuccess,
)
from src.boundary.resolver import BoundaryError, BoundaryResolver, BoundarySuccess
from src.boundary.response_formatter import ResponseFormatter
from src.boundary.ui.grid_io import (
    GRID_SIZE,
    GridParseError,
    apply_solution,
    grid_to_cell_texts,
    read_grid,
)
from src.boundary.ui.samples import SAMPLE_MAGIC_SQUARE, SAMPLE_PUZZLE

_STATUS_INFO = "color: #1f4b7a;"
_STATUS_SUCCESS = "color: #1b6b2f; font-weight: bold;"
_STATUS_ERROR = "color: #a11b1b; font-weight: bold;"


class GridEditor(QWidget):
    """Editable 4×4 grid of line edits."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._cells: list[list[QLineEdit]] = []
        layout = QGridLayout(self)
        layout.setSpacing(6)

        font = QFont()
        font.setPointSize(14)

        for row in range(GRID_SIZE):
            row_cells: list[QLineEdit] = []
            for col in range(GRID_SIZE):
                cell = QLineEdit()
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setMaxLength(2)
                cell.setFixedSize(52, 40)
                cell.setFont(font)
                cell.setPlaceholderText("·")
                layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self._cells.append(row_cells)

    def set_grid(self, grid: list[list[int]]) -> None:
        """Populate cells from a 4×4 integer grid."""
        texts = grid_to_cell_texts(grid)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self._cells[row][col].setText(texts[row][col])

    def clear_grid(self) -> None:
        """Clear all cells."""
        for row in self._cells:
            for cell in row:
                cell.clear()

    def read_grid(self) -> list[list[int]]:
        """Read current cell values as integers."""
        texts = [[cell.text() for cell in row] for row in self._cells]
        return read_grid(texts)

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable editing."""
        for row in self._cells:
            for cell in row:
                cell.setEnabled(enabled)


class SolveTab(QWidget):
    """Solve a partial grid with exactly two blank cells."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._resolver = BoundaryResolver()

        root = QVBoxLayout(self)
        hint = QLabel(
            "Enter a 4×4 grid with exactly two blank cells (empty or 0). "
            "Values 1–16 must not repeat."
        )
        hint.setWordWrap(True)
        root.addWidget(hint)

        self._editor = GridEditor()
        root.addWidget(self._editor, alignment=Qt.AlignmentFlag.AlignCenter)

        button_row = QHBoxLayout()
        self._solve_button = QPushButton("Solve")
        self._sample_button = QPushButton("Load sample")
        self._clear_button = QPushButton("Clear")
        button_row.addWidget(self._solve_button)
        button_row.addWidget(self._sample_button)
        button_row.addWidget(self._clear_button)
        button_row.addStretch()
        root.addLayout(button_row)

        self._status = QLabel("Ready.")
        self._status.setWordWrap(True)
        root.addWidget(self._status)
        root.addStretch()

        self._solve_button.clicked.connect(self._on_solve)
        self._sample_button.clicked.connect(self._on_load_sample)
        self._clear_button.clicked.connect(self._on_clear)

    def _set_status(self, text: str, level: str = "info") -> None:
        style = {
            "info": _STATUS_INFO,
            "success": _STATUS_SUCCESS,
            "error": _STATUS_ERROR,
        }[level]
        self._status.setText(text)
        self._status.setStyleSheet(style)

    def _on_load_sample(self) -> None:
        self._editor.set_grid(SAMPLE_PUZZLE)
        self._set_status("Sample puzzle loaded. Two blanks at (2,3) and (4,4).")

    def _on_clear(self) -> None:
        self._editor.clear_grid()
        self._set_status("Grid cleared.")

    def _on_solve(self) -> None:
        try:
            grid = self._editor.read_grid()
        except GridParseError as error:
            self._set_status(error.message, level="error")
            return

        result = self._resolver.solve(grid)
        if isinstance(result, BoundaryError):
            self._set_status(f"{result.code}: {result.message}", level="error")
            return

        assert isinstance(result, BoundarySuccess)
        filled = apply_solution(grid, result.result)
        self._editor.set_grid(filled)
        formatted = ResponseFormatter.format_success(result.result)
        r1, c1, n1, r2, c2, n2 = result.result
        self._set_status(
            f"Solved. {formatted}\n"
            f"Placed {n1} at ({r1},{c1}), {n2} at ({r2},{c2}).",
            level="success",
        )


class VerifyTab(QWidget):
    """Verify a complete 4×4 magic square."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._verifier = CompleteGridVerifier()

        root = QVBoxLayout(self)
        hint = QLabel(
            "Enter a complete 4×4 grid using numbers 1–16 exactly once (no blanks)."
        )
        hint.setWordWrap(True)
        root.addWidget(hint)

        self._editor = GridEditor()
        root.addWidget(self._editor, alignment=Qt.AlignmentFlag.AlignCenter)

        button_row = QHBoxLayout()
        self._verify_button = QPushButton("Verify")
        self._sample_button = QPushButton("Load magic square")
        self._clear_button = QPushButton("Clear")
        button_row.addWidget(self._verify_button)
        button_row.addWidget(self._sample_button)
        button_row.addWidget(self._clear_button)
        button_row.addStretch()
        root.addLayout(button_row)

        self._status = QLabel("Ready.")
        self._status.setWordWrap(True)
        root.addWidget(self._status)
        root.addStretch()

        self._verify_button.clicked.connect(self._on_verify)
        self._sample_button.clicked.connect(self._on_load_sample)
        self._clear_button.clicked.connect(self._on_clear)

    def _set_status(self, text: str, level: str = "info") -> None:
        style = {
            "info": _STATUS_INFO,
            "success": _STATUS_SUCCESS,
            "error": _STATUS_ERROR,
        }[level]
        self._status.setText(text)
        self._status.setStyleSheet(style)

    def _on_load_sample(self) -> None:
        self._editor.set_grid(SAMPLE_MAGIC_SQUARE)
        self._set_status("Known valid magic square loaded.")

    def _on_clear(self) -> None:
        self._editor.clear_grid()
        self._set_status("Grid cleared.")

    def _on_verify(self) -> None:
        try:
            grid = self._editor.read_grid()
        except GridParseError as error:
            self._set_status(error.message, level="error")
            return

        if any(value == 0 for row in grid for value in row):
            self._set_status(
                "Verification requires a complete grid with no blank cells.",
                level="error",
            )
            return

        result = self._verifier.verify(grid)
        if isinstance(result, VerifyError):
            self._set_status(f"{result.code}: {result.message}", level="error")
            return

        assert isinstance(result, VerifySuccess)
        if result.is_magic:
            self._set_status(
                f"Valid magic square. All line sums equal {result.magic_constant}.",
                level="success",
            )
        else:
            self._set_status(
                f"Not a magic square. Each row, column, and diagonal must sum to "
                f"{result.magic_constant}.",
                level="error",
            )


class MainWindow(QMainWindow):
    """Application main window with Solve and Verify tabs."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Magic Square 4×4")
        self.setMinimumSize(420, 380)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        title = QLabel("Magic Square 4×4")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.addTab(SolveTab(), "Solve puzzle")
        tabs.addTab(VerifyTab(), "Verify")
        layout.addWidget(tabs)

        about = QLabel(
            "Solve: fill two blanks to complete a magic square (sum = 34).\n"
            "Verify: check whether a full grid is a valid magic square."
        )
        about.setWordWrap(True)
        about.setStyleSheet("color: #555;")
        layout.addWidget(about)
