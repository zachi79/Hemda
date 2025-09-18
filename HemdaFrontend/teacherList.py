import streamlit as st
from sendRequest import sendRequest
import pandas as pd


def teacherList():
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
    col_form1, col_form2, col_form3 = st.columns([1, 4, 1])
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