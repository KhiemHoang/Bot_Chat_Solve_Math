from tensorflow.python.keras import models
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn import preprocessing
import pickle

import vietnamese_nlp as vnlp
import numpy as np
import pickle
import pandas as pd

import sys
np.set_printoptions(threshold=sys.maxsize)

def predict_math_type(annotator, text):
    X_data = pickle.load(open('data/X_test.pkl', 'rb'))
    y_data = pickle.load(open('data/y_test.pkl', 'rb'))

    tfidf_vect = TfidfVectorizer(analyzer='word')
    tfidf_vect.fit(X_data)
    X_data_tfidf =  tfidf_vect.transform(X_data)

    svd = TruncatedSVD(n_components=80, random_state=42)
    svd.fit(X_data_tfidf)   
    X_data_tfidf_svd = svd.transform(X_data_tfidf)
    # print (y_data[:100])

    encoder = preprocessing.LabelEncoder()
    y_data_n = encoder.fit_transform(y_data)
    # print (y_data_n[:100])

    test_doc = vnlp.preprocessing_prediction(annotator, text)
    test_doc_tfidf = tfidf_vect.transform([text])    
    test_doc_svd = svd.transform(test_doc_tfidf)
    
    # print (y_data_n)
    new_model = models.load_model('MyModel_v2.h5')
    arr = new_model.predict(test_doc_svd)
    arr = arr[0]
    result = np.where(arr == np.amax(arr))
    result = result[0]
    # print (arr)
    # print (result[0]) 
    return result[0]