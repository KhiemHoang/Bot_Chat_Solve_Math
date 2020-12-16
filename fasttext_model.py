import regex as re
from keras.preprocessing.text import Tokenizer
import gensim
import numpy as np
from gensim.models.fasttext import FastText
import pandas as pd
from string import punctuation
from vietnamese_standardized import text_preprocess

def fstxt(annotator, data, text):
    corpus = []
    for i in data:
        corpus.append(str(i).split(" "))
    corpus[:1]

    model = FastText(corpus, size=100, workers=4, window=5)

    print(model[text])

