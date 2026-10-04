# PyLactate

PyLactate is a Python-based framework for lactate test analysis, threshold determination, and performance diagnostics.

The project focuses on scientific transparency, reproducibility, and extensibility. Raw data is preserved at all times, while analysis-specific corrections and annotations are stored separately.

## Author

Stefan Meisenbacher

## Current Features

- CSV import for structured lactate test data
- Data validation
- Session-based data correction
- Manual load assignment
- Manual load unit assignment
- Measurement classification
  - preload
  - load
  - afterload
  - false
- Measurement selection for analysis
- Polynomial curve fitting
- Jupyter Notebook workflow

## Architecture

The project follows a layered architecture:

```text
CSV
│
▼
MeasurementRecord
│
▼
LactateTest
│
▼
Validation
│
▼
AnalysisSession
│
├─ manual corrections
├─ load assignment
├─ measurement classification
│
▼
MeasurementSelector
│
▼
FitStrategy
│
▼
FitResult
│
▼
ThresholdStrategy
│
▼
ThresholdResult
```

## Project Structure

```text
pylactate/
│
├── model/
├── importers/
├── validation/
├── analysis/
├── fitting/
├── plotting/
└── thresholds/
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd LactateMaster
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

### Windows

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Example Notebook

Start Jupyter:

```bash
jupyter notebook
```

Open:

```text
notebooks/01_architecture_smoke_test.ipynb
```

## Data Model

### Raw Data

Raw CSV data is represented by immutable objects.

```python
MeasurementRecord
```

Raw data is never modified.

### Analysis Session

All user modifications are stored in:

```python
AnalysisSession
```

Examples:

- assigning load stages
- changing load units
- classifying measurements
- excluding measurements from fitting

## Planned Features

### Curve Fitting

- Cubic spline
- Logistic fit
- Gompertz fit
- Exponential fit

### Threshold Detection

LS1:

- Baseline + 0.5 mmol/L
- Baseline + 1.0 mmol/L

LS2:

- Fixed 4 mmol/L
- Dmax
- Dickhuth
- Stegmann

### Visualization

- Single test plots
- Multi-test comparison
- Threshold visualization
- Export to PNG
- Export to PDF

## Development

Format and lint:

```bash
ruff check .
```

Type checking:

```bash
mypy .
```

Run tests:

```bash
pytest
```

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.
