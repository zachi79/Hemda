import streamlit as st
from sendRequest import sendRequest
import pandas as pd


def roomsList():
    col_form1, col_form2, col_form3  = st.columns([5, 5, 5])
    with col_form2:

        data = sendRequest("getRoomsList", None, "get")
        df_rooms = pd.DataFrame(data['roomsList'])
        df_rooms.columns = ['מספר חדר', 'יעוד']
        st.dataframe(df_rooms, use_container_width=True)
    pass
