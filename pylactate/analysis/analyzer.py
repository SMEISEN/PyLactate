from dataclasses import dataclass, field

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import (
    FitAnalysis,
    TestAnalysis,
)
from pylactate.plotting.test_plotter import TestPlotter
from pylactate.fitting.base import FitStrategy
from pylactate.model.enums import ThresholdType
from pylactate.thresholds.base import LT1Method, LT2Method



@dataclass(slots=True)
class Analyzer:
    """
    Führt die komplette Analyse eines Tests durch.

    Das letzte Analyseergebnis wird intern gespeichert
    und kann anschließend für Plotting oder weitere
    Auswertungen verwendet werden.
    """

    context: AnalysisContext

    fit_methods: list[FitStrategy]

    lt1_methods: list[LT1Method]

    lt2_methods: list[LT2Method]

    _analysis: TestAnalysis | None = field(
        init=False,
        default=None,
    )

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

        self._analysis = TestAnalysis(
            fit_analyses=fit_analyses,
            selected_fit=selected_fit,
        )

        return self._analysis

    @property
    def analysis(self) -> TestAnalysis:
        """
        Liefert das zuletzt berechnete Analyseergebnis.
        """

        if self._analysis is None:
            raise RuntimeError(
                "Es wurde noch keine Analyse ausgeführt."
            )

        return self._analysis

    def plot(self) -> None:
        """
        Führt den internen Plotter mit dem zuletzt
        berechneten Analyseergebnis aus.
        """

        if self._analysis is None:
            raise RuntimeError(
                "Vor plot() muss run() ausgeführt werden."
            )

        plotter = TestPlotter()

        for fit_analysis in self._analysis.fit_analyses:
            plotter.plot(
                context=self.context,
                analysis=fit_analysis,
            )
