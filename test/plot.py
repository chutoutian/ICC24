from matplotlib import cm
import matplotlib.pyplot as plt

import numpy as np
import sys
import os

weight = 1.414
scheme = 'pensieve'
file_base = './results'
subset = 0
base = './results1'
epoch = 40000

if len(sys.argv) > 1:
    base = sys.argv[1]
    weight = sys.argv[2]
    subset = sys.argv[3]
    scheme = sys.argv[4]
    epoch = sys.argv[5]


def ordering(directory, stp=True):
    spl = directory.split('=')
    if len(spl) > 2:
        return int(spl[2].split('_')[0]) if stp else int(spl[3])
    else:
        return -1


fig = plt.figure(figsize=(20, 8))
fig.suptitle(f'MCTS on subset {subset} weight={weight} scheme={scheme}')
size = len(os.listdir(file_base))
ax = fig.add_subplot(211)
# ax.set_ylim((100, 130))
ax.set_xlabel('trace_idx')
ax.set_ylabel('rwd')

ax2 = fig.add_subplot(212)
ax2.set_ylim((0, 0.4))
ax2.set_xlabel('chunk_idx')
ax2.set_ylabel('time per chunk')

markers = ['+', '1']
rwd_colors = cm.get_cmap('viridis')(np.linspace(0, 1, size))

for _, directories, _ in os.walk(file_base):
    directories.sort(key=lambda d: ordering(d, False))
    directories.sort(key=lambda d: ordering(d, True))
    for nd, d in enumerate(directories):
        rwd = []
        elapsed = []
        buffer_counter = 0
        prev_time = 0
        flag = False
        try:
            step = int(d.split('=')[2].split('_')[0])
            sample = int(d.split('=')[3])
        except IndexError:
            flag = True
        for _, _, filenames in os.walk(os.path.join(file_base, d)):
            for f in filenames:
                rwd_per_chunk = 0
                with open(f'{file_base}/{d}/{f}', 'r', encoding='utf8') as fp:
                    for i, line in enumerate(fp):
                        line = line.split()
                        if not line:
                            break
                        rwd_per_chunk += float(line[-2])
                        elapsed.append(round(float(line[-1])-prev_time, 3))
                        prev_time = round(float(line[-1]), 3)

                rwd.append(rwd_per_chunk)

        avg1 = round(np.average(rwd), 2)
        avg2 = round(np.average(elapsed), 3)
        if not flag:
            ax.plot(np.arange(len(rwd)), rwd, color=rwd_colors[nd], marker=markers[0],
                    label=f'rwd:step={step}-smp={sample}-avg_rwd={avg1}')
            ax2.plot(np.arange(len(elapsed)), elapsed, color=rwd_colors[nd], marker=markers[0],
                     label=f'time:avg_elapsed={avg2}')
        else:
            ax.plot(np.arange(len(rwd)), rwd, color='r', marker=markers[1],
                    label=f'rwd:non-mcts-avg_rwd={avg1}')
            ax2.plot(np.arange(len(elapsed)), elapsed, color='r', marker=markers[1],
                     label=f'time:avg_elapsed={avg2}')

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
box2 = ax2.get_position()
ax2.set_position([box2.x0, box2.y0, box2.width * 0.8, box2.height])

ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
if len(sys.argv) > 1:
    plt.savefig(f'{base}/mcts_subset={subset}_scheme={scheme}_{epoch}.jpg')
    exit()
plt.show()


