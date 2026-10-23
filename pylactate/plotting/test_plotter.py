from __future__ import annotations

import matplotlib.pyplot as plt

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import FitAnalysis
from pylactate.analysis.selector import MeasurementSelector
from pylactate.model.enums import ThresholdType


class TestPlotter:

    def plot(
        self,
        context: AnalysisContext,
        analysis: FitAnalysis,
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

        load_unit = (
            measurements[0].load_unit
            if measurements
            else ""
        )

        plt.figure(figsize=(12, 7))

        # Messpunkte
        plt.scatter(
            x,
            y,
            color="tab:blue",
            s=50,
            label="Messpunkte",
            zorder=5,
        )

        fit_result = analysis.fit_result

        # Fitkurve
        plt.plot(
            fit_result.x_dense,
            fit_result.y_dense,
            color="black",
            linewidth=2.5,
            label=fit_result.strategy_name,
            zorder=3,
        )

        colors = {
            ThresholdType.LT1: "tab:green",
            ThresholdType.LT2: "tab:red",
        }

        markers = [
            "o",
            "s",
            "^",
            "D",
            "v",
            "P",
            "X",
        ]

        # maximale Länge für tabellenartige Legendeneinträge
        threshold_results = [
            result
            for results in analysis.thresholds.values()
            for result in results
        ]

        max_name_length = (
            max(
                (
                    len(r.method_name)
                    for r in threshold_results
                ),
                default=0,
            )
            + 4
        )

        for threshold_type, results in (
            analysis.thresholds.items()
        ):

            color = colors.get(
                threshold_type,
                "gray",
            )

            for idx, result in enumerate(results):

                marker = markers[
                    idx % len(markers)
                ]

                plt.scatter(
                    result.load,
                    result.lactate,
                    s=120,
                    color=color,
                    marker=marker,
                    edgecolors="black",
                    linewidth=0.7,
                    zorder=10,
                    label=(
                        f"{result.method_name:<{max_name_length}}"
                        f"{result.load:.1f} {load_unit}"
                    ),
                )

                plt.axvline(
                    result.load,
                    color=color,
                    linestyle="--",
                    linewidth=1.5,
                    alpha=0.4,
                )

        plt.xlabel(
            f"Last [{load_unit}]"
        )

        plt.ylabel(
            "Laktat [mmol/L]"
        )

        plt.title(
            fit_result.strategy_name
        )

        plt.grid(
            True,
            alpha=0.3,
        )

        handles, labels = (
            plt.gca()
            .get_legend_handles_labels()
        )

        unique = dict(
            zip(labels, handles)
        )

        plt.legend(
            unique.values(),
            unique.keys(),
            loc="upper left",
            prop={
                "family": "monospace",
            },
            framealpha=0.95,
        )

        plt.tight_layout()

        plt.show()
