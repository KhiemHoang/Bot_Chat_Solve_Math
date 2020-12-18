from flask import Flask, render_template, url_for, request
import pandas as pd
import pickle
from vncorenlp import VnCoreNLP
import change_in_out
import combine
import increase_decrease
import train_model as model
import predict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn import preprocessing
import vietnamese_nlp as vnlp
import train_model as model
from tensorflow.python.keras import models
import numpy as np

app = Flask(__name__)


annotator = VnCoreNLP("VnCoreNLP\VnCoreNLP-1.1.1.jar", annotators="wseg, pos", max_heap_size='-Xmx2g')

@app.route('/')
def home():
	return render_template('home.html')

# @app.route("/get")
# #function for the bot response
# def get_bot_response():
#     userText = request.args.get('msg')
#     return str(englishBot.get_response(userText))

@app.route('/predict_math_type',methods=['POST'])
def predict_math_type():
    X_data = pickle.load(open('data/X_train.pkl', 'rb'))
    y_data = pickle.load(open('data/y_train.pkl', 'rb'))

    tfidf_vect = TfidfVectorizer(analyzer='word')
    tfidf_vect.fit(X_data)
    X_data_tfidf =  tfidf_vect.transform(X_data)

    svd = TruncatedSVD(n_components=80, random_state=42)
    svd.fit(X_data_tfidf)   
    X_data_tfidf_svd = svd.transform(X_data_tfidf)

    encoder = preprocessing.LabelEncoder()
    y_data_n = encoder.fit_transform(y_data)

    text = request.args.get('msg')

    test_doc = vnlp.preprocessing_prediction(annotator, text)
    test_doc_tfidf = tfidf_vect.transform([text])    
    test_doc_svd = svd.transform(test_doc_tfidf)
    
    # print (y_data_n)
    new_model = models.load_model('MyModel_v2.h5')
    arr = new_model.predict(test_doc_svd)
    arr = arr[0]
    result = np.where(arr == np.amax(arr))
    my_prediction = result[0]
    annotator.close()
    return render_template('result.html',prediction = my_prediction)



if __name__ == '__main__':
	app.run(debug=True)
