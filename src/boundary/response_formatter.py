"""Format Boundary success responses for external consumers."""


class ResponseFormatter:
    """Serialize successful solver output as a fixed text contract."""

    @staticmethod
    def format_success(result: list[int]) -> str:
        """Return ``OK [r1,c1,n1,r2,c2,n2]`` without spaces inside the bracket."""
        payload = ",".join(str(value) for value in result)
        return f"OK [{payload}]"
