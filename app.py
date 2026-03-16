import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Term Planner", layout="wide")

QUARTERS = ["Oct", "Jan", "Apr", "Jul"]
YEARS = [2026, 2027, 2028, 2029]
SEQUENCE_STANDARD = ["A", "B", "C", "D"]
SEQUENCE_B_Y3 = ["A", "B", "A", "B"]

st.title("Term Planner")

col1, col2 = st.columns(2)
with col1:
    quarter = st.selectbox("Select intake:", QUARTERS)
with col2:
    year = st.selectbox("Select year:", YEARS)

q_index = QUARTERS.index(quarter)

intakes = []
qi = q_index
y = year
q = QUARTERS[qi]
while len(intakes) < 12:
    intakes.append((q, y))
    qi -= 1
    if qi < 0:
        qi = len(QUARTERS) - 1
    q = QUARTERS[qi]
    if q == "Oct":
        y -= 1

year1_intakes = [f"{q} {y}" for q, y in intakes[:4]]
year2_intakes = [f"{q} {y}" for q, y in intakes[4:8]]
year3_intakes = [f"{q} {y}" for q, y in intakes[8:10]]

def get_foundation_modules(df, q_index):
    q = SEQUENCE_STANDARD[q_index]
    return df[df["Quarter"] == q]

def get_bachelor_modules(df, q_index):
    q_y12 = SEQUENCE_STANDARD[q_index]
    q_y3 = SEQUENCE_B_Y3[q_index]

    return df[
        ((df["Year"].isin([1,2])) & (df["Quarter"] == q_y12)) |
        ((df["Year"] == 3) & (df["Quarter"] == q_y3))
    ]

for file in sorted(os.listdir("programs")):
    if not file.endswith(".csv"):
        continue

    program_name = file.split(".")[0].upper()
    df = pd.read_csv(os.path.join("programs", file))

    st.subheader(program_name)

    if file.startswith("f"):
        result = get_foundation_modules(df, q_index)
    elif file.startswith("b"):
        result = get_bachelor_modules(df, q_index)
    else:
        continue

    result = result.copy()

    def map_intakes(row):
        if row["Year"] == 1:
            return ", ".join(year1_intakes)
        elif row["Year"] == 2:
            return ", ".join(year2_intakes)
        elif row["Year"] == 3:
            return ", ".join(year3_intakes)
        else:
            return ""

    result["Intakes"] = result.apply(map_intakes, axis=1)
    result = result.reset_index(drop=True)

    st.dataframe(result, use_container_width=True, hide_index=True)