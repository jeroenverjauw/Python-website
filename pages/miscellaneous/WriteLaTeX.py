import streamlit as st
from pathlib import Path
import subprocess

# Constants
OUTPUT_DIR = Path("pages/miscellaneous/write_latex")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  # Create it if it doesn't exist
TEX_FILE = OUTPUT_DIR / "main.tex"
PDF_FILE = OUTPUT_DIR / "main.pdf"
SVG_FILE = OUTPUT_DIR / "output.svg"
PNG_FILE = OUTPUT_DIR / "output.png"
DPI_OPTIONS = [72, 96, 150, 200, 300, 400, 600, 900, 1200]

# Functions
def crop_svg_with_inkscape(input_svg, output_svg):
    subprocess.run([
        "inkscape", input_svg,
        "--export-area-drawing",
        "--export-plain-svg",
        "-o", output_svg
    ], check=True)

def write_tex_file(latex_code: str, filepath: Path):
    latex_content = r"""
\documentclass{article}
\pagestyle{empty}
\usepackage{braket}
\usepackage{amsmath}
\begin{document}
""" + latex_code + r"""
\end{document}
"""
    filepath.write_text(latex_content)

def compile_latex_to_pdf(tex_file: Path, output_dir: Path):
    subprocess.run([
        "pdflatex", "-interaction=nonstopmode", "-output-format=pdf",
        f"-output-directory={output_dir.resolve()}", str(tex_file.name)
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=output_dir, timeout=60, text=True, check=True)

def convert_pdf_to_svg(pdf_file: Path, svg_file: Path):
    subprocess.run(["pdf2svg", str(pdf_file), str(svg_file)], check=True)

def convert_svg_to_png(svg_file: Path, png_file: Path, dpi: int):
    subprocess.run([
        "inkscape", str(svg_file),
        "--export-type=png",
        "--export-filename", str(png_file),
        f"--export-dpi={dpi}"
    ], check=True)

def load_file_bytes(path: Path):
    return path.read_bytes() if path.exists() else None

# Streamlit UI
st.title("LaTeX Rendered and Exporter")

latex_input = st.text_area(
    r"""Enter LaTeX code (rendered inside \begin{align*}...\end{align*})""",
    "E = \sqrt{(mc^2)^2 + (pc)^2}"
)
formatted_latex = rf"\begin{{align*}}{latex_input}\end{{align*}}"
st.latex(formatted_latex)

image_format = st.radio("Select image format", ["PNG", "SVG"])
dpi = None
if image_format == "PNG":
    dpi = st.select_slider("DPI for PNG export", options=DPI_OPTIONS, value=300)

if latex_input:
    write_tex_file(formatted_latex, TEX_FILE)
    compile_latex_to_pdf(TEX_FILE, OUTPUT_DIR)
    convert_pdf_to_svg(PDF_FILE, SVG_FILE)
    crop_svg_with_inkscape(SVG_FILE, SVG_FILE)

    if image_format == "SVG":
        svg_bytes = load_file_bytes(SVG_FILE)
        if svg_bytes:
            st.download_button("📄 Download SVG", svg_bytes, "equation.svg", "image/svg+xml")

    elif image_format == "PNG":
        convert_svg_to_png(SVG_FILE, PNG_FILE, dpi)
        png_bytes = load_file_bytes(PNG_FILE)
        if png_bytes:
            st.download_button("📄 Download PNG", png_bytes, "equation.png", "image/png")
