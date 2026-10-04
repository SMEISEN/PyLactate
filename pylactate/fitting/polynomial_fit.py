from __future__ import annotations

import numpy as np

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import FitResult
from pylactate.analysis.selector import MeasurementSelector
from pylactate.fitting.base import FitStrategy


class PolynomialFit(FitStrategy):
    """
    Polynomieller Fit auf Basis von numpy.polyfit().
    """

    def __init__(
        self,
        degree: int = 3,
    ) -> None:
        if degree < 1:
            raise ValueError(
                "Der Polynomgrad muss >= 1 sein."
            )

        self.degree = degree

        self.name = f"Polynomial Degree {degree}"

    def fit(
        self,
        context: AnalysisContext,
    ) -> FitResult:
        """
        Führt einen polynomialen Fit durch.

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

        # Leere Datenmenge
        if len(x) == 0:
            raise ValueError(
                "Keine Messpunkte für den Fit vorhanden."
            )

        # Gleich viele x- und y-Werte
        if len(x) != len(y):
            raise ValueError(
                "Anzahl von x- und y-Werten stimmt nicht überein."
            )

        # NaN prüfen
        if np.isnan(x).any():
            raise ValueError(
                "Laststufen enthalten NaN-Werte."
            )

        if np.isnan(y).any():
            raise ValueError(
                "Laktatwerte enthalten NaN-Werte."
            )

        # Infinite Werte prüfen
        if np.isinf(x).any():
            raise ValueError(
                "Laststufen enthalten unendliche Werte."
            )

        if np.isinf(y).any():
            raise ValueError(
                "Laktatwerte enthalten unendliche Werte."
            )

        # Unterschiedliche Laststufen prüfen
        unique_x = np.unique(x)

        if len(unique_x) < 2:
            raise ValueError(
                "Für einen Fit werden mindestens zwei "
                "unterschiedliche Laststufen benötigt."
            )

        # Für Grad n werden mindestens n+1 unterschiedliche
        # Stützpunkte benötigt

        if len(unique_x) < self.degree + 1:
            raise ValueError(
                f"Polynomgrad {self.degree} benötigt "
                f"mindestens {self.degree + 1} "
                "unterschiedliche Laststufen."
            )

        try:
            coefficients = np.polyfit(
                x,
                y,
                deg=self.degree,
            )
        except np.linalg.LinAlgError as exc:
            raise ValueError(
                "Polynomfit konnte aufgrund "
                "ungültiger Daten nicht berechnet "
                "werden."
            ) from exc

        model = np.poly1d(coefficients)

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

        x_dense = np.linspace(
            x.min(),
            x.max(),
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
