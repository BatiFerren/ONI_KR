import matplotlib.markers
import matplotlib.pyplot as plt
import numpy as np
import math


def multiple_by_coef(point, coef):
    y = [round(item*coef, 2) for item in point['y']]
    x = [point['x'] for i in range(point['y'].__len__())]
    # out_pnt = {'x': x, 'y': sorted(y)}
    out_pnt = {'x': x, 'y': y}
    return out_pnt


def calculate_average_y(pnts):
    list_aver_y = []
    for item in pnts:
        list_aver_y.append(round(sum(item['y'])/item['y'].__len__(), 2))
    return list_aver_y


def calculate_aver_sqr_fail(pnts, list_averages_y):
    list_aver_sqr_fail = []
    i = 0
    for item in pnts:
        list_sqr_diff_aver_and_y = []
        for inner_item in item['y']:
            list_sqr_diff_aver_and_y.append(math.pow((list_averages_y[i]-inner_item), 2))
        i += 1
        list_aver_sqr_fail.append(round(sum(list_sqr_diff_aver_and_y)/((item['y'].__len__() - 1) if item['y'].__len__() > 1 else 1), 2))
    return list_aver_sqr_fail


def calculate_v(pnts, list_averages_y, list_aver_sqr_fails):
    i = 0
    for item in pnts:
        list_v = []
        for inner_item in item['y']:
            a = abs(inner_item - list_averages_y[i])
            b = math.sqrt(((item['y'].__len__() - 1)/item['y'].__len__())*list_aver_sqr_fails[i])
            list_v.append(round(a/b, 2) if b != 0 else 0)
            # list_v.append((abs(inner_item - list_averages_y[i]))/math.sqrt(((item['y'].__len__() - 1)/item['y'].__len__())*list_aver_sqr_fails[i]))
        i += 1
        item['v'] = list_v
    return pnts


def find_miss(pnts, vmax):
    for item in pnts:
        for i in range(item['x'].__len__()):
            if item['v'][i] > vmax:
                item['x'].pop(i)
                item['y'].pop(i)
                item['v'].pop(i)
    return pnts


def convert_to_log(pnts, averages_y):
    res = []
    for i in range(1, pnts.__len__()):
        res.append({'log_x': round(math.log10(pnts[i]['x'][0]), 3), 'log_y': round(math.log10(averages_y[i]), 3)})
    return res


def create_points_for_pow(pnts, a, k):
    res = []
    for i in range(1, pnts.__len__()):
        res.append({'x': pnts[i]['x'], 'y': round(a*math.pow(pnts[i]['x'], k), 2)})
    return res


def main():
    coef_A = 1.1
    alpha = 0.95
    v_max = 1.81
    pnt1 = {'x': 0, 'y': [0]}
    pnt2 = {'x': 10, 'y': [11.2, 13.0, 11.4, 9.8, 11.6]}
    pnt3 = {'x': 20, 'y': [14.3, 12.2, 14.4, 16.2, 14.8]}
    pnt4 = {'x': 30, 'y': [16.5, 15.2, 17.1, 16.6, 18.4]}
    pnt5 = {'x': 40, 'y': [18.2, 17.4, 16.0, 18.3, 20.5]}
    pnt6 = {'x': 50, 'y': [19.5, 20.1, 18.9, 19.4, 22.0]}
    pnt7 = {'x': 60, 'y': [20.9, 20.3, 18.5, 20.6, 22.8]}
    start_pnt = [pnt1, pnt2, pnt3, pnt4, pnt5, pnt6, pnt7]
    print('Start points: ', start_pnt)
    point1 = multiple_by_coef(pnt1, coef_A)
    point2 = multiple_by_coef(pnt2, coef_A)
    point3 = multiple_by_coef(pnt3, coef_A)
    point4 = multiple_by_coef(pnt4, coef_A)
    point5 = multiple_by_coef(pnt5, coef_A)
    point6 = multiple_by_coef(pnt6, coef_A)
    point7 = multiple_by_coef(pnt7, coef_A)
    points = [point1, point2, point3, point4, point5, point6, point7]
    print('Result points: ', points)
    averages_y = calculate_average_y(points)
    print('Averages y: ', averages_y)
    average_sqr_fails = calculate_aver_sqr_fail(points, averages_y)
    print('Delta S in square: ', average_sqr_fails)
    new_points = calculate_v(points, averages_y, average_sqr_fails)
    print('Points with v: ', new_points)
    points_without_miss = find_miss(new_points, v_max)
    print('Points without misses: ', points_without_miss)
    new_averages_y = calculate_average_y(points_without_miss)
    print('New averages y: ', new_averages_y)
    log_points = convert_to_log(points_without_miss, new_averages_y)
    print('Logarithm points: ', log_points)
    list_log_x = [item['log_x'] for item in log_points]
    print('List log_x: ', list_log_x)
    list_log_y = [item['log_y'] for item in log_points]
    print('List log_y: ', list_log_y)
    multiple_logX_logY = [round(list_log_x[i]*list_log_y[i], 3) for i in range(list_log_x.__len__())]
    print('X*Y: ', multiple_logX_logY)
    sqr_logX = [round(math.pow(list_log_x[i], 2), 3) for i in range(list_log_x.__len__())]
    print('Sqr_X: ', sqr_logX)
    print('Sum logX: ', round(sum(list_log_x), 3))
    print('Sum logY: ', round(sum(list_log_y), 3))
    print('Sum X*Y: ', round(sum(multiple_logX_logY), 3))
    print('Sum Sqr_X: ', round(sum(sqr_logX), 3))

    # TODO: Need to make calculating parameters A and k by matrix method
    par_A = 0.771
    par_k = 0.33

    a = round(math.pow(10, par_A), 3)
    print('Parameter a: ', a)
    math_curve = create_points_for_pow(start_pnt, a, par_k)
    print('Mathematical curve: ', math_curve)

    delta_S = [round(math.sqrt(item), 3) for item in average_sqr_fails]
    print('Delta S: ', delta_S)
    delta_S_series_30_40 = [round(delta_S[3]/math.sqrt(5), 3), round(delta_S[4]/math.sqrt(5), 3)]
    print('Delta S for series for points 30 and 40: ', delta_S_series_30_40)
    coef_stud = 2.78
    interval_pnt1 = {'x': [30, 30], 'y': [new_averages_y[3] - coef_stud*delta_S_series_30_40[0], new_averages_y[3] + coef_stud*delta_S_series_30_40[0]]}
    interval_pnt2 = {'x': [40, 40], 'y': [new_averages_y[4] - coef_stud * delta_S_series_30_40[1],
                                          new_averages_y[4] + coef_stud * delta_S_series_30_40[1]]}
    interval_points = [interval_pnt1, interval_pnt2]
    print(interval_points)
    epsilon_30 = (coef_stud*delta_S_series_30_40[0]/new_averages_y[3])*100
    epsilon_40 = (coef_stud * delta_S_series_30_40[1] / new_averages_y[4]) * 100
    epsilon = [round(epsilon_30, 2), round(epsilon_40, 2)]
    print('Epsilon: ', epsilon)



    x1 = np.array(point1['x'])
    y1 = np.array(point1['y'])
    x2 = np.array(point2['x'])
    y2 = np.array(point2['y'])
    x3 = np.array(point3['x'])
    y3 = np.array(point3['y'])
    x4 = np.array(point4['x'])
    y4 = np.array(point4['y'])
    x5 = np.array(point5['x'])
    y5 = np.array(point5['y'])
    x6 = np.array(point6['x'])
    y6 = np.array(point6['y'])
    x7 = np.array(point7['x'])
    y7 = np.array(point7['y'])
    aver_x = np.array([points[0]['x'][0], points[1]['x'][0], points[2]['x'][0], points[3]['x'][0], points[4]['x'][0], points[5]['x'][0], points[6]['x'][0]])
    # aver_y = np.array([points[0]['y'][0], points[1]['y'][2], points[2]['y'][2], points[3]['y'][2], points[4]['y'][2], points[5]['y'][2], points[6]['y'][2]])
    aver_y = np.array(new_averages_y)

    fig1, ax1 = plt.subplots()
    mark = matplotlib.markers.MarkerStyle(marker='o', fillstyle='none')
    ax1.scatter(x1, y1, c='b', s=50, marker=mark)
    ax1.scatter(x2, y2, c='b', s=50, marker=mark)
    ax1.scatter(x3, y3, c='b', s=50, marker=mark)
    ax1.scatter(x4, y4, c='b', s=50, marker=mark)
    ax1.scatter(x5, y5, c='b', s=50, marker=mark)
    ax1.scatter(x6, y6, c='b', s=50, marker=mark)
    ax1.scatter(x7, y7, c='b', s=50, marker=mark)
    ax1.plot(aver_x, aver_y)
    ax1.grid()

    fig2, ax2 = plt.subplots()
    x_log = np.array([item['log_x'] for item in log_points])
    y_log = np.array([item['log_y'] for item in log_points])
    ax2.plot(x_log, y_log, marker=mark)
    ax2.grid()

    curv_x = np.array([item['x'] for item in math_curve])
    curv_x = np.insert(curv_x, 0, 0)
    curv_y = np.array([item['y'] for item in math_curve])
    curv_y = np.insert(curv_y, 0, 0)
    fig3, ax3 = plt.subplots()
    mark = matplotlib.markers.MarkerStyle(marker='o', fillstyle='none')
    ax3.scatter(x1, y1, c='b', s=50, marker=mark)
    ax3.scatter(x2, y2, c='b', s=50, marker=mark)
    ax3.scatter(x3, y3, c='b', s=50, marker=mark)
    ax3.scatter(x4, y4, c='b', s=50, marker=mark)
    ax3.scatter(x5, y5, c='b', s=50, marker=mark)
    ax3.scatter(x6, y6, c='b', s=50, marker=mark)
    ax3.scatter(x7, y7, c='b', s=50, marker=mark)
    ax3.plot(curv_x, curv_y)
    interval_curve_x = np.array([30, 40])
    interval_curve_y1 = np.array([interval_pnt1['y'][0], interval_pnt2['y'][0]])
    interval_curve_y2 = np.array([interval_pnt1['y'][1], interval_pnt2['y'][1]])
    ax3.plot(interval_curve_x, interval_curve_y1, c='b')
    ax3.plot(interval_curve_x, interval_curve_y2, c='b')
    ax3.grid()

    # plt.grid()
    plt.show()


if __name__ == '__main__':
    main()
