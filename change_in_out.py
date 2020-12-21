import vietnamese_nlp as vnlp
import get_position_function as func
import pandas as pd

def get_pos_df(df_final, df_pos):
    df_final, df_pos = func.is_question(df_final, df_pos)
    df_final, df_pos, owner_set = func.find_owner_1(df_final, df_pos)
    df_final, df_pos = func.find_owner_2(df_final, df_pos, owner_set)
    df_final, df_pos = func.find_verb(df_final, df_pos)
    df_final, df_pos = func.find_object(df_final, df_pos)
    df_final, df_pos = func.find_quantity(df_final, df_pos)
    return df_final, df_pos

def solve_math_problem(annotator, text, math_type):
    answer = ''
    de_bai = '<b>Đề bài: </b>' + text + '<br> <br>'

    match = ""
    if (math_type == 'change_in'):
        change_in_1 = '<b> Cách giải</b> <br> Đây là dạng toán A nhận từ B. Cách giải như sau: <br>'
        change_in_2 = """- A có 'x' đồ vật. B có 'y' đồ vật. A nhận từ B 'z' đồ vật. <br>"""
        change_in_3 = "- Vậy: A có số đồ vật = <b>x + z</b> <br>"
        change_in_4 = "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbspB có số đồ vật = <b>y - z</b> <br><br><br>"

        match = change_in_1 + change_in_2 + change_in_3 + change_in_4

    elif (math_type == 'change_out'):
        change_out_1 = '<b> Cách giải</b> <br> Đây là dạng toán B nhận từ A. Cách giải như sau: <br>'
        change_out_2 = """- A có 'x' đồ vật. B có 'y' đồ vật. A cho B 'z' đồ vật.<br>"""
        change_out_3 = "- Vậy: A có số đồ vật = <b>x - z</b><br>"
        change_out_4 = "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbspB có số đồ vật = <b>y + z</b><br><br><br>"
        match = change_out_1 + change_out_2 + change_out_3 + change_out_4

    df_final = pd.DataFrame(columns=['sentence', 'owner_1', 'verb', 'owner_2', 'main_object', 'sub_object', 'quantity', 'is_question'])
    for i in text.split('. '):
        df_final = df_final.append({'sentence': i}, ignore_index=True)
        df_final[['owner_1', 'verb', 'owner_2', 'main_object', 'sub_object', 'is_question']] = df_final[['owner_1', 'verb', 'owner_2', 'main_object', 'sub_object', 'is_question']].fillna('').astype(str)

    for i in text.split('. '):
        df_pos = pd.DataFrame()
        df_pos = vnlp.postagging_for_text(annotator,text)

    df_final, df_pos = get_pos_df(df_final, df_pos)

    first_owner = df_final['owner_1'].iloc[0]
    second_owner = ''
    num_1 = df_final['quantity'].iloc[0]
    num_2 = 0

    answer_format = ''
    answer_1 = ''
    answer_2 = ''
    answer_3 = ''
    answer_4 = ''
    answer_5 = ''
    for i in range(len(df_final)):
        flag = df_final['is_question'].iloc[i]
        
        if flag == 'NO':            
            owner_1 = df_final['owner_1'].iloc[i]
            owner_2 = df_final['owner_2'].iloc[i]
            verb = df_final['verb'].iloc[i]
            main_obj = df_final['main_object'].iloc[i]
            sub_obj = df_final['sub_object'].iloc[i]
            quantity = df_final['quantity'].iloc[i]

            if owner_2 == '':
                answer_1 = str(first_owner) + ' ' + str(verb) + ': ' + str(num_1) + ' ' + str(main_obj) + ' ' + str(sub_obj) + '<br>'
                if owner_1 != first_owner:
                    second_owner = owner_1
                    num_2 = quantity
                    answer_2 = str(second_owner) + ' ' + str(verb) + ': ' + str(num_2) + ' ' + str(main_obj) + ' ' + str(sub_obj) + '<br>'

            else:
                answer_3 = str(first_owner) + ' ' + str(verb) + ' ' + str(owner_2) + ': ' + str(quantity) + ' ' + str(main_obj) + ' ' + str(sub_obj) + '<br>'
                if (math_type == 'change_in'):
                    if owner_1 == first_owner:
                        num_1 = num_1 + quantity
                        num_2 = num_2 - quantity
                    elif owner_1 == second_owner:
                        num_1 = num_2 + quantity
                        num_2 = num_1 - quantity
                elif (math_type == 'change_out'):
                    if owner_1 == first_owner:
                        num_1 = num_1 - quantity
                        num_2 = num_2 + quantity
                    elif owner_1 == second_owner:
                        num_1 = num_2 - quantity
                        num_2 = num_1 + quantity

        elif flag == 'YES':
            if owner_1 == first_owner:
                answer_4 = 'Số ' + str(main_obj) + ' ' + str(sub_obj) + ' mà ' + str(owner_1) + ' có: ' + str(num_1) + ' ' + str(main_obj) + ' ' + str(sub_obj) + '<br>'
                answer_5 = 'Số ' + str(main_obj) + ' ' + str(sub_obj) + ' mà ' + str(second_owner) + ' có: ' + str(num_2) + ' ' + str(main_obj) + ' ' + str(sub_obj) + '<br>'
                answer_format = answer_1 + answer_2 + answer_3 + answer_4 +answer_5
            elif owner_1 == second_owner:
                answer_1 = 'Số ' + str(main_obj) + ' ' + str(sub_obj) + ' mà ' + str(owner_2) + ' có: ' + str(num_1) + ' ' + str(main_obj) + ' ' + str(sub_obj) + '<br>'
                answer_2  ='Số ' + str(main_obj) + ' ' + str(sub_obj) + ' mà ' + str(first_owner) + ' có: ' + str(num_2) + ' ' + str(main_obj) + ' ' + str(sub_obj) + '<br>'
                answer_format = answer_1 + answer_2 + answer_3 + answer_4 +answer_5

        else:
            answer_format = 'Bài này khó quá, hiện tại mình chưa có đáp án. Mong bạn thông cảm.'

    answer = de_bai + match + answer_format
    return answer