from vncorenlp import VnCoreNLP
# import change_in_out
# import combine
# import increase_decrease
# import train_model as model
import predict
# import data.create_data as create_data
# import fasttext as ft
# import pickle


if __name__ == '__main__':
    annotator = VnCoreNLP("VnCoreNLP\VnCoreNLP-1.1.1.jar", annotators="wseg, pos", max_heap_size='-Xmx2g')

    # text = 'Jack có 15 trái bóng tròn màu xanh vào ngày hôm qua. Kelly có 5 trái bóng tròn màu xanh. Vậy Jack và Kelly có bao nhiêu trái bóng?'
    # text = 'Cậu bé có 5 bó củi. Cậu bé bị mất 2 bó củi nữa. Hỏi cậu bé có bao nhiêu bó củi?'
    # text = 'Hiếu sở hữu 6 quả chuối. Vy sở hữu 71 quả chuối. Hiếu giữ 24 quả chuối từ Vy. Hỏi Hiếu và Vy có bao nhiêu quả chuối?'
    # math_type = 'change_in'

    # if math_type == 'change_out' or math_type == 'change_in':
    #     change_in_out.solve_math_problem(annotator, text, math_type)
    # elif math_type == 'combine':
    #     combine.solve_math_problem(annotator, text, math_type)
    # elif math_type == 'increase' or math_type == 'decrease':
    #     increase_decrease.solve_math_problem(annotator, text, math_type)
    
    text = 'Xuân cầm 7 mô hình. Thầy cầm 60 mô hình. Hỏi Xuân và Thầy có tổng cộng bao nhiêu mô hình?'
    predict.predict_math_type(annotator, text)
    # model.dump_file(annotator)
    # model.train_and_test()
    # X_data = pickle.load(open('data/X_test.pkl', 'rb'))
    # X_test = pickle.load(open('data/X_test.pkl', 'rb'))
    # ft.fstxt(annotator, X_data, X_test)
    annotator.close()

    # create_data.out_data()
