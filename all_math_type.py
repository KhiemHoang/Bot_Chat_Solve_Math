import increase_decrease
import change_in_out
import combine
from vncorenlp import VnCoreNLP
import predict

annotator = VnCoreNLP("VnCoreNLP\VnCoreNLP-1.1.1.jar", annotators="wseg, pos", max_heap_size='-Xmx2g')

def get_answer(user_input):
    answer = ''
    math_type = predict.predict_math_type(annotator,user_input)

    if (math_type == 'change_in' or math_type == 'change_out'):
        answer = change_in_out.solve_math_problem(annotator,user_input,math_type)
    elif (math_type == 'combine'):
        answer = combine.solve_math_problem(annotator,user_input,math_type)
    elif (math_type == 'increase' or math_type == 'decrease'):
        answer = increase_decrease.solve_math_problem(annotator,user_input,math_type)
    return answer