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

    column_names = ['ID', 'שם המורה', 'מספר טלפון', 'מקצוע', 'צבע']
    df = pd.DataFrame(data["teachers_list"], columns=column_names)
    st.session_state.teachers_df = df


    # --- Styling the DataFrame ---
    # A function that takes a single cell value and returns a CSS style string
    def color_cell(val):
        return f'background-color: {val}'

    # Apply the style to the 'צבע' column
    styled_df = st.session_state.teachers_df.style.applymap(color_cell, subset=['צבע'])

    # Use columns to center the dataframe
    col1, col2, col3 = st.columns([1, 4, 1])

    with col2:
        # Display the styled DataFrame
        st.dataframe(styled_df, use_container_width=True)

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
            teacher_color = st.color_picker("בחר צבע למורה", "#FF4B4B")
            submitted = st.form_submit_button("הוסף מורה")

            if submitted:
                if teacher_name and teacher_phone and teacher_subject:
                    payload = {
                        'name': teacher_name,
                        'phone': teacher_phone,
                        'profession': teacher_subject,
                        'color': teacher_color
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

    col_form1, col_form2, col_form3  = st.columns([1, 4, 1])
    with col_form2:

        data = sendRequest("getRoomsList", None, "get")
        df_rooms = pd.DataFrame(data['roomsList'])
        df_rooms.columns = ['מספר חדר', 'יעוד']
        st.dataframe(df_rooms, use_container_width=True)
elif selected == "רשימת בתי ספר":
    col_form1, col_form2, col_form3  = st.columns([1, 4, 1])
    with col_form2:
        data = sendRequest("getSchoolsList", None, "get")
        df_school = pd.DataFrame(data['schoolsList'])
        df_school.columns = ['שם בית ספר', 'מספר טלפון', 'כתובת']
        st.dataframe(df_school, use_container_width=True)
        st.write("---")
        st.write("### הוספת בית ספר")
    col_form1, col_form2, col_form3 = st.columns([1, 4, 1])
    with col_form2:
        with st.form("add_teacher_form"):
            teacher_name = st.text_input("שם בית ספר")
            teacher_phone = st.text_input("מספר טלפון")
            teacher_subject = st.text_input("כתובת")
            submitted = st.form_submit_button("הוסף בית ספר")

            if submitted:
                # בדיקה שכל השדות הוזנו
                if teacher_name and teacher_phone and teacher_subject:
                    new_teacher = pd.DataFrame([{
                        'שם בית ספר': teacher_name,
                        'מספר טלפון': teacher_phone,
                        'כתובת': teacher_subject
                    }])
                    st.session_state.teachers_df = pd.concat([st.session_state.teachers_df, new_teacher], ignore_index=True)
                    st.success(f"בית ספר {teacher_name} נוסף בהצלחה!")
                    st.rerun()
                else:
                    st.error("יש למלא את כל השדות כדי להוסיף בית ספר.")
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

        # יצירת שלוש עמודות
        # [1, 2, 1] - יוצר עמודה שמאלית צרה, עמודה מרכזית רחבה, ועמודה ימנית צרה.
        col1, col2, col3 = st.columns([1, 2, 1])

        # הצבת הכותרת בעמודה האמצעית
        with col2:
            st.markdown("<h3 style='text-align: center;'> מערכת שעות קבועה</h3>", unsafe_allow_html=True)

        years = [f'{year}-{year+1}' for year in range(2025, 2040)]

        # Fetch data for dropdowns
        schools_data = sendRequest("getSchoolsList", None, "get")
        school_names = [school[0] for school in schools_data['schoolsList']]

        rooms_data = sendRequest("getRoomsList", None, "get")
        room_numbers = [room[0] for room in rooms_data['roomsList']]

        teachers_data = sendRequest("getTeacherList", None, "get")
        teacher_names = [teacher[1] for teacher in teachers_data['teachers_list']]

        # Define grades and subjects
        grades = [f'י{i + 1}' for i in range(3)] + [f'יא{i + 1}' for i in range(3)] + [f'יב{i + 1}' for i in range(3)]
        subjects = ['כימיה', 'פיסיקה']  # Example subjects

        # Define days of the week in Hebrew
        days_of_week = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]

        # Generate time options from 07:15 to 20:00, in 15-minute increments
        start_time_options = pd.date_range("07:15", "20:00", freq="15min").strftime("%H:%M").tolist()

        # Use columns to align form inputs
        col_form1, col_form2, col_form3 = st.columns([1,20,1])

        with col_form2:
            with st.form("add_fixed_lesson_form"):
                col11, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10   = st.columns(11)
                with col11:
                    year_selection = st.selectbox("בחר שנה:", years, key="list11")

                with col1:
                    school_selection = st.selectbox("בחר בית ספר:", school_names, key="list1")

                with col2:
                    grade_selection = st.selectbox("בחר שכבה", grades, key="list2")

                with col3:
                    room_selection = st.selectbox("בחר חדר:", room_numbers, key="list3")

                with col4:
                    subject_selection = st.selectbox("בחר מקצוע:", subjects, key="list4")

                with col5:
                    teacher_selection = st.selectbox("בחר מורה:", teacher_names, key="list5")

                with col6:
                    day_selection = st.selectbox("בחר יום בשבוע:", days_of_week, key="list6")

                with col7:
                    start_time = st.selectbox("בחר שעת התחלה:", start_time_options, key="list7")

                with col8:
                    start_time_index = start_time_options.index(start_time)
                    end_time_options = start_time_options[start_time_index + 1:]  # End time must be after start time
                    end_time = st.selectbox("בחר שעת סיום:", start_time_options, key="list8")

                with col9:
                    submitted = st.form_submit_button("הוסף שיעור")

                with col10:
                    deleteSub = st.form_submit_button("מחק שיעור")

                if submitted:

                    payload = {
                        "year": year_selection,
                        "school": school_selection,
                        "grade": grade_selection,
                        "room": room_selection,
                        "subject": subject_selection,
                        "teacher": teacher_selection,
                        "day": day_selection, # Add the new day field
                        "start_time": start_time,
                        "end_time": end_time
                    }
                    sendRequest("setFixedTimeTable", payload, "post")

                    st.success(
                        f"שיעור חדש נוסף בהצלחה: {subject_selection} עם {teacher_selection} בבית ספר {school_selection}, שכבה {grade_selection}, חדר {room_selection} ביום {day_selection} בין השעות {start_time} ל-{end_time}.")
                    st.rerun()

        fixedTimeTable = sendRequest("getFixedTimeTable", None, "post")

        time_intervals = pd.date_range("07:30", "20:00", freq="15min").strftime("%H:%M").tolist()

        data = {
            "שעה": time_intervals
        }

        for room in room_numbers:
            data[room] = [""] * len(time_intervals)

        df_schedule = pd.DataFrame(data)

        # Display the DataFrame as a table in Streamlit
        st.dataframe(df_schedule, use_container_width=True,hide_index=True)

    elif sub_selected == "שוטפת":
        st.write("כאן תוצג מערכת שעות שוטפת.")
    elif sub_selected == "עבור מורה":
        st.write("כאן תוצג מערכת שעות עבור מורה ספציפי.")
    elif sub_selected == "לבית ספר":
        st.write("כאן תוצג מערכת שעות עבור בית הספר כולו.")
elif selected == "לוח מבחנים":
    st.title("לוח מבחנים")
    st.write("כאן תמצאו את לוח מבחנים.")