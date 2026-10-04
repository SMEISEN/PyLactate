from abc import ABC, abstractmethod

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import FitResult


class FitStrategy(ABC):
    """
    Basisklasse für alle Fit-Strategien.
    """

    name: str

    @abstractmethod
    def fit(
        self,
        context: AnalysisContext,
    ) -> FitResult:
        """
        Führt den Fit durch.
        """
        raise NotImplementedError
