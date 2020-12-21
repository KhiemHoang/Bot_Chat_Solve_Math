import pandas as pd
import matplotlib.pyplot as plt


def draw_label():
    df = pd.DataFrame()
    df = pd.read_csv("data/train_data.csv")

    change_in = len(df[df['problem_type'] == 'change_in'])
    change_out = len(df[df['problem_type'] == 'change_out'])
    combine = len(df[df['problem_type'] == 'combine'])
    increase = len(df[df['problem_type'] == 'increase'])
    decrease = len(df[df['problem_type'] == 'decrease'])

    data_list = [['change_in', change_in], ['change_out', change_out], ['combine', combine], ['increase', increase], ['decrease', decrease]] 
    
    data = pd.DataFrame(data_list, columns = ['labels', 'quantity']) 

    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(data.labels, data.quantity)
    plt.show()