import streamlit as st
from pathlib import Path
import subprocess
from subprocess import run, PIPE

import drawsvg as draw
import scipy
import numpy as np
import base64

def write_tex_file(latex_code: str, filepath: Path, fontsize: float):
    latex_content = rf"""
\documentclass{{extarticle}}
\pagestyle{{empty}}
\usepackage{{anyfontsize}}
\usepackage{{braket}}
\usepackage{{amsmath}}
\begin{{document}}
\fontsize{{{fontsize}}}{{{fontsize * 1.2}}}\selectfont
{latex_code}
\end{{document}}
"""
    filepath.write_text(latex_content.strip(), encoding="utf-8")


     
def compile_latex_to_pdf(tex_file: Path, output_dir: Path):
    subprocess.run([
        "pdflatex", "-interaction=nonstopmode", "-output-format=pdf",
        f"-output-directory={output_dir.resolve()}", str(tex_file.resolve()) 
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=output_dir, 
    timeout=60, text=True, check=False)

def convert_pdf_to_svg(pdf_file: Path, svg_file: Path):
    subprocess.run([
    r"inkscape",
    str(pdf_file),
    "--export-type=svg",
    "--export-filename=" + str(svg_file)
], check=True)
    subprocess.run([
        r"inkscape", svg_file,
        "--export-area-drawing",
        "--export-plain-svg",
        "-o", svg_file
    ], check=True)