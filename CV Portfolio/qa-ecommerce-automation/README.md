# QA E-commerce Automation

Automation project for the Flask e-commerce demo.

## Prerequisites

The Flask application should be running at:

http://localhost:5000

## Setup

Open a terminal in this folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the tests

```powershell
pytest
```

## Initial project structure

- `tests/api/` - API automation
- `tests/ui/` - future browser/UI automation
- `tests/database/` - future database validation
- `utils/` - reusable helpers
- `test_data/` - test data

Start with the API tests, then expand into UI and database testing.
