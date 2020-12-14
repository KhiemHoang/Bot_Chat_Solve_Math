import regex as re
from keras.preprocessing.text import Tokenizer
import gensim
import numpy as np
from gensim.models.fasttext import FastText
import pandas as pd
from string import punctuation
from vietnamese_standardized import text_preprocess


test_data = open('E:/thesis/code/Bot_Chat_Solve_Math/test_data.txt', encoding="utf8")

data = test_data.read()
data_processed = text_preprocess(data)
# test_data.write(data_processed)
test_data.close()

print(data_processed)

corpus = []
for i in data_processed:
    corpus.append(str(i).split(" "))
corpus[:1]


model = FastText(corpus, size=100, workers=4, window=5)

print(np.shape(model['thầy giáo']))

