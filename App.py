# streamlit App
import streamlit as st
import numpy as np

# Path: App.py
# streamlit App
import json
import faiss
from sentence_transformers import SentenceTransformer
from streamlit_chat import message
import tiktoken
import re

# our local libs
from main import process_user_dat
import openai_query

st.set_page_config(page_title="Heaps Good", page_icon=":robot:")
st.header("Heaps Good")

@st.cache_data
def load_index(index_path):
    index = faiss.read_index(index_path)
    return index

@st.cache_data(persist="disk") # cache the input and response for each basic user input sent to OpenAI - mainly so when we repeat a test we don't hit the API
def openai_story(text_input,token_count):
    story = openai_query.get_openAI_story(previous=text_input,token_count=token_count)
    return story

@st.cache_data(persist="disk") # cache the input and response for each basic user input sent to OpenAI - mainly so when we repeat a test we don't hit the API
def get_key_activities(story):
    key_activities = openai_query.get_key_activities(story)
    sentencify=re.sub(r'\n','.\n',key_activities)
    return sentencify

# I think tiktoken caches locally by default
tiktoken_encoding = tiktoken.get_encoding("cl100k_base")

def trim_input(input):
    tokens = tiktoken_encoding.encode(input)
    if len(tokens) > 300:
        trimmed_input = input[0:2500] # Try based on average 5 chars per token - most likely to work
        tokens = tiktoken_encoding.encode(trimmed_input)
        if len(tokens) > 300:
            trimmed_input = input[0:300] # In case it's a space separated set of single chars or something - worst case
            tokens = tiktoken_encoding.encode(trimmed_input)
    else:
        trimmed_input = input
    return trimmed_input, len(tokens)

indexHols = load_index('faiss_Holidays.index')
indexTouristOps = load_index('faiss_TouristOps.index')

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

def get_text():
    input_text = st.text_input("Text: ", "", key="input")
    return input_text

user_input, token_count = trim_input(get_text())

if user_input:
    story = openai_story(user_input,token_count)
    key_activities = get_key_activities(story)
    activity_providers = process_user_dat(key_activities) #qa_chain({'question': user_input,'chat_history':[]})
    st.session_state.past.append(user_input)
    st.session_state.generated.append("\nStory:\n" + str(story) + "\nActivities:\n" + str(key_activities)+ "\nCheck out these places to plan your holiday:\n" + str(activity_providers))

if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
