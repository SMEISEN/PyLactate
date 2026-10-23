from __future__ import annotations

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.interpolate import UnivariateSpline


def cubic_spline(
    x: np.ndarray,
    y: np.ndarray,
) -> CubicSpline:
    """
    Erstellt einen kubischen Spline.
    """

    return CubicSpline(
        x,
        y,
        extrapolate=True,
    )


def weighted_spline(
    x: np.ndarray,
    y: np.ndarray,
    weights: np.ndarray,
    spline_degree: int = 3,
) -> UnivariateSpline:
    """
    Erstellt einen gewichteten Spline.

    Args:
        x:
            Stützstellen.

        y:
            Messwerte.

        weights:
            Gewichte (typischerweise 1 / sigma).

        spline_degree:
            Grad des Splines.

    Returns:
        Konfiguriertes UnivariateSpline-Modell.
    """

    return UnivariateSpline(
        x=x,
        y=y,
        w=weights,
        k=spline_degree,
        s=None,
    )
