from enum import Enum


class PointClass(str, Enum):
    """
    Fachliche Klassifikation eines Messpunktes.

    Diese Klassifikation entsteht während der Analyse
    und ist nicht zwingend identisch mit dem CSV-Feld
    'Measurement type'.
    """

    PRELOAD = "preload"
    LOAD = "load"
    AFTERLOAD = "afterload"
    FALSE = "false"
