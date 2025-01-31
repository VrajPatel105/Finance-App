import streamlit as st
from database.db_manager import Database


@st.cache_resource
def get_database():
    db = Database()
    return db