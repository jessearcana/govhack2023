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

# @st.cache_data(persist="disk") # cache the input and response for each basic user input sent to OpenAI - mainly so when we repeat a test we don't hit the API
def openai_story(text_input,token_count):
    story = openai_query.get_openAI_story(previous=text_input,token_count=token_count)
    return story

# @st.cache_data(persist="disk") # cache the input and response for each basic user input sent to OpenAI - mainly so when we repeat a test we don't hit the API
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
    input_text = st.text_area("Tell us about recent holiday experiences (anywhere) that you think are relevant to understand the kinds of things you might like. For an example try the default pre-populated content: (100 to 200 words is good)", value="We spent 2 weeks touring around Melbourne and Victoria. We really enjoyed swimming, wine tasting and the food in Mornington peninsula. The accommodation was right near the beach and we had fish and chips on the beach. The area had a historic old court house (pictured here: https://prov.vic.gov.au/archive/851C686B-F7EA-11E9-AE98-1F3D2DB4AC9B) and we enjoyed learning about it. We also visited the Grampians and stayed at the Hall's gap camping area (which historically looked like this: https://prov.vic.gov.au/archive/7F0F7D3A-F7EA-11E9-AE98-F771DF383C74?image=10). The drive from Mornington to Hall's gap was long which was quite tiring.", key="input")
    return input_text

with st.expander("Details", expanded=False):
    st.markdown("""
Note: After the Govhack submission deadline we noticed we neglected to point out that the live demo here runs from the v2 branch, and we also felt that the readme for the project should also be displayed here. So, here is the readme content from the [main branch](https://raw.githubusercontent.com/jessearcana/govhack2023/main/README.md) and the clickable [v2 branch link.](https://github.com/jessearcana/govhack2023/tree/v2) Other than this we have not made any changes after the 5pm deadline.

# Problem Statement

"What makes a great holiday?" is personal. Everyone has their own blend of unwinding and exploring. In South Australia, we understand that not everyone wants the same experience. Maybe the standard tourist packages don't work for you and you want to mix and match your own holiday. We also understand that not everyone has time to study travel guides and reviews -- a holiday is supposed to be a break from getting organised and not make more work for you.

South Australia has an enormous variety of holiday activities for you to enjoy. So many, in fact, that we think many people will be overwhelmed with choice.

# Our Proposal

Introducing "Heaps Good". Heaps Good is a machine learning assistant that you can talk to to describe the sort of holiday activities that you want. Currently in proof-of-concept form, Heaps Good has a small database of travel activities, locations, and tourism providers that it uses to make recommendations based on what you request. It uses the latest technology in Natural Language Processing, vector databases, and similarity searching to tailor its recommendations to your requirements.

# Description

Heaps Good analyses free text typed by the user. It uses large language models to create a response, and semantic embedding coupled with vector databases to ensure that the presented content is grounded to reality (LLMs have a habit of hallucinating imaginary answers). There are several benefits of our approach compared to current product offerings

## benefit 1

Results are customised to the user, and reflect inferred interests that the user might have.


## benefit 2

Tourist research has become difficult because of the commercial capture of information sources. This has lead to tourists having a sub-optimal experience, as well as a tendency to funnel tourists into a few large, well-known, activies.
Tourism SA, because of its non-commercial nature, has an opportunity to build a portal that is designed with the _tourist_ and the _delivery of an excellent holiday_ as the principal design considerations. Such a portal is currently lacking because commercial systems tend to prioritise _paying for product placement_ above the tourist experience.

## benefit 3

Our portal will, over time, create a dataset of its own from which it can learn and thus improve performance

# Commercial vision
We believe that Heaps Good can become the main way of planning holidays in South Australia, and a significant commercial advantage for the state. By keeping the portal itself non-commercial, it can focus on delivering the best outcome for tourists, leading to better experience, repeat custom, and word-of-mouth effects.

# Envisioned Improvements

This is currently a proof-of-concept product only.

There are many possibilities to extend this platform to improve usability. Some ideas are that it more-effectively considers:
 - transport between activities, inlcuding mapping
 - client classification to make inferences about wants (for example, clients who play golf might also like drinking wine, whereas clients who enjoy go-kart racing might prefer beer). There are thousands of similar inferences that can be made by analysing the communication received from the client - the words they use, the manner of expression, the sound of their voice, their travel companions, etc
 - finding "Hidden Gems" (for those who want them), such as the rock pool at Innes National Park, Stokes Bay, or Skillogalee Winery
 - engage in discourse rather than a single request. The client will be able to say "I want more of that" or "I won't want to do that because", "I want something more cultural", "I want somehting random", and the system will adapt its proposal accordingly
 - making a learning system that understands the sorts of recommendations that different people respond well to
 We have the knowledge and skill to implement all of the above, but have not done so due to time constraints.
 - improving the database of available destinations

# Featured datasets

 - Google Places
 - Synthetic data
 - Australian Tourism Data Warehouse (ATDW)

# last slide
Heaps Good has been made by the Adelaide consultancy, Apex Arcana. We specialise in data science and helping people to make the most of their data. Please talk to use about how we can help you.
""",help="Context added after the competition close deadline")

user_input, token_count = trim_input(get_text())

go_button=st.button('Make me a holiday!')

if (go_button==True and user_input) :
    story = openai_story(user_input,token_count)
    key_activities = get_key_activities(story)
    activity_providers = process_user_dat(key_activities) #qa_chain({'question': user_input,'chat_history':[]})
    st.session_state.past.append(user_input)
    st.session_state.generated.append("\nStory:\n" + str(story) + "\nActivities:\n" + str(key_activities)+ "\nCheck out these places to plan your holiday:\n" + str(activity_providers))

if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
