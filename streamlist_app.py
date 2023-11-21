import streamlit as st
import requests
import datetime

# api_key = ""

st.set_page_config(
    page_title = "HCI -Final Project (change this lol)"
)

page = st.sidebar.selectbox(
    "Pick a page",
    ["Search Page","Watchlist Page", "Layout Page","Movie Page", "TV Page"]
)

if page =="Search Page":
    st.write("Under Construction")
elif page =="Watchlist Page":
    st.write("Under Construction")
elif page == "Layout Page":
    st.write("Under Construction")
elif page == "Movie Page":
    st.write("Under Construction")
elif page =="Tv Page":
    st.write("Under Construction")
else:
    st.write("Under Construction")