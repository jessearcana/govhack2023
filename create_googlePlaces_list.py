# read json article
import json
with open('holiday_data.json') as json_file:
    holiday_data = json.load(json_file)

import os
googAPI = os.environ.get("googAPI") 
from googleplaces import GooglePlaces, types, lang


googPlacesHoliday = list()
for holiday in holiday_data['holidays']:
    google_places = GooglePlaces(googAPI)
    query_result = google_places.text_search(lat_lng = None,query='tourist destinations', location = holiday['location'] + ", South Australia")
    for place in query_result.places:
        place.get_details()
        googPlacesHoliday.append(place)

import pickle as pkl
pkl.dump(googPlacesHoliday, open("googPlacesHoliday.pkl", "wb"))

# create a new faiss index
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# load BERT model
model = SentenceTransformer('msmarco-distilbert-base-dot-prod-v3') # bert-base-nli-mean-tokens

googlePlaces_index = faiss.IndexFlatL2(768)

# embed and add each descriptor from the holiday data
for place in googPlacesHoliday:
    # embed text
    embedding = model.encode(place.name)
    # add vector to faiss
    googlePlaces_index.add(np.array([embedding]))

googPlaces = {'index': googlePlaces_index, 'places': googPlacesHoliday}
pkl.dump(googPlaces, open("googPlacesHoliday.pkl", "wb"))