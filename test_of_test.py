from pyvi import ViTokenizer, ViPosTagger
import gensim

def get_data(df_model):
    X = []
    y = []
    for text in df_model['problem'].head(2):
        lines = text
        lines = gensim.utils.simple_preprocess(lines)
        lines = ' '.join(lines)
        lines = ViTokenizer.tokenize(lines)
        print (lines)

        X.append(lines)
    for text in df_model['problem_type']:
        y.append(text)

    #print(X)
    print(y)
    # return X, y