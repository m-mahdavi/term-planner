import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Term Planner", layout="centered")


SEQUENCE_B = {
    "Oct": ["1A", "1B", "1C", "1D", "2A", "2B", "2C", "2D", "3A", "3B", "3C", "3D"],
    "Jan": ["1B", "1C", "1D", "1A", "2B", "2C", "2D", "2A", "3B", "3A", "3C", "3D"],
    "Apr": ["1C", "1D", "1A", "1B", "2C", "2D", "2A", "2B", "3A", "3B", "3C", "3D"],
    "Jul": ["1D", "1A", "1B", "1C", "2D", "2A", "2B", "2C", "3B", "3A", "3C", "3D"]
}
SEQUENCE_M12 = {
    "Oct": ["1A", "1B", "1C", "1D"],
    "Jan": ["1B", "1C", "1A", "1D"],
    "Apr": ["1A", "1B", "1C", "1D"],
    "Jul": ["1B", "1C", "1A", "1D"]
}
SEQUENCE_M18 = {
    "Oct": ["1A", "1B", "1C", "1D", "2A", "2B"],
    "Jan": ["1B", "1C", "1D", "1A", "2A", "2B"],
    "Apr": ["1A", "1B", "1C", "1D", "2A", "2B"],
    "Jul": ["1B", "1C", "1D", "1A", "2A", "2B"]
}
SEQUENCE_M24 = {
    "Oct": ["1A", "1B", "1C", "1D", "2A", "2B", "2C", "2D"],
    "Jan": ["1B", "1C", "1D", "1A", "2B", "2A", "2C", "2D"],
    "Apr": ["1A", "1B", "1C", "1D", "2A", "2B", "2C", "2D"],
    "Jul": ["1B", "1C", "1D", "1A", "2B", "2A", "2C", "2D"]
}
QUARTERS = ["Oct", "Jan", "Apr", "Jul"]
YEARS = [2026, 2027, 2028, 2029]


st.title("Term Planner")

col1, col2 = st.columns(2)
with col1:
    quarter = st.selectbox("Select intake:", QUARTERS)
with col2:
    year = st.selectbox("Select year:", YEARS)

intakes = []
qi, y = QUARTERS.index(quarter), year
while len(intakes) < 12:
    q = QUARTERS[qi]
    intakes.append((q, y))
    qi -= 1
    if qi < 0:
        qi = len(QUARTERS) - 1
    if q == "Jan":
        y -= 1

def build_quarter_intake_mapping(intakes, sequence):
    mapping = {}
    for i, intake in enumerate(intakes):
        if i < len(sequence[intake[0]]):
            q = sequence[intake[0]][i]
            if q not in mapping:
                mapping[q] = []
            mapping[q].append(intake)
    return mapping

quarter_intake_mapping_b = build_quarter_intake_mapping(intakes, SEQUENCE_B)
quarter_intake_mapping_m12 = build_quarter_intake_mapping(intakes, SEQUENCE_M12)
quarter_intake_mapping_m18 = build_quarter_intake_mapping(intakes, SEQUENCE_M18)
quarter_intake_mapping_m24 = build_quarter_intake_mapping(intakes, SEQUENCE_M24)

def build_result_table(df, quarter_mapping):
    parts = []
    for key, intake_list in quarter_mapping.items():
        year_val = int(key[0])
        quarter_val = key[1]
        filtered = df[
            (df["Year"] == year_val) &
            (df["Quarter"] == quarter_val)
        ].copy()
        filtered["Intakes"] = ", ".join(f"{q} {y}" for q, y in intake_list)
        parts.append(filtered)
    if parts:
        return pd.concat(parts).reset_index(drop=True)
    return pd.DataFrame(columns=df.columns.tolist() + ["Intakes"])

for file in sorted(os.listdir("programs")):
    if not file.endswith(".csv"):
        continue

    program_name, program_version = file.split(".")[0].split("_")
    st.subheader(program_name.upper() + " - " + program_version.upper())
    df = pd.read_csv(os.path.join("programs", file))

    if program_version in ["f", "p"]:
        result = df[df["Quarter"] == ["A", "B", "C", "D"][QUARTERS.index(quarter)]].copy()
    elif program_version == "b":
        result = build_result_table(df, quarter_intake_mapping_b)
    elif program_version == "m12":
        result = build_result_table(df, quarter_intake_mapping_m12)
    elif program_version == "m18":
        result = build_result_table(df, quarter_intake_mapping_m18)
    elif program_version == "m24":
        result = build_result_table(df, quarter_intake_mapping_m24)
    else:
        continue
        
    result = result.reset_index(drop=True)
    st.dataframe(result, use_container_width=True, height=len(result)*35 + 40, hide_index=True)