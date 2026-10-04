from dataclasses import dataclass
from pathlib import Path

from pylactate.model.raw import MeasurementRecord


@dataclass(frozen=True, slots=True)
class LactateTest:
    """
    Ein importierter Test.

    Enthält ausschließlich Rohdaten.
    """

    source_file: Path

    records: tuple[MeasurementRecord, ...]

    @property
    def load_unit(self) -> str:
        """
        Last-Einheit des Tests.
        """

        if not self.records:
            return ""

        return self.records[0].load_unit
