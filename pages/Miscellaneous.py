import streamlit as st

def load_page2():
    from pages.miscellaneouss.WriteLaTeX import main
    main()

    
st.sidebar.button('Write LaTeX text', on_click=load_page2)