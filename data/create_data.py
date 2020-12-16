# import pandas as pd
# import numpy as np
# import random
# pd.set_option('display.max_colwidth', None)
# df_data = pd.DataFrame(columns=['problem', 'problem_type'])
# sentence_1 = ''
# sentence_2 = ''
# sentence_3 = ''
# sentence_4 = ''

# #subject list
# owner_1st = ['Hà','Lan','An','Vy','Xuân','Phụng','Nga','Bố','Con','Mẹ','Chị','Anh','Tôi','Bạn','Long','Tuấn','Trung','Thầy','Vũ','Hiếu','Quân']

# owner_2nd = ['Anh','Hằng','Linh','Đức','Huy','Lý','Lành','Phương','Cậu','Mình','Tớ','Cường','Trâm','Trúc','Mai','Long', 'Cô']

# #object list
# object_1st = ['cái kẹo','quả táo','quả cam','quả lê','quả chuối','quả mận',
#                     'cây viết','quyển sách','viên bi','quả táo','quyển truyện',
#                     'trái bóng','cái bánh', 'cây gậy', 'cây thước', 'hộp kẹo',
#                     'cái vòng', 'cái khẩu trang', 'quả bóng xanh', 'cái xe đỏ',
#                     'hộp bút vàng', 'cái quần trắng', 'cuốn sách hay', 'cái gối ôm',
#                     'dây tai nghe', 'cái bàn phím', 'cái lắc tay', 'chiếc khăn phiêu']

# object_2nd = ['cái lồng đèn', 'mô hình', 'cái khẩu trang', 'cái áo đen', 'lon bia',
#                     'lon nước ngọt', 'hạt ngọc', 'cái mắt kính', 'cái hộp gỗ', 
#                     'cây đèn cầy', 'cái chong chóng', 'khúc gỗ', 'hạt đậu đỏ',
#                     'trái bắp ngô', 'quả tên lửa']

# #action_list
# general_action_list = ['có', 'sở hữu', 'cầm', 'giữ', 'nắm', 'cầm']

# #case_list
# case_list = ['change_in','change_out','increase','decrease','combine']

# #keyword_list
# change_in_list = ['nhận','mua','mượn', 'nhận', 'lấy', 'nhặt', 'cầm', 'giữ']
# change_out_list = ['đưa','bán','phân phát','tặng', 'gửi','ném', 'hiến']
# increase_list = ['mua thêm','tìm thấy','tìm được','có thêm','nhận thêm','nhặt được', 'mang thêm']
# decrease_list = ['bị mất','ăn mất','sử dụng','bỏ đi','đặt xuống', 'bỏ ra', 'bán đi', 'gửi đi', 'ném đi']
# combine_list = ['cùng nhau','tổng cộng', 'tất cả']


# #create change_in type
# def change_in(first_subject,second_subject,object_subject,general_action,keyword):
    
#     first_number = random.randint(1,100)
#     second_number = random.randint(1,100)
#     third_number = random.randint(1,100)
#     order_2 = random.randint(1,2)
    
#     sentence_1 = first_subject + ' ' + general_action + ' %s '%(first_number) + object_subject + '. '
#     sentence_2 = second_subject + ' ' + general_action + ' %s '%(second_number) + object_subject + '. ' 
#     sentence_3 = first_subject + ' ' + keyword + ' %s '%(third_number) + object_subject + ' từ ' + second_subject
#     if order_2 == 1:
#         sentence_4 = '. Hỏi ' + first_subject + ' và ' + second_subject + ' có bao nhiêu ' + object_subject + '?'
#     elif order_2 == 2:
#         sentence_4 = '. Hỏi ' + second_subject + ' và ' + first_subject + ' có bao nhiêu ' + object_subject + '?'

#     problem = sentence_1 + sentence_2 + sentence_3 + sentence_4
#     return problem

# #create change_out type
# def change_out(first_subject,second_subject,object_subject,general_action,keyword):

#     first_number = random.randint(1,100)
#     second_number = random.randint(1,100)
#     third_number = random.randint(1,100)
#     while (third_number > first_number) or (third_number > second_number):
#         third_number = random.randint(1,100)
#     order_2 = random.randint(1,2)
    
#     sentence_1 = first_subject + ' ' + general_action + ' %s '%(first_number) + object_subject + '. '
#     sentence_2 = second_subject + ' ' + general_action + ' %s '%(second_number) + object_subject + '. ' 
#     sentence_3 = first_subject + ' ' + keyword + ' %s '%(third_number) + object_subject + ' cho ' + second_subject
#     if order_2 == 1:
#         sentence_4 = '. Hỏi ' + first_subject + ' và ' + second_subject + ' có bao nhiêu ' + object_subject + '?'
#     elif order_2 == 2:
#         sentence_4 = '. Hỏi ' + second_subject + ' và ' + first_subject + ' có bao nhiêu ' + object_subject + '?'

#     problem = sentence_1 + sentence_2 + sentence_3 + sentence_4
#     return problem

# #create increase type
# def increase(first_subject,second_subject,object_subject,general_action,keyword):
    
#     first_number = random.randint(1,100)
#     second_number = random.randint(1,100)
    
#     sentence_1 = first_subject + ' ' + general_action + ' %s '%(first_number) + object_subject + '. '
#     sentence_2 = first_subject + ' ' + keyword + ' %s '%(second_number) + object_subject + ' nữa. Hỏi '
#     sentence_3 = first_subject + ' có bao nhiêu ' + object_subject + '?'

#     problem = sentence_1 + sentence_2 + sentence_3
        
#     return problem

# #create decrease type
# def decrease(first_subject,second_subject,object_subject,general_action,keyword):
    
#     first_number = random.randint(1,100)
#     second_number = random.randint(1,first_number)
    
#     sentence_1 = first_subject + ' ' + general_action + ' %s '%(first_number) + object_subject + '. '
#     sentence_2 = first_subject + ' ' + keyword + ' %s '%(second_number) + object_subject + '. Hỏi '
#     sentence_3 = first_subject + ' còn bao nhiêu ' + object_subject + '?'

#     problem = sentence_1 + sentence_2 + sentence_3
       
#     return problem

# #create combine type
# def combine(first_subject,second_subject,object_subject,general_action,keyword_combine):
    
#     first_number = random.randint(1,100)
#     second_number = random.randint(1,100)
    
#     sentence_1 = first_subject + ' ' + general_action + ' %s '%(first_number) + object_subject + '. '
#     sentence_2 = second_subject + ' ' + general_action + ' %s '%(second_number) + object_subject + '. Hỏi '
#     sentence_3 = first_subject + ' và ' + second_subject + ' có ' + keyword_combine + ' bao nhiêu ' + object_subject + '?'

#     problem = sentence_1 + sentence_2 + sentence_3
       
#     return problem

# #def main():
# def out_data():
#     df_data = pd.DataFrame(columns=['problem', 'problem_type'])
#     for i in range (0, 2000):    
#         first_subject = random.choice(owner_2nd)
#         second_subject = random.choice(owner_2nd)
#         while(first_subject == second_subject):
#             second_subject = random.choice(owner_2nd)
        
#         object_subject = random.choice(object_2nd)
#         general_action = random.choice(general_action_list)
        
#         keyword_change_in = random.choice(change_in_list)
#         keyword_change_out = random.choice(change_out_list)
#         keyword_increase = random.choice(increase_list)
#         keyword_reduction = random.choice(decrease_list)
#         keyword_combine = random.choice(combine_list)
        
#         case = random.choice(case_list)

#         if(case == 'change_in'):
#             problem = change_in(first_subject,second_subject,object_subject,general_action,keyword_change_in)
#             df_data = df_data.append({'problem': problem, 'problem_type': 'change_in'}, ignore_index=True)
#         elif(case == 'change_out'):
#             problem = change_out(first_subject,second_subject,object_subject,general_action,keyword_change_out)
#             df_data = df_data.append({'problem': problem, 'problem_type': 'change_out'}, ignore_index=True)
#         elif(case == 'increase'):
#             problem = increase(first_subject,second_subject,object_subject,general_action,keyword_increase)
#             df_data = df_data.append({'problem': problem, 'problem_type': 'increase'}, ignore_index=True)
#         elif(case == 'decrease'):
#             problem = decrease(first_subject,second_subject,object_subject,general_action,keyword_reduction)
#             df_data = df_data.append({'problem': problem, 'problem_type': 'decrease'}, ignore_index=True)
#         elif(case == 'combine'):
#             problem = combine(first_subject,second_subject,object_subject,general_action,keyword_combine)
#             df_data = df_data.append({'problem': problem, 'problem_type': 'combine'}, ignore_index=True)     

#     df_data.to_csv('data/test_data.csv', index=False, encoding="utf-8-sig")
#     print('done')