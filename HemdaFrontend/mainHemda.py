# mainHemda.py
import pandas
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import calendar
from datetime import date

import mainPage
import rooms
import schools
import teacherList
import testsBoard
import timeTable
from sendRequest import sendRequest
import components


# --- Page Configuration and CSS ---
st.set_page_config(layout="wide")

hide_streamlit_ui = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_ui, unsafe_allow_html=True)

# This new CSS snippet hides the default Streamlit sidebar
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# More aggressive CSS to remove all margins and padding
st.markdown("""
<style>
.block-container {
    padding-top: 0rem; /* Adjust this value as needed */
    padding-bottom: 0rem;
    padding-left: 5rem;
    padding-right: 5rem;
}
.appview-container .main .block-container {
    padding-top: 0rem;
    padding-bottom: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
}
.st-emotion-cache-1pl3fpy {
    padding-top: 0rem;
    padding-bottom: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
}
.st-emotion-cache-1ghy2tt {
    padding-top: 0rem;
    padding-bottom: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
}
.st-emotion-cache-1dp5vir {
    padding-top: 0rem;
    padding-bottom: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
}
</style>
""", unsafe_allow_html=True)

# --- Custom Horizontal Menu ---
selected = components.display_main_menu()

# --- Display content based on menu selection ---
if selected == "ראשי":
    mainPage.mainPage()
elif selected == "רשימת מורים":
    teacherList.teacherList()
elif selected == "רשימת חדרים":
    rooms.roomsList()
elif selected == "רשימת בתי ספר":
    schools.schoolsList()
elif selected == "מערכת שעות":
    timeTable.timeTable()
elif selected == "לוח מבחנים":
    testsBoard.testsBoard()