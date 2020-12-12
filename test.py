from sklearn import model_selection, preprocessing, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import decomposition, ensemble
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import train_test_split

import pandas as pd
from keras.preprocessing import text, sequence
from keras import layers, models, optimizers
from keras.layers import *

from vncorenlp import VnCoreNLP
import numpy as np
import gensim
import pickle
import regex as re
import chuanhoa_tiengviet as chuanhoa

#For NLP
uniChars = "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴÂĂĐÔƠƯ"
unsignChars = "aaaaaaaaaaaaaaaaaeeeeeeeeeeediiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAAEEEEEEEEEEEDIIIOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYAADOOU"

def loaddicchar():
    dic = {}
    char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
        '|')
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        '|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic

def covert_unicode(txt):  
    dicchar = loaddicchar()
    return re.sub(
        r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
        lambda x: dicchar[x.group()], txt)

def pre_process_train_data(df):
    with VnCoreNLP(address="http://127.0.0.1", port=9000) as vncorenlp:
        X = []
        y = []

        for text in df['problem']:
            text = covert_unicode(text)
            #text = chuanhoa.chuan_hoa_dau_cau_tieng_viet(text)
            text = gensim.utils.simple_preprocess(text)
            text = [' '.join(text)]

            #code to understand
            str = ""    
            for s in text:
                s1 = vncorenlp.tokenize(s)
                str = str + " " + s1
            X.append(str.strip())

        for text in df['problem_type']:
            y.append(text)

        print('Done NLP')
        return X, y


def preprocessing_doc(text):
    with VnCoreNLP(address="http://127.0.0.1", port=9000) as vncorenlp:
        X = []
        text = covert_unicode(text)
        #texts = [[word.lower() for word in line.split()] for line in doc]
        text = gensim.utils.simple_preprocess(text)
        text = [' '.join(text)]

        str = "" 
        for s in text:
            s1 = vncorenlp.tokenize(s)
            str = str + " " + s1
        X.append(str.strip())

    return X

#TF-IDF SVD
def tf_idf(X_train, X_test):
    tfidf_vect = TfidfVectorizer(analyzer='word')
    tfidf_vect.fit(X_train)
    tfidf_vect.fit(X_test)

    X_data_tfidf =  tfidf_vect.transform(X_train)
    X_test_tfidf =  tfidf_vect.transform(X_test)

    svd = TruncatedSVD(n_components=100, random_state=42)
    svd.fit(X_data_tfidf)
    svd.fit(X_test_tfidf)

    X_data_tfidf_svd = svd.transform(X_data_tfidf)
    X_test_tfidf_svd = svd.transform(X_test_tfidf)

    return X_data_tfidf_svd, X_test_tfidf_svd

def tf_idf_test_only(X_train):
    tfidf_vect = TfidfVectorizer(analyzer='word')
    tfidf_vect.fit(X_train)

    X_data_tfidf =  tfidf_vect.transform(X_train)

    svd = TruncatedSVD(n_components=10, random_state=42)
    svd.fit(X_data_tfidf)

    X_data_tfidf_svd = svd.transform(X_data_tfidf)

    return X_data_tfidf_svd

def count_vect(X_train, X_test):
    count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
    count_vect.fit(X_train)
    count_vect.fit(X_test)
    X_data_count = count_vect.transform(X_train)
    X_test_count = count_vect.transform(X_test)

    return X_data_count, X_test_count


#training model
#LSTM
def create_lstm_model():
    input_layer = Input(shape=(100,))
    
    layer = Reshape((10, 10))(input_layer)
    layer = LSTM(128, activation='relu')(layer)
    layer = Dense(512, activation='relu')(layer)
    layer = Dense(512, activation='relu')(layer)
    layer = Dense(128, activation='relu')(layer)
    
    output_layer = Dense(10, activation='softmax')(layer)
    
    classifier = models.Model(input_layer, output_layer)
    
    classifier.compile(optimizer=optimizers.Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    return classifier


#train model
def train_model(classifier, X_data, y_data, X_test, y_test, is_neuralnet=False, n_epochs=3):       
    X_train, X_val, y_train, y_val = train_test_split(X_data, y_data, test_size=0.1, random_state=42)
    
    if is_neuralnet:
        classifier.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=n_epochs, batch_size=512)
        
        val_predictions = classifier.predict(X_val)
        test_predictions = classifier.predict(X_test)
        val_predictions = val_predictions.argmax(axis=-1)
        test_predictions = test_predictions.argmax(axis=-1)
    else:
        classifier.fit(X_train, y_train)
    
        train_predictions = classifier.predict(X_train)
        val_predictions = classifier.predict(X_val)
        test_predictions = classifier.predict(X_test)
        
    print("Validation accuracy: ", metrics.accuracy_score(val_predictions, y_val))
    print("Test accuracy: ", metrics.accuracy_score(test_predictions, y_test))



if __name__ == "__main__":
    print('Load data for NLP test')
    #get data for testing
    #df_test = pd.DataFrame()
    #df_test = pd.read_csv("data/test_data.csv")
    #X_test, y_test = pre_process_train_data(df_test)
    #pickle.dump(X_test, open('data/X_test.pkl', 'wb'))
    #pickle.dump(y_test, open('data/y_test.pkl', 'wb'))


    print('Load data for NLP train')
    #get data for trainning
    #df_train = pd.DataFrame()
    #df_train = pd.read_csv("data/train_data.csv")
    #X_train, y_train = pre_process_train_data(df_train)
    #pickle.dump(X_train, open('data/X_train.pkl', 'wb'))
    #pickle.dump(y_train, open('data/y_train.pkl', 'wb'))
    
    print('Done data for NLP')

    print('Load data for train')
    #get data for training
    X_train = pickle.load(open('data/X_train.pkl', 'rb'))
    y_train = pickle.load(open('data/y_train.pkl', 'rb'))

    #get data for testing
    X_test = pickle.load(open('data/X_test.pkl', 'rb'))
    y_test = pickle.load(open('data/y_test.pkl', 'rb'))
    print('Done data for train')

    print('training')
    #transform label
    encoder = preprocessing.LabelEncoder()
    y_data_n = encoder.fit_transform(y_train)
    y_test_n = encoder.fit_transform(y_test)
    print(encoder.classes_)
    
    #training
    classifier = create_lstm_model()
    X_data_tfidf_svd, X_test_tfidf_svd = tf_idf(X_train, X_test)
    train_model(classifier=classifier, X_data=X_data_tfidf_svd, y_data=y_data_n, X_test=X_test_tfidf_svd, y_test=y_test_n, is_neuralnet=True, n_epochs=10) 

    #Test prediction
    test_doc = 'Ngạn có 5 cái kẹp tóc. Ngạn cho Hà Lan 2 cái kẹp tóc. Hỏi Ngạn còn lại bao nhiêu cái kẹp tóc?'
    test_doc = preprocessing_doc(test_doc)
    print(test_doc)


    #X_data = pickle.load(open('data/X_train.pkl', 'rb'))
    #y_data = pickle.load(open('data/y_train.pkl', 'rb'))

    test_doc_tfidf = tf_idf_test_only(test_doc)
    print(np.shape(test_doc_tfidf))

    classifier.predict(test_doc_tfidf)
