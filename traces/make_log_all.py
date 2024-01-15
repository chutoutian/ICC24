import json
import sys
import os
import re
import csv
import mpl_toolkits.axisartist as axisartist
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

json_path = ''
testUE_path = ''
cell_path = ''
train_path = ''
test_path = ''
all_path = ''


def seperate(i=1):
    for k in range(2,7):
        path = 'Set' + str(k) + 'All.log'
        sub_path = 'Set' + str(k) + '/subset' + str(k)
        with open(path,'r', encoding='utf-8') as f:
            line = f.readlines()
            all_dict = []
            time_index = 1
            for i in range(len(line)):
                data = line[i].split()
                all_dict.append(
                    {
                        'time': time_index,
                        'Mac': int(data[1]),
                        'PDCP': int(data[2]),
                        'MCS': int(data[3]),
                        'Cell_Mac': int(data[4]),
                        'Cell_PRB': int(data[5]),
                        'bw': int(data[6])
                    }
                )
                time_index += 1
                if (i+1) % 200 == 0:
                    with open(sub_path + '_' + str(int((i+1)/200)) + '.log', 'w+') as f:
                        for d in all_dict:
                            f.write('%d\t%d\t%d\t%d\t%d\t%d\t%d\n' % (
                                d['time'], d['Mac'], d['PDCP'], d['MCS'], d['Cell_Mac'], d['Cell_PRB'], d['bw']))
                        f.close()
                    all_dict = []
                    time_index = 1


def plot_traces(i=1):
    Macs = [[] for i in range(5)]
    PDCPs = []
    MCSs = []
    Cell_Macs = []
    Cell_PRBs = []
    bws = []
    Net_Name = ['Mac', 'MCS', 'PRB', 'Throughput']
    #Label = [Net_Name[i-1]+ '-set1', Net_Name[i-1]+ '-set2', Net_Name[i-1]+ '-set3', Net_Name[i-1]+ '-set4', Net_Name[i-1]+ '-set5', Net_Name[i-1]+ '-allsets']
    Network = [[] for i in range(4)]
    All_Net = []
    path = './Set' + str(i+1) + 'All.log'
    with open(path,'r', encoding='utf-8') as f:
        line = f.readlines()
        for j in range(len(line)):
            data = line[j].split()
            Network[0].append(float(data[1]) /10000000)
            Network[1].append(float(data[3]) )
            Network[2].append(float(data[5])/100)
            Network[3].append(float(data[6]) /10000)





    fig = plt.figure(figsize=(10, 6))
    ax = axisartist.Subplot(fig, 111)
    fig.add_axes(ax)
    ax.axis["bottom"].set_axisline_style("-|>", size=1.5)
    ax.axis["left"].set_axisline_style("-|>", size=1.5)
    ax.axis["top"].set_visible(False)
    ax.axis["right"].set_visible(False)
    ax.axis["bottom"].label.set_text('Time (s)')
    ax.axis["bottom"].label.set_fontsize(22)
    ax.axis["left"].label.set_text('Information')
    ax.axis["left"].label.set_fontsize(22)
    ax.axis["bottom"].major_ticklabels.set_fontsize(22)
    ax.axis["left"].major_ticklabels.set_fontsize(22)
    ax.tick_params(width=2)
    ax.grid(axis="y")

    A, = plt.plot(Network[0][10000:10200:2], color='#6639a6', label=Net_Name[0], markerfacecolor='none', marker='o', markersize=10, markevery=3, linewidth='2')
    #B, = plt.plot(Network[1][0:100], color='#521262', label=Net_Name[1], markerfacecolor='none', marker='+', markersize=10, markevery=3,
    #              linewidth='2')
    C, = plt.plot(Network[2][10000:10200:2], color='#3490de', label=Net_Name[2], markerfacecolor='none', marker='d', markersize=10, markevery=3,
                  linewidth='2')
    D, = plt.plot(Network[3][10000:10200:2], color='#5684ae', label=Net_Name[3], markerfacecolor='none', marker='^', markersize=10, markevery=3,
                  linewidth='2')
    plt.legend(loc='best', fontsize=16)
    fig.savefig('traces.eps', format='eps')
    plt.show()
    plt.close()


def plot_CDF(i=1):
    Macs = [[] for i in range(5)]
    PDCPs = []
    MCSs = []
    Cell_Macs = []
    Cell_PRBs = []
    bws = []
    Net_Name = ['Mac', 'PDCP', 'MCS', 'CellMac', 'PRB', 'Throughput']
    Label = [Net_Name[i-1]+ '-set1', Net_Name[i-1]+ '-set2', Net_Name[i-1]+ '-set3', Net_Name[i-1]+ '-set4', Net_Name[i-1]+ '-set5', Net_Name[i-1]+ '-allsets']
    Network = [[] for i in range(6)]
    All_Net = []
    for k in range(2,8):
        path = './Set' + str(k) + 'All.log'
        with open(path,'r', encoding='utf-8') as f:
            line = f.readlines()
            for j in range(len(line)):
                data = line[j].split()
                Network[k-2].append(float(data[i]) /10000)





    fig = plt.figure(figsize=(10, 6))
    ax = axisartist.Subplot(fig, 111)
    fig.add_axes(ax)
    ax.axis["bottom"].set_axisline_style("-|>", size=1.5)
    ax.axis["left"].set_axisline_style("-|>", size=1.5)
    ax.axis["top"].set_visible(False)
    ax.axis["right"].set_visible(False)
    ax.axis["bottom"].label.set_text('Throughput (Mbits/)')
    ax.axis["bottom"].label.set_fontsize(22)
    ax.axis["left"].label.set_text('CDF')
    ax.axis["left"].label.set_fontsize(22)
    ax.axis["bottom"].major_ticklabels.set_fontsize(22)
    ax.axis["left"].major_ticklabels.set_fontsize(22)
    ax.tick_params(width=2)
    ax.grid(axis="y")

    ecdf_case1 = sm.distributions.ECDF(Network[0])
    x_set2 = np.linspace(min(Network[0]), max(Network[0]))
    Net_set2 = ecdf_case1(x_set2)

    ecdf_case2 = sm.distributions.ECDF(Network[1])
    x_set3 = np.linspace(min(Network[1]), max(Network[1]))
    Net_set3 = ecdf_case2(x_set3)

    ecdf_case3 = sm.distributions.ECDF(Network[2])
    x_set4 = np.linspace(min(Network[2]), max(Network[2]))
    Net_set4 = ecdf_case3(x_set4)

    ecdf_BL1 = sm.distributions.ECDF(Network[3])
    x_set5 = np.linspace(min(Network[3]), max(Network[3]))
    Net_set5 = ecdf_BL1(x_set5)

    ecdf_BL2 = sm.distributions.ECDF(Network[4])
    x_set6 = np.linspace(min(Network[4]), max(Network[4]))
    Net_set6 = ecdf_BL2(x_set6)

    ecdf_BL3 = sm.distributions.ECDF(Network[5])
    x_set7 = np.linspace(min(Network[5]), max(Network[5]))
    Net_set7 = ecdf_BL3(x_set7)

    A, = plt.plot(x_set2, Net_set2, color='#6639a6', label=Label[0], markerfacecolor='none', marker='o', markersize=10, markevery=3, linewidth='2')
    B, = plt.plot(x_set3, Net_set3, color='#521262', label=Label[1], markerfacecolor='none', marker='+', markersize=10, markevery=3,
                  linewidth='2')
    C, = plt.plot(x_set4, Net_set4, color='#3490de', label=Label[2], markerfacecolor='none', marker='d', markersize=10, markevery=3,
                  linewidth='2')
    D, = plt.plot(x_set5, Net_set5, color='#5684ae', label=Label[3], markerfacecolor='none', marker='^', markersize=10, markevery=3,
                  linewidth='2')
    E, = plt.plot(x_set6, Net_set6, color='darkviolet', label=Label[4], markerfacecolor='none', marker='v', markersize=10, markevery=3,
                  linewidth='2')
    F, = plt.plot(x_set7, Net_set7, color='violet', label=Label[5], markerfacecolor='none', marker='*', markersize=10, markevery=3,
                  linewidth='2')
    plt.legend(loc='best', fontsize=16)
    fig.savefig(Net_Name[i-1] + '.eps', format='eps')
    plt.show()
    plt.close()


def main(set=1):
    # n = len(sys.argv)
    # assert n==2, "Must have exactly one argument"
    global json_path, testUE_path, cell_path, train_path, test_path, all_path

    train_path = 'Set%dTrain.log' % set
    test_path = 'Set%dTest.log' % set
    all_path = 'Set%dAll.log' % set
    files = os.listdir("./")

    train_dict = []
    test_dict = []
    all_dict = []

    Macs = []
    PDCPs = []
    MCSs = []
    Cell_Macs = []
    Cell_PRBs = []
    bws = []  # store the bandwidth

    for f in files:
        if (re.match('Set%d' % (set), f)):
            if (re.match('(.*).json', f)):
                json_path = f
            elif (re.match('(.*)CellPara', f)):
                cell_path = f
            elif (re.match('(.*)TestUE', f)):
                testUE_path = f
    print(json_path, '\n', cell_path, '\n', testUE_path)
    set_json = {}
    with open(json_path) as jf:
        set_json = json.load(jf)

    for ent in set_json['entries']:
        bws.append(int(ent['dlBw']))

    with open(testUE_path) as tf:
        csvreader = csv.reader(tf)
        next(csvreader)
        for i, row in enumerate(csvreader):
            if (i % 7 == 0):
                Macs.append(int(row[3]))
            elif (i % 7 == 1):
                PDCPs.append(max(0, int(row[3])))
            elif (i % 7 == 3):
                MCSs.append(int(row[3]))

    with open(cell_path) as cf:
        csvreader = csv.reader(cf)
        next(csvreader)
        for i, row in enumerate(csvreader):
            if (i % 2 == 0):
                Cell_Macs.append(int(row[3]))
            else:
                Cell_PRBs.append(int(row[3]))
    dict_len = min(len(Macs), len(PDCPs), len(MCSs), len(Cell_Macs), len(Cell_PRBs), len(bws))  # remove reduandant data
    ##train_len = (int)(dict_len * 2 / 3)
    ##test_len = dict_len - train_len
    ##assert test_len > 0, "test_len<0! dict_len: %d" % dict_len
    index = 0
    for i in range(dict_len):
        if (bws[i] != 0 and PDCPs[i] != 0 and MCSs[i] != -1 and Cell_Macs[i] != -1):
            all_dict.append(
                {
                    'time': index + 1,
                    'Mac': Macs[i],
                    'PDCP': PDCPs[i],
                    'MCS': MCSs[i],
                    'Cell_Mac': Cell_Macs[i],
                    'Cell_PRB': Cell_PRBs[i],
                    'bw': bws[i]
                }
            )
            index += 1
    with open(all_path, 'w+') as f:
        for d in all_dict:
            f.write('%d\t%d\t%d\t%d\t%d\t%d\t%d\n' % (
                d['time'], d['Mac'], d['PDCP'], d['MCS'], d['Cell_Mac'], d['Cell_PRB'], d['bw']))
        f.close()


    '''
    for i in range(test_len):
        if (bws[i + train_len] != 0):
            test_dict.append(
                {
                    'time': i + 1,
                    'Mac': Macs[i + train_len],
                    'PDCP': PDCPs[i + train_len],
                    'MCS': MCSs[i + train_len],
                    'Cell_Mac': Cell_Macs[i + train_len],
                    'Cell_PRB': Cell_PRBs[i + train_len],
                    'bw': bws[i + train_len]
                }
            )



    with open(train_path, 'w+') as f:
        for d in train_dict:
            f.write('%d\t%d\t%d\t%d\t%d\t%d\t%d\n' % (
            d['time'], d['Mac'], d['PDCP'], d['MCS'], d['Cell_Mac'], d['Cell_PRB'], d['bw']))
        f.close()

    with open(test_path, "w+") as f:
        for d in test_dict:
            f.write('%d\t%d\t%d\t%d\t%d\t%d\t%d\n' % (
            d['time'], d['Mac'], d['PDCP'], d['MCS'], d['Cell_Mac'], d['Cell_PRB'], d['bw']))
        f.close()
    '''


if __name__ == '__main__':

    #for i in range(2, 7):
    #    main(i)
    #for i in range(1,7):
    #plot_CDF(6)
    plot_traces(1)
    #seperate()