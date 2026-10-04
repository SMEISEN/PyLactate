from dataclasses import dataclass

from pylactate.model.session import AnalysisSession


@dataclass(slots=True)
class AnalysisContext:
    """
    Gemeinsamer Laufzeitkontext für
    Fits und Schwellenmethoden.
    """

    session: AnalysisSession
