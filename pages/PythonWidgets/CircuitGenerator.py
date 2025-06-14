import streamlit as st
from pathlib import Path
import subprocess
from subprocess import run, PIPE

output_dir = Path(".")

def crop_svg_with_inkscape(input_svg, output_svg):
    cmd = [
        "inkscape", input_svg,
        "--export-area-drawing",
        "--export-plain-svg",
        "-o", output_svg
    ]
    subprocess.run(cmd, check=True)

def write_tex_file(latex_code, output_dir):
    latex_content = r"""
\documentclass{article}
\pagestyle{empty} % This removes page numbers from all pages

\usepackage{braket}
\usepackage{amsmath}
\begin{document}
""" + \
    latex_code + \
r"""
\end{document}"""

    # Save to .tex file
    with open("main.tex", "w") as f:
        f.write(latex_content)

st.title("Quantum circuit generator")
latex_code = st.text_area(r"""Enter LaTeX code (code is rendered within \begin{align*}...\end{align*})""", "E = \ket{1}")
latex_code = r"""\begin{align*}""" + latex_code + r"""\end{align*}""" 
st.latex(latex_code)

image_format = st.radio("Select image format", ["PNG", "SVG"])

dpi_options = [72, 96, 150, 200, 300, 400, 600, 900, 1200]
if image_format == 'PNG':
    dpi = st.select_slider(
        "DPI for PNG image export",
        options=dpi_options,
        value=300
    )

if latex_code: 
    write_tex_file(latex_code, output_dir)

    process = run(args=['pdflatex', '-interaction=nonstopmode', '-output-format=pdf', 
                        f'-output-directory={output_dir.resolve()}', 'main.tex'],
            stdout=PIPE, stderr=PIPE, cwd=output_dir,
            timeout=60, text=True)

    process = run(args = ['pdf2svg', 'main.pdf', 'output.svg'])

    crop_svg_with_inkscape('output.svg', 'output.svg')


    svg_path = output_dir / 'output.svg'
    

    if svg_path.exists():
        with open(svg_path, "rb") as f:
            svg_bytes = f.read()

    if image_format=='SVG':
        st.download_button(
            label="📄 Download svg",
            data=svg_bytes,
            file_name="equation.svg",
            mime="image/svg+xml"
        )
    elif image_format=='PNG':
        subprocess.run(["inkscape", "test.svg","--export-type=png",
                     "--export-filename=output.png",
                    f"--export-dpi={dpi}"
                    ])
        png_path = output_dir / 'output.png'
        if png_path.exists():
            with open(png_path, "rb") as f:
                png_bytes = f.read()
        st.download_button(
            label="📄 Download png",
            data=png_bytes,
            file_name="equation.png",
            mime="image/png"
        )


