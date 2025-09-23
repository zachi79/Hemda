import streamlit as st
from streamlit_option_menu import option_menu
from src.common.sendRequest import sendRequest
import pandas as pd


def staticTimeTable():
    col1, col2, col3 = st.columns([1, 2, 1])

    years = [f'{year}-{year + 1}' for year in range(2025, 2040)]

    # Fetch data for dropdowns
    schools_data = sendRequest("getSchoolsList", None, "get")
    school_names = [school[0] for school in schools_data['schoolsList']]

    rooms_data = sendRequest("getRoomsList", None, "get")
    room_numbers = [room[0] for room in rooms_data['roomsList']]

    teachers_data = sendRequest("getTeacherList", None, "get")
    columns = ['id', 'teachername', 'phone', 'prof','email', 'color']
    teachers_dataDF = pd.DataFrame(teachers_data['teachers_list'], columns=columns)

    # Define grades and subjects
    grades = [f'י{i + 1}' for i in range(3)] + [f'יא{i + 1}' for i in range(3)] + [f'יב{i + 1}' for i in range(3)]
    subjects = ['כימיה', 'פיסיקה']  # Example subjects

    # Define days of the week in Hebrew
    days_of_week = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]

    # Generate time options from 07:15 to 20:00, in 15-minute increments
    start_time_options = pd.date_range("07:30", "20:00", freq="15min").strftime("%H:%M").tolist()
    col_formUp1, col_formUp2, col_formUp3 = st.columns([2, 1, 2])
    with col_formUp2:
        yearSelectedCol, daySelectedCol = st.columns(2)
        with yearSelectedCol:
            year_selection = st.selectbox("בחר שנה:", years, key="list11")
        with daySelectedCol:
            day_selection = st.selectbox("בחר יום בשבוע:", days_of_week, key="list6")
    # Use columns to align form inputs
    col_form1, col_form2, col_form3 = st.columns([1, 20, 1])

    with col_form2:
        with st.form("add_fixed_lesson_form"):
            col1, col2, col3, col4, col5, col7, col8, col9, col10 = st.columns(9)

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
                    "day_of_week": day_selection,  # Add the new day field
                    "start_time": start_time,
                    "end_time": end_time,
                    "yearSelect": year_selection,
                    "teacher_name": teacher_selection,
                    "profession": subject_selection,
                    "schoolName": school_selection,
                    "schoolClass": grade_selection,
                    "room_number": room_selection
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
                    "day_of_week": day_selection,  # Add the new day field
                    "start_time": start_time,
                    "end_time": end_time
                }

                sendRequest("setFixedTimeTable", payload, "post")

                st.success(
                    f"שיעור חדש נוסף בהצלחה: {subject_selection} עם {teacher_selection} בבית ספר {school_selection}, שכבה {grade_selection}, חדר {room_selection} ביום {day_selection} בין השעות {start_time} ל-{end_time}.")
                st.rerun()

    fixedTimeTable = sendRequest("getFixedTimeTable", None, "post")
    columns = ['Day', 'Start_Time', 'End_Time', 'Year', 'Teacher', 'Prof', 'School', 'Class', 'Room']
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

    pass

def timeTable():
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
        staticTimeTable()
    elif sub_selected == "שוטפת":
        st.write("כאן תוצג מערכת שעות שוטפת.")
    elif sub_selected == "עבור מורה":
        st.write("כאן תוצג מערכת שעות עבור מורה ספציפי.")
    elif sub_selected == "לבית ספר":
        st.write("כאן תוצג מערכת שעות עבור בית הספר כולו.")

    pass