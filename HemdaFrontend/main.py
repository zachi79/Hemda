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

elif st.session_state.current_page == 'מערכת שעות קבועה':
    # Inject custom CSS for styling the table
    st.set_page_config(layout="wide")
    st.title('ניהול מערכת בית ספר - מערכת שעות קבועה')
    start_time = datetime.strptime("07:30", "%H:%M")
    end_time = datetime.strptime("20:00", "%H:%M")
    time_interval = timedelta(minutes=15)

    # יצירת רשימת השעות
    current_time = start_time
    times = []
    while current_time <= end_time:
        times.append(current_time.strftime("%H:%M"))
        current_time += time_interval

    # יצירת רשימת החדרים
    data = sendRequest("getRoomsList", None, "get")
    df_rooms = pd.DataFrame(data['roomsList'])
    rooms = list(df_rooms[0])
    # יצירת DataFrame ריק עם השעות והחדרים
    data = {room: [""] * len(times) for room in rooms}
    df = pd.DataFrame(data, index=times)
    st.dataframe(df.style.set_properties(**{"text-align": "center"}), height=500)

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        data = sendRequest("getSchoolsList", None, "get")
        optionsSchoollName = list(pd.DataFrame(data['schoolsList'])[0])
        selected_option1 = st.selectbox('בחר בית ספר', optionsSchoollName)

    with col2:
        options = ['י1', 'י2', 'י3', 'י4','יא1', 'יא2', 'יא3', 'יא4','יב1', 'יב2', 'יב3', 'יב4']
        selected_option2 = st.selectbox('בחר שכבה וכיתה', options)

    with col3:
        optionsProf = [ 'כימיה', 'פיסיקה']
        selected_option3 = st.selectbox('מקצוע', optionsProf)

    with col4:
        data = sendRequest("getTeacherList", None, "get")
        teacherNamedb = pd.DataFrame(data['teachers_list'])
        if selected_option3 == 'כימיה':
            optionsTeacherName = teacherNamedb[teacherNamedb[3] == 'כימיה']
            optionsTeacherName = optionsTeacherName[1].tolist()
        elif selected_option3 == 'פיסיקה':
            optionsTeacherName = teacherNamedb[teacherNamedb[3] == 'פיסיקה']
            optionsTeacherName = optionsTeacherName[1].tolist()
        else:
            optionsTeacherName = list(teacherNamedb)[1]
        selected_option4 = st.selectbox('בחר מורה', optionsTeacherName)

    # Place the button in the fifth column
    with col5:
        # Add an empty space above the button to align it with the selectboxes
        st.write("")
        st.write("")
        if st.button('הוספה'):
            st.write('Button clicked!')
            # You can process the selected options here
            st.write(
                f"The selected options are: {selected_option1}, {selected_option2}, {selected_option3}, {selected_option4}")

    with col6:
        # Add an empty space above the button to align it with the selectboxes
        st.write("")
        st.write("")
        if st.button('מחק'):
            st.write('Button clicked!')
            # You can process the selected options here
            st.write(
                f"The selected options are: {selected_option1}, {selected_option2}, {selected_option3}, {selected_option4}")

elif st.session_state.current_page == 'מערכת שעות שבועית שותפת':
    st.title('ניהול מערכת בית ספר')
    st.header("מערכת שעות שבועית שותפת")

elif st.session_state.current_page == 'לוח מבחנים':
    st.title('ניהול מערכת בית ספר')
    st.header("לוח מבחנים")
