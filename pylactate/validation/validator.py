from itertools import pairwise

from pylactate.model.test import LactateTest
from pylactate.validation.issues import ValidationIssue


class TestValidator:
    """
    Technische Prüfung der Rohdaten eines Laktattests.
    """

    def validate(
        self,
        test: LactateTest,
    ) -> list:
        """
        Validiert einen importierten Laktattest.

        Args:
            test:
                Der zu prüfende Test.

        Returns:
            Liste gefundener Validierungsprobleme.
        """
        issues: list[ValidationIssue] = []

        self._validate_measurements(test, issues)
        self._validate_loads(test, issues)

        return issues

    def _validate_measurements(
        self,
        test: LactateTest,
        issues: list[ValidationIssue],
    ) -> None:
        """
        Prüft einzelne Messpunkte.
        """
        mids: set[str] = set()

        for record in test.records:

            if record.mid in mids:
                issues.append(
                    ValidationIssue(
                        severity="ERROR",
                        message="Doppelte MID.",
                        measurement_mid=record.mid,
                    )
                )

            mids.add(record.mid)

            if record.load is None:
                issues.append(
                    ValidationIssue(
                        severity="ERROR",
                        message="Fehlende Laststufe.",
                        measurement_mid=record.mid,
                    )
                )

            elif record.load < 0:
                issues.append(
                    ValidationIssue(
                        severity="ERROR",
                        message="Negative Laststufe.",
                        measurement_mid=record.mid,
                    )
                )

            if record.lactate_value < 0:
                issues.append(
                    ValidationIssue(
                        severity="ERROR",
                        message="Negativer Laktatwert.",
                        measurement_mid=record.mid,
                    )
                )

            if record.heart_rate < 40:
                issues.append(
                    ValidationIssue(
                        severity="WARNING",
                        message="HF < 40.",
                        measurement_mid=record.mid,
                    )
                )

            if record.heart_rate > 240:
                issues.append(
                    ValidationIssue(
                        severity="WARNING",
                        message="HF > 240.",
                        measurement_mid=record.mid,
                    )
                )

    def _validate_loads(
        self,
        test: LactateTest,
        issues: list[ValidationIssue],
    ) -> None:
        """
        Prüft die Struktur der Laststufen.
        """
        loads = [
            record.load
            for record in test.records
            if record.load is not None
        ]

        if not loads:
            issues.append(
                ValidationIssue(
                    severity="ERROR",
                    message="Keine Laststufen vorhanden.",
                )
            )
            return

        unique_loads = set(loads)

        if len(unique_loads) < 2:
            issues.append(
                ValidationIssue(
                    severity="ERROR",
                    message=(
                        "Alle Laststufen sind identisch. "
                        "Ein Kurvenfit ist nicht möglich."
                    ),
                )
            )

        if len(unique_loads) < len(loads):
            issues.append(
                ValidationIssue(
                    severity="WARNING",
                    message=(
                        "Mehrere Messpunkte besitzen "
                        "identische Laststufen."
                    ),
                )
            )

        if len(unique_loads) < 4:
            issues.append(
                ValidationIssue(
                    severity="WARNING",
                    message=(
                        "Sehr wenige unterschiedliche "
                        "Laststufen vorhanden."
                    ),
                )
            )

        for previous, current in pairwise(loads):
            if current < previous:
                issues.append(
                    ValidationIssue(
                        severity="WARNING",
                        message=(
                            "Laststufen sind nicht "
                            "monoton steigend."
                        ),
                    )
                )
                break
