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
    print('Đề bài: ', text)
    print ('')

    if (math_type == 'increase'):
        print ('Đây là dạng toán tăng số lượng. Cách giải như sau:')  
        print ("""- A có 'x' đồ vật. A có thêm 'y' đồ vật.""")
        print ("""- Vậy A có số đồ vật = x + y""")
        print ('')
    elif (math_type == 'decrease'):
        print ('Đây là dạng toán giảm số lượng. Cách giải như sau:')  
        print ("""- A có 'x' đồ vật. A có thêm 'y' đồ vật.""")
        print ("""- Vậy A có số đồ vật = x - y""")
        print ('')

    df_final = pd.DataFrame(columns=['sentence', 'owner_1', 'verb', 'main_object', 'sub_object', 'quantity', 'is_question'])
    for i in text.split('. '):
        df_final = df_final.append({'sentence': i}, ignore_index=True)
        df_final[['owner_1', 'verb', 'main_object', 'sub_object', 'is_question']] = df_final[['owner_1', 'verb', 'main_object', 'sub_object', 'is_question']].fillna('').astype(str)

    for i in text.split('. '):
        df_pos = pd.DataFrame()
        df_pos = vnlp.postagging_for_text(annotator,text)

    print (df_pos)
    df_final, df_pos = get_pos_df(df_final, df_pos)
    print (df_final)
    print ('')

    num_1 = df_final['quantity'].iloc[0]
    num_2 = 0
    for i in range(len(df_final)):
        owner_1 = df_final['owner_1'].iloc[i]
        verb = df_final['verb'].iloc[i]
        main_obj = df_final['main_object'].iloc[i]
        sub_obj = df_final['sub_object'].iloc[i]
        quantity = df_final['quantity'].iloc[i]
        flag = df_final['is_question'].iloc[i]

        if flag == 'NO':
            print (owner_1, verb, ':', quantity, main_obj, sub_obj)
            if num_1 != quantity:
                num_2 = quantity
        
        elif flag == 'YES':
            if math_type == 'increase':
                print ('Số', main_obj, sub_obj, 'mà', owner_1, 'có:', num_1 + num_2, main_obj )
            elif math_type == 'decrease':
                print ('Số', main_obj, sub_obj, 'mà', owner_1, 'còn:', num_1 - num_2, main_obj)

        else:
            print('Bài này khó quá, hiện tại mình chưa có đáp án. Mong bạn thông cảm.')