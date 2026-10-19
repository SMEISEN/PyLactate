from __future__ import annotations

import numpy as np

from pylactate.analysis.results import ThresholdResult
from pylactate.model.session import MeasurementReview


def first_crossing(
    x_dense: np.ndarray,
    y_dense: np.ndarray,
    target: float,
) -> tuple[float, float]:
    """
    Liefert die erste Stelle, an der die Kurve
    einen Zielwert überschreitet.
    """

    indices = np.where(y_dense >= target)[0]

    if len(indices) == 0:
        raise ValueError(
            f"Zielwert {target:.2f} mmol/l "
            "wurde nicht erreicht."
        )

    idx = int(indices[0])

    return (
        float(x_dense[idx]),
        float(y_dense[idx]),
    )


def nearest_heart_rate(
    measurements: list[MeasurementReview],
    load: float,
) -> float | None:
    """
    Bestimmt die Herzfrequenz des nächstliegenden
    Messpunktes zur Laststufe.
    """

    if not measurements:
        return None

    nearest = min(
        measurements,
        key=lambda m: abs(m.load - load),
    )

    return nearest.record.heart_rate


def build_threshold(
    method_name: str,
    load: float,
    lactate: float,
    heart_rate: float | None,
) -> ThresholdResult:
    return ThresholdResult(
        method_name=method_name,
        load=load,
        lactate=lactate,
        heart_rate=heart_rate,
    )
