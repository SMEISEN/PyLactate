from abc import ABC, abstractmethod

import numpy as np

from pylactate.analysis.context import AnalysisContext
from pylactate.analysis.results import (
    FitResult,
    ThresholdResult,
)
from pylactate.model.enums import ThresholdType


class ThresholdMethod(ABC):

    threshold_type: ThresholdType

class ThresholdMethod(ABC):

    threshold_type: ThresholdType

    def create_result(
        self,
        context: AnalysisContext,
        load: float,
        lactate: float,
    ) -> ThresholdResult:
        return ThresholdResult(
            method_name=self.name,
            threshold_type=self.threshold_type,
            load=load,
            lactate=lactate,
            heart_rate=self.interpolate_heart_rate(
                context=context,
                load=load,
            ),
        )

    def interpolate_heart_rate(
        self,
        context: AnalysisContext,
        load: float,
    ) -> float | None:
        """
        Interpoliert die Herzfrequenz anhand der
        umliegenden Messpunkte.
        """

        measurements = sorted(
            context.session.measurements,
            key=lambda m: m.load,
        )

        if not measurements:
            return None

        if len(measurements) == 1:
            return measurements[0].record.heart_rate

        for left, right in zip(
            measurements[:-1],
            measurements[1:],
        ):
            if left.load <= load <= right.load:

                hr_left = left.record.heart_rate
                hr_right = right.record.heart_rate

                if hr_left is None or hr_right is None:
                    return None

                factor = (
                    (load - left.load)
                    / (right.load - left.load)
                )

                return (
                    hr_left
                    + factor * (hr_right - hr_left)
                )

        # Außerhalb des Messbereichs:
        nearest = min(
            measurements,
            key=lambda m: abs(m.load - load),
        )

        return nearest.record.heart_rate


class LT1Method(ThresholdMethod, ABC):
    """
    Basisklasse für LT1-Methoden.
    """

    threshold_type = ThresholdType.LT1


class LT2Method(ThresholdMethod, ABC):
    """
    Basisklasse für LT2-Methoden.
    """

    threshold_type = ThresholdType.LT2
