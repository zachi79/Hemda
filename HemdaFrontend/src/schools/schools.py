import streamlit as st
from src.common.sendRequest import sendRequest
import pandas as pd


def schoolsList():
    col_form1, col_form2, col_form3 = st.columns([1, 4, 1])
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
                    st.session_state.teachers_df = pd.concat([st.session_state.teachers_df, new_teacher],
                                                             ignore_index=True)
                    st.success(f"בית ספר {teacher_name} נוסף בהצלחה!")
                    st.rerun()
                else:
                    st.error("יש למלא את כל השדות כדי להוסיף בית ספר.")
    pass