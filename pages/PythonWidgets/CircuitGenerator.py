import streamlit as st
import subprocess
import tempfile
from pathlib import Path

def latex_to_svg(latex_code: str) -> Path:
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = Path(tmpdir) / "formula.tex"
        pdf_path = Path(tmpdir) / "formula.pdf"
        svg_path = Path(tmpdir) / "formula.svg"

        # Wrap in minimal LaTeX document
        tex_content = rf"""
\documentclass{{standalone}}
\usepackage{{amsmath}}
\begin{{document}}
${latex_code}$
\end{{document}}
        """

        tex_path.write_text(tex_content)

        subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_path.name], cwd=tmpdir, check=True)
        subprocess.run(["pdf2svg", pdf_path.name, svg_path.name], cwd=tmpdir, check=True)

        return svg_path.read_bytes()

# Streamlit UI
st.title("LaTeX to SVG Renderer")

latex_input = st.text_area("Enter LaTeX math:", value=r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}")
if st.button("Render as SVG"):
    try:
        svg_data = latex_to_svg(latex_input)
        st.image(svg_data)
        st.download_button("Download SVG", svg_data, file_name="formula.svg", mime="image/svg+xml")
    except subprocess.CalledProcessError as e:
        st.error("Error rendering LaTeX. Ensure pdflatex and pdf2svg are installed.")
