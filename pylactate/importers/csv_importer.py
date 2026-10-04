from datetime import datetime
from pathlib import Path

import pandas as pd

from pylactate.model.raw import (
    MeasurementRecord,
)
from pylactate.model.test import LactateTest

EXPECTED_COLUMNS = [
    "MID",
    "Mem Pos",
    "Date",
    "Time",
    "Test type",
    "Step length",
    "Load",
    "Load unit",
    "Lactate value",
    "Heart rate",
    "Measurement type",
]


class CsvImporter:

    @staticmethod
    def _to_float(
        value: str | float | None,
    ) -> float | None:

        if value is None:
            return None

        value = str(value).strip()

        if value == "":
            return None

        return float(value.replace(",", "."))

    def load(
        self,
        file_path: str | Path,
    ) -> LactateTest:

        df = pd.read_csv(
            file_path,
            sep=";",
            dtype=str,
        )

        if list(df.columns) != EXPECTED_COLUMNS:
            raise ValueError(
                "CSV-Header entspricht nicht "
                "dem erwarteten Format."
            )

        records: list[MeasurementRecord] = []

        for row in df.to_dict(
            orient="records"
        ):

            date_obj = datetime.strptime(
                row["Date"],
                "%d.%m.%Y",
            ).date()

            time_obj = datetime.strptime(
                row["Time"],
                "%H:%M:%S",
            ).time()

            records.append(
                MeasurementRecord(
                    mid=row["MID"],
                    mem_pos=row["Mem Pos"],
                    date=date_obj,
                    time=time_obj,
                    test_type=row["Test type"],
                    step_length=self._to_float(
                        row["Step length"]
                    ),
                    load=self._to_float(
                        row["Load"]
                    )
                    or 0.0,
                    load_unit=row["Load unit"],
                    lactate_value=self._to_float(
                        row["Lactate value"]
                    )
                    or 0.0,
                    heart_rate=int(
                        row["Heart rate"]
                    ),
                    measurement_type=(
                        row["Measurement type"]
                        or None
                    ),
                )
            )

        return LactateTest(
            source_file=Path(file_path),
            records=tuple(records),
        )
