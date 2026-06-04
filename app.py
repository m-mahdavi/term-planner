import os
import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Term Planner", layout="centered")


SEQUENCES = {
    "fp": {
        "Oct": ["1A", "1B"],
        "Jan": ["1B", "1C"],
        "Apr": ["1C", "1D"],
        "Jul": ["1D", "1A"]
    },
    "b": {
        "Oct": ["1A", "1B", "1C", "1D", "2A", "2B", "2C", "2D", "3A", "3B", "3C", "3D"],
        "Jan": ["1B", "1C", "1D", "1A", "2B", "2C", "2D", "2A", "3B", "3A", "3C", "3D"],
        "Apr": ["1C", "1D", "1A", "1B", "2C", "2D", "2A", "2B", "3A", "3B", "3C", "3D"],
        "Jul": ["1D", "1A", "1B", "1C", "2D", "2A", "2B", "2C", "3B", "3A", "3C", "3D"]
    },
    "m12": {
        "Oct": ["1A", "1B", "1C", "1D"],
        "Jan": ["1B", "1C", "1A", "1D"],
        "Apr": ["1A", "1B", "1C", "1D"],
        "Jul": ["1B", "1C", "1A", "1D"]
    },
    "m18": {
        "Oct": ["1A", "1B", "1C", "1D", "2A", "2B"],
        "Jan": ["1B", "1C", "1D", "1A", "2A", "2B"],
        "Apr": ["1A", "1B", "1C", "1D", "2A", "2B"],
        "Jul": ["1B", "1C", "1D", "1A", "2A", "2B"]
    },
    "m24": {
        "Oct": ["1A", "1B", "1C", "1D", "2A", "2B", "2C", "2D"],
        "Jan": ["1B", "1C", "1D", "1A", "2B", "2A", "2C", "2D"],
        "Apr": ["1A", "1B", "1C", "1D", "2A", "2B", "2C", "2D"],
        "Jul": ["1B", "1C", "1D", "1A", "2B", "2A", "2C", "2D"]
    },
    "mkibm": {
        "Oct": ["1A", "1B", "1C", "1D", "2A", "2B", "2C", "2D"],
        "Jan": ["1B", "1C", "1D", "1A", "2B", "2A", "2C", "2D"],
        "Apr": ["1C", "1D", "1A", "1B", "2A", "2B", "2C", "2D"],
        "Jul": ["1C", "1A", "1B", "1D", "2B", "2A", "2C", "2D"] 
    }
}
QUARTERS = ["Oct", "Jan", "Apr", "Jul"]
YEARS = [datetime.datetime.now().year + i for i in range(5)]


def load_program_files(base_path):
    data = []
    subfolders = ["others", "bachelors", "masters"]
    if os.path.exists(base_path):
        for sub in subfolders:
            sub_path = os.path.join(base_path, sub)
            if os.path.exists(sub_path):
                for file in sorted(os.listdir(sub_path)):
                    if file.endswith(".csv"):
                        data.append({
                            "path": os.path.join(sub_path, file),
                            "filename": file,
                            "type": sub
                        })
    return data

def build_quarter_intake_mapping(intakes, sequence):
    mapping = {}
    for i, intake in enumerate(intakes):
        if i < len(sequence[intake[0]]):
            q = sequence[intake[0]][i]
            if q not in mapping:
                mapping[q] = []
            mapping[q].append(intake)
    return mapping

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


st.title("Term Planner")

col1, col2 = st.columns(2)
with col1:
    quarter = st.selectbox("Select intake:", QUARTERS)
with col2:
    year = st.selectbox("Select year:", YEARS)

col_a, col_b = st.columns(2)
with col_a:
    show_bs = st.checkbox("Business School (BS)")
with col_b:
    show_cs = st.checkbox("Computer Science School (CS)")


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

selected_files = []
if show_bs:
    files = load_program_files(os.path.join("programs", "bs"))
    for f in files: f["school"] = "Business School (BS)"
    selected_files.extend(files)
if show_cs:
    files = load_program_files(os.path.join("programs", "cs"))
    for f in files: f["school"] = "Computer Science School (CS)"
    selected_files.extend(files)

current_school = None
current_type = None

for item in selected_files:

    if item["school"] != current_school:
        current_school = item["school"]
        st.header(f"🏢 {current_school}")
        st.divider()
        current_type = None 
    if item["type"] != current_type:
        current_type = item["type"]
        st.markdown(f"## 🎓 {current_type.title()}")
    
    file_path = item["path"]
    filename = item["filename"]
    base_name = filename.rsplit('.', 1)[0]
    program_name, sequence_key = base_name.rsplit('_', 1)
    
    st.subheader(f"{program_name.replace('_', ' ').upper()} ({sequence_key.upper()})")
    st.caption(f"Category: {item['type'].title()} | Source: {file_path}")
    
    df = pd.read_csv(file_path)
    mapping = build_quarter_intake_mapping(intakes, SEQUENCES[sequence_key])
    result = build_result_table(df, mapping)          
    table_height = min(len(result) * 35 + 40, 500) 
    st.dataframe(result, use_container_width=True, hide_index=True, height=table_height)
