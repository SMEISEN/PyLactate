from dataclasses import dataclass
from datetime import date, time


@dataclass(frozen=True, slots=True)
class MeasurementRecord:
    """
    1:1-Abbildung einer CSV-Zeile.

    Diese Daten werden niemals verändert.
    """

    mid: str
    mem_pos: str

    date: date
    time: time

    test_type: str

    step_length: float | None

    load: float
    load_unit: str

    lactate_value: float

    heart_rate: int

    measurement_type: str | None
