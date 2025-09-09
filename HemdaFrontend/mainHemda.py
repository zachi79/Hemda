# mainHemda.py
import pandas
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

        years = [f'{year}-{year+1}' for year in range(2025, 2040)]

        # Fetch data for dropdowns
        schools_data = sendRequest("getSchoolsList", None, "get")
        school_names = [school[0] for school in schools_data['schoolsList']]

        rooms_data = sendRequest("getRoomsList", None, "get")
        room_numbers = [room[0] for room in rooms_data['roomsList']]

        teachers_data = sendRequest("getTeacherList", None, "get")
        columns = ['id','teachername','phone','prof','color']
        teachers_dataDF = pandas.DataFrame(teachers_data['teachers_list'],columns=columns)


        # Define grades and subjects
        grades = [f'י{i + 1}' for i in range(3)] + [f'יא{i + 1}' for i in range(3)] + [f'יב{i + 1}' for i in range(3)]
        subjects = ['כימיה', 'פיסיקה']  # Example subjects

        # Define days of the week in Hebrew
        days_of_week = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]

        # Generate time options from 07:15 to 20:00, in 15-minute increments
        start_time_options = pd.date_range("07:30", "20:00", freq="15min").strftime("%H:%M").tolist()
        col_formUp1, col_formUp2, col_formUp3 = st.columns([2, 1,2])
        with col_formUp2:
            yearSelectedCol, daySelectedCol = st.columns(2)
            with yearSelectedCol:
                year_selection = st.selectbox("בחר שנה:", years, key="list11")
            with daySelectedCol:
                day_selection = st.selectbox("בחר יום בשבוע:", days_of_week, key="list6")
        # Use columns to align form inputs
        col_form1, col_form2, col_form3 = st.columns([1,20,1])

        with col_form2:
            with st.form("add_fixed_lesson_form"):
                col1, col2, col3, col4, col5, col7, col8, col9, col10   = st.columns(9)


                with col1:
                    school_selection = st.selectbox("בחר בית ספר:", school_names, key="list1")

                with col2:
                    grade_selection = st.selectbox("בחר שכבה", grades, key="list2")

                with col3:
                    room_selection = st.selectbox("בחר חדר:", room_numbers, key="list3")

                with col4:
                    subject_selection = st.selectbox("בחר מקצוע:", subjects, key="list4")

                with col5:
                    teachers_by_prof = teachers_dataDF[teachers_dataDF['prof'] == 'כימיה']
                    teacher_names = teachers_by_prof['teachername'].tolist()
                    teacher_selection = st.selectbox("בחר מורה:", teacher_names, key="list5")

                with col7:
                    start_time = st.selectbox("בחר שעת התחלה:", start_time_options, key="list7")

                with col8:
                    start_time_index = start_time_options.index(start_time)
                    end_time_options = start_time_options[start_time_index + 1:]  # End time must be after start time
                    end_time = st.selectbox("בחר שעת סיום:", end_time_options, key="list8")

                with col9:
                    submitted = st.form_submit_button("הוסף שיעור")

                with col10:
                    deleteSub = st.form_submit_button("מחק שיעור")

                if deleteSub:
                    payload = {
                        "yearSelect": year_selection,
                        "schoolName": school_selection,
                        "schoolClass": grade_selection,
                        "room_number": room_selection,
                        "profession": subject_selection,
                        "teacher_name": teacher_selection,
                        "day_of_week": day_selection,  # Add the new day field
                        "start_time": start_time,
                        "end_time": end_time
                    }

                    sendRequest("delFixedTimeTable", payload, "post")

                    st.success(
                        f"שיעור נמחק בהצלחה: {subject_selection} עם {teacher_selection} בבית ספר {school_selection}, שכבה {grade_selection}, חדר {room_selection} ביום {day_selection} בין השעות {start_time} ל-{end_time}.")
                    st.rerun()
                if submitted:

                    payload = {
                        "yearSelect": year_selection,
                        "schoolName": school_selection,
                        "schoolClass": grade_selection,
                        "room_number": room_selection,
                        "profession": subject_selection,
                        "teacher_name": teacher_selection,
                        "day_of_week": day_selection, # Add the new day field
                        "start_time": start_time,
                        "end_time": end_time
                    }

                    sendRequest("setFixedTimeTable", payload, "post")

                    st.success(
                        f"שיעור חדש נוסף בהצלחה: {subject_selection} עם {teacher_selection} בבית ספר {school_selection}, שכבה {grade_selection}, חדר {room_selection} ביום {day_selection} בין השעות {start_time} ל-{end_time}.")
                    st.rerun()

        fixedTimeTable = sendRequest("getFixedTimeTable", None, "post")
        columns = ['ID', 'Day', 'Start_Time', 'End_Time', 'Year', 'Teacher', 'Prof', 'School', 'Class', 'Room']
        # Create the DataFrame
        fixedTimeTableDF = pd.DataFrame(fixedTimeTable['fixedTimeTable'])
        # Assign column names
        if len(fixedTimeTableDF) > 0:
            fixedTimeTableDF.columns = columns[:len(fixedTimeTableDF.columns)]
            fixedTimeTableDFSSelected = fixedTimeTableDF[fixedTimeTableDF['Day'] == day_selection]

        time_intervals = pd.date_range("07:30", "20:00", freq="15min").strftime("%H:%M").tolist()
        data = {
            "שעה": time_intervals
        }
        for room in room_numbers:
            data[room] = [""] * len(time_intervals)
        df_schedule = pd.DataFrame(data)
        if len(fixedTimeTableDF) > 0:
            for _, row in fixedTimeTableDFSSelected.iterrows():
                room = row['Room']

                # Check if the room exists in the schedule columns
                if room in df_schedule.columns:
                    start_time = pd.to_datetime(row['Start_Time']).strftime('%H:%M')
                    end_time = pd.to_datetime(row['End_Time']).strftime('%H:%M')

                    # Generate the time intervals for the current class
                    class_time_intervals = pd.date_range(start_time, end_time, freq='15min', inclusive='left').strftime(
                        '%H:%M').tolist()

                    # Create a string with the class details
                    class_info = f"{row['Prof']}<br>{row['Teacher']}<br>{row['School']}<br>{row['Class']}"

                    # Update the schedule DataFrame for each time interval
                    for time_slot in class_time_intervals:
                        df_schedule.loc[df_schedule['שעה'] == time_slot, room] = class_info
        # Display the DataFrame as a table in Streamlit
        # --- Styling Logic ---
        def color_cells_with_text(val):
            """
            Applies a blue background to cells that are not empty.
            """
            # Check if the cell value is not an empty string
            if val != "":
                teacher_name = val.split('<br>')[1]
                color = teachers_dataDF.loc[teachers_dataDF['teachername'] == teacher_name, 'color'].iloc[0]
                return f'background-color: {color};'
            return ''


        # Apply the styling function using .style.map()
        styled_df = df_schedule.style.map(color_cells_with_text, subset=df_schedule.columns.difference(['שעה']))

        st.markdown(styled_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    elif sub_selected == "שוטפת":
        st.write("כאן תוצג מערכת שעות שוטפת.")
    elif sub_selected == "עבור מורה":
        st.write("כאן תוצג מערכת שעות עבור מורה ספציפי.")
    elif sub_selected == "לבית ספר":
        st.write("כאן תוצג מערכת שעות עבור בית הספר כולו.")
elif selected == "לוח מבחנים":
    st.title("לוח מבחנים")
    st.write("כאן תמצאו את לוח מבחנים.")