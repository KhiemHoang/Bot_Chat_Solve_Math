from vncorenlp import VnCoreNLP
import change_in_out
import combine
import increase_decrease


if __name__ == '__main__':
    annotator = VnCoreNLP("VnCoreNLP\VnCoreNLP-1.1.1.jar", annotators="wseg, pos", max_heap_size='-Xmx2g')
    print (annotator)
    #text = 'Jack có 15 trái bóng tròn màu xanh vào ngày hôm qua. Kelly có 5 trái bóng tròn màu xanh. Vậy Jack và Kelly có bao nhiêu trái bóng?'
    text = 'Cậu bé có 5 bó củi. Cậu bé bị mất 2 bó củi nữa. Hỏi cậu bé có bao nhiêu bó củi?'
    #text = 'Jack có 15 trái bóng tròn màu xanh vào ngày hôm qua. Kelly có 5 trái bóng tròn màu xanh. Jack cho Kelly 6 trái. Vậy Jack có bao nhiêu trái bóng?'
    math_type = 'decrease'

    if math_type == 'change_out' or math_type == 'change_in':
        change_in_out.solve_math_problem(annotator, text, math_type)
    elif math_type == 'combine':
        combine.solve_math_problem(annotator, text, math_type)
    elif math_type == 'increase' or math_type == 'decrease':
        increase_decrease.solve_math_problem(annotator, text, math_type)

    annotator.close()
