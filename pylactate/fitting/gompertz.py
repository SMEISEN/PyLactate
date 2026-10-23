from __future__ import annotations

import numpy as np
from scipy.optimize import curve_fit

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import FitResult
from pylactate.analysis.selector import MeasurementSelector
from pylactate.fitting.base import FitStrategy


class GompertzFit(FitStrategy):
    """
    Gompertz-Fit für Laktatkurven.

    Modell:

        y = a * exp(-b * exp(-c * x))

    mit:
        a = obere Asymptote
        b = Verschiebung
        c = Wachstumsrate
    """

    def __init__(
        self,
        extrapolation_factor: float = 0.2,
    ) -> None:
        super().__init__(
            extrapolation_factor=extrapolation_factor,
        )

        self.name = "Gompertz"

    @staticmethod
    def _gompertz(
        x: np.ndarray,
        a: float,
        b: float,
        c: float,
    ) -> np.ndarray:
        """
        Gompertz-Funktion.
        """
        return a * np.exp(
            -b * np.exp(-c * x)
        )

    def fit(
        self,
        context: AnalysisContext,
    ) -> FitResult:
        """
        Führt einen Gompertz-Fit durch.

        Args:
            context:
                Analysekontext.

        Returns:
            FitResult
        """

        selector = MeasurementSelector()

        measurements = selector.get_fit_measurements(
            context.session
        )

        x = np.array(
            [
                m.load
                for m in measurements
            ],
            dtype=float,
        )

        y = np.array(
            [
                m.record.lactate_value
                for m in measurements
            ],
            dtype=float,
        )

        if len(x) == 0:
            raise ValueError(
                "Keine Messpunkte für den Fit vorhanden."
            )

        if len(x) != len(y):
            raise ValueError(
                "Anzahl von x- und y-Werten stimmt nicht überein."
            )

        if np.isnan(x).any():
            raise ValueError(
                "Laststufen enthalten NaN-Werte."
            )

        if np.isnan(y).any():
            raise ValueError(
                "Laktatwerte enthalten NaN-Werte."
            )

        if np.isinf(x).any():
            raise ValueError(
                "Laststufen enthalten unendliche Werte."
            )

        if np.isinf(y).any():
            raise ValueError(
                "Laktatwerte enthalten unendliche Werte."
            )

        unique_x = np.unique(x)

        if len(unique_x) < 3:
            raise ValueError(
                "Für den Gompertz-Fit werden mindestens "
                "drei unterschiedliche Laststufen benötigt."
            )

        order = np.argsort(x)

        x = x[order]
        y = y[order]

        p0 = [
            max(y) * 1.2,
            1.0,
            0.01,
        ]

        lower_bounds = [
            0.0,
            0.0,
            0.0,
        ]

        upper_bounds = [
            np.inf,
            np.inf,
            np.inf,
        ]

        try:
            parameters, _ = curve_fit(
                self._gompertz,
                x,
                y,
                p0=p0,
                bounds=(
                    lower_bounds,
                    upper_bounds,
                ),
                maxfev=10000,
            )
        except RuntimeError as exc:
            raise ValueError(
                "Gompertz-Fit konnte nicht berechnet werden."
            ) from exc

        def model(
            values: np.ndarray,
        ) -> np.ndarray:
            return self._gompertz(
                values,
                *parameters,
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
            - self.extrapolation_factor * x_range,
            x.max()
            + self.extrapolation_factor * x_range,
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
