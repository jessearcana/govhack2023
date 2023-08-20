#from get_story import get_user_story_audio
import openai_query



# read json article
import json
with open('holiday_data.json') as json_file:
    holiday_data = json.load(json_file)
with open('tourism_operators.json') as json_file:
    tourist_operators_data = json.load(json_file)

def get_relevant_google_places(vector_in):
    import pickle as pkl
    googPlaces = pkl.load(open("googPlacesHoliday.pkl", "rb"))
    # search faiss index for nearest neighbour
    k = 1
    D, I = googPlaces['index'].search(np.array([vector_in]), k) # sanity check: search for user story in holiday data
    return googPlaces['places'][I[0][0]]
    

# create a new faiss index
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# load BERT model
model = SentenceTransformer('msmarco-distilbert-base-dot-prod-v3') # bert-base-nli-mean-tokens


### ####################
### create faiss index
### ####################
indexTouristOps = faiss.IndexFlatL2(768)
indexHols = faiss.IndexFlatL2(768)

# embed and add each descriptor from the holiday data
for holiday in holiday_data['holidays']:
    # embed text
    embedding = model.encode(holiday['description'])
    # add vector to faiss
    indexHols.add(np.array([embedding]))
# write index to file
faiss.write_index(indexHols, "faiss_Holidays.index")

# embed and add each descriptor from the tourist operators data
for tourist_operator in tourist_operators_data['tourism_operators']:
    # embed text
    embedding = model.encode(tourist_operator['description'])
    # add vector to faiss
    indexTouristOps.add(np.array([embedding]))
# write index to file
faiss.write_index(indexTouristOps, "faiss_TouristOps.index")

### #####################
### get/process user data
### #####################

def process_user_dat(text):
    # record user speech from microphone, pass to google for speech to text conversion
    # story = get_user_story_audio()
    story = text
    # embed user story
    embedding = model.encode(story)

    # search faiss index for nearest neighbour
    k = 1
    D, I = indexHols.search(np.array([embedding]), k) # sanity check: search for user story in holiday data
    # print("Holiday data:")

    D, I = indexTouristOps.search(np.array([embedding]), k) # search for user story in tourist operators data
    # print("Tourist operators data:")
    hols_dat = holiday_data['holidays'][I[0][0]]
    tour_ops = tourist_operators_data['tourism_operators'][I[0][0]]
    googlePlaces = get_relevant_google_places(embedding)
    output = [hols_dat, tour_ops, googlePlaces]
    return output

# process_user_dat('wine and golf')

# vector_in = embedding
output = process_user_dat("tell me abnout a mountain biking holiday for a family of four")
narrative = openai_query.get_openAI_summary(output)
print(narrative)