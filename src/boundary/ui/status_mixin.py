"""Shared status label styling for PyQt6 tabs."""

from PyQt6.QtWidgets import QLabel, QVBoxLayout

_STATUS_INFO = "color: #1f4b7a;"
_STATUS_SUCCESS = "color: #1b6b2f; font-weight: bold;"
_STATUS_ERROR = "color: #a11b1b; font-weight: bold;"


class StatusMixin:
    """Provide a styled status label and setter for tab widgets."""

    _status: QLabel

    def _init_status_label(self, root: QVBoxLayout) -> None:
        """Attach a ready status label to *root*."""
        self._status = QLabel("Ready.")
        self._status.setWordWrap(True)
        root.addWidget(self._status)

    def _set_status(self, text: str, level: str = "info") -> None:
        """Update status text and color level (info, success, error)."""
        style = {
            "info": _STATUS_INFO,
            "success": _STATUS_SUCCESS,
            "error": _STATUS_ERROR,
        }[level]
        self._status.setText(text)
        self._status.setStyleSheet(style)
