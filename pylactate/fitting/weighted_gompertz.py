from __future__ import annotations

import numpy as np
from scipy.optimize import curve_fit

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import FitResult
from pylactate.analysis.selector import MeasurementSelector
from pylactate.fitting.base import FitStrategy
from pylactate.fitting.sigma_models import (
    SigmaFunction,
    lactate_scout_sport_sigma,
)


def gompertz(
    x: np.ndarray,
    a: float,
    b: float,
    c: float,
) -> np.ndarray:
    """
    Gompertz-Funktion.

    y = a * exp(-b * exp(-c * x))
    """

    return (
        a
        * np.exp(
            -b
            * np.exp(
                -c * x
            )
        )
    )


class WeightedGompertzFit(FitStrategy):
    """
    Gompertz-Fit mit Berücksichtigung
    der Messunsicherheit.
    """

    def __init__(
        self,
        sigma_function: SigmaFunction = (
            lactate_scout_sport_sigma
        ),
        extrapolation_factor: float = 0.2,
    ) -> None:

        super().__init__(
            extrapolation_factor=extrapolation_factor
        )

        self.sigma_function = sigma_function

        self.name = "Weighted Gompertz"

    def fit(
        self,
        context: AnalysisContext,
    ) -> FitResult:

        selector = MeasurementSelector()

        measurements = (
            selector.get_fit_measurements(
                context.session
            )
        )

        x = np.array(
            [m.load for m in measurements],
            dtype=float,
        )

        y = np.array(
            [
                m.record.lactate_value
                for m in measurements
            ],
            dtype=float,
        )

        sigma = np.array(
            [
                self.sigma_function(
                    value
                )
                for value in y
            ],
            dtype=float,
        )

        x_min = np.min(x)
        x_max = np.max(x)

        x_scaled = (x - x_min) / (x_max - x_min)

        params, _ = curve_fit(
            gompertz,
            x_scaled,
            y,
            p0=[np.max(y) * 1.5, 3.0, 5.0],
            bounds=(
                [0.0, 0.0, 0.0],
                [
                    np.max(y) * 10.0,
                    20.0,
                    20.0,
                ],
            ),
            sigma=sigma,
            absolute_sigma=True,
            maxfev=50000,
        )

        def model(
            values: np.ndarray,
        ) -> np.ndarray:
            values_scaled = (
                values - x_min
            ) / (
                x_max - x_min
            )
            return gompertz(
                values_scaled,
                *params,
            )

        y_pred = model(x)

        residuals = y - y_pred

        ss_res = np.sum(
            residuals ** 2
        )

        ss_tot = np.sum(
            (y - np.mean(y)) ** 2
        )

        r_squared = (
            1.0 - ss_res / ss_tot
            if ss_tot > 0
            else 1.0
        )

        rmse = float(
            np.sqrt(
                np.mean(
                    residuals ** 2
                )
            )
        )

        x_range = x.max() - x.min()

        x_dense = np.linspace(
            x.min()
            - self.extrapolation_factor
            * x_range,
            x.max()
            + self.extrapolation_factor
            * x_range,
            500,
        )

        y_dense = model(
            x_dense
        )

        confidence_score = max(
            0.0,
            min(
                100.0,
                r_squared * 100.0,
            ),
        )

        return FitResult(
            strategy_name=self.name,
            x_dense=x_dense,
            y_dense=y_dense,
            fitted_model=model,
            r_squared=float(r_squared),
            rmse=rmse,
            confidence_score=confidence_score,
        )
