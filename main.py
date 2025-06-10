import streamlit as st
from PIL import Image

st.header("Jeroen's first webpage", divider= 'gray')
st.subheader('Homepage')

value = st.text_input('some text here: ')
st.markdown('value: ' + value)
value2 = st.text_input('some text here2 : ')
st.markdown('value: ' + value2)
st.image("IMG_0748.JPG")

# st.sidebar.page_link("pages/Python widgets/Circuit generator.py")
