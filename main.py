from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import pymorphy2

app = FastAPI()
morph = pymorphy2.MorphAnalyzer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class WordRequest(BaseModel):
    word: str

class BatchRequest(BaseModel):
    words: List[str]

def get_lemma(word: str) -> str:
    parsed = morph.parse(word.lower().strip())
    return parsed[0].normal_form if parsed else word.lower().strip()

@app.get("/")
def root():
    return {"status": "ok", "service": "lemmatizer"}

@app.post("/lemmatize")
def lemmatize(req: WordRequest):
    lemma = get_lemma(req.word)
    return {"word": req.word, "lemma": lemma}

@app.post("/lemmatize/batch")
def lemmatize_batch(req: BatchRequest):
    results = [{"word": w, "lemma": get_lemma(w)} for w in req.words]
    return {"results": results}
