# mainHemda.py
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

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
    st.title("ראשי")
    st.write("ברוכים הבאים לעמוד הראשי.")
elif selected == "רשימת מורים":

    data = sendRequest("getTeacherList", None, "get")

    column_names = ['ID', 'שם המורה', 'מספר טלפון', 'מקצוע']
    df = pd.DataFrame(data["teachers_list"], columns=column_names)
    st.session_state.teachers_df = df

    # Use columns to center the dataframe
    col1, col2, col3 = st.columns([1, 4, 1])

    with col2:
        st.dataframe(st.session_state.teachers_df, use_container_width=True)

    # --- The rest of your code for forms ---
    st.write("---")
    # You can also use columns for the forms to align them
    col_form1, col_form2, col_form3  = st.columns([1, 4, 1])
    with col_form2:
        st.write("### הוספת מורה חדש")
        with st.form("add_teacher_form"):
            teacher_name = st.text_input("שם המורה")
            teacher_phone = st.text_input("מספר טלפון")
            teacher_subject = st.text_input("מקצוע")

            submitted = st.form_submit_button("הוסף מורה")

            if submitted:
                if teacher_name and teacher_phone and teacher_subject:
                    payload = {
                        'name': teacher_name,
                        'phone': teacher_phone,
                        'profession': teacher_subject
                    }
                    data = sendRequest("setNewTeacher", payload, "post")
                    st.success(f"המורה {teacher_name} נוסף בהצלחה!")
                    st.rerun()
                else:
                    st.error("יש למלא את כל השדות כדי להוסיף מורה.")

    # --- מחיקת מורה ---
    st.write("---")
    # השתמש בעמודות כדי למרכז את הטופס
    col_del1, col_del2, col_del3 = st.columns([1, 4, 1])

    with col_del2:
        st.write("### מחיקת מורה")
        if not st.session_state.teachers_df.empty:
            teachers_list = st.session_state.teachers_df['שם המורה'].tolist()
            teacher_to_delete = st.selectbox("בחר מורה למחיקה", teachers_list)

            if st.button("מחק מורה"):
                st.session_state.teachers_df = st.session_state.teachers_df[
                    st.session_state.teachers_df['שם המורה'] != teacher_to_delete]
                st.success(f"המורה {teacher_to_delete} נמחק בהצלחה!")
                st.rerun()
        else:
            st.write("אין מורים למחיקה.")
    pass
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