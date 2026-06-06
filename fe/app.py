import streamlit as st
import requests

server_url="http://127.0.0.1:8000"
st.title("AI Weather Forecast")

city=st.text_input("Enter city")

question=st.text_input("ask your question")

if st.button("ask answer"):
    res=requests.post(f"{server_url}/get_weather",params={
                            "city":city,
                            "question":question})
    st.success(res.json()["messages"][-1]["content"])