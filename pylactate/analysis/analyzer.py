from dataclasses import dataclass, field

import numpy as np

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import (
    FitAnalysis,
    FitResult,
    TestAnalysis,
    ThresholdResult,
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

            if fit_result.simulation_results:

                self._calculate_threshold_statistics(
                    context=self.context,
                    fit_result=fit_result,
                    thresholds=thresholds,
                )

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

    def _calculate_threshold_statistics(
        self,
        context: AnalysisContext,
        fit_result: FitResult,
        thresholds: dict[
            ThresholdType,
            list[ThresholdResult],
        ],
    ) -> None:

        threshold_methods = {
            ThresholdType.LT1: self.lt1_methods,
            ThresholdType.LT2: self.lt2_methods,
        }

        for threshold_type, methods in (
            threshold_methods.items()
        ):

            for method, threshold_result in zip(
                methods,
                thresholds[threshold_type],
            ):

                simulated_results = [
                    method.calculate(
                        context,
                        simulation_fit,
                    )
                    for simulation_fit in (
                        fit_result.simulation_results
                    )
                ]

                loads = np.array(
                    [
                        result.load
                        for result in simulated_results
                    ]
                )

                lactates = np.array(
                    [
                        result.lactate
                        for result in simulated_results
                    ]
                )

                heart_rates = np.array(
                    [
                        result.heart_rate
                        for result in simulated_results
                        if result.heart_rate
                        is not None
                    ]
                )

                threshold_result.load_std = float(
                    np.std(loads)
                )

                threshold_result.load_ci_lower = float(
                    np.percentile(
                        loads,
                        2.5,
                    )
                )

                threshold_result.load_ci_upper = float(
                    np.percentile(
                        loads,
                        97.5,
                    )
                )

                threshold_result.lactate_std = float(
                    np.std(lactates)
                )

                threshold_result.lactate_ci_lower = float(
                    np.percentile(
                        lactates,
                        2.5,
                    )
                )

                threshold_result.lactate_ci_upper = float(
                    np.percentile(
                        lactates,
                        97.5,
                    )
                )

                if len(heart_rates) > 0:

                    threshold_result.heart_rate_std = (
                        float(
                            np.std(
                                heart_rates
                            )
                        )
                    )

                    threshold_result.heart_rate_ci_lower = (
                        float(
                            np.percentile(
                                heart_rates,
                                2.5,
                            )
                        )
                    )

                    threshold_result.heart_rate_ci_upper = (
                        float(
                            np.percentile(
                                heart_rates,
                                97.5,
                            )
                        )
                    )
