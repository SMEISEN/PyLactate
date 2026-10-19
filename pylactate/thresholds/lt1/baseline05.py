from __future__ import annotations

import numpy as np

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import (
    FitResult,
    ThresholdResult,
)
from pylactate.thresholds.base import LT1Method


class Baseline05LT1Method(LT1Method):

    name = "Baseline + 0.5 mmol/l"

    def calculate(
        self,
        context: AnalysisContext,
        fit_result: FitResult,
    ) -> ThresholdResult:

        baseline = float(fit_result.y_dense[0])
        target = baseline + 0.5

        indices = np.where(
            fit_result.y_dense >= target
        )[0]

        if len(indices) == 0:
            raise ValueError(
                "LT1 konnte nicht bestimmt werden."
            )

        idx = int(indices[0])

        return self.create_result(
            context=context,
            load=float(fit_result.x_dense[idx]),
            lactate=float(fit_result.y_dense[idx]),
        )
