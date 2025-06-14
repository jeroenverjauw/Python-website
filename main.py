import streamlit as st

Home = st.Page("pages/Home.py",title="")
Circuit_generator = st.Page("pages/PythonWidgets/CircuitGenerator.py", title="Circuit generator", )
writelatex = st.Page("pages/miscellaneous/WriteLaTeX.py", title="Write LaTeX", )

pg = st.navigation(
        {
            "": [Home,],
            "Python widgets": [Circuit_generator,],
            "Miscellaneous": [writelatex,]
        }
    )

pg.run()