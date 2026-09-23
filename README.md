# Smart Kitchen

Smart Kitchen is an intelligent meal-planning and inventory-management prototype designed around shared kitchens and student-dorm environments.

The system combines rule-based planning, NLP-based recipe processing, inventory tracking, and a Flask web interface with real-time updates.

## What it demonstrates

- Multi-fridge inventory management
- Ingredient quantity and expiration tracking
- Recipe recommendations based on available ingredients, kitchenware, and serving count
- Shopping-list generation for missing ingredients
- NLP preprocessing and rule extraction from unstructured recipes
- Real-time inventory updates through Flask-SocketIO
- Both CLI and web application workflows

## Architecture

```text
                    ┌────────────────────┐
                    │   Recipe / Fridge  │
                    │      JSON data     │
                    └─────────┬──────────┘
                              │
             ┌────────────────▼────────────────┐
             │        Planning engine          │
             │ ingredient + serving + tooling  │
             │             rules                │
             └──────────────┬─────────────────┘
                            │
              ┌─────────────▼─────────────┐
              │       Recommendations      │
              │  recipes + missing items   │
              └─────────────┬─────────────┘
                            │
                 ┌──────────▼──────────┐
                 │ Flask / SocketIO UI │
                 │      + SQLite       │
                 └─────────────────────┘

NLP pipeline:
raw recipes → text cleaning → rule extraction → structured recipes
```

## Tech stack

- Python 3.10+
- Flask
- Flask-SocketIO
- SQLite
- spaCy
- HTML / CSS / JavaScript
- JSON-based domain data

## Project structure

```text
Smart-Kitchen/
├── backend/              # Inventory, planning, and ordering logic
├── data/                 # Fridges, kitchenware, and recipe datasets
├── docs/                 # Supporting project documentation
├── nlp/                  # Recipe preprocessing and rule extraction
├── static/               # Frontend assets
├── templates/            # Flask templates
├── main.py               # CLI and web entry point
└── requirements.txt      # Python dependencies
```

## Getting started

### Prerequisites

- Python 3.10+
- pip
- A virtual environment is recommended

### 1. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare the data

The project uses files in `data/` for fridge inventories, available kitchenware, and recipe content.

When recipe source data changes, regenerate the NLP-derived data:

```bash
python nlp/clean_text.py
python nlp/rule_extractor.py
```

### 4. Run the CLI

```bash
python main.py
```

### 5. Run the web application

```bash
python main.py web
```

Then open:

```text
http://localhost:5000
```

## Core workflow

A typical planning request combines:

1. selected fridge inventories;
2. serving requirements;
3. available kitchenware;
4. recipe ingredients and extracted rules;
5. ingredient freshness and quantities.

The planner uses that information to identify suitable recipes and generate the missing-item list.

## NLP pipeline

Recipe text can be processed into a more structured representation:

```text
Unstructured recipe
        │
        ▼
Text cleaning
        │
        ▼
Entity / pattern extraction
        │
        ▼
Structured recipe + rules
```

This part of the project is intended as an applied NLP component rather than a general-purpose language understanding system.

## Notes and limitations

- The application is a prototype and is designed primarily for local demonstration.
- SQLite is used for simplicity.
- Inventory and recipe datasets are local project data rather than a production-scale data service.
- The recommendation logic is rule-driven and can be extended with learned ranking or personalization in a future version.

## License

License information should be added here when the project license is finalized.
