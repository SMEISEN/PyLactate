from dataclasses import dataclass
from typing import Any

import numpy as np

from pylactate.model.enums import ThresholdType


@dataclass(slots=True)
class ThresholdResult:

    method_name: str

    threshold_type: ThresholdType

    load: float

    lactate: float

    heart_rate: float | None


@dataclass(slots=True)
class FitResult:
    """
    Ergebnis einer Fitstrategie.
    """

    strategy_name: str

    x_dense: np.ndarray

    y_dense: np.ndarray

    fitted_model: Any

    r_squared: float

    rmse: float

    confidence_score: float


@dataclass(slots=True)
class FitAnalysis:
    """
    Ein Fit und dessen
    Schwellenergebnisse.
    """

    fit_result: FitResult

    thresholds: dict[
        ThresholdType,
        list[ThresholdResult],
    ]


@dataclass(slots=True)
class TestAnalysis:
    """
    Analyse eines Tests
    über mehrere Fitstrategien.
    """

    fit_analyses: list[FitAnalysis]

    selected_fit: FitAnalysis
