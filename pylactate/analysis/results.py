from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(slots=True)
class ThresholdResult:
    """
    Ergebnis einer LS-Methode.
    """

    method_name: str

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
    Ein Fit und dessen LS-Ergebnisse.
    """

    fit_result: FitResult

    thresholds: list[ThresholdResult]


@dataclass(slots=True)
class TestAnalysis:
    """
    Analyse eines Tests
    über mehrere Fitstrategien.
    """

    fit_analyses: list[FitAnalysis]

    selected_fit: FitAnalysis
