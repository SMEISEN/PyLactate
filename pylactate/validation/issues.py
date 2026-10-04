from dataclasses import dataclass


@dataclass(slots=True)
class ValidationIssue:
    """
    Ergebnis einer Validierung.
    """

    severity: str

    message: str

    measurement_mid: str | None = None
