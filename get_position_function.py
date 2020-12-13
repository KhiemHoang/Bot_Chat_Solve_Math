import pandas as pd
def find_owner_1(df_final, df_pos):
    owner_set = []
    for fin in range(len(df_final)):
        check_pos = 0
        for pos in range(len(df_pos)):
            if fin == pos:
                for col in range(len(df_pos.columns)):
                    word_tag = ['Np', 'N', 'P', 'Nc']
                    word = df_pos.loc[pos, '%s'%(col)]

                    if word[1] in word_tag and word != 'null value':
                        df_final.at[fin, 'owner_1'] = word[0]
                        owner_set.append('%s'%(word[0]))
                        df_pos.at[fin, '%s'%(col)] = 'null value'

                        while check_pos < (len(df_pos.columns) - col):
                            sub_owner = df_pos.loc[pos, '%s'%(col + check_pos)]
                            if sub_owner != 'null value' and sub_owner[1] in word_tag:
                                sub_str = df_final['owner_1'].iloc[pos] + ' ' + sub_owner[0]
                                df_final.at[pos, 'owner_1'] = sub_str
                                df_pos.at[pos, '%s'%(col + check_pos)] = 'null value'                            
                            elif sub_owner != 'null value' and sub_owner[1] not in word_tag:
                                break
                            check_pos = check_pos + 1
                        break
    return df_final, df_pos, owner_set

def find_owner_2(df_final, df_pos, owner_set):
    for fin in range(len(df_final)):
        for pos in range(len(df_pos)):
            if fin == pos:
                for col in range(len(df_pos.columns)):
                    word_tag = ['Np', 'N', 'P']
                    word = df_pos.loc[pos, '%s'%(col)]

                    if word != 'null value' and word[1] in word_tag and word[0] in owner_set:
                        df_final.at[fin, 'owner_2'] = word[0]
                        df_pos.at[fin, '%s'%(col)] = 'null value'
                        break
    return df_final, df_pos

def find_verb(df_final, df_pos):
    for fin in range(len(df_final)):
        for pos in range(len(df_pos)):
            if fin == pos:
                for col in range(len(df_pos.columns)):
                    word_tag = ['V', 'E', 'R']
                    word_flag = ['Hỏi', 'Tổng_cộng']
                    word = df_pos.loc[pos, '%s'%(col)]

                    if word != 'null value' and word[1] in word_tag and word[0] not in word_flag:
                        df_final.at[fin, 'verb'] = word[0]
                        df_pos.at[fin, '%s'%(col)] = 'null value'
                        sub_verb = df_pos.loc[pos, '%s'%(col + 1)]
                        while sub_verb != 'null value' and sub_verb[1] in word_tag:
                            sub_str = df_final['verb'].iloc[pos] + ' ' + sub_verb[0]
                            df_final.at[fin, 'verb'] = sub_str
                            df_pos.at[fin, '%s'%(col + 1)] = 'null value'
                            break
                        break
    return df_final, df_pos

def find_object(df_final, df_pos):
    for fin in range(len(df_final)):    
        check_pos = 0
        for pos in range(len(df_pos)):
            if fin == pos:
                for col in range(len(df_pos.columns)):
                    word_tag = ['Nc', 'N', 'Nu']
                    sub_word_tag = ['Nc', 'N', 'Nu', 'A']
                    word = df_pos.loc[pos, '%s'%(col)]

                    if word != 'null value' and word[1] in word_tag:
                        df_final.at[fin, 'main_object'] = word[0]
                        df_pos.at[fin, '%s'%(col)] = 'null value'

                        while check_pos < (len(df_pos.columns) - col):
                            sub_obj = df_pos.loc[pos, '%s'%(col + check_pos)]
                            if sub_obj != 'null value' and sub_obj[1] in sub_word_tag:
                                sub_str = df_final['sub_object'].iloc[pos] + ' ' + sub_obj[0]
                                df_final.at[fin, 'sub_object'] = sub_str
                                df_pos.at[pos, '%s'%(col + check_pos)] = 'null value'                            
                            elif sub_obj != 'null value' and sub_obj[1] not in sub_word_tag:
                                break
                            check_pos = check_pos + 1
                        break
    return df_final, df_pos

def find_quantity(df_final, df_pos):
    for fin in range(len(df_final)):
        for pos in range(len(df_pos)):
            if fin == pos:
                for col in range(len(df_pos.columns)):
                    word_tag = ['M']
                    word = df_pos.loc[pos, '%s'%(col)]

                    if word != 'null value' and word[1] in word_tag:
                        df_final.at[fin, 'quantity'] = int(word[0])
                        df_pos.at[fin, '%s'%(col)] = 'null value'
                        break
    return df_final, df_pos

def is_question(df_final, df_pos):
    for fin in range(len(df_final)):
        for pos in range(len(df_pos)):
            if fin == pos:
                for col in range(len(df_pos.columns)):
                    word_flag = ['Hỏi', 'Tổng_cộng', 'Vậy']
                    word = df_pos.loc[pos, '%s'%(col)]

                    if word != 'null value' and word[0] in word_flag:
                        df_final['is_question'] = 'NO'
                        df_final.at[fin, 'is_question'] = 'YES'
                        df_pos.at[fin, '%s'%(col)] = 'null value'
                        break
    return df_final, df_pos
