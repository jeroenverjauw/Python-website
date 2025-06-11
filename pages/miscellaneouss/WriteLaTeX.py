import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
from pylatex import Document, Section, Command
from pylatex import Document, Section, Math, Command
from pylatex.utils import italic, NoEscape

st.title("LaTeX Renderer and Exporter")

latex_code = st.text_area("Enter LaTeX code (no $ signs needed)", "E = \sqrt{(mc^2)^2+(pc)^2}")

dpi = st.slider("DPI for image export", min_value=50, max_value=600, value=150)
image_format = st.radio("Select image format", ["PNG", "SVG"])

if latex_code:

    plt.rcParams['text.usetex'] = True
    st.latex(fr'''{latex_code}''')

    fig, ax = plt.subplots(figsize=(0.01, 0.01))
    fig.patch.set_alpha(0.0)
    ax.axis("off")

    buf = BytesIO()

    ax.text(0.5, 0.5, fr'${latex_code}$', fontsize=20, ha='center', va='center')
    # Set format and dpi
    if image_format == "PNG":
        fig.savefig(buf, format="png", dpi=dpi, bbox_inches='tight', pad_inches=0.1, transparent=True)
        mime = "image/png"
        ext = "png"
    else:
        fig.savefig(buf, format="svg", bbox_inches='tight', pad_inches=0.1, transparent=True)
        mime = "image/svg+xml"
        ext = "svg"

    buf.seek(0)

    st.download_button(
        label=f"📥 Download {image_format}",
        data=buf,
        file_name=f"latex_output.pdf",
        mime="application/pdf"
    )