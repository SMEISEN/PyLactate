from __future__ import annotations

import matplotlib.pyplot as plt

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import FitResult
from pylactate.analysis.selector import MeasurementSelector


class TestPlotter:

    def plot_fit(
        self,
        context: AnalysisContext,
        fit_result: FitResult,
    ) -> None:
        selector = MeasurementSelector()

        measurements = (
            selector.get_all_measurements(
                context.session
            )
        )

        x = [m.load for m in measurements]

        y = [
            m.record.lactate_value
            for m in measurements
        ]
                
        if measurements:
            load_unit = measurements[0].load_unit
        else:
            load_unit = ""

        plt.figure(figsize=(10, 6))

        plt.scatter(
            x,
            y,
            label="Messpunkte",
        )

        plt.plot(
            fit_result.x_dense,
            fit_result.y_dense,
            linewidth=2,
            label=fit_result.strategy_name,
        )


        plt.xlabel(
            f"Last [{load_unit}]"
        )
        plt.ylabel("Laktat [mmol/L]")

        plt.grid(True)

        plt.legend()

        plt.show()
