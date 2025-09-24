import streamlit as st
from datetime import date
import calendar
from streamlit_option_menu import option_menu
import pandas as pd

from src.common.sendRequest import sendRequest


def display_calendar_month(year, month):
    """
    Displays a calendar grid for a given month and year in Streamlit.
    """
    # Use Hebrew day names in the correct order (Sunday to Saturday)
    hebrew_day_names = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]

    #st.markdown(f"## {calendar.month_name[month]} {year}")

    # Create columns for the day names
    cols = st.columns(7)
    for i, day in enumerate(hebrew_day_names):
        with cols[i]:
            st.markdown(f"**{day}**", unsafe_allow_html=True)

    # Iterate through the weeks of the month
    for week in calendar.Calendar().monthdatescalendar(year, month):
        # Create columns for each week
        cols = st.columns(7)
        for i, day_date in enumerate(week):
            with cols[i]:
                # The square size and style
                container_style = """
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                margin: 2px;
                text-align: center;
                height: 120px;
                display: flex;
                flex-direction: column;
                justify-content: flex-start;
                """

                day_content = ""
                # Check if the day is in the current month
                if day_date.month == month:
                    day_content += f"**{day_date.day}**"
                    if day_date in st.session_state.notes:
                        note_text = st.session_state.notes[day_date]
                        day_content += f"""
                        <div style="overflow-y: auto; max-height: 70px; font-size: 12px; text-align: right; margin-top: 5px;">
                            {note_text}
                        </div>
                        """
                    st.markdown(
                        f'<div style="{container_style}">{day_content}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    # For days from the previous/next month, display an empty or faded square
                    st.markdown(
                        f'<div style="{container_style} border: none;"></div>',
                        unsafe_allow_html=True
                    )


def monthTestBoard():
    st.set_page_config(layout="wide")

    # Initialize session state for the current date and notes
    if 'current_date' not in st.session_state:
        st.session_state.current_date = date.today()
    if 'notes' not in st.session_state:
        st.session_state.notes = {}

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("⬅️ חודש קודם"):
            current_date = st.session_state.current_date
            if current_date.month == 1:
                st.session_state.current_date = date(current_date.year - 1, 12, 1)
            else:
                st.session_state.current_date = date(current_date.year, current_date.month - 1, 1)
            st.rerun()

    with col2:
        st.markdown(
            "<div style='text-align: center; font-size: 24px; font-weight: bold;'> "
            f"{st.session_state.current_date.strftime('%B %Y')}"
            "</div>",
            unsafe_allow_html=True
        )

    with col3:
        if st.button("חודש הבא ➡️"):
            current_date = st.session_state.current_date
            if current_date.month == 12:
                st.session_state.current_date = date(current_date.year + 1, 1, 1)
            else:
                st.session_state.current_date = date(current_date.year, current_date.month + 1, 1)
            st.rerun()

    display_calendar_month(st.session_state.current_date.year, st.session_state.current_date.month)

    st.markdown("---")

    # Text input and buttons for adding/deleting notes
    st.subheader("הוסף/מחק טקסט מהיומן")

    days_in_month = calendar.monthrange(st.session_state.current_date.year, st.session_state.current_date.month)[1]
    days_list = [d for d in range(1, days_in_month + 1)]

    selected_day = st.selectbox("בחר יום:", days_list)
    note_text = st.text_input("הכנס טקסט:", "")

    col4, col5 = st.columns([1, 1])

    with col4:
        if st.button("הכנס טקסט"):
            if note_text:
                full_date = date(st.session_state.current_date.year, st.session_state.current_date.month, selected_day)
                st.session_state.notes[full_date] = note_text
                st.success(f"הטקסט הוכנס ליום {selected_day} בהצלחה!")
                st.rerun()
            else:
                st.warning("נא להזין טקסט")

    with col5:
        if st.button("מחק טקסט"):
            full_date = date(st.session_state.current_date.year, st.session_state.current_date.month, selected_day)
            if full_date in st.session_state.notes:
                del st.session_state.notes[full_date]
                st.success(f"הטקסט נמחק מיום {selected_day} בהצלחה!")
                st.rerun()
            else:
                st.warning("אין טקסט למחוק ביום זה")

    st.markdown("---")

    pass


def testsBoard():

    sub_selected = option_menu(
        menu_title=None,
        #options=["רשימה", "רשימה2", "חודשי"],
        options=["רשימה"],
        #icons=["person", "calendar-check", "calendar"],
        icons=["calendar"],
        menu_icon=None,
        default_index=0,
        orientation="horizontal",
    )

    if sub_selected == "חודשי":
        monthTestBoard()

    elif sub_selected == "רשימה22":
        schools_data = sendRequest("getSchoolsList", None, "get")
        SCHOOLS = [school[0] for school in schools_data['schoolsList']]

        rooms_data = sendRequest("getRoomsList", None, "get")
        ROOMS = [room[0] for room in rooms_data['roomsList']]

        GRADES = ['י1', 'י2', 'י3', 'יא1', 'יא2', 'יא3', 'יב1', 'יב2', 'יב3']
        SUBJECTS = ['כימיה', 'פיסיקה','']

        teachers_data = sendRequest("getTeacherList", None, "get")
        columns = ['id', 'teachername', 'phone', 'prof', 'email', 'color']
        teachers_dataDF = pd.DataFrame(teachers_data['teachers_list'], columns=columns)
        TEACHERS =  teachers_dataDF['teachername'].tolist()# ['מורה א', 'מורה ב', 'מורה ג', 'מורה ד']

        #TEACHERS = ['מורה א', 'מורה ב', 'מורה ג', 'מורה ד']
        #SUBJECTS = ['כימיה', 'פיסיקה', 'כימיה','פיסיקה']

        # --- הגדרת מבנה הטבלה ההתחלתית ---
        # יצירת DataFrame ראשוני עם עמודות ריקות/ברירת מחדל
        # ניתן להוסיף שורות דוגמה אם רוצים
        data = {
            'בית ספר': [SCHOOLS[0]],
            'שכבה': [GRADES[0]],
            'מורה': [TEACHERS[0]],
            'מקצוע': [SUBJECTS[0]],  # בחירת מקצועות: נתחיל עם אחד
            'חדר': [ROOMS[0]],
            'מבחן 1': [date.today()],
            'מבחן 2': [date.today()],
            'מבחן 3': [date.today()],
            'מבחן 4': [date.today()],
            'מבחן 5': [date.today()],
            'מבחן 6': [date.today()],
            'מבחן מתכונת': [date.today()],
            'בגרות מעבדה': [date.today()],
            'סימון שליחה במייל': [False]
        }

        df = pd.DataFrame(data)

        # --- כותרת ופקדים ---
        st.title('📝 טבלת תכנון בחינות - עריכה ושמירה')
        st.caption('ניתן לערוך כל שורה ולהוסיף שורות חדשות.')

        # --- פונקציה לעריכת ה-DataFrame באמצעות st.data_editor ---
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",  # מאפשר למשתמש להוסיף ולמחוק שורות
            column_config={
                'בית ספר': st.column_config.SelectboxColumn(
                    'בית ספר',
                    help='בחר את שם בית הספר',
                    width='small',
                    options=SCHOOLS,
                    required=True,
                ),
                'שכבה': st.column_config.SelectboxColumn(
                    'שכבה',
                    help='בחר את שכבת הלימוד',
                    width='small',
                    options=GRADES,
                    required=True,
                ),
                'מורה': st.column_config.SelectboxColumn(
                    'מורה',
                    help='בחר את שם המורה',
                    width='medium',
                    options=TEACHERS,
                    required=True,
                ),
                'מקצוע': st.column_config.SelectboxColumn(
                    'מקצוע',  # למרות הבקשה לכימיה/פיסיקה בלבד, ב-data_editor רגיל קשה לייצר Multiselect
                    help='בחר את המקצוע: כימיה או פיסיקה',
                    options=SUBJECTS,
                    required=True
                ),
                'חדר': st.column_config.SelectboxColumn(
                    'חדר',
                    help='בחר חדר',
                    width='small',
                    options=ROOMS,
                    required=True,
                ),
                'מבחן 1': st.column_config.DateColumn(
                    'מבחן 1',
                    help='תאריך המבחן הראשון (POPUP)',
                    format="YYYY-MM-DD",
                    min_value=date.today()
                ),
                'מבחן 2': st.column_config.DateColumn(
                    'מבחן 2',
                    help='תאריך המבחן השני (POPUP)',
                    format="YYYY-MM-DD",
                    min_value=date.today()
                ),
                'מבחן 3': st.column_config.DateColumn(
                    'מבחן 3',
                    help='תאריך המבחן השני (POPUP)',
                    format="YYYY-MM-DD",
                    min_value=date.today()
                ),
                'מבחן 4': st.column_config.DateColumn(
                    'מבחן 4',
                    help='תאריך המבחן השני (POPUP)',
                    format="YYYY-MM-DD",
                    min_value=date.today()
                ),
                'מבחן 5': st.column_config.DateColumn(
                    'מבחן 5',
                    help='תאריך המבחן השני (POPUP)',
                    format="YYYY-MM-DD",
                    min_value=date.today()
                ),
                'מבחן 6': st.column_config.DateColumn(
                    'מבחן 6',
                    help='תאריך המבחן השני (POPUP)',
                    format="YYYY-MM-DD",
                    min_value=date.today()
                ),
                'מבחן מתכונת': st.column_config.DateColumn(
                    'מבחן מתכונת',
                    help='תאריך מבחן המתכונת (POPUP)',
                    format="YYYY-MM-DD",
                    min_value=date.today()
                ),
                'בגרות מעבדה': st.column_config.DateColumn(
                    'בגרות מעבדה',
                    help='תאריך בחינת בגרות המעבדה (POPUP)',
                    format="YYYY-MM-DD",
                    min_value=date.today()
                ),
                'סימון שליחה במייל': st.column_config.CheckboxColumn(
                    'סימון שליחה במייל',
                    help='סמן לאחר שליחת המייל',
                    width='small',
                    default=False
                )
            },
            use_container_width=True
        )
        teacherSelected = edited_df.iloc[-1]["מורה"]
        subjectSelected = teachers_dataDF.loc[teachers_dataDF['teachername'] == teacherSelected, 'prof'].iloc[0]
        edited_df.iloc[-1]["מקצוע"] = subjectSelected
    elif sub_selected == "רשימה11":
        schools_data = sendRequest("getSchoolsList", None, "get")
        SCHOOLS = [school[0] for school in schools_data['schoolsList']]

        rooms_data = sendRequest("getRoomsList", None, "get")
        ROOMS = [room[0] for room in rooms_data['roomsList']]

        GRADES = ['י1', 'י2', 'י3', 'יא1', 'יא2', 'יא3', 'יב1', 'יב2', 'יב3']
        SUBJECTS = ['כימיה', 'פיסיקה','']

        teachers_data = sendRequest("getTeacherList", None, "get")
        columns = ['id', 'teachername', 'phone', 'prof', 'email', 'color']
        teachers_dataDF = pd.DataFrame(teachers_data['teachers_list'], columns=columns)
        TEACHERS =  teachers_dataDF['teachername'].tolist()# ['מורה א', 'מורה ב', 'מורה ג', 'מורה ד']

        #TEACHERS = ['מורה א', 'מורה ב', 'מורה ג', 'מורה ד']
        #SUBJECTS = ['כימיה', 'פיסיקה', 'כימיה','פיסיקה']

        # --- הגדרת מבנה הטבלה ההתחלתית ---
        # יצירת DataFrame ראשוני עם עמודות ריקות/ברירת מחדל
        # ניתן להוסיף שורות דוגמה אם רוצים
        if 'df' not in st.session_state:
            data = {
                'בית ספר': [SCHOOLS[0]],
                'שכבה': [GRADES[0]],
                'מורה': [TEACHERS[0]],
                'מקצוע': [SUBJECTS[0]],
                'חדר': [ROOMS[0]],
                'מבחן 1': [date.today()],
                'מבחן 2': [date.today()],
                'מבחן 3': [date.today()],
                'מבחן 4': [date.today()],
                'מבחן 5': [date.today()],
                'מבחן 6': [date.today()],
                'מבחן מתכונת': [date.today()],
                'בגרות מעבדה': [date.today()],
                'סימון שליחה במייל': [False]
            }
            st.session_state.df = pd.DataFrame(data)

        # --- Callback function to handle changes ---
        def update_subject():
            edited_rows = st.session_state["data_editor"]["edited_rows"]
            added_rows = st.session_state["data_editor"]["added_rows"]

            # Check for changes in existing rows
            for index, changes in edited_rows.items():
                if "מורה" in changes:
                    teacherSelected = changes["מורה"]
                    # Find the corresponding subject in your original data
                    subjectSelected = \
                    teachers_dataDF.loc[teachers_dataDF['teachername'] == teacherSelected, 'prof'].iloc[0]
                    st.session_state.df.loc[index, "מקצוע"] = subjectSelected

            # Check for newly added rows
            for new_row in added_rows:
                if "מורה" in new_row:
                    teacherSelected = new_row["מורה"]
                    subjectSelected = \
                    teachers_dataDF.loc[teachers_dataDF['teachername'] == teacherSelected, 'prof'].iloc[0]
                    st.session_state.df.iloc[-1]["מקצוע"] = subjectSelected

        #df = pd.DataFrame(data)

        # --- כותרת ופקדים ---
        st.title('📝 טבלת תכנון בחינות - עריכה ושמירה')
        st.caption('ניתן לערוך כל שורה ולהוסיף שורות חדשות.')

        # --- פונקציה לעריכת ה-DataFrame באמצעות st.data_editor ---
        edited_df = st.data_editor(
            st.session_state.df,
            num_rows="dynamic",
            key="data_editor",
            on_change=update_subject,  # Pass the callback function here
            column_config={
                'בית ספר': st.column_config.SelectboxColumn('בית ספר', options=SCHOOLS, required=True),
                'שכבה': st.column_config.SelectboxColumn('שכבה', options=GRADES, required=True),
                'מורה': st.column_config.SelectboxColumn('מורה', options=TEACHERS, required=True),
                'מקצוע': st.column_config.SelectboxColumn('מקצוע', options=SUBJECTS, required=True),
                'חדר': st.column_config.SelectboxColumn('חדר', options=ROOMS, required=True),
                'מבחן 1': st.column_config.DateColumn('מבחן 1', format="YYYY-MM-DD", min_value=date.today()),
                'מבחן 2': st.column_config.DateColumn('מבחן 2', format="YYYY-MM-DD", min_value=date.today()),
                'מבחן 3': st.column_config.DateColumn('מבחן 3', format="YYYY-MM-DD", min_value=date.today()),
                'מבחן 4': st.column_config.DateColumn('מבחן 4', format="YYYY-MM-DD", min_value=date.today()),
                'מבחן 5': st.column_config.DateColumn('מבחן 5', format="YYYY-MM-DD", min_value=date.today()),
                'מבחן 6': st.column_config.DateColumn('מבחן 6', format="YYYY-MM-DD", min_value=date.today()),
                'מבחן מתכונת': st.column_config.DateColumn('מבחן מתכונת', format="YYYY-MM-DD", min_value=date.today()),
                'בגרות מעבדה': st.column_config.DateColumn('בגרות מעבדה', format="YYYY-MM-DD", min_value=date.today()),
                'סימון שליחה במייל': st.column_config.CheckboxColumn('סימון שליחה במייל', default=False)
            },
            use_container_width=True
        )

        st.write(st.session_state.df)
        # teacherSelected = edited_df.iloc[-1]["מורה"]
        # subjectSelected = teachers_dataDF.loc[teachers_dataDF['teachername'] == teacherSelected, 'prof'].iloc[0]
        # edited_df.iloc[-1]["מקצוע"] = subjectSelected

    elif sub_selected == "רשימה":

        data = sendRequest("getTestsBoard", None, "get")
        schools_data = sendRequest("getSchoolsList", None, "get")
        SCHOOLS = [school[0] for school in schools_data['schoolsList']]

        rooms_data = sendRequest("getRoomsList", None, "get")
        ROOMS = [room[0] for room in rooms_data['roomsList']]

        GRADES = ['י1', 'י2', 'י3', 'יא1', 'יא2', 'יא3', 'יב1', 'יב2', 'יב3']
        SUBJECTS = ['כימיה', 'פיסיקה','']

        teachers_data = sendRequest("getTeacherList", None, "get")
        columns = ['id', 'teachername', 'phone', 'prof', 'email', 'color']
        teachers_dataDF = pd.DataFrame(teachers_data['teachers_list'], columns=columns)
        TEACHERS =  teachers_dataDF['teachername'].tolist()# ['מורה א', 'מורה ב', 'מורה ג', 'מורה ד']

        # data = {
        #     'בית ספר': [SCHOOLS[0]],
        #     'שכבה': [GRADES[0]],
        #     'מורה': [TEACHERS[0]],
        #     'מקצוע': [SUBJECTS[0]],  # בחירת מקצועות: נתחיל עם אחד
        #     'חדר': [ROOMS[0]],
        #     'מבחן 1': [date.today()],
        #     'מבחן 2': [date.today()],
        #     'מבחן 3': [date.today()],
        #     'מבחן 4': [date.today()],
        #     'מבחן 5': [date.today()],
        #     'מבחן 6': [date.today()],
        #     'מבחן מתכונת': [date.today()],
        #     'בגרות מעבדה': [date.today()],
        #     'סימון שליחה במייל': [False]
        # }
        table_columns = ['בית ספר',
            'שכבה',
            'מורה',
            'מקצוע',
            'חדר',
            'מבחן 1',
            'מבחן 2',
            'מבחן 3',
            'מבחן 4',
            'מבחן 5',
            'מבחן 6',
            'מבחן מתכונת',
            'בגרות מעבדה',
            'סימון שליחה במייל'
        ]
        if data['testsBoard']:
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame(columns=table_columns)

        col_form1, col_form2, col_form3= st.columns([1, 2, 1])
        with col_form2:
            st.title('📝 טבלת תכנון בחינות - עריכה ושמירה')

        st.caption('ניתן לערוך כל שורה ולהוסיף שורות חדשות.')

        # --- פונקציה לעריכת ה-DataFrame באמצעות st.data_editor ---
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",  # מאפשר למשתמש להוסיף ולמחוק שורות
            column_config={
                'בית ספר': st.column_config.SelectboxColumn(
                    'בית ספר',
                    help='בחר את שם בית הספר',
                    width='small',
                    options=SCHOOLS,
                    required=True,
                ),
                'שכבה': st.column_config.SelectboxColumn(
                    'שכבה',
                    help='בחר את שכבת הלימוד',
                    width='small',
                    options=GRADES,
                    required=True,
                ),
                'מורה': st.column_config.SelectboxColumn(
                    'מורה',
                    help='בחר את שם המורה',
                    width='medium',
                    options=TEACHERS,
                    required=True,
                ),
                'מקצוע': st.column_config.SelectboxColumn(
                    'מקצוע',  # למרות הבקשה לכימיה/פיסיקה בלבד, ב-data_editor רגיל קשה לייצר Multiselect
                    help='בחר את המקצוע: כימיה או פיסיקה',
                    options=SUBJECTS,
                    required=True
                ),
                'חדר': st.column_config.SelectboxColumn(
                    'חדר',
                    help='בחר חדר',
                    width='small',
                    options=ROOMS,
                    required=True,
                ),
                'מבחן 1': st.column_config.DateColumn(
                    'מבחן 1',
                    help='תאריך המבחן הראשון (POPUP)',
                    format="YYYY-MM-DD",
                    min_value=date.today()
                ),
                'מבחן 2': st.column_config.DateColumn(
                    'מבחן 2',
                    help='תאריך המבחן השני (POPUP)',
                    format="YYYY-MM-DD",
                    min_value=date.today()
                ),
                'מבחן 3': st.column_config.DateColumn(
                    'מבחן 3',
                    help='תאריך המבחן השני (POPUP)',
                    format="YYYY-MM-DD",
                    min_value=date.today()
                ),
                'מבחן 4': st.column_config.DateColumn(
                    'מבחן 4',
                    help='תאריך המבחן השני (POPUP)',
                    format="YYYY-MM-DD",
                    min_value=date.today()
                ),
                'מבחן 5': st.column_config.DateColumn(
                    'מבחן 5',
                    help='תאריך המבחן השני (POPUP)',
                    format="YYYY-MM-DD",
                    min_value=date.today()
                ),
                'מבחן 6': st.column_config.DateColumn(
                    'מבחן 6',
                    help='תאריך המבחן השני (POPUP)',
                    format="YYYY-MM-DD",
                    min_value=date.today()
                ),
                'מבחן מתכונת': st.column_config.DateColumn(
                    'מבחן מתכונת',
                    help='תאריך מבחן המתכונת (POPUP)',
                    format="YYYY-MM-DD",
                    min_value=date.today()
                ),
                'בגרות מעבדה': st.column_config.DateColumn(
                    'בגרות מעבדה',
                    help='תאריך בחינת בגרות המעבדה (POPUP)',
                    format="YYYY-MM-DD",
                    min_value=date.today()
                ),
                'סימון שליחה במייל': st.column_config.CheckboxColumn(
                    'סימון שליחה במייל',
                    help='סמן לאחר שליחת המייל',
                    width='small',
                    default=False
                )
            },
            #use_container_width=True
            width = 'stretch'
        )

        button_css = """
            <style>
            div.stButton > button:first-child {
                background-color: #4CAF50; /* Green background */
                color: white;
                font-size: 20px;
                font-weight: bold;
                border-radius: 12px;
                border: 2px solid black;
                padding: 10px 24px;
                cursor: pointer;
                /* Add a smooth transition for the color change */
                transition: background-color 0.3s ease;
            }

            /* Change color to yellow on hover */
            div.stButton > button:hover {
                background-color: #FFC107; /* Gold/yellow color */
            }

            /* Change color to a darker yellow when the button is actively being pressed */
            div.stButton > button:active {
                background-color: #FF12FF; 
            }
            </style>
        """

        st.markdown(button_css, unsafe_allow_html=True)

        # Create the button with the custom style
        if st.button("Apply"):
            print("send testsBoard Data")
            payload = edited_df
            data = sendRequest("setTestsBoard", payload, "post")

    elif sub_selected == "רשימה2":
        st.write("כאן תוצג רשימת מבחנים.")


        # יצירת DataFrame לדוגמה (כמו טבלת ה-Excel שלך)
        data = {
            'שם מוצר': ['עט', 'עיפרון', 'מחברת', 'סרגל', 'עט'],
            'קטגוריה': ['כתיבה', 'כתיבה', 'ציוד משרדי', 'כלי מדידה', 'כתיבה'],
            'מחיר': [5, 3, 12, 8, 5],
            'מלאי': [150, 0, 75, 200, 150]
        }
        df = pd.DataFrame(data)

        st.title("טבלת מוצרים עם סינון")

        # הצגת הטבלה עם סינון מובנה
        # st.dataframe() מציגה כברירת מחדל את אייקון המסנן ליד כותרות העמודות
        st.dataframe(
            df,
            use_container_width=True,  # הטבלה תתפרס על רוחב המסך
        )

        st.title("בחירת תאריך")

        # הפקודה st.date_input יוצרת את לוח השנה הקופץ
        selected_date = st.date_input(
            "בחר תאריך:",  # הכיתוב שיופיע מעל הוידג'ט
            date.today(),  # הגדרת תאריך ברירת המחדל (היום)
            min_value=date(2023, 1, 1),  # הגבלת טווח תאריכים מינימלי
            max_value=date(2040, 12, 31)  # הגבלת טווח תאריכים מקסימלי
        )

        # הצגת התאריך שנבחר על ידי המשתמש
        st.write("התאריך שבחרת:", selected_date)
        st.write("סוג האובייקט בפייתון:", type(selected_date))


