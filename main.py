import streamlit as st

Home = st.Page("pages/Home.py",title="")
Circuit_generator = st.Page("pages/PythonWidgets/CircuitGenerator/CircuitGenerator.py", title="Circuit generator", )
writelatex = st.Page("pages/miscellaneous/WriteLaTeX.py", title="Write LaTeX", )
markovian = st.Page("pages/QuantumComputingInformation/Markovian_NoneMarkovian.py", title="Markovian noise", )

pg = st.navigation(
        {
            "": [Home,],
            "Quantum computing information": [markovian,],
            "Python widgets": [Circuit_generator,],
            "Miscellaneous": [writelatex,]
        }
    )

pg.run()