from sklearn import model_selection, preprocessing, metrics, svm
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split

from keras import layers, models, optimizers
from keras.layers import *

import vietnamese_nlp as vnlp
import pickle
import pandas as pd

def dump_file(annotator):
    # get data for testing
    df_test = pd.DataFrame()
    df_test = pd.read_csv("data/test_data.csv")
    X_test, y_test = vnlp.pre_process_train_data(annotator, df_test)
    pickle.dump(X_test, open('data/X_test.pkl', 'wb'))
    pickle.dump(y_test, open('data/y_test.pkl', 'wb'))

    # get data for trainning
    df_train = pd.DataFrame()
    df_train = pd.read_csv("data/train_data.csv")
    X_train, y_train = vnlp.pre_process_train_data(annotator,df_train)
    pickle.dump(X_train, open('data/X_train.pkl', 'wb'))
    pickle.dump(y_train, open('data/y_train.pkl', 'wb'))

def load_train_file():
    #get data for training
    X_train = pickle.load(open('data/X_train.pkl', 'rb'))
    y_train = pickle.load(open('data/y_train.pkl', 'rb'))

    return X_train, y_train

def load_test_file():
    #get data for testing
    X_test = pickle.load(open('data/X_test.pkl', 'rb'))
    y_test = pickle.load(open('data/y_test.pkl', 'rb'))

    return X_test, y_test

def word_vertorize(X_data):
    tfidf_vect = TfidfVectorizer(analyzer='word')
    tfidf_vect.fit(X_data)

    X_data_tfidf =  tfidf_vect.transform(X_data)

    svd = TruncatedSVD(n_components=70, random_state=42)
    svd.fit(X_data_tfidf)

    X_data_tfidf_svd = svd.transform(X_data_tfidf)

    return X_data_tfidf_svd


#train model
def load_model(self):
    self.model = self.build_model((self.max_length, self.word_dim))
    self.model.load_weights(self.model_path)

def build_model(self, input_dim):
    model = Sequential()

    model.add(LSTM(64, return_sequences=True, input_shape=input_dim))
    model.add(Dropout(0.2))
    model.add(LSTM(32))
    model.add(Dense(self.n_class, activation="softmax"))

    model.compile(loss=keras.losses.categorical_crossentropy,
                optimizer=keras.optimizers.Adadelta(),
                metrics=['accuracy'])
    return model

def train(self, X, y):
    self.model = self.build_model(input_dim=(X.shape[1], X.shape[2]))
    self.model.fit(X, y, batch_size=self.batch_size, epochs=self.n_epochs)
    self.model.save_weights(self.model_path)

def predict(self, X):
    if self.model is None:
        self.load_model()
    y = self.model.predict(X)
    return y

def train_and_test(annotator):
    X_train, y_train = load_train_file()
    X_test, y_test = load_test_file()

    encoder = preprocessing.LabelEncoder()
    y_data_n = encoder.fit_transform(y_train)
    y_test_n = encoder.fit_transform(y_test)

    classifier = create_lstm_model()
    X_data_tfidf_svd = word_vertorize(X_train)
    X_test_tfidf_svd = word_vertorize(X_test)
    train_model(classifier, X_data=X_data_tfidf_svd, y_data=y_data_n, X_test=X_test_tfidf_svd, y_test=y_test_n, is_neuralnet=True)

    # model.save('MyModel.h5')

    text = 'Chú có 1 quyển vở. Chú bị mất 1 quyển vở . Hỏi Chú còn bao nhiêu quyển vở?'

    tfidf_vect = TfidfVectorizer(analyzer='word')
    tfidf_vect.fit(X_train)
    X_data_tfidf =  tfidf_vect.transform(X_train)

    svd = TruncatedSVD(n_components=70, random_state=42)
    svd.fit(X_data_tfidf)   
    X_data_tfidf_svd = svd.transform(X_data_tfidf)

    encoder = preprocessing.LabelEncoder()
    y_data_n = encoder.fit_transform(y_train)

    test_doc = vnlp.preprocessing_prediction(annotator, text)
    test_doc_tfidf = tfidf_vect.transform([text])    
    test_doc_svd = svd.transform(test_doc_tfidf)
    
    print(classifier.predict(test_doc_svd))
