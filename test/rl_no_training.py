import os
os.environ['CUDA_VISIBLE_DEVICES']=''
import numpy as np
import tensorflow as tf
import fixed_env as env
import a3c
import load_trace
import time
import sys

ENUM = {'Mac': 1,'PDCP': 2, 'MCS': 3, 'CellMac': 4, 'PRB': 5}
SCHEME = []


S_INFO = 3 + len(SCHEME)
S_LEN = 8  # take how many frames in the past
A_DIM = 6
ACTOR_LR_RATE = 0.0001
CRITIC_LR_RATE = 0.001
VIDEO_BIT_RATE = [300,750,1200,1850,2850,4300]  # Kbps
BUFFER_NORM_FACTOR = 10.0
CHUNK_TIL_VIDEO_END_CAP = 48.0
M_IN_K = 1000.0
REBUF_PENALTY = 4.3  # 1 sec rebuffering -> 3 Mbps
SMOOTH_PENALTY = 1
DEFAULT_QUALITY = 1  # default video quality without agent
RANDOM_SEED = 42
RAND_RANGE = 1000
# log in format of time_stamp bit_rate buffer_size rebuffer_time chunk_size download_time reward

if len(sys.argv) > 2:
    SUBSET = int(sys.argv[1])
    EPOCH = int(sys.argv[2])
    BASE = sys.argv[3]
    LAYER = int(sys.argv[4])
    NEURON = int(sys.argv[5])
else:
    LAYER = 1
    NEURON = 8
    EPOCH = 4e4
    SUBSET = 3
    BASE = 'pensieve'

NN_MODEL = f'./models/{BASE}/nn_model_layer={LAYER}_neuron={NEURON}_ep_{EPOCH}.ckpt'


def main():
    SUMMARY_DIR = f'results/nonMCTS_subset={SUBSET}'
    LOG_FILE = SUMMARY_DIR + '/log_sim_rl'
    if not os.path.exists(SUMMARY_DIR):
        os.mkdir(SUMMARY_DIR)

    np.random.seed(RANDOM_SEED)

    assert len(VIDEO_BIT_RATE) == A_DIM

    if not os.path.exists(SUMMARY_DIR):
        os.makedirs(SUMMARY_DIR)

    all_cooked_time, all_cooked_bw, all_cooked_Macs, all_file_names = load_trace.load_trace(scheme=SCHEME, subset=SUBSET)

    net_env = env.Environment(all_cooked_time=all_cooked_time,
                              all_cooked_bw=all_cooked_bw,
                              all_cooked_Macs=all_cooked_Macs)

    log_path = LOG_FILE + '_' + all_file_names[net_env.trace_idx]
    log_file = open(log_path, 'wb')

    with tf.Session() as sess:

        actor = a3c.ActorNetwork(sess,
                                 state_dim=[S_INFO, S_LEN], action_dim=A_DIM,
                                 learning_rate=ACTOR_LR_RATE, neuron=NEURON, layer=LAYER, phy=S_INFO)

        critic = a3c.CriticNetwork(sess,
                                   state_dim=[S_INFO, S_LEN],
                                   learning_rate=CRITIC_LR_RATE, neuron=NEURON, layer=LAYER, phy=S_INFO)

        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()  # save neural net parameters

        # restore neural net parameters
        nn_model = NN_MODEL
        if nn_model is not None:  # nn_model is the path to file
            saver.restore(sess, nn_model)
            print("Model restored.")

        time_stamp = 0

        last_bit_rate = DEFAULT_QUALITY
        bit_rate = DEFAULT_QUALITY

        action_vec = np.zeros(A_DIM)
        action_vec[bit_rate] = 1

        s_batch = [np.zeros((S_INFO, S_LEN))]
        a_batch = [action_vec]
        r_batch = []
        entropy_record = []

        video_count = 0
        start = time.time()

        while True:  # serve video forever
            # the action is from the last decision
            # this is to make the framework similar to the real
            delay, sleep_time, buffer_size, rebuf, \
            video_chunk_size, next_video_chunk_sizes, \
            end_of_video, video_chunk_remain, Ave_Macs = \
                net_env.get_video_chunk(bit_rate)

            time_stamp += delay  # in ms
            time_stamp += sleep_time  # in ms

            # reward is video quality - rebuffer penalty - smoothness
            log_bit_rate = np.log(15 * VIDEO_BIT_RATE[bit_rate] / float(VIDEO_BIT_RATE[-1]))
            log_last_bit_rate = np.log(15 * VIDEO_BIT_RATE[last_bit_rate] / float(VIDEO_BIT_RATE[-1]))

            reward = log_bit_rate \
                     - REBUF_PENALTY * rebuf \
                     - SMOOTH_PENALTY * np.abs(log_bit_rate - log_last_bit_rate)

            r_batch.append(reward)

            last_bit_rate = bit_rate
            elapsed = time.time() - start

            # log time_stamp, bit_rate, buffer_size, reward
            log_file.write((str(time_stamp / M_IN_K) + '\t' +
                            str(VIDEO_BIT_RATE[bit_rate]) + '\t' +
                            str(buffer_size) + '\t' +
                            str(rebuf) + '\t' +
                            str(video_chunk_size) + '\t' +
                            str(delay) + '\t' +
                            str(reward) + '\t' +
                            str(elapsed) + '\n').encode())
            log_file.flush()

            # retrieve previous state
            if len(s_batch) == 0:
                state = [np.zeros((S_INFO, S_LEN))]
            else:
                state = np.array(s_batch[-1], copy=True)

            # dequeue history record
            state = np.roll(state, -1, axis=1)

            # this should be S_INFO number of terms
            state[0, -1] = VIDEO_BIT_RATE[bit_rate] / float(np.max(VIDEO_BIT_RATE))  # last quality
            state[1, -1] = buffer_size / BUFFER_NORM_FACTOR  # 10 sec
            state[2, -1] = float(video_chunk_size) / float(delay) / M_IN_K  # kilo byte / ms ; download rate
            for i in range(3, S_INFO):
                state[i, -1] = Ave_Macs[i - 3]
            # state[3, -1] = float(delay) / M_IN_K / BUFFER_NORM_FACTOR  # 10 sec  ; download time
            # state[4, :A_DIM] = np.array(next_video_chunk_sizes) / M_IN_K / M_IN_K  # mega byte ;  next chunk sizes
            # state[5, -1] = np.minimum(video_chunk_remain, CHUNK_TIL_VIDEO_END_CAP) / float(CHUNK_TIL_VIDEO_END_CAP)

            action_prob = actor.predict(np.reshape(state, (1, S_INFO, S_LEN)))
            action_cumsum = np.cumsum(action_prob)
            bit_rate = (action_cumsum > np.random.randint(1, RAND_RANGE) / float(RAND_RANGE)).argmax()
            # Note: we need to discretize the probability into 1/RAND_RANGE steps,
            # because there is an intrinsic discrepancy in passing single state and batch states

            s_batch.append(state)

            entropy_record.append(a3c.compute_entropy(action_prob[0]))

            if end_of_video:
                log_file.write('\n'.encode())
                log_file.close()

                last_bit_rate = DEFAULT_QUALITY
                bit_rate = DEFAULT_QUALITY  # use the default action here

                del s_batch[:]
                del a_batch[:]
                del r_batch[:]

                action_vec = np.zeros(A_DIM)
                action_vec[bit_rate] = 1

                s_batch.append(np.zeros((S_INFO, S_LEN)))
                a_batch.append(action_vec)
                entropy_record = []

                print("video count", video_count)
                video_count += 1

                if video_count >= len(all_file_names):
                    break

                log_path = LOG_FILE + '_' + all_file_names[net_env.trace_idx]
                log_file = open(log_path, 'wb')


if __name__ == '__main__':
    main()
