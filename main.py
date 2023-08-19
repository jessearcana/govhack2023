from get_story import get_user_story_audio

# read json article
import json
with open('holiday_data.json') as json_file:
    holiday_data = json.load(json_file)
with open('tourism_operators.json') as json_file:
    tourist_operators_data = json.load(json_file)

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
    story = get_user_story_audio()

    # embed user story
    embedding = model.encode(story)

    # search faiss index for nearest neighbour
    k = 1
    D, I = indexHols.search(np.array([embedding]), k) # sanity check: search for user story in holiday data
    print("Holiday data:")
    # print(D)
    # print(I)
    # print(holiday_data['holidays'][I[0][0]])
    D, I = indexTouristOps.search(np.array([embedding]), k) # search for user story in tourist operators data
    print("Tourist operators data:")
    # print(D)
    # print(I)
    # print(tourist_operators_data['tourism_operators'][I[0][0]])
    output = [holiday_data['holidays'][I[0][0]], tourist_operators_data['tourism_operators'][I[0][0]]]
    return output
