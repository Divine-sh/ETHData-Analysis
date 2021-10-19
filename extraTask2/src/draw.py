import pandas as pd
import matplotlib.pyplot as plt


# 参数依次为list,抬头,X轴标签,Y轴标签,XY轴的范围
def draw_hist(myList, Title, Xlabel, Ylabel, Xmin, Xmax, Ymin, Ymax):
    plt.hist(myList, 100)
    plt.xlabel(Xlabel)
    plt.xlim(Xmin, Xmax)
    plt.ylabel(Ylabel)
    plt.ylim(Ymin, Ymax)
    plt.title(Title)
    plt.show()


if __name__ == '__main__':
    data = pd.read_csv('../output/output_2021_10_12.csv')
    print(data['fb_lastBuddle_quantile'])
    quantile_list = []
    z_num = 0
    for v in data['fb_lastBuddle_quantile']:
        print(float(v.strip('%')))
        x = float(v.strip('%'))
        quantile_list.append(x)
        if -0.0001 < x < 0.0001:
            z_num = z_num + 1
    print(z_num)

    draw_hist(quantile_list, 'quantile-num', 'quantile', 'num', 0, 100, 0, 20)