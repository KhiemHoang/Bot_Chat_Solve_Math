# from vncorenlp import VnCoreNLP
# import change_in_out
# import combine
# import increase_decrease
import train_model as model
# import predict
# import data.create_data as create_data
# import fasttext as ft
# import pickle


if __name__ == '__main__':
    # annotator = VnCoreNLP("VnCoreNLP\VnCoreNLP-1.1.1.jar", annotators="wseg, pos", max_heap_size='-Xmx2g')

    # text = 'Jack có 15 trái bóng tròn màu xanh vào ngày hôm qua. Kelly có 5 trái bóng tròn màu xanh. Vậy Jack và Kelly có bao nhiêu trái bóng?'
    # text = 'Cậu bé có 5 bó củi. Cậu bé bị mất 2 bó củi nữa. Hỏi cậu bé có bao nhiêu bó củi?'
    # text = 'Jack có 15 trái bóng tròn màu xanh vào ngày hôm qua. Kelly có 5 trái bóng tròn màu xanh. Jack cho Kelly 6 trái. Vậy Jack có bao nhiêu trái bóng?'
    # math_type = 'decrease'

    # # print ('done')

    # if math_type == 'change_out' or math_type == 'change_in':
    #     change_in_out.solve_math_problem(annotator, text, math_type)
    # elif math_type == 'combine':
    #     combine.solve_math_problem(annotator, text, math_type)
    # elif math_type == 'increase' or math_type == 'decrease':
    #     increase_decrease.solve_math_problem(annotator, text, math_type)
    
    # text = 'Khiêm có 3 cây viết. An có 5 cây viết. Khiêm cho An 2 cây. Hỏi Khiêm còn mấy cây?'
    # predict.predict_math_type(annotator, text)
    # model.dump_file(annotator)
    model.train_and_test()
    # X_data = pickle.load(open('data/X_test.pkl', 'rb'))
    # X_test = pickle.load(open('data/X_test.pkl', 'rb'))
    # ft.fstxt(annotator, X_data, X_test)
    # annotator.close()

    # create_data.out_data()
