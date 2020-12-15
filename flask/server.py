from flask import Flask, render_template, request
from string import Template
from OpenSSL import SSL
import pickle
import requests
import json
import pandas as pd
import numpy as np

score_sample = {}
score_sample['hour'] = np.array([18])
score_sample['Route'] = np.array([0])
score_sample['daym'] = np.array([21])
score_sample['month'] = np.array([0])
score_sample['year'] = np.array([5])
score_sample['Direction'] = np.array([1])
score_sample['day'] = np.array([1])

# columns that are required for scoring
score_cols = ['Route','Direction','hour','year','month','daym','day']




app = Flask(__name__)

HTML_TEMPLATE = Template("""
<h1>Hello ${file_name}!</h1>
<img src="https://image.tmdb.org/t/p/w342/${file_name}" alt="poster for ${file_name}">
""")



@app.route('/')
def home():   
    ''' render home page that is served at localhost and allows the user to enter details about their streetcar trip'''
    title_text = "Test title"
    title = {'titlename':title_text}
    return render_template('home.html',title=title)
 
    
@app.route('/show-prediction/')
def about():
    ''' get the scoring parameters entered in home.html, assemble them into a dataframe, run that dataframe through pipelines
        apply the trained model to the output of the pipeline, and display the interpreted score in show-prediction.html
    '''
    # the scoring parameters are sent to this page as parameters on the URL link from home.html
    # load the scoring parameter values into a dictionary indexed by the column names expected by the pipelines
    score_values_dict = {}
    score_values_dict['Route'] = request.args.get('route')
    score_values_dict['Direction'] = request.args.get('direction')
    score_values_dict['year'] = int(request.args.get('year'))
    score_values_dict['month'] = int(request.args.get('month'))
    score_values_dict['daym'] = int(request.args.get('daym'))
    score_values_dict['day'] = int(request.args.get('day'))
    score_values_dict['hour'] = int(request.args.get('hour'))
    # echo the parameter values
    for value in score_values_dict:
        logging.warning("value for "+value+" is: "+str(score_values_dict[value]))
    # load the trained model
    loaded_model = load_model(model_path)
    loaded_model._make_predict_function()
    logging.warning("DISPLAY PRED: model loaded")
    # load the pipelines
    pipeline1 = load(open(pipeline1_path, 'rb'))
    pipeline2 = load(open(pipeline2_path, 'rb'))
    logging.warning("DISPLAY PRED: pipelines loaded")
    # create and load scoring parameters dataframe (containing the scoring parameters)that will be fed into the pipelines
    score_df = pd.DataFrame(columns=score_cols)
    logging.warning("score_df before load is "+str(score_df))
    for col in score_cols:
        score_df.at[0,col] = score_values_dict[col]
    # apply the pipelines to the scoring parameters dataframe
    prepped_xform1 = pipeline1.transform(score_df)
    prepped_xform2 = pipeline2.transform(prepped_xform1)
    logging.warning("prepped_xform2 is ",prepped_xform2)
    # apply the trained model to the output of the pipelines to get a score
    pred = loaded_model.predict(prepped_xform2, batch_size=BATCH_SIZE)
    logging.warning("pred is "+str(pred))
    # get a result string from the value of the score
    if pred[0][0] >= 0.5:
        predict_string = "yes, delay predicted"
    else:
        predict_string = "no delay predicted"
    prediction = {'prediction_key':predict_string}
    # render the page that will show the prediction
    return(render_template('show-prediction.html',prediction=prediction))
 



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    