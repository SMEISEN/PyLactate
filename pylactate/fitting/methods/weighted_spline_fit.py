from __future__ import annotations

import numpy as np
from scipy.interpolate import UnivariateSpline

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import FitResult
from pylactate.analysis.selector import MeasurementSelector
from pylactate.fitting.base import FitStrategy
from pylactate.fitting.models.spline import weighted_spline
from pylactate.fitting.sigma.sigma_models import (
    SigmaFunction,
    lactate_scout_sport_sigma,
)


class WeightedSplineFit(FitStrategy):
    """
    Gewichteter kubischer Spline-Fit.

    Die Gewichte werden aus den Standardabweichungen
    der Sigma-Funktion berechnet:

        w = 1 / sigma
    """

    def __init__(
        self,
        sigma_function: SigmaFunction = (
            lactate_scout_sport_sigma
        ),
        extrapolation_factor: float = 0.2,
        spline_degree: int = 3,
    ) -> None:

        super().__init__(
            extrapolation_factor=extrapolation_factor
        )

        if spline_degree < 1 or spline_degree > 5:
            raise ValueError(
                "spline_degree muss zwischen "
                "1 und 5 liegen."
            )

        self.sigma_function = sigma_function
        self.spline_degree = spline_degree

        self.name = (
            f"Weighted Spline k={spline_degree}"
        )

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

        order = np.argsort(x)

        x = x[order]
        y = y[order]

        sigma = np.array(
            [
                self.sigma_function(
                    value
                )
                for value in y
            ],
            dtype=float,
        )

        weights = 1.0 / sigma

        model = weighted_spline(
            x=x,
            y=y,
            weights=weights,
            spline_degree=self.spline_degree,
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

        y_dense = model(x_dense)

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
