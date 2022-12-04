import pandas as pd

'''
DWCONV1:DCONV:IN    padding_dout_vld - padding_dout[7:0]
DWCONV1:DCONV:OUT   dconv_dout_vld   - dconv_dout[7:0]
'''

WAVE_CSV_FILE = "00_Data/ILA/dwconv1_dconv_inout.csv"
VLD_SIGNAL = "padding_dout_vld"
DATA_SIGNAL = "padding_dout[7:0]"

def high_level_trigger(wave_csv_file, vld_signal, data_signal):
    handle = pd.read_csv(wave_csv_file)
    target_list = handle[handle[vld_signal] == "1"][data_signal].to_list()
    return target_list