# mainHemda.py
import streamlit as st
from streamlit_option_menu import option_menu

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
selected = option_menu(
    menu_title=None,
    options=["ראשי", "רשימת מורים", "רשימת חדרים", "רשימת בתי ספר","מערכת שעות" ,"לוח מבחנים"],
    icons=["house", "person-fill", "door-open-fill", "building-fill", "table", "table","clock"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# --- Display content based on menu selection ---
if selected == "ראשי":
    st.title("ראשי")
    st.write("ברוכים הבאים לעמוד הראשי.")
elif selected == "רשימת מורים":
    st.switch_page("pages/teachers.py")
elif selected == "רשימת חדרים":
    st.switch_page("pages/rooms.py")
elif selected == "רשימת בתי ספר":
    st.switch_page("pages/schools.py")
elif selected == "מערכת שעות":
    # Nested horizontal menu for the "מערכת שעות" page
    sub_selected = option_menu(
        menu_title=None,
        options=["קבועה", "שוטפת", "עבור מורה", "לבית ספר"],
        icons=["calendar", "calendar-check", "person", "building"],
        menu_icon=None,
        default_index=0,
        orientation="horizontal",
    )

    # Display content based on sub-menu selection
    if sub_selected == "קבועה":
        st.write("כאן תוצג מערכת שעות קבועה.")
    elif sub_selected == "שוטפת":
        st.write("כאן תוצג מערכת שעות שוטפת.")
    elif sub_selected == "עבור מורה":
        st.write("כאן תוצג מערכת שעות עבור מורה ספציפי.")
    elif sub_selected == "לבית ספר":
        st.write("כאן תוצג מערכת שעות עבור בית הספר כולו.")
elif selected == "לוח מבחנים":
    st.title("לוח מבחנים")
    st.write("כאן תמצאו את לוח מבחנים.")