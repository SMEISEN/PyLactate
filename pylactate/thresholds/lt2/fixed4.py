from __future__ import annotations

import numpy as np

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import (
    FitResult,
    ThresholdResult,
)
from pylactate.thresholds.base import LT2Method


class Fixed4LT2Method(LT2Method):

    name = "Fixed 4 mmol/l"

    def calculate(
        self,
        context: AnalysisContext,
        fit_result: FitResult,
    ) -> ThresholdResult:

        indices = np.where(
            fit_result.y_dense >= 4.0
        )[0]

        if len(indices) == 0:
            raise ValueError(
                "4 mmol/l wurde nicht erreicht."
            )

        idx = int(indices[0])

        return self.create_result(
            context=context,
            load=float(fit_result.x_dense[idx]),
            lactate=float(fit_result.y_dense[idx]),
        )
