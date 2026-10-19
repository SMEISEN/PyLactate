from abc import ABC, abstractmethod

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import FitResult


class FitStrategy(ABC):
    """
    Basisklasse für alle Fit-Strategien.
    """

    name: str

    def __init__(
        self,
        extrapolation_factor: float = 0.2,
    ) -> None:
        """
        Args:
            extrapolation_factor:
                Anteil des Lastbereichs, der links und rechts
                für die dichte Fitkurve extrapoliert wird.

                Beispiel:
                    min_load = 100
                    max_load = 300

                    range = 200

                    extrapolation_factor = 0.2

                    => 40 W links und rechts
            """
        if extrapolation_factor < 0:
            raise ValueError(
                "extrapolation_factor muss >= 0 sein."
            )

        self.extrapolation_factor = extrapolation_factor

    @abstractmethod
    def fit(
        self,
        context: AnalysisContext,
    ) -> FitResult:
        """
        Führt den Fit durch.
        """
        raise NotImplementedError
