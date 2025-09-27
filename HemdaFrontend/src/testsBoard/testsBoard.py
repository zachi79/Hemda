import streamlit as st
from datetime import date
import calendar
from streamlit_option_menu import option_menu
import pandas as pd

from src.common.sendRequest import sendRequest
from src.testsBoard import prepareTestsBoard


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

    dataDF, teachersList, schoolsList, roomsList, grades, subject  = prepareTestsBoard.prepareTestsBoard()

    col_form1, col_form2, col_form3= st.columns([1, 2, 1])
    with col_form2:
        st.title('📝 טבלת תכנון בחינות - עריכה ושמירה')

    st.caption('ניתן לערוך כל שורה ולהוסיף שורות חדשות.')

    # --- פונקציה לעריכת ה-DataFrame באמצעות st.data_editor ---
    edited_df = st.data_editor(
        dataDF,
        num_rows="dynamic",  # מאפשר למשתמש להוסיף ולמחוק שורות
        column_config={
            'schoolSelect': st.column_config.SelectboxColumn(
                'בית הספר',
                help='בחר את שם בית הספר',
                width='small',
                options=schoolsList,
                required=True,
            ),
            'classSelect': st.column_config.SelectboxColumn(
                'שכבה',
                help='בחר את שכבת הלימוד',
                width='small',
                options=grades,
                required=True,
            ),
            'teacherSelect': st.column_config.SelectboxColumn(
                'מורה',
                help='בחר את שם המורה',
                width='medium',
                options=teachersList,
                required=True,
            ),
            'profSelect': st.column_config.SelectboxColumn(
                'מקצוע',  # למרות הבקשה לכימיה/פיסיקה בלבד, ב-data_editor רגיל קשה לייצר Multiselect
                disabled=True,
                width='small',
                help='המקצוע: כימיה או פיסיקה',
                options=["פיסיקה","כימיה"],
            ),
            'roomSelect': st.column_config.SelectboxColumn(
                'חדר',
                help='בחר חדר',
                width='small',
                options=roomsList,
                required=True,
            ),
            'test1': st.column_config.DateColumn(
                'מבחן 1',
                help='תאריך המבחן הראשון (POPUP)',
                format="YYYY-MM-DD",
                min_value=date.today()
            ),
            'test2': st.column_config.DateColumn('מבחן 2',help='תאריך המבחן השני (POPUP)',format="YYYY-MM-DD",min_value=date.today()),
            'test3': st.column_config.DateColumn(
                'מבחן 3',
                help='תאריך המבחן השני (POPUP)',
                format="YYYY-MM-DD",
                min_value=date.today()
            ),
            'test4': st.column_config.DateColumn(
                'מבחן 4',
                help='תאריך המבחן השני (POPUP)',
                format="YYYY-MM-DD",
                min_value=date.today()
            ),
            'test5': st.column_config.DateColumn(
                'מבחן 5',
                help='תאריך המבחן השני (POPUP)',
                format="YYYY-MM-DD",
                min_value=date.today()
            ),
            'test6': st.column_config.DateColumn(
                'מבחן 6',
                help='תאריך המבחן השני (POPUP)',
                format="YYYY-MM-DD",
                min_value=date.today()
            ),
            'matkonetTest': st.column_config.DateColumn(
                'מבחן מתכונת',
                help='תאריך מבחן המתכונת (POPUP)',
                format="YYYY-MM-DD",
                min_value=date.today()
            ),
            'labTest': st.column_config.DateColumn(
                'בגרות מעבדה',
                help='תאריך בחינת בגרות המעבדה (POPUP)',
                format="YYYY-MM-DD",
                min_value=date.today()
            ),
            'selectEmailSend': st.column_config.CheckboxColumn(
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
        payload = edited_df.to_json(orient='records')
        data = sendRequest("setTestsBoard", payload, "post")
        st.rerun()

