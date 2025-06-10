import streamlit as st

def load_page1():
    from pages.PythonWidgets.CircuitGenerator import main
    main()

    
st.sidebar.button('Circuit Generator', on_click=load_page1)

