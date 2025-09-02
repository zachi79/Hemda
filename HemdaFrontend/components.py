import streamlit as st
from streamlit_option_menu import option_menu

def display_main_menu():
    selected = option_menu(
        menu_title=None,
        options=["ראשי", "רשימת מורים", "רשימת חדרים", "רשימת בתי ספר","מערכת שעות" ,"לוח מבחנים"],
        icons=["house", "person-fill", "door-open-fill", "building-fill", "table", "table","clock"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )
    return selected
