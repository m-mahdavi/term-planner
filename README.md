# Term Planner

**Term Planner** is a web application that helps automate academic planning by showing which modules should be offered for each intake of students across different programs.

## Features
- Displays modules for each program according to the selected intake and quarter.
- Automatically calculates first, second, and third-year intakes.
- Adds an "Intakes" column showing all cohorts a module will be offered to.
- Supports foundation and bachelor programs.
- Wide layout for easy reading of tables.

## Folder Structure
- `programs/` – contains CSV files with the curricula of different programs.
- `app.py` – main Streamlit application.

## Usage
1. Install dependencies:
```bash
pip install -r requirements.txt