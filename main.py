# import streamlit as st
# from PIL import Image

# st.header("Jeroen's first webpage", divider= 'gray')
# st.subheader('Homepage')

# value = st.text_input('some text here: ')
# st.markdown('value: ' + value)
# value2 = st.text_input('some text here2 : ')
# st.markdown('value: ' + value2)
# st.image("IMG_0748.JPG")

# # st.sidebar.page_link("pages/Python widgets.py")

# import streamlit as st
# from st_pages import add_page_title, get_nav_from_toml

# # st.set_page_config(layout="wide")

# # If you want to use the no-sections version, this
# # defaults to looking in .streamlit/pages.toml, so you can
# # just call `get_nav_from_toml()`
# nav = get_nav_from_toml("pages_sections.toml")

# pg = st.navigation(nav)

# add_page_title(pg)

# pg.run()

import streamlit as st

Circuit_generator = st.Page("pages/PythonWidgets/CircuitGenerator.py", title="Circuit generator", )
writelatex = st.Page("pages/miscellaneous/WriteLaTeX.py", title="Write LaTeX", )

pg = st.navigation(
        {
            "Python widgets": [Circuit_generator,],
            "Miscellaneous": [writelatex,]
        }
    )

pg.run()