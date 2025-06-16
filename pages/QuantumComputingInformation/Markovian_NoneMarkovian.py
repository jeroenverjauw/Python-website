import streamlit as st

st.set_page_config(page_title="Quantum Error Types", layout="centered")

st.title("Markovian vs Non-Markovian Errors in Quantum Systems")

st.markdown("""
In quantum computing, it's crucial to understand the nature of noise and errors that affect qubits. These errors can be broadly categorized into **Markovian** (memoryless) and **Non-Markovian** (history-dependent) types.

The table below provides a high-level comparison:
""")

st.markdown("""
| Feature              | Markovian Errors                        | Non-Markovian Errors                      |
|----------------------|-----------------------------------------|-------------------------------------------|
| **Memory**           | No memory (memoryless)                  | Has memory of past states                 |
| **Mathematical Model** | Lindblad master equation                | Integro-differential equations            |
| **Noise Correlation**| Uncorrelated in time                    | Time-correlated                           |
| **Simulation**       | Easier to model                         | Complex to simulate                       |
| **Examples**         | Depolarizing, amplitude damping         | 1/f noise, slow environmental fluctuations|
""")

st.markdown("""
### Notes:
- **Markovian errors** are often assumed in theoretical models due to their simplicity.
- **Non-Markovian errors** are more realistic in many physical quantum systems and require advanced error mitigation techniques.
""")

st.success("Explore these error models when designing robust quantum algorithms!")