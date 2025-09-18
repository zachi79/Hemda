import streamlit as st


def mainPage():
    col1, col2, col3 = st.columns([5, 5, 5])
    with col2:
        #st.write("ברוכים הבאים למערכת ניהול שעות")
        st.markdown("<h1 style='text-align: center; color: black;'>ברוכים הבאים למערכת ניהול שעות</h1>",
                    unsafe_allow_html=True)
        st.image(r".\Pictures\HEMDA1.jpg")
    pass