from dataclasses import dataclass

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import (
    FitAnalysis,
    TestAnalysis,
)
from pylactate.fitting.base import FitStrategy
from pylactate.model.enums import ThresholdType
from pylactate.thresholds.base import LT1Method, LT2Method


@dataclass(slots=True)
class Analyzer:
    """
    Führt die komplette Analyse eines Tests durch.

    Für jede Fitstrategie werden sämtliche
    LT1- und LT2-Methoden berechnet.
    """

    context: AnalysisContext

    fit_methods: list[FitStrategy]

    lt1_methods: list[LT1Method]

    lt2_methods: list[LT2Method]

    def run(self) -> TestAnalysis:

        fit_analyses: list[FitAnalysis] = []

        for fit_method in self.fit_methods:

            fit_result = fit_method.fit(
                self.context,
            )

            thresholds = {
                ThresholdType.LT1: [
                    method.calculate(
                        self.context,
                        fit_result,
                    )
                    for method in self.lt1_methods
                ],
                ThresholdType.LT2: [
                    method.calculate(
                        self.context,
                        fit_result,
                    )
                    for method in self.lt2_methods
                ],
            }

            fit_analyses.append(
                FitAnalysis(
                    fit_result=fit_result,
                    thresholds=thresholds,
                )
            )

        selected_fit = max(
            fit_analyses,
            key=lambda x: (
                x.fit_result.confidence_score
            ),
        )

        return TestAnalysis(
            fit_analyses=fit_analyses,
            selected_fit=selected_fit,
        )
