from pages.miscellaneous.WriteLaTeX import load_file_bytes
import streamlit as st
from pathlib import Path
import subprocess
from subprocess import run, PIPE 

import drawsvg as draw
import scipy
import numpy as np
import base64

from pages.PythonWidgets.CircuitGenerator.functions import *

def load_file_bytes(path: Path):
    return path.read_bytes() if path.exists() else None

# Constants
OUTPUT_DIR = Path("pages/PythonWidgets/CircuitGenerator")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  # Create it if it doesn't exist
TEX_FILE = OUTPUT_DIR / "main.tex"
PDF_FILE = OUTPUT_DIR / "main.pdf"
SVG_FILE = OUTPUT_DIR / "output.svg"

default_fontsize = 27 # I think I will have to work with rescaling factors

st.title("Quantum circuit generator")


# Width input with unit
col1, col2 = st.columns([2,1])
with col1:
    width_value = st.number_input("Width", min_value=1, value=100)
with col2:
    width_unit = st.selectbox("Unit", ["px", "cm", "mm", "in"])

# Rows and columns
# Width input with unit
col1, col2 = st.columns([1,1])
with col1:
    rows = st.number_input("Number of rows", min_value=1, value=2)
with col2:
    cols = st.number_input("Number of columns", min_value=1, value=3)

st.subheader("Row division")

division_type = st.selectbox(
    "Division type",
    ["absolute units", "percentages", "relative"]
)

col_inputs = []

# Determine the target total only for constrained modes
if division_type == "absolute units":
    target_total = width_value
elif division_type == "percentages":
    target_total = 100
else:
    target_total = None  # "relative" mode (no constraint)

cols_container = st.columns(cols)

# INPUT FOR ALL BUT LAST COLUMN
for i in range(cols - 1):
    with cols_container[i]:
        val = st.number_input(
            f"Col {i+1}",
            value=0.0,
            min_value=0.0,
            key=f"col_input_{i}",
        )
        col_inputs.append(val)

# ---- LAST COLUMN LOGIC ----
with cols_container[-1]:
    if division_type in ["absolute units", "percentages"]:
        # Auto-calculate the last value (read-only)
        remaining = target_total - sum(col_inputs)
        remaining = max(0.0, remaining)  # avoid negative when user overfills

        st.number_input(
            f"Col {cols} (auto)",
            value=remaining,
            key=f"col_input_{cols-1}",
            disabled=True,
        )
        col_inputs.append(remaining)

    else:
        # Relative mode (user can freely edit last column)
        val_last = st.number_input(
            f"Col {cols}",
            value=0.0,
            min_value=0.0,
            key=f"col_input_{cols-1}",
        )
        col_inputs.append(val_last) 

# Example LaTeX expression
latex_expr = st.text_input("write something here")
if latex_expr:
    st.write(latex_expr)
    file_name_latex_expr = latex_expr.replace("\\", "").replace("$", "")
    write_tex_file(latex_expr, TEX_FILE, default_fontsize)
    compile_latex_to_pdf(TEX_FILE, OUTPUT_DIR)
    convert_pdf_to_svg(PDF_FILE, OUTPUT_DIR / f"{file_name_latex_expr}.svg")


    svg_bytes = load_file_bytes(OUTPUT_DIR / f"{file_name_latex_expr}.svg")
    if svg_bytes:
        st.download_button("📄 Download SVG", svg_bytes, "equation.svg", "image/svg+xml")



    # # --- Generate SVG ---
    # svg_width = f"{width_value}{width_unit}"
    # svg_height = f"{rows*50}{width_unit}"  # simple proportional height

    # # --- Load your LaTeX SVG ---
    # with open(f"{OUTPUT_DIR}/{file_name_latex_expr}.svg", "r", encoding="utf-8") as f:
    #     latex_svg = f.read()

    # # Optional: strip XML header if present
    # if "<?xml" in latex_svg:
    #     latex_svg = latex_svg.split("?>", 1)[1]

    # # Example SVG: draw a rectangle with given width/height
    # svg_content = f"""
    # <svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}">
    #     <rect x="0" y="0" width="{svg_width}" height="{svg_height}" fill="white" stroke="black"/>
    #     <g transform="translate(20,50)">
    #         {latex_svg}
    #     </g>
    #     <g transform="translate(20,10) scale(2)">
    #         {latex_svg}
    #     </g> 
    # </svg>
    # """

    # # Show SVG in app
    # st.subheader("Preview SVG")
    # st.image(f"data:image/svg+xml;base64,{base64.b64encode(svg_content.encode()).decode()}")

    # # Download button
    # b64 = base64.b64encode(svg_content.encode()).decode()
    # href = f'<a href="data:image/svg+xml;base64,{b64}" download="drawing.svg">📥 Download SVG</a>'
    # st.markdown(href, unsafe_allow_html=True)
    # Display what was entered
    # st.write("Width:", width_value, width_unit)
    # st.write("Rows:", rows, "Columns:", cols)
    # st.write("Row values:", col_inputs)
