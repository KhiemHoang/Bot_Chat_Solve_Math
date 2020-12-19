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
    print('Đề bài: ', text)
    print ('')
    if (math_type == 'change_in'):
        print ('Đây là dạng toán A nhận từ B. Cách giải như sau:')  
        print ("""- A có 'x' đồ vật. B có 'y' đồ vật. A nhận từ B 'z' đồ vật.""")
        print ("""- Vậy A có số đồ vật = x + z""")
        print ("""      B có số đồ vật = y - z""")
        print ('')
    elif (math_type == 'change_out'):
        print ('Đây là dạng toán B nhận từ A. Cách giải như sau:')
        print ("""A có 'x' đồ vật. B có 'y' đồ vật. A cho B 'z' đồ vật.""")
        print ("""Vậy A có số đồ vật = x - z""")
        print ("""    B có số đồ vật = y + z""")
        print ('')

    df_final = pd.DataFrame(columns=['sentence', 'owner_1', 'verb', 'owner_2', 'main_object', 'sub_object', 'quantity', 'is_question'])
    for i in text.split('. '):
        df_final = df_final.append({'sentence': i}, ignore_index=True)
        df_final[['owner_1', 'verb', 'owner_2', 'main_object', 'sub_object', 'is_question']] = df_final[['owner_1', 'verb', 'owner_2', 'main_object', 'sub_object', 'is_question']].fillna('').astype(str)

    for i in text.split('. '):
        df_pos = pd.DataFrame()
        df_pos = vnlp.postagging_for_text(annotator,text)

    df_final, df_pos = get_pos_df(df_final, df_pos)
    print (df_final)
    
    first_owner = df_final['owner_1'].iloc[0]
    second_owner = ''
    num_1 = df_final['quantity'].iloc[0]
    num_2 = 0

    for i in range(len(df_final)):
        owner_1 = df_final['owner_1'].iloc[i]
        owner_2 = df_final['owner_2'].iloc[i]
        verb = df_final['verb'].iloc[i]
        main_obj = df_final['main_object'].iloc[i]
        sub_obj = df_final['sub_object'].iloc[i]
        quantity = df_final['quantity'].iloc[i]
        flag = df_final['is_question'].iloc[i]
        
        if owner_2 == '' and flag == 'NO':
            print (owner_1, verb, ':', quantity, main_obj, sub_obj)
            if owner_1 != first_owner:
                second_owner = owner_1
                num_2 = quantity

        elif flag == 'NO':
            print (owner_1 , verb, owner_2, ':', quantity, main_obj, sub_obj)
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
                print ('Số', main_obj, sub_obj, 'mà', owner_1, 'hiện có:', num_1)
                print ('Số', main_obj, sub_obj, 'mà', second_owner, 'hiện có:', num_2)
            elif owner_1 == second_owner:
                print ('Số', main_obj, sub_obj, 'mà', owner_2, 'hiện có:', num_1)
                print ('Số', main_obj, sub_obj, 'mà', first_owner, 'hiện có:', num_2)

        else:
            print('Bài này khó quá, hiện tại mình chưa có đáp án. Mong bạn thông cảm.')