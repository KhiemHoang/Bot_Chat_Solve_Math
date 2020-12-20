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

def combine(annotator, text, math_type):
    answer = ''
    print('Đề bài: ', text)
    print ('')

    print ('Đây là dạng toán tổng của A và B. Cách giải như sau:')  
    print ("""- A có 'x' đồ vật. B có 'y' đồ vật.""")
    print ("""- Vậy A và B có số đồ vật = x + y""")
    print ('')

    df_final = pd.DataFrame(columns=['sentence', 'owner_1', 'verb', 'owner_2', 'main_object', 'sub_object', 'quantity', 'is_question'])
    for i in text.split('. '):
        df_final = df_final.append({'sentence': i}, ignore_index=True)
        df_final[['owner_1', 'verb', 'owner_2', 'main_object', 'sub_object', 'is_question']] = df_final[['owner_1', 'verb', 'owner_2', 'main_object', 'sub_object', 'is_question']].fillna('').astype(str)

    for i in text.split('. '):
        df_pos = pd.DataFrame()
        df_pos = vnlp.postagging_for_text(annotator,text)

    df_final, df_pos = get_pos_df(df_final, df_pos)
    # print (df_final)
    # print (df_pos)
    # print ('')

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

        if flag == 'NO':
            print (owner_1, verb, ':', quantity, main_obj, sub_obj)
            if owner_1 != first_owner:
                second_owner = owner_1
                num_2 = quantity
        
        elif flag == 'YES':
            answer = 'Tổng số' + str(main_obj) +' ' + str(sub_obj) + ' mà ' + str(first_owner) + ' và ' + str(second_owner) + ' có: ' + str(num_1 + num_2)
            # print ('Tổng số', main_obj, sub_obj, 'mà', first_owner, 'và', second_owner, 'có:', num_1 + num_2)

        else:
            answer = 'Bài này khó quá, hiện tại mình chưa có đáp án. Mong bạn thông cảm.'
            # print('Bài này khó quá, hiện tại mình chưa có đáp án. Mong bạn thông cảm.')
    return answer