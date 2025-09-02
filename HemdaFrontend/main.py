from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
import json
from sendRequest import sendRequest

# הגדרת המצב ההתחלתי של הדף.
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'ראשי'

# --- יצירת התפריט הצדדי ככפתורים ---
st.sidebar.title('ניווט')

if st.sidebar.button('ראשי'):
    st.session_state.current_page = 'ראשי'
if st.sidebar.button('מורים'):
    st.session_state.current_page = 'מורים'
if st.sidebar.button('רשימת בתי ספר'):
    st.session_state.current_page = 'רשימת בתי ספר'
if st.sidebar.button('רשימת חדרי לימוד'):
    st.session_state.current_page = 'רשימת חדרי לימוד'
if st.sidebar.button('רשימת תלמידים'):
    st.session_state.current_page = 'רשימת תלמידים'
if st.sidebar.button('מערכת שעות קבועה'):
    st.session_state.current_page = 'מערכת שעות קבועה'
if st.sidebar.button('מערכת שעות שבועית שותפת'):
    st.session_state.current_page = 'מערכת שעות שבועית שותפת'
if st.sidebar.button('לוח מבחנים'):
    st.session_state.current_page = 'לוח מבחנים'

# --- הצגת התוכן בהתאם ל-session_state ---

if st.session_state.current_page == 'ראשי':
    st.set_page_config(layout="centered")
    st.title('ניהול מערכת בית ספר')
    st.header("עמוד הבית")
    st.write("""
    **ברוכים הבאים למערכת ניהול בית הספר.**

    בחר באחת האפשרויות בתפריט הצד כדי לצפות במידע הרלוונטי.
    """)


elif st.session_state.current_page == 'מורים':
    st.set_page_config(layout="centered")
    st.title('ניהול מערכת בית ספר')
    st.header("רשימת מורים")
    data = sendRequest("getTeacherList", None, "get")
    #
    column_names = ['ID', 'שם המורה', 'מספר טלפון', 'מקצוע']
    df = pd.DataFrame(data["teachers_list"], columns=column_names)
    st.session_state.teachers_df = df
    st.dataframe(st.session_state.teachers_df, use_container_width=True)

    # --- טופס להוספת מורה חדש ---
    st.write("---")
    st.write("### הוספת מורה חדש")
    with st.form("add_teacher_form"):
        teacher_name = st.text_input("שם המורה")
        teacher_phone = st.text_input("מספר טלפון")
        teacher_subject = st.text_input("מקצוע")

        submitted = st.form_submit_button("הוסף מורה")

        if submitted:
            # בדיקה שכל השדות הוזנו
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
    st.write("### מחיקת מורה")

    # בדיקה שיש מורים בטבלה
    if not st.session_state.teachers_df.empty:
        # יצירת רשימה נפתחת עם שמות המורים
        teachers_list = st.session_state.teachers_df['שם המורה'].tolist()
        teacher_to_delete = st.selectbox("בחר מורה למחיקה", teachers_list)

        if st.button("מחק מורה"):
            # סינון המורה הנבחר ומחיקתו מהטבלה
            st.session_state.teachers_df = st.session_state.teachers_df[
                st.session_state.teachers_df['שם המורה'] != teacher_to_delete]
            st.success(f"המורה {teacher_to_delete} נמחק בהצלחה!")
            st.rerun()
    else:
        st.write("אין מורים למחיקה.")

elif st.session_state.current_page == 'רשימת בתי ספר':
    st.set_page_config(layout="centered")
    st.title('ניהול מערכת בית ספר')
    st.header("רשימת בתי ספר")
    data = sendRequest("getSchoolsList", None, "get")
    df_school = pd.DataFrame(data['schoolsList'])
    df_school.columns = ['שם בית ספר', 'מספר טלפון', 'כתובת']
    st.dataframe(df_school, use_container_width=True)
    st.write("---")
    st.write("### הוספת בית ספר")
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

elif st.session_state.current_page == 'רשימת חדרי לימוד':
    st.set_page_config(layout="centered")
    st.title('ניהול מערכת בית ספר')
    st.header("רשימת חדרי לימוד")
    data = sendRequest("getRoomsList", None, "get")
    df_rooms = pd.DataFrame(data['roomsList'])
    df_rooms.columns = ['מספר חדר', 'יעוד']
    st.dataframe(df_rooms, use_container_width=True)


elif st.session_state.current_page == 'רשימת תלמידים':
    st.set_page_config(layout="centered")
    st.title('ניהול מערכת בית ספר')
    st.header("רשימת תלמידים")
    st.write("כאן תוצג רשימת התלמידים.")

    students_data = {
        'שם התלמיד': ['נועה', 'איתי', 'יעל', 'דוד'],
        'כיתה': ['א', 'ב', 'א', 'ג']
    }
    df_students = pd.DataFrame(students_data)
    st.dataframe(df_students, use_container_width=True)

elif 'current_page' in st.session_state and st.session_state.current_page == 'מערכת שעות קבועה':
    st.set_page_config(layout="wide")
    st.title('ניהול מערכת בית ספר - מערכת שעות קבועה')

    # Initialize the DataFrame and times list in session state only once
    if 'df' not in st.session_state:
        start_time = datetime.strptime("07:30", "%H:%M")
        end_time = datetime.strptime("20:00", "%H:%M")
        time_interval = timedelta(minutes=15)

        current_time = start_time
        times = []
        while current_time <= end_time:
            times.append(current_time.strftime("%H:%M"))
            current_time += time_interval

        data = sendRequest("getRoomsList", None, "get")
        df_rooms = pd.DataFrame(data['roomsList'])
        rooms = list(df_rooms[0])

        data = {room: [""] * len(times) for room in rooms}
        st.session_state.df = pd.DataFrame(data, index=times)
        st.session_state.times = times

    # --- New Column Configuration ---
    column_config = {}
    for room in st.session_state.df.columns:
        column_config[room] = st.column_config.TextColumn(
            label=room,
            width="medium"  # You can use "small", "medium", "large", or a pixel value like 150
        )

    # You can also configure the index (time column) if needed
    column_config['index'] = st.column_config.TextColumn(
        label="שעה",
        width="small"
    )

    # Display the DataFrame with the new column configuration
    st.dataframe(
        st.session_state.df,
        column_config=column_config,
        hide_index=False,
        use_container_width=True
    )

    # Display the DataFrame from session state
    #st.dataframe(st.session_state.df.style.set_properties(**{"text-align": "center"}), height=500)

    # All your columns and widgets go here
    col10, col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(10)  # Changed to 8 columns as per previous advice

    with col10:
        options = ['א','ב','ג','ד','ה','ו']
        selected_option10 = st.selectbox('בחר יום', options)

    with col1:
        data = sendRequest("getSchoolsList", None, "get")
        optionsSchoollName = list(pd.DataFrame(data['schoolsList'])[0])
        selected_option1 = st.selectbox('בחר בית ספר', optionsSchoollName)

    with col2:
        options = ['י1', 'י2', 'י3', 'י4', 'יא1', 'יא2', 'יא3', 'יא4', 'יב1', 'יב2', 'יב3', 'יב4']
        selected_option2 = st.selectbox('בחר שכבה וכיתה', options)

    with col3:
        optionsProf = ['כימיה', 'פיסיקה']
        selected_option3 = st.selectbox('מקצוע', optionsProf)

    with col4:
        data = sendRequest("getTeacherList", None, "get")
        teacherNamedb = pd.DataFrame(data['teachers_list'])
        teacher_profs = {
            'כימיה': teacherNamedb[teacherNamedb[3] == 'כימיה'],
            'פיסיקה': teacherNamedb[teacherNamedb[3] == 'פיסיקה']
        }
        filtered_teachers_df = teacher_profs.get(selected_option3, pd.DataFrame())
        optionsTeacherName = filtered_teachers_df[1].tolist()
        selected_option4 = st.selectbox('בחר מורה', optionsTeacherName)

    with col5:
        data = sendRequest("getRoomsList", None, "get")
        optionsRooms = list(pd.DataFrame(data['roomsList'])[0])
        selected_option5 = st.selectbox('חדר', optionsRooms)

    with col6:
        selected_option6 = st.selectbox('שעת התחלה', st.session_state.times)

    with col7:
        selected_option7 = st.selectbox('שעת סיום', st.session_state.times)

    with col8:
        st.write("")
        st.write("")
        if st.button('הוספה'):
            start_index = st.session_state.times.index(selected_option6)
            end_index = st.session_state.times.index(selected_option7)
            content = f"מורה: {selected_option4}\nכיתה: {selected_option2}"
            room_column = selected_option5

            # Update the DataFrame in session state
            st.session_state.df.loc[st.session_state.times[start_index]:st.session_state.times[end_index],
            room_column] = content

            # This is optional but can help ensure the UI updates immediately
            st.rerun()
    with col9:
        st.write("")
        st.write("")
        if st.button('מחיקה'):
            start_index = st.session_state.times.index(selected_option6)
            end_index = st.session_state.times.index(selected_option7)
            room_column = selected_option5

            # Use a blank string to "delete" the data from the table
            st.session_state.df.loc[st.session_state.times[start_index]:st.session_state.times[end_index],
            room_column] = ""
            st.rerun()

elif st.session_state.current_page == 'מערכת שעות שבועית שותפת':
    st.title('ניהול מערכת בית ספר')
    st.header("מערכת שעות שבועית שותפת")

elif st.session_state.current_page == 'לוח מבחנים':
    st.title('ניהול מערכת בית ספר')
    st.header("לוח מבחנים")
