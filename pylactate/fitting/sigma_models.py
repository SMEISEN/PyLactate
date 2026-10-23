from __future__ import annotations

from collections.abc import Callable


SigmaFunction = Callable[[float], float]


def constant_sigma(
    sigma: float,
) -> SigmaFunction:
    """
    Erstellt ein Sigma-Modell mit konstanter
    Standardabweichung.

    Args:
        sigma:
            Standardabweichung in mmol/l.

    Returns:
        Funktion zur Berechnung der Standardabweichung.

    Raises:
        ValueError:
            Falls sigma <= 0.
    """
    if sigma <= 0:
        raise ValueError(
            "sigma muss > 0 sein."
        )

    def model(
        lactate_value: float,
    ) -> float:
        return sigma

    return model


def relative_sigma(
    relative_error: float,
) -> SigmaFunction:
    """
    Relatives Fehlermodell.

    Beispiel:
        relative_error = 0.03

        => sigma = lactate * 0.03

    Args:
        relative_error:
            Relativer Fehler als Dezimalzahl.

    Returns:
        Funktion zur Berechnung der Standardabweichung.

    Raises:
        ValueError:
            Falls relative_error <= 0.
    """
    if relative_error <= 0:
        raise ValueError(
            "relative_error muss > 0 sein."
        )

    def model(
        lactate_value: float,
    ) -> float:
        return max(
            lactate_value * relative_error,
            1e-9,
        )

    return model


def mixed_sigma(
    absolute_error: float,
    relative_error: float,
) -> SigmaFunction:
    """
    Gemischtes Fehlermodell.

    Verwendet den größeren Wert aus absolutem
    und relativem Fehler.

    Formel:
        sigma = max(
            absolute_error,
            lactate * relative_error,
        )

    Args:
        absolute_error:
            Absoluter Fehler in mmol/l.

        relative_error:
            Relativer Fehler als Dezimalzahl.

    Returns:
        Funktion zur Berechnung der Standardabweichung.
    """
    if absolute_error <= 0:
        raise ValueError(
            "absolute_error muss > 0 sein."
        )

    if relative_error <= 0:
        raise ValueError(
            "relative_error muss > 0 sein."
        )

    def model(
        lactate_value: float,
    ) -> float:
        return max(
            absolute_error,
            lactate_value * relative_error,
        )

    return model


def lactate_scout_sport_sigma(
    lactate_value: float,
) -> float:
    """
    Sigma-Modell gemäß Lactate Scout Sport.

    Herstellerangabe:

    - 0.5 bis 6.7 mmol/l:
        SD <= 0.2 mmol/l

    - 6.8 bis 25 mmol/l:
        CV <= 3 %

    Returns:
        Geschätzte Standardabweichung in mmol/l.
    """
    if lactate_value <= 6.7:
        return 0.2

    return lactate_value * 0.03


def lactate_scout_sport_interpolated_sigma(
    lactate_value: float,
) -> float:
    """
    Glatte Approximation der Lactate-Scout-Spezifikation.

    Bis 6.7 mmol/l wird sigma = 0.2 verwendet.

    Danach erfolgt eine lineare Interpolation bis
    25 mmol/l und anschließend eine Fortschreibung
    mit 3 % relativem Fehler.

    Returns:
        Geschätzte Standardabweichung in mmol/l.
    """
    if lactate_value <= 6.7:
        return 0.2

    if lactate_value >= 25.0:
        return lactate_value * 0.03

    sigma_low = 0.2
    sigma_high = 25.0 * 0.03

    ratio = (
        (lactate_value - 6.7)
        / (25.0 - 6.7)
    )

    return (
        sigma_low
        + ratio
        * (sigma_high - sigma_low)
    )
