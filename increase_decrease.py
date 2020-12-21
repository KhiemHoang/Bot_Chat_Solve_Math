import vietnamese_nlp as vnlp
import get_position_function as func
import pandas as pd


def get_pos_df(df_final, df_pos):
    df_final, df_pos = func.is_question(df_final, df_pos)
    df_final, df_pos, owner_set = func.find_owner_1(df_final, df_pos)
    df_final, df_pos = func.find_verb(df_final, df_pos)
    df_final, df_pos = func.find_object(df_final, df_pos)
    df_final, df_pos = func.find_quantity(df_final, df_pos)
    return df_final, df_pos

def solve_math_problem(annotator, text, math_type):
    answer = ''
    de_bai = '<b>Đề bài: </b> ' + text + '<br><br>'

    match = ''
    if (math_type == 'increase'):
        match = """<b> Cách giải </b> <br> Đây là dạng toán tăng số lượng. Cách giải như sau: <br>
        - A có 'x' đồ vật. A có thêm 'y' đồ vật. <br>
        - Vậy A có số đồ vật = <b>x + y</b> <br><br>"""

    elif (math_type == 'decrease'):
        match = """<b> Cách giải </b> <br> Đây là dạng toán giảm số lượng. Cách giải như sau:' <br>
        - A có 'x' đồ vật. A mất đi 'y' đồ vật.
        - Vậy A có số đồ vật = <b>x - y</b> <br><br>"""

    df_final = pd.DataFrame(columns=['sentence', 'owner_1', 'verb', 'main_object', 'sub_object', 'quantity', 'is_question'])
    for i in text.split('. '):
        df_final = df_final.append({'sentence': i}, ignore_index=True)
        df_final[['owner_1', 'verb', 'main_object', 'sub_object', 'is_question']] = df_final[['owner_1', 'verb', 'main_object', 'sub_object', 'is_question']].fillna('').astype(str)

    for i in text.split('. '):
        df_pos = pd.DataFrame()
        df_pos = vnlp.postagging_for_text(annotator,text)

    # print (df_pos)
    df_final, df_pos = get_pos_df(df_final, df_pos)
    # print (df_final)
    # print ('')

    answer_format = ''
    answer_format_1 = ''
    answer_format_2 = ''
    answer_format_3 = ''

    owner_1 = df_final['owner_1'].iloc[0]
    num_1 = df_final['quantity'].iloc[0]
    main_verb = verb = df_final['verb'].iloc[0]
    num_2 = 0
    for i in range(len(df_final)):
        flag = df_final['is_question'].iloc[i]

        if flag == 'NO':
            verb = df_final['verb'].iloc[i]
            main_obj = df_final['main_object'].iloc[i]
            sub_obj = df_final['sub_object'].iloc[i]
            quantity = df_final['quantity'].iloc[i]
            
            if main_verb != verb:
                num_2 = quantity
                answer_format_2 = str(owner_1) + ' ' + str(verb) + ': ' + str(num_2) + ' ' + str(main_obj) + ' ' + str(sub_obj) + '<br>'
                if (math_type == 'decrease') and (num_2 > num_1):
                    answer_format = "Logic của bài toán sai rồi. Số lượng mất đi phải bé hơn số lượng ban đầu."
                    break  
            else:          
                answer_format_1 = str(owner_1) + ' ' + str(verb) + ': ' + str(num_1) + ' ' + str(main_obj) + ' ' + str(sub_obj) + '<br>'        

        elif flag == 'YES':
            if math_type == 'increase':
                answer_format_3 = 'Số ' + str(main_obj) + ' ' + str(sub_obj) + ' mà ' + str(owner_1) + ' có: ' + str(num_1 + num_2) + ' ' + str(main_obj)
                # print ('Số', main_obj, sub_obj, 'mà', owner_1, 'có:', num_1 + num_2, main_obj )
                answer_format = answer_format_1 + answer_format_2 + answer_format_3
            elif math_type == 'decrease':
                answer_format_3 = 'Số ' + str(main_obj) + ' ' + str(sub_obj) + ' mà ' + str(owner_1) + ' còn: ' + str(num_1 - num_2) + ' ' + str(main_obj)
                # print ('Số', main_obj, sub_obj, 'mà', owner_1, 'còn:', num_1 - num_2, main_obj)
                answer_format = answer_format_1 + answer_format_2 + answer_format_3

        else:
            answer = 'Bài này khó quá, hiện tại mình chưa có đáp án. Mong bạn thông cảm.'
            # print('Bài này khó quá, hiện tại mình chưa có đáp án. Mong bạn thông cảm.')

    print (answer_format_1, answer_format_2)
    answer = de_bai + match + answer_format
    return answer