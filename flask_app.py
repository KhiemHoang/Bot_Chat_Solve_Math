from flask import Flask, render_template, url_for, request
from vncorenlp import VnCoreNLP

import predict
import increase_decrease
import change_in_out
import combine

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
    user_input = request.form['user_input']
    bot_response = ''
    math_type = predict.predict_math_type(annotator,user_input)
    if (math_type == 'change_in' or math_type == 'change_out'):
        bot_response = change_in_out.solve_math_problem(annotator,user_input,math_type)
    elif (math_type == 'combine'):
        bot_response = combine.solve_math_problem(annotator,user_input,math_type)
    elif (math_type == 'increase' or math_type == 'decrease'):
        bot_response = increase_decrease.solve_math_problem(annotator,user_input,math_type)
    
    print("Friend: "+bot_response)
    return render_template('home.html',user_input=user_input,bot_response=bot_response)

if __name__ == '__main__':
	app.run(debug=True)
