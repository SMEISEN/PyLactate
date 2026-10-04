from dataclasses import dataclass

from pylactate.model.enums import PointClass
from pylactate.model.raw import MeasurementRecord
from pylactate.model.test import LactateTest


@dataclass(slots=True)
class MeasurementReview:
    """
    Editierbare Bewertung eines Messpunktes.
    """

    record: MeasurementRecord

    point_class: PointClass

    included_in_fit: bool = True

    comment: str = ""

    corrected_load: float | None = None

    corrected_load_unit: str | None = None

    @property
    def load(self) -> float:
        """
        Liefert die korrigierte Laststufe,
        falls vorhanden.
        """

        if self.corrected_load is not None:
            return self.corrected_load

        return self.record.load

    @property
    def load_unit(self) -> str:
        """
        Liefert die aktive Last-Einheit.
        """

        if self.corrected_load_unit is not None:
            return self.corrected_load_unit

        return self.record.load_unit


@dataclass(slots=True)
class AnalysisSession:
    """
    Arbeitskopie eines Tests.

    Hier erfolgen alle manuellen Änderungen.
    """

    test: LactateTest

    measurements: list[MeasurementReview]

    @classmethod
    def from_test(
        cls,
        test: LactateTest,
    ) -> "AnalysisSession":

        measurements = [
            MeasurementReview(
                record=record,
                point_class=PointClass.LOAD,
            )
            for record in test.records
        ]

        return cls(
            test=test,
            measurements=measurements,
        )

    def get(
        self,
        mid: str,
    ) -> MeasurementReview:

        for measurement in self.measurements:

            if measurement.record.mid == mid:
                return measurement

        raise KeyError(
            f"MID '{mid}' nicht gefunden."
        )

    def mark_false(
        self,
        mid: str,
        reason: str = "",
    ) -> None:

        measurement = self.get(mid)

        measurement.point_class = PointClass.FALSE
        measurement.included_in_fit = False
        measurement.comment = reason

    def include_in_fit(
        self,
        mid: str,
    ) -> None:
        """
        Nimmt einen Messpunkt wieder in die Auswertung auf.
        """

        measurement = self.get(mid)

        measurement.included_in_fit = True


    def exclude_from_fit(
        self,
        mid: str,
    ) -> None:
        """
        Entfernt einen Messpunkt aus dem Fit.
        """

        measurement = self.get(mid)

        measurement.included_in_fit = False

    def set_classification(
        self,
        mid: str,
        point_class: PointClass,
    ) -> None:
        """
        Setzt eine neue Klassifikation.
        """

        measurement = self.get(mid)

        measurement.point_class = point_class

    def assign_loads(
        self,
        loads: list[float] | None = None,
        start: float | None = None,
        step: float | None = None,
    ) -> None:
        """
        Korrigiert Laststufen für die aktuelle Session.

        Variante 1:

            assign_loads(
                loads=[8, 10, 12, 14, 16, 18, 20]
            )

        Variante 2:

            assign_loads(
                start=8,
                step=2,
            )

        Args:
            loads:
                Explizite Laststufenliste.

            start:
                Startwert für die automatische Generierung.

            step:
                Schrittweite für die automatische Generierung.

        Raises:
            ValueError:
                Falls die Parameterkombination ungültig ist.
        """

        # Variante: Liste

        if loads is not None:

            if len(loads) != len(self.measurements):
                raise ValueError(
                    "Anzahl Laststufen stimmt nicht mit "
                    "Anzahl Messpunkte überein."
                )

            for measurement, load in zip(
                self.measurements,
                loads,
            ):
                measurement.corrected_load = float(load)

            return

        # Variante: Start + Schritt

        if start is not None and step is not None:

            for index, measurement in enumerate(
                self.measurements
            ):
                measurement.corrected_load = (
                    start + index * step
                )

            return

        raise ValueError(
            "Entweder 'loads' oder "
            "'start' und 'step' angeben."
        )

    def set_load_unit(
        self,
        unit: str,
    ) -> None:
        """
        Setzt die Last-Einheit für die gesamte Session.
        """

        for measurement in self.measurements:
            measurement.corrected_load_unit = unit