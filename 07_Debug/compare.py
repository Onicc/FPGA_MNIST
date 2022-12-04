import tim
import ila

'''
DWCONV1:DCONV:IN    padding_dout_vld - padding_dout[7:0]
DWCONV1:DCONV:OUT   dconv_dout_vld   - dconv_dout[7:0]
'''

# DWCONV1:PADDING:IN
WAVE_CSV_FILE = "00_Data/ILA/dwconv1.csv"
WAVE_TIM_FILE = "00_Data/TIM/dwconv1_padding_in.tim"
VIVADO_VLD_SIGNAL = "input_vld"
VIVADO_DATA_SIGNAL = "input_din[7:0]"
COCOTB_VLD_SIGNAL = "input_vld"
COCOTB_DATA_SIGNAL = "input_din[7:0]"

# DWCONV1:DCONV:IN
WAVE_CSV_FILE = "00_Data/ILA/dwconv1.csv"
WAVE_TIM_FILE = "00_Data/TIM/dwconv1_dconv_in.tim"
VIVADO_VLD_SIGNAL = "padding_dout_vld"
VIVADO_DATA_SIGNAL = "padding_dout[7:0]"
COCOTB_VLD_SIGNAL = "input_vld"
COCOTB_DATA_SIGNAL = "input_din[7:0]"

# DWCONV1:PCONV:IN
WAVE_CSV_FILE = "00_Data/ILA/dwconv1.csv"
WAVE_TIM_FILE = "00_Data/TIM/dwconv1_pconv_in.tim"
VIVADO_VLD_SIGNAL = "dconv_dout_vld"
VIVADO_DATA_SIGNAL = "dconv_dout[7:0]"
COCOTB_VLD_SIGNAL = "input_vld"
COCOTB_DATA_SIGNAL = "input_din[7:0]"

# # DWCONV1:PCONV:OUT
# WAVE_CSV_FILE = "00_Data/ILA/dwconv1.csv"
# WAVE_TIM_FILE = "00_Data/TIM/dwconv1_pconv_out.tim"
# VIVADO_VLD_SIGNAL = "pconv_dout_vld"
# VIVADO_DATA_SIGNAL = "pconv_dout[47:0]"
# COCOTB_VLD_SIGNAL = "conv_dout_vld"
# COCOTB_DATA_SIGNAL = "conv_dout[47:0]"

target_vivado = ila.high_level_trigger(WAVE_CSV_FILE, VIVADO_VLD_SIGNAL, VIVADO_DATA_SIGNAL)
target_cocotb = tim.high_level_trigger(WAVE_TIM_FILE, COCOTB_VLD_SIGNAL, COCOTB_DATA_SIGNAL)

error_list = []
for d1, d2 in zip(target_vivado, target_cocotb):
    d1 = d1.upper() # 统一大写
    d2 = d2.upper() # 统一大写
    print(d1, d2)
    if(d1 != d2):
        error_list.append([d1, d2])

print("[vivado] total: {}".format(len(target_vivado)))
print("[cocotb] total: {}".format(len(target_cocotb)))
if(len(error_list) != 0):
    print("Error List:")
    print(error_list)
else:
    print("Pass!!!")