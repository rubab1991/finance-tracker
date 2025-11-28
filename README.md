# Personal Finance Tracker CLI

This is a professional CLI application for tracking expenses, income, budgets, and generating financial insights.

## Features

- **Transaction Management**: Add, list, and manage income and expense transactions.
- **Budgeting**: Set monthly budgets for different categories and track your spending against them.
- **Financial Analytics**: Get a detailed financial report with spending analysis, savings rate, and a financial health score.
- **Smart Assistant**: An AI-powered assistant to answer your financial questions.
- **Data Management**: Export, import, backup, and reset your financial data.
- **Web Dashboard**: A simple web interface to visualize your financial data.

## Tech Stack

- **Language**: Python 3.11+
- **CLI Framework**: `questionary`
- **UI Library**: `rich`
- **Web Dashboard**: `streamlit`
- **Storage**: Plain text files (CSV format)
- **Package Manager**: `uv`

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd finance-tracker
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt 
    # or if you have uv installed
    uv pip install -r requirements.txt
    ```
    *Note: A `requirements.txt` file will need to be generated from `pyproject.toml`.*

## How to Run

### Main CLI Application

To start the main command-line interface, run:

```bash
python main.py
```

This will launch an interactive menu where you can access all the features of the finance tracker.

### Web Dashboard

To launch the web dashboard, you have two options:

1.  **From the CLI:**
    - Run the main application (`python main.py`).
    - Select the "Launch Web Dashboard" option from the menu.

2.  **Directly from the terminal:**
    ```bash
    streamlit run dashboard.py
    ```

This will open a new tab in your web browser with the financial dashboard.

## Project Structure

```
finance-tracker/
├── main.py                    # Entry point with menu loop
├── dashboard.py               # Streamlit web dashboard
├── database/
│   ├── transactions.txt       # All transactions
│   └── budgets.txt            # Budget allocations
├── features/
│   ├── transactions/
│   ├── budgets/
│   ├── analytics/
│   ├── smart_assistant/
│   ├── data_management/
│   └── data/
│       └── provider.py        # Centralized data loading logic
├── backups/                   # For data backups
├── pyproject.toml             # Project metadata and dependencies
└── README.md
```
