from pylactate.model.enums import PointClass
from pylactate.model.session import AnalysisSession, MeasurementReview


class MeasurementSelector:
    """
    Selektiert Messpunkte aus einer AnalysisSession.

    Die Klasse kapselt sämtliche Regeln, welche Messpunkte
    für Fits oder andere Analyseverfahren verwendet werden
    dürfen.
    """

    def get_fit_measurements(
        self,
        session: AnalysisSession,
    ) -> list[MeasurementReview]:
        """
        punkte, die für einen Kurvenfit
        verwendet werden dürfen.

        Regeln:
        - PointClass.LOAD
        - included_in_fit == True

        Args:
            session:
                Aktuelle Analyse-Session.

        Returns:
            Liste gültiger Messpunkte.
        """
        return [
            measurement
            for measurement in session.measurements
            if (
                measurement.point_class == PointClass.LOAD
                and measurement.included_in_fit
            )
        ]

    def get_preload_measurements(
        self,
        session: AnalysisSession,
    ) -> list:
        """
        Liefert alle PRELOAD-Messpunkte.

        Args:
            session:
                Aktuelle Analyse-Session.

        Returns:
            Liste der PRELOAD-Messpunkte.
        """
        return [
            measurement
            for measurement in session.measurements
            if measurement.point_class == PointClass.PRELOAD
        ]

    def get_load_measurements(
        self,
        session: AnalysisSession,
    ) -> list:
        """
        Liefert alle LOAD-Messpunkte.

        Args:
            session:
                Aktuelle Analyse-Session.

        Returns:
            Liste der LOAD-Messpunkte.
        """
        return [
            measurement
            for measurement in session.measurements
            if measurement.point_class == PointClass.LOAD
        ]

    def get_afterload_measurements(
        self,
        session: AnalysisSession,
    ) -> list:
        """
        Liefert alle AFTERLOAD-Messpunkte.

        Args:
            session:
                Aktuelle Analyse-Session.

        Returns:
            Liste der AFTERLOAD-Messpunkte.
        """
        return [
            measurement
            for measurement in session.measurements
            if measurement.point_class == PointClass.AFTERLOAD
        ]

    def get_false_measurements(
        self,
        session: AnalysisSession,
    ) -> list:
        """
        Liefert alle als FALSE markierten Messpunkte.

        Args:
            session:
                Aktuelle Analyse-Session.

        Returns:
            Liste der ausgeschlossenen Messpunkte.
        """
        return [
            measurement
            for measurement in session.measurements
            if measurement.point_class == PointClass.FALSE
        ]

    def get_all_measurements(
        self,
        session: AnalysisSession,
    ) -> list:
        """
        Liefert sämtliche Messpunkte.

        Args:
            session:
                Aktuelle Analyse-Session.

        Returns:
            Liste aller Messpunkte.
        """
        return list(session.measurements)
