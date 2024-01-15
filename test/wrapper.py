import os

WEIGHT = 1.414
SUBSET = 4
pair = {'model': ['pensieve', 'cellmac_prb_mac'], 'layer': [1, 4], 'neuron': [128, 128]}
epochs = [40000]  # pensieve: 39700, cpm: 40000
DISCOUNT = 0.7
index = 0
grp_base = './graphics'

BASE = pair['model'][index]
LAYER = pair['layer'][index]
NEURON = pair['neuron'][index]

for EPOCH in epochs:
    os.system(f'python ./rl_no_training.py {SUBSET} {EPOCH} {BASE} {LAYER} {NEURON}')

    for MCTS_FUTURE_CHUNK_COUNT in [1, 3, 5]:
        for SAMPLING in [30, 50, 100]:
            print(f'*********python ./MCTS_prop.py step:{MCTS_FUTURE_CHUNK_COUNT} sample:{SAMPLING}*********')
            os.system(f'python ./MCTS_prop.py {MCTS_FUTURE_CHUNK_COUNT} {SAMPLING} {WEIGHT} {SUBSET} {EPOCH} {BASE} {LAYER} {NEURON} {DISCOUNT}')

    os.system(f'python ./plot.py {grp_base} {WEIGHT} {SUBSET} {BASE} {EPOCH}')
