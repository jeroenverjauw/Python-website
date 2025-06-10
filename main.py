import streamlit as st
from PIL import Image

st.header("Jeroen's first webpage", divider= 'gray')
st.subheader('Homepage')

value = st.text_input('some text here: ')
st.markdown('value: ' + value)

st.image("IMG_0748.JPG")


