import os

TIM_FILE = "00_Data/TIM/dwconv1_padding_in.tim"
VLD_SIGNAL = "input_vld"
DATA_SIGNAL = "input_din[7:0]"

def tim2list(tim_file, signal_name):
    status = 0
    target_list = []
    time_list = []
    with open(tim_file) as f:
        while True:
            line = f.readline()
            if(len(line) < 1):
                break
            if((signal_name+'\n') in line.split(" ")):
                # 匹配信号名称
                status = 1
            if("Position:" in line.split(" ")):
                # 下一个其实信号判断，到下一信号后取消采样
                status = 0
            if(status and ("Edge:" in line.split(" "))):
                # 获取数据，并去除空数据
                split_list = []
                for d in line.split(" "):
                    if(d != ''):
                        split_list.append(d)
                target_list.append(split_list[-1][:-1])
                time_list.append(int(float(split_list[1])))
    return time_list, target_list


def high_level_trigger(tim_file, vld_signal, data_signal):
    target_list = []
    val_time_list, val_target_list = tim2list(tim_file, vld_signal)
    data_time_list, data_target_list = tim2list(tim_file, data_signal)
    for v_t, v_d in zip(val_time_list, val_target_list):
        if(v_d == "1"):
            for i in range(len(data_time_list)-1):
                if(data_time_list[i] <= v_t < data_time_list[i+1]):
                    target_list.append(data_target_list[i])
            if(v_t >= data_time_list[-1]):
                target_list.append(data_target_list[-1])
    return target_list
