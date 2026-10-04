from pylactate.analysis.results import FitAnalysis


class FitEvaluator:
    """
    Wählt die beste Fit-Strategie.
    """

    @staticmethod
    def select_best_fit(
        analyses: list[FitAnalysis],
    ) -> FitAnalysis:

        if not analyses:
            raise ValueError(
                "Keine Fit-Analysen vorhanden."
            )

        return max(
            analyses,
            key=lambda analysis: (
                analysis.fit_result.confidence_score
            ),
        )
