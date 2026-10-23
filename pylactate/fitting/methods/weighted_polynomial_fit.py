from __future__ import annotations

import numpy as np

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import FitResult
from pylactate.analysis.selector import MeasurementSelector
from pylactate.fitting.base import FitStrategy
from pylactate.fitting.models.polynominal import weighted_polynomial
from pylactate.fitting.sigma.sigma_models import (
    SigmaFunction,
    lactate_scout_sport_sigma,
)


class WeightedPolynomialFit(FitStrategy):
    """
    Gewichteter polynomialer Fit.

    Die Standardabweichung jedes Messpunkts wird durch eine
    Sigma-Funktion bestimmt.

    Die Gewichte werden gemäß numpy.polyfit() berechnet:

        w = 1 / sigma

    Messpunkte mit kleiner Standardabweichung haben dadurch
    einen stärkeren Einfluss auf den Fit.
    """

    def __init__(
        self,
        degree: int = 3,
        sigma_function: SigmaFunction = (
            lactate_scout_sport_sigma
        ),
        extrapolation_factor: float = 0.2,
    ) -> None:
        super().__init__(
            extrapolation_factor=extrapolation_factor
        )

        if degree < 1:
            raise ValueError(
                "Der Polynomgrad muss >= 1 sein."
            )

        self.degree = degree
        self.sigma_function = sigma_function

        self.name = (
            f"Weighted Polynomial Degree {degree}"
        )

    def fit(
        self,
        context: AnalysisContext,
    ) -> FitResult:
        """
        Führt einen gewichteten Polynomial-Fit durch.
        """

        selector = MeasurementSelector()

        measurements = (
            selector.get_fit_measurements(
                context.session
            )
        )

        if len(measurements) < self.degree + 1:
            raise ValueError(
                f"Mindestens {self.degree + 1} "
                f"Messpunkte erforderlich "
                f"für Grad {self.degree}."
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

        if len(unique_x) < 2:
            raise ValueError(
                "Für einen Fit werden mindestens zwei "
                "unterschiedliche Laststufen benötigt."
            )

        if len(unique_x) < self.degree + 1:
            raise ValueError(
                f"Polynomgrad {self.degree} benötigt "
                f"mindestens {self.degree + 1} "
                "unterschiedliche Laststufen."
            )

        sigma = np.array(
            [
                self.sigma_function(
                    lactate_value
                )
                for lactate_value in y
            ],
            dtype=float,
        )

        if np.isnan(sigma).any():
            raise ValueError(
                "Sigma-Funktion liefert NaN-Werte."
            )

        if np.isinf(sigma).any():
            raise ValueError(
                "Sigma-Funktion liefert unendliche Werte."
            )

        if np.any(sigma <= 0):
            raise ValueError(
                "Sigma-Funktion muss ausschließlich "
                "positive Werte liefern."
            )

        # numpy.polyfit erwartet Gewichte
        # proportional zu 1 / sigma
        weights = 1.0 / sigma

        try:
            model = weighted_polynomial(
                x=x,
                y=y,
                degree=self.degree,
                weights=weights,
            )
        except np.linalg.LinAlgError as exc:
            raise ValueError(
                "Gewichteter Polynomfit konnte "
                "nicht berechnet werden."
            ) from exc

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
            r_squared=float(
                r_squared
            ),
            rmse=rmse,
            confidence_score=confidence_score,
        )
