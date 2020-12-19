from flask import Flask, render_template, url_for, request
import pandas as pd
import pickle
from vncorenlp import VnCoreNLP
# import solve_math
import train_model as model
import predict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn import preprocessing
import vietnamese_nlp as vnlp
import train_model as model
from tensorflow.python.keras import models
import numpy as np

import increase_decrease

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

# @app.route('/get',methods=['POST'])
# def get_bot_response():
#     userText = request.args.get('msg')
#     return str(predict.predict_math_type(userText))

@app.route('/process',methods=['POST'])
def process():
<<<<<<< Updated upstream
    annotator = VnCoreNLP("VnCoreNLP\VnCoreNLP-1.1.1.jar", annotators="wseg, pos", max_heap_size='-Xmx2g')
    user_input = request.form['user_input']

    math_type = predict.predict_math_type(annotator,user_input)
    
    bot_response = str(bot_response)


    print("Friend: "+bot_response)
    return render_template('home.html',user_input=user_input,bot_response=bot_response)
    
=======
    user_input = request.form['user_input']
    bot_response = ''
    math_type = predict.predict_math_type(annotator,user_input)
    # if (math_type == 'change_in' or math_type == 'change_out'):
    #     bot_response = solve_math.change_in_out(annotator,user_input,math_type)
    # elif (math_type == 'combine'):
    #     bot_response = solve_math.combine(annotator,user_input,math_type)
    if (math_type == 'increase' or math_type == 'decrease'):
        bot_response = increase_decrease.solve_math_problem(annotator,user_input,math_type)
    # bot_response = 
    print("Friend: "+bot_response)
    return render_template('home.html',user_input=user_input,bot_response=bot_response)
    
>>>>>>> Stashed changes

if __name__ == '__main__':
	app.run(debug=True)
