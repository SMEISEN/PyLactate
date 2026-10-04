from abc import ABC, abstractmethod

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import FitResult, ThresholdResult


class ThresholdMethod(ABC):

    name: str

    @abstractmethod
    def calculate(
        self,
        context: AnalysisContext,
        fit_result: FitResult,
    ) -> ThresholdResult:
        """
        Berechnet LS1 oder LS2.
        """
        raise NotImplementedError
