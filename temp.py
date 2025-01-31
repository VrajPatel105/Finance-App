import streamlit as st
from streamlit_lottie import st_lottie
import requests
import json

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        r.raise_for_status()  # Raises an HTTPError for bad responses
        return r.json()
    except Exception as e:
        st.error(f"Error loading Lottie animation: {str(e)}")
        return None

# Use direct JSON URL instead of lottie.host URL
lottie_url = "https://lottie.host/2b78dd02-e9a2-4f8a-81a7-7fa44e1f4b7e/9fHByB2zdS.json"  # Replace with your JSON URL

lottie_json = load_lottieurl(lottie_url)

if lottie_json:
    st_lottie(
        lottie_json,
        speed=1,
        height=300,
        width=300,
        key="lottie"
    )
else:
    st.warning("Failed to load Lottie animation")