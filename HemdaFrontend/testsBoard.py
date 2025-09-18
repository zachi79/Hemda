import streamlit as st
from datetime import date
import calendar

def display_calendar_month(year, month):
    """
    Displays a calendar grid for a given month and year in Streamlit.
    """
    # Use Hebrew day names in the correct order (Sunday to Saturday)
    hebrew_day_names = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]

    st.markdown(f"## {calendar.month_name[month]} {year}")

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

def testsBoard():
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

