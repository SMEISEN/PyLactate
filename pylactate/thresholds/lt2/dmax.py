from __future__ import annotations

import numpy as np

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import (
    FitResult,
    ThresholdResult,
)
from pylactate.thresholds.base import LT2Method


class DmaxLT2Method(LT2Method):

    name = "Dmax"

    def calculate(
        self,
        context: AnalysisContext,
        fit_result: FitResult,
    ) -> ThresholdResult:

        x = fit_result.x_dense
        y = fit_result.y_dense

        start = np.array([
            x[0],
            y[0],
        ])

        end = np.array([
            x[-1],
            y[-1],
        ])

        line = end - start
        norm = np.linalg.norm(line)

        if norm == 0:
            raise ValueError(
                "Dmax konnte nicht berechnet werden."
            )

        distances = []

        for xi, yi in zip(x, y):

            point = np.array([xi, yi])

            distance = (
                abs(
                    np.cross(
                        line,
                        point - start,
                    )
                )
                / norm
            )

            distances.append(distance)

        idx = int(np.argmax(distances))

        return self.create_result(
            context=context,
            load=float(x[idx]),
            lactate=float(y[idx]),
        )
