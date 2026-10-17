# PyLactate Architektur-Manifest

## Vision

PyLactate ist eine wissenschaftliche Python-Bibliothek zur Analyse von Laktatmessungen, Kurvenanpassung und Schwellenwertbestimmung.

Das System soll:

- reproduzierbare Ergebnisse liefern
- fachliche Algorithmen klar von Infrastruktur trennen
- einfach erweiterbar sein
- wissenschaftlich nachvollziehbar bleiben
- testbar und wartbar sein

---

# 1. Fachlichkeit vor Technik

Die Paketstruktur orientiert sich an fachlichen Domänen:

```text
importers
model
analysis
fitting
thresholds
validation
plotting
```

Nicht technische Schichten bestimmen die Architektur, sondern der Analyseprozess.

---

# 2. Das Domain-Modell ist die zentrale Wahrheit

Alle Analysen arbeiten auf einheitlichen Domänenobjekten.

```python
Session
RawMeasurement
AnalysisResult
Threshold
```

### Regel

Es dürfen keine Dictionaries zwischen Modulen transportiert werden, wenn ein Domänenobjekt existiert.

### Ziele

- Typensicherheit
- bessere IDE-Unterstützung
- verständliche Schnittstellen

---

# 3. Abhängigkeiten zeigen nach innen

### Erlaubte Richtung

```text
plotting
    ↓

analysis
    ↓

thresholds
    ↓

model
```

Importer liefern Daten in das Modell.

```text
importers → model
```

### Nicht erlaubt

```text
model → analysis
model → plotting
thresholds → plotting
```

Der fachliche Kern kennt keine Darstellungsschicht.

---

# 4. Algorithmen sind austauschbar

Jeder Analyse- oder Fitting-Algorithmus implementiert ein gemeinsames Interface.

Beispiel:

```python
from typing import Protocol


class FitAlgorithm(Protocol):
    def fit(self, session: Session) -> FitResult:
        ...
```

### Ziele

- Erweiterbarkeit
- Austauschbarkeit
- Open/Closed Principle

Mögliche Implementierungen:

- Polynomial Fit
- Spline Fit
- Dmax
- LogLog
- Machine-Learning-Verfahren

---

# 5. Pure Functions bevorzugen

Analysefunktionen sollen keine Seiteneffekte besitzen.

### Bevorzugt

```python
result = calculate_threshold(
    session,
    fit_result,
)
```

### Vermeiden

```python
session.threshold = threshold
```

### Vorteile

- Testbarkeit
- Nachvollziehbarkeit
- Reproduzierbarkeit

---

# 6. Ergebnisse sind immutable

Analyseergebnisse werden nach ihrer Erstellung nicht verändert.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class AnalysisResult:
    ...
```

### Vorteile

- keine versteckten Nebeneffekte
- sichere Weiterverarbeitung
- einfachere Parallelisierung
- bessere Debugbarkeit

---

# 7. Validierung am Systemrand

Fehlerhafte Daten werden früh erkannt.

```text
CSV
 ↓
Importer
 ↓
Validation
 ↓
Model
```

### Architekturregel

Nach erfolgreicher Validierung darf der Rest des Systems davon ausgehen, dass die Daten gültig sind.

```text
Session ist gültig.
```

Keine redundanten Prüfungen innerhalb jedes Algorithmus.

---

# 8. Visualisierung ist nur ein Konsument

Plotting darf keine Berechnungen enthalten.

### Falsch

```python
plot_threshold(session)
```

wenn innerhalb der Funktion Schwellen neu berechnet werden.

### Richtig

```python
result = calculate_threshold(session)

plot_threshold(result)
```

Visualisierung konsumiert ausschließlich bereits berechnete Ergebnisse.

---

# 9. Erweiterung durch neue Module

Neue Features werden durch neue Implementierungen ergänzt.

### Bevorzugt

```text
fitting/
├── base.py
├── polynomial_fit.py
├── spline_fit.py
└── logistic_fit.py
```

### Vermeiden

```python
if fit_type == "poly":
    ...
elif fit_type == "spline":
    ...
elif fit_type == "logistic":
    ...
```

Große Verzweigungen erschweren Wartung und Erweiterung.

---

# 10. Reproduzierbarkeit hat Priorität

Jedes Analyseergebnis muss vollständig nachvollziehbar sein.

Ein Analyseergebnis dokumentiert:

```python
{
    "algorithm": "...",
    "parameters": {...},
    "input_data": "...",
    "version": "..."
}
```

### Ziel

Ein wissenschaftliches Ergebnis muss auch Jahre später reproduziert werden können.

---

# Zielarchitektur

```text
               +----------------+
               |   CSV Import   |
               +----------------+
                        |
                        v
               +----------------+
               |   Validation   |
               +----------------+
                        |
                        v
               +----------------+
               |     Model      |
               +----------------+
                        |
       +----------------+----------------+
       |                                 |
       v                                 v
+--------------+               +----------------+
|   Fitting    |               |  Thresholds    |
+--------------+               +----------------+
       |                                 |
       +---------------+-----------------+
                       |
                       v
              +----------------+
              |   Analysis     |
              +----------------+
                       |
                       v
              +----------------+
              |    Results     |
              +----------------+
                       |
                       v
              +----------------+
              |    Plotting    |
              +----------------+
```

---

# Definition of Done

Jeder neue Beitrag zum Projekt muss folgende Kriterien erfüllen:

- ✅ Type Hints vorhanden
- ✅ Ruff ohne Fehler
- ✅ Pytest-Test vorhanden
- ✅ Keine zyklischen Abhängigkeiten
- ✅ Keine Fachlogik im Plotting
- ✅ Domänenobjekte statt Dictionaries
- ✅ Reproduzierbare Ergebnisse
- ✅ Vollständige Docstrings für öffentliche APIs

---

# Empfohlene Weiterentwicklung

## Zusätzliche Verzeichnisse

```text
pylactate/

├── analysis/
├── fitting/
├── importers/
├── model/
├── plotting/
├── thresholds/
├── validation/

├── interfaces/
│   └── protocols.py

├── services/
│   └── analysis_service.py

└── tests/
```

## interfaces/

Enthält ausschließlich Verträge und Protokolle:

```python
FitAlgorithm
ThresholdAlgorithm
Importer
Validator
```

## services/

Orchestriert komplexere Analyseabläufe:

```python
AnalysisService
```

Der Service koordiniert:

1. Import
2. Validierung
3. Fitting
4. Schwellenbestimmung
5. Ergebnisaufbereitung

ohne Fachlogik zu duplizieren.

---

# Architekturprinzipien

1. Fachlichkeit vor Technik
2. Explizite Abhängigkeiten
3. Domain Driven Design Light
4. Pure Functions bevorzugen
5. Immutability wo sinnvoll
6. Austauschbare Algorithmen
7. Frühe Validierung
8. Reproduzierbare Wissenschaft
9. Testbarkeit als Architekturziel
10. Erweiterbarkeit ohne Änderung bestehender Komponenten

---

## Leitsatz

> Jede Analyse muss nachvollziehbar, reproduzierbar und durch Hinzufügen neuer Algorithmen erweiterbar sein, ohne bestehende Komponenten verändern zu müssen.