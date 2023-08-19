# convert pdf files to txt
import os
import subprocess

outdir = "files/"
for filename in os.listdir(outdir):
    if filename.endswith(".pdf"):
        subprocess.call(["pdftotext", outdir+filename])
        continue
    else:
        continue

# loop through txt files, embed with BERT, add vector to faiss
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# load BERT model
model = SentenceTransformer('msmarco-distilbert-base-dot-prod-v3') # bert-base-nli-mean-tokens

# load faiss index
index = faiss.read_index("faiss.index")

# loop through txt files
outdir = "files/"
for filename in os.listdir(outdir):
    if filename.endswith(".txt"):
        # get text
        with open(outdir+filename, 'r') as f:
            text = f.read()
        # embed text
        embedding = model.encode(text)
        # add vector to faiss
        index.add(np.array([embedding]))
        continue

