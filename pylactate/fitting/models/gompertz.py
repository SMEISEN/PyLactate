from __future__ import annotations

import numpy as np


def gompertz(
    x: np.ndarray,
    a: float,
    b: float,
    c: float,
) -> np.ndarray:
    """
    Gompertz-Funktion.

    Modell:

        y = a * exp(-b * exp(-c * x))

    Args:
        x:
            Unabhängige Variable.

        a:
            Obere Asymptote.

        b:
            Verschiebungsparameter.

        c:
            Wachstumsrate.

    Returns:
        Berechnete y-Werte.
    """

    return a * np.exp(-b * np.exp(-c * x))
