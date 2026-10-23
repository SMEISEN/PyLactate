from __future__ import annotations

from dataclasses import replace

import numpy as np

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import FitResult
from pylactate.fitting.base import FitStrategy
from pylactate.fitting.sigma.sigma_models import (
    SigmaFunction,
    lactate_scout_sport_sigma,
)


class MonteCarloFit(FitStrategy):
    """
    Monte-Carlo-Wrapper für beliebige Fit-Methoden.

    Die Messpunkte werden entsprechend der
    Sigma-Funktion gestört und anschließend
    mit der übergebenen Fit-Methode gefittet.

    Das zurückgegebene FitResult entspricht
    der mittleren Kurve aller Simulationen.
    """

    def __init__(
        self,
        fit_method: FitStrategy,
        sigma_function: SigmaFunction = (
            lactate_scout_sport_sigma
        ),
        simulations: int = 1000,
        extrapolation_factor: float = 0.2,
    ) -> None:

        super().__init__(
            extrapolation_factor=extrapolation_factor
        )

        if simulations < 1:
            raise ValueError(
                "simulations muss >= 1 sein."
            )

        self.fit_method = fit_method
        self.sigma_function = sigma_function
        self.simulations = simulations

        self.name = (
            f"Monte Carlo "
            f"({fit_method.name})"
        )

    def fit(
        self,
        context: AnalysisContext,
    ) -> FitResult:

        simulation_curves: list[np.ndarray] = []

        reference_result: FitResult | None = None

        rng = np.random.default_rng()

        for _ in range(self.simulations):

            simulated_measurements = []

            for measurement in (
                context.session.measurements
            ):

                value = (
                    measurement
                    .record
                    .lactate_value
                )

                sigma = (
                    self.sigma_function(
                        value
                    )
                )

                simulated_value = float(
                    rng.normal(
                        loc=value,
                        scale=sigma,
                    )
                )

                simulated_record = replace(
                    measurement.record,
                    lactate_value=simulated_value,
                )

                simulated_measurement = replace(
                    measurement,
                    record=simulated_record,
                )

                simulated_measurements.append(
                    simulated_measurement
                )

            simulated_session = replace(
                context.session,
                measurements=simulated_measurements,
            )

            simulated_context = replace(
                context,
                session=simulated_session,
            )

            result = self.fit_method.fit(
                simulated_context,
            )

            if reference_result is None:
                reference_result = result

            simulation_curves.append(
                result.y_dense
            )

        if reference_result is None:
            raise ValueError(
                "Keine Monte-Carlo-Simulation "
                "durchgeführt."
            )

        curves = np.asarray(
            simulation_curves
        )

        mean_curve = np.mean(
            curves,
            axis=0,
        )

        lower_band = np.percentile(
            curves,
            2.5,
            axis=0,
        )

        upper_band = np.percentile(
            curves,
            97.5,
            axis=0,
        )

        return FitResult(
            strategy_name=self.name,
            x_dense=reference_result.x_dense,
            y_dense=mean_curve,
            fitted_model=None,
            r_squared=reference_result.r_squared,
            rmse=reference_result.rmse,
            confidence_score=reference_result.confidence_score,
            lower_band=lower_band,
            upper_band=upper_band,
        )
