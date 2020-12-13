import vietnamese_nlp as vnlp
import test_of_test as test
import pickle
import pandas as pd

def dump_file(annotator):
    # get data for testing
    df_test = pd.DataFrame()
    df_test = pd.read_csv("data/test.csv")
    X_test, y_test = vnlp.pre_process_train_data(annotator, df_test)
    pickle.dump(X_test, open('data/X_test.pkl', 'wb'))
    pickle.dump(y_test, open('data/y_test.pkl', 'wb'))

    # get data for trainning
    df_train = pd.DataFrame()
    df_train = pd.read_csv("data/train_data.csv")
    X_train, y_train = pre_process_train_data(annotator,df_train)
    pickle.dump(X_train, open('data/X_train.pkl', 'wb'))
    pickle.dump(y_train, open('data/y_train.pkl', 'wb'))

    