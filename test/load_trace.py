import os

COOKED_TRACE_FOLDER = './cooked_traces/'
NORM = [1, 1e7, 1e3, 1, 1e7, 1, 1, 1]


def load_trace(cooked_trace_folder=COOKED_TRACE_FOLDER, scheme=None, subset=-1):
    if len(scheme) > 0:
        _cooked_files = os.listdir(cooked_trace_folder)
        cooked_files = []
        if subset != -1:
            for i in range(len(_cooked_files)):
                index = _cooked_files[i].find('subset')
                if int(_cooked_files[i][index + len('subset')]) == subset:
                    cooked_files.append(_cooked_files[i])
        else:
            cooked_files = _cooked_files
        all_cooked_time = []
        all_cooked_bw = []
        all_cooked_Macs = []
        all_file_names = []
        for m in range(len(scheme)):
            all_cooked_Macs.append([])
        for cooked_file in cooked_files:
            file_path = cooked_trace_folder + cooked_file
            cooked_time = []
            cooked_bw = []
            cooked_Macs = []
            for m in range(len(scheme)):
                cooked_Macs.append([])
            with open(file_path, 'rb') as f:
                for line in f:
                    parse = line.split()
                    cooked_time.append(float(parse[0]))
                    for m in range(len(cooked_Macs)):
                        # prb: float(parse[5]), mac: float(parse[1]) / 1e7,  cellmac: float(parse[4]) / 1e7
                        # mcs: float(parse[3]), pdcp: float(parse[2]) / 1e3
                        # pensieve, nonmdp: None
                        cooked_Macs[m].append(float(parse[scheme[m]]) / NORM[scheme[m]])
                    cooked_bw.append(float(parse[6]) / 10000)
            all_cooked_time.append(cooked_time)
            all_cooked_bw.append(cooked_bw)
            all_file_names.append(cooked_file)
            for m in range(len(cooked_Macs)):
                all_cooked_Macs[m].append(cooked_Macs[m])

        return all_cooked_time, all_cooked_bw, all_cooked_Macs, all_file_names
    else:
        _cooked_files = os.listdir(cooked_trace_folder)
        cooked_files = []
        if subset != -1:
            for i in range(len(_cooked_files)):
                index = _cooked_files[i].find('subset')
                if int(_cooked_files[i][index+len('subset')]) == subset:
                    cooked_files.append(_cooked_files[i])
        else:
            cooked_files = _cooked_files
        all_cooked_time = []
        all_cooked_bw = []
        all_file_names = []
        for cooked_file in cooked_files:
            file_path = cooked_trace_folder + cooked_file
            cooked_time = []
            cooked_bw = []
            with open(file_path, 'rb') as f:
                for line in f:
                    parse = line.split()
                    cooked_time.append(float(parse[0]))
                    cooked_bw.append(float(parse[6]) / 10000)
            all_cooked_time.append(cooked_time)
            all_cooked_bw.append(cooked_bw)
            all_file_names.append(cooked_file)

        return all_cooked_time, all_cooked_bw, [all_cooked_time], all_file_names
