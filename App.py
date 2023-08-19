# streamlit App
from streamlit import *
import numpy as np

# Path: App.py
# streamlit App
import json
import faiss
from sentence_transformers import SentenceTransformer
from streamlit_chat import message

import streamlit as st
# from audio_recorder_streamlit import audio_recorder

# audio_bytes = audio_recorder()
# if audio_bytes:
#     st.audio(audio_bytes, format="audio/wav")


st.set_page_config(page_title="Holiday Assistant", page_icon=":robot:")
st.header("Holiday Assistant")

indexHols = faiss.read_index('faiss_Holidays.index')
indexTouristOps = faiss.read_index('faiss_TouristOps.index')
model = SentenceTransformer('msmarco-distilbert-base-dot-prod-v3') # bert-base-nli-mean-tokens


# read json article
import json
with open('holiday_data.json') as json_file:
    holiday_data = json.load(json_file)
with open('tourism_operators.json') as json_file:
    tourist_operators_data = json.load(json_file)

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

def get_text():
    input_text = st.text_input("Text: ", "", key="input")
    return input_text

user_input = get_text()
from main import process_user_dat

# May want this in future to break out into an interactive session (from https://code-maven.com/switch-to-interactive-mode-from-python-script)
# import code
# code.interact(local=locals())

if user_input:
    output = process_user_dat(user_input) #qa_chain({'question': user_input,'chat_history':[]})
    st.session_state.past.append(user_input)
    st.session_state.generated.append(str(output))

if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
