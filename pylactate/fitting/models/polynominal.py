from __future__ import annotations

import numpy as np


def polynomial(
    x: np.ndarray,
    y: np.ndarray,
    degree: int,
) -> np.poly1d:
    """
    Erstellt ein Polynommodell.

    Args:
        x:
            Laststufen.

        y:
            Laktatwerte.

        degree:
            Polynomgrad.

    Returns:
        Gefittetes Polynommodell.
    """

    coefficients = np.polyfit(
        x,
        y,
        deg=degree,
    )

    return np.poly1d(
        coefficients
    )


def weighted_polynomial(
    x: np.ndarray,
    y: np.ndarray,
    degree: int,
    weights: np.ndarray,
) -> np.poly1d:
    """
    Erstellt ein gewichtetes Polynommodell.

    Args:
        x:
            Laststufen.

        y:
            Laktatwerte.

        degree:
            Polynomgrad.

        weights:
            Gewichte gemäß numpy.polyfit(),
            typischerweise 1 / sigma.

    Returns:
        Gefittetes Polynommodell.
    """

    coefficients = np.polyfit(
        x,
        y,
        deg=degree,
        w=weights,
    )

    return np.poly1d(
        coefficients
    )
