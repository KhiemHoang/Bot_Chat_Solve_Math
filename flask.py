from flask import Flask, render_template, url_for, request
import pandas as pd
import pickle

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict_math_type(annotator, text):
    X_data = pickle.load(open('data/X_train.pkl', 'rb'))
    y_data = pickle.load(open('data/y_train.pkl', 'rb'))

    tfidf_vect = TfidfVectorizer(analyzer='word')
    tfidf_vect.fit(X_data)
    X_data_tfidf =  tfidf_vect.transform(X_data)

    svd = TruncatedSVD(n_components=70, random_state=42)
    svd.fit(X_data_tfidf)   
    X_data_tfidf_svd = svd.transform(X_data_tfidf)

    encoder = preprocessing.LabelEncoder()
    y_data_n = encoder.fit_transform(y_data)

    test_doc = vnlp.preprocessing_prediction(annotator, text)
    test_doc_tfidf = tfidf_vect.transform([text])    
    test_doc_svd = svd.transform(test_doc_tfidf)
    
    # print (y_data_n)
    new_model = models.load_model('MyModel.h5')
    arr = new_model.predict(test_doc_svd)
    arr = arr[0]
    result = np.where(arr == np.amax(arr))
    result = result[0]
    print (arr)
    print (result[0]) 



if __name__ == '__main__':
	app.run(debug=True)