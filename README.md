# Term Planner

**Term Planner** is a web application that helps automate academic planning by showing which modules should be offered for each intake of students across different programs.

## Folder Structure
- `programs/` – contains CSV files with the curricula of different programs.
- `app.py` – main Streamlit application.

## Usage
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Run the web application:
```bash
streamlit run app.py
```
3. Select the desired quarter and year at the top of the page to view module offerings for each program.