import streamlit as st
import subprocess
import tempfile
from pathlib import Path
import latextools

st.title("Quantum circuit generator")

def renderLatexEquation(f, border = '1pt'):
    packages = []
    commands = []
    config = latextools.DocumentConfig('standalone', ('border=' + border,))
    proj = latextools.LatexProject()
    content = latextools.BasicContent(f)
    doc = content.as_document(path='./test.tex', config=config)
    doc = latextools.LatexDocument(path='./test.tex', config=config, contents=(content,))
    proj.add_file(doc)
    proj.write_src('.')
    proj.add_file(latextools.LatexDocument(path='main.tex', config=config, contents=doc.contents))
    pdf = proj.compile_pdf(tmp_dir = "./")
    pdf.save('./test.pdf')
    return pdf.as_svg()

latex_code = st.text_area("Enter LaTeX code (no $ signs needed)", "$E = \ket{1}$")

if latex_code: 
    st.download_button(
        label=f"📥 Download pdf",
        data=renderLatexEquation(latex_code),
        file_name=f"latex_output.{ext}",
        mime="application/pdf"
    )