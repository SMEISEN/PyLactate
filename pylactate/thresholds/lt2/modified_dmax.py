from __future__ import annotations

import numpy as np

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import (
    FitResult,
    ThresholdResult,
)
from pylactate.thresholds.base import (
    LT1Method,
    LT2Method,
)
from pylactate.thresholds.lt1.baseline05 import (
    Baseline05LT1Method,
)


class ModifiedDmaxMethod(LT2Method):
    """
    Modified Dmax.

    Verbindet den LT1-Punkt mit dem letzten Punkt
    der Fitkurve und bestimmt den Punkt mit dem
    größten senkrechten Abstand zu dieser Linie.

    Die verwendete LT1-Methode ist frei
    konfigurierbar.
    """

    name = "Modified Dmax"

    def __init__(
        self,
        lt1_method: LT1Method | None = None,
    ) -> None:
        self.lt1_method = (
            lt1_method
            if lt1_method is not None
            else Baseline05LT1Method()
        )

    def calculate(
        self,
        context: AnalysisContext,
        fit_result: FitResult,
    ) -> ThresholdResult:

        lt1_result = (
            self.lt1_method.calculate(
                context=context,
                fit_result=fit_result,
            )
        )

        x_dense = fit_result.x_dense
        y_dense = fit_result.y_dense

        lt1_idx = int(
            np.argmin(
                np.abs(
                    x_dense
                    - lt1_result.load
                )
            )
        )

        x = x_dense[lt1_idx:]
        y = y_dense[lt1_idx:]

        if len(x) < 2:
            raise ValueError(
                "Zu wenige Stützpunkte "
                "für Modified Dmax."
            )

        start_x = float(x[0])
        start_y = float(y[0])

        end_x = float(x[-1])
        end_y = float(y[-1])

        dx = end_x - start_x
        dy = end_y - start_y

        denominator = np.sqrt(
            dx ** 2 + dy ** 2
        )

        if denominator == 0:
            raise ValueError(
                "Modified-Dmax-Linie konnte "
                "nicht berechnet werden."
            )

        distances = np.abs(
            dy * x
            - dx * y
            + end_x * start_y
            - end_y * start_x
        ) / denominator

        idx = int(
            np.argmax(
                distances
            )
        )

        load = float(
            x[idx]
        )

        lactate = float(
            y[idx]
        )

        return self.create_result(
            context=context,
            load=load,
            lactate=lactate,
        )
