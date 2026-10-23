from __future__ import annotations

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
from pylactate.thresholds.utils import (
    first_crossing,
)


class DickhuthMethod(LT2Method):
    """
    Dickhuth-Schwelle.

    Definition:

        LT1 + 1.5 mmol/l

    Die verwendete LT1-Methode kann
    konfiguriert werden.
    """

    name = "Dickhuth"

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

        target = (
            lt1_result.lactate
            + 1.5
        )

        load, lactate = first_crossing(
            fit_result.x_dense,
            fit_result.y_dense,
            target,
        )

        return self.create_result(
            context=context,
            load=load,
            lactate=lactate,
        )
