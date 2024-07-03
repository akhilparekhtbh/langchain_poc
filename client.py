import streamlit as st
import requests

base_url = "http://localhost:8000"


def get_openai_response(endpoint, data):
    response = requests.post(
        f"{base_url}{endpoint}",
        json=data,
        headers={"Content-Type": "application/json"},
    )
    print(response.text)
    return response.json()["output"]


def get_essay(input_text):
    data = {"input": {"topic": input_text}}
    return get_openai_response("/essay/invoke", data)["content"]


def get_blog(input_text):
    data = {"input": {"topic": input_text}}
    return get_openai_response("/blog/invoke", data)["content"]


def get_translation(input_text):
    data = {"input": {"text": input_text}}
    return get_openai_response("/translate/invoke", data)["content"]


st.title("Query Helper")
input_text_1 = st.text_input("Write an essay on ...")
input_text_2 = st.text_input("Write a blog on ...")
input_text_3 = st.text_input("Translate this into English ...")


if input_text_1:
    print(input_text_1)
    essay = get_essay(input_text_1)
    st.write(essay)

if input_text_2:
    blog = get_blog(input_text_2)
    st.write(blog)

if input_text_3:
    translation = get_translation(input_text_3)
    st.write(translation)
