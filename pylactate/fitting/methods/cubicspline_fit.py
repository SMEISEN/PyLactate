from __future__ import annotations

import numpy as np
from scipy.interpolate import CubicSpline

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import FitResult
from pylactate.analysis.selector import MeasurementSelector
from pylactate.fitting.base import FitStrategy
from pylactate.fitting.models.spline import cubic_spline


class CubicSplineFit(FitStrategy):

    def __init__(
        self,
        extrapolation_factor: float = 0.2,
    ) -> None:
        super().__init__(
            extrapolation_factor=extrapolation_factor
        )

        self.name = "Cubic Spline"

    def fit(
        self,
        context: AnalysisContext,
    ) -> FitResult:

        measurements = (
            MeasurementSelector()
            .get_fit_measurements(
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

        model = cubic_spline(x=x, y=y)

        y_pred = model(x)

        residuals = y - y_pred

        ss_res = np.sum(residuals ** 2)
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

        return FitResult(
            strategy_name=self.name,
            x_dense=x_dense,
            y_dense=y_dense,
            fitted_model=model,
            r_squared=float(r_squared),
            rmse=rmse,
            confidence_score=max(
                0.0,
                min(
                    100.0,
                    r_squared * 100.0,
                ),
            ),
        )
