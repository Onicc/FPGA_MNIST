import numpy as np
import binascii
import sys

PARAM_PATH = "00_Data/Param/xen"
WEIGHT_ROM_PATH = "00_Data/ROM/weight_rom.coe"
S_KERNAL = 3
C_IN = 1
C_INTER = 6
C_OUT = 10

def load(xen_path):
    narray = None
    with open(xen_path) as f:
        shape = [int(d) for d in f.__next__()[1:-1].split(',')]
        narray = np.genfromtxt(f, delimiter=',').reshape(shape)
    return narray

def integer2bin(integer_value, bitwidth = 32):
    bin_value = ""
    if(integer_value < 0):
        bin_value = bin(integer_value & 0xffffffff)
        bin_value = bin_value[-bitwidth:]
    else:
        bin_value = bin(integer_value).split("b")[-1]
        if(len(bin_value) >= bitwidth):
            bin_value = bin_value[-(bitwidth-1):]
        head = ""
        if(len(bin_value) < bitwidth):
            for i in range(bitwidth - len(bin_value) - 1):
                head += "0"
        bin_value = "0" + head + bin_value

    return bin_value

def intarray2bin(intarray, bitwidth):
    function_vector = np.vectorize(integer2bin)
    bin_array = function_vector(intarray, bitwidth)
    bin_line = np.reshape(bin_array, -1)
    bin_total = ""
    for d in bin_line:
        bin_total += d
    return bin_total

def hex_complement(value, bitwidth):
    """十六进制补0

    notes: hex must no prefix
    """
    hex_value = value
    complement = ""
    if(len(hex_value) != round(bitwidth/4)):
        for i in range(round(bitwidth/4)-len(hex_value)):
            complement += "0"
        hex_value = hex_value + complement
    return hex_value

def bin2hex(value, bitwidth):
    """二进制字符串转十六进制的字符串, 自动从后面补0
    """
    bin_value = value
    hex_value = hex(int(bin_value, 2))[2:]
    complement = ""
    for i in range(bitwidth//4-len(hex_value)):
        complement += "0"
    hex_value = complement + hex_value
    return hex_value

def bin2hex_low_first(value, bitwidth):
    """二进制字符串转十六进制的字符串, 自动从高位补0, 地位有效
    """
    bin_value = value
    hex_value = hex(int(bin_value, 2))[2:]
    complement = ""
    for i in range(bitwidth//4-len(hex_value)):
        complement += "0"
    hex_value = complement + hex_value
    
    hex_value = hex_value[::-1]
    hex_value_low_first = ""
    for i in range(len(hex_value)//2):
        hex_value_low_first = hex_value_low_first + hex_value[i*2:i*2+2][::-1]

    print(int(bitwidth/8), end=", ")
    return hex_value_low_first

def round_numbers(input, bitweight=8):
    output = input
    if(input%bitweight != 0):
        output = (input//bitweight+1)*bitweight
    return output

def param_data():
    bitwidth = 8
    xen_path = PARAM_PATH

    weight_map = {}
    weight_map["b1"] = xen_path + "/b1.xen"
    weight_map["b2"] = xen_path + "/b2.xen"
    weight_map["b3"] = xen_path + "/b3.xen"
    weight_map["b4"] = xen_path + "/b4.xen"
    weight_map["b5"] = xen_path + "/b5.xen"
    weight_map["b6"] = xen_path + "/b6.xen"
    weight_map["b7"] = xen_path + "/b7.xen"
    weight_map["b8"] = xen_path + "/b8.xen"
    weight_map["shift_b1"] = xen_path + "/shift_b1.xen"
    weight_map["shift_b2"] = xen_path + "/shift_b2.xen"
    weight_map["shift_b3"] = xen_path + "/shift_b3.xen"
    weight_map["shift_b4"] = xen_path + "/shift_b4.xen"
    weight_map["shift_b5"] = xen_path + "/shift_b5.xen"
    weight_map["shift_b6"] = xen_path + "/shift_b6.xen"
    weight_map["shift_b7"] = xen_path + "/shift_b7.xen"
    weight_map["shift_b8"] = xen_path + "/shift_b8.xen"
    weight_map["shift_input1"] = xen_path + "/shift_input1.xen"
    weight_map["shift_input2"] = xen_path + "/shift_input2.xen"
    weight_map["shift_input3"] = xen_path + "/shift_input3.xen"
    weight_map["shift_input4"] = xen_path + "/shift_input4.xen"
    weight_map["shift_input5"] = xen_path + "/shift_input5.xen"
    weight_map["shift_input6"] = xen_path + "/shift_input6.xen"
    weight_map["shift_input7"] = xen_path + "/shift_input7.xen"
    weight_map["shift_input8"] = xen_path + "/shift_input8.xen"
    weight_map["shift_io1"] = xen_path + "/shift_io1.xen"
    weight_map["shift_io2"] = xen_path + "/shift_io2.xen"
    weight_map["shift_io3"] = xen_path + "/shift_io3.xen"
    weight_map["shift_io4"] = xen_path + "/shift_io4.xen"
    weight_map["shift_io5"] = xen_path + "/shift_io5.xen"
    weight_map["shift_io6"] = xen_path + "/shift_io6.xen"
    weight_map["shift_io7"] = xen_path + "/shift_io7.xen"
    weight_map["shift_io8"] = xen_path + "/shift_io8.xen"
    weight_map["shift_w1"] = xen_path + "/shift_w1.xen"
    weight_map["shift_w2"] = xen_path + "/shift_w2.xen"
    weight_map["shift_w3"] = xen_path + "/shift_w3.xen"
    weight_map["shift_w4"] = xen_path + "/shift_w4.xen"
    weight_map["shift_w5"] = xen_path + "/shift_w5.xen"
    weight_map["shift_w6"] = xen_path + "/shift_w6.xen"
    weight_map["shift_w7"] = xen_path + "/shift_w7.xen"
    weight_map["shift_w8"] = xen_path + "/shift_w8.xen"
    weight_map["w1"] = xen_path + "/w1.xen"
    weight_map["w2"] = xen_path + "/w2.xen"
    weight_map["w3"] = xen_path + "/w3.xen"
    weight_map["w4"] = xen_path + "/w4.xen"
    weight_map["w5"] = xen_path + "/w5.xen"
    weight_map["w6"] = xen_path + "/w6.xen"
    weight_map["w7"] = xen_path + "/w7.xen"
    weight_map["w8"] = xen_path + "/w8.xen"


    w1 = load(weight_map["w1"])
    shift_w1 = load(weight_map["shift_w1"])
    b1 = load(weight_map["b1"])
    shift_b1 = load(weight_map["shift_b1"])
    shift_io1 = load(weight_map["shift_io1"])

    w2 = load(weight_map["w2"])
    shift_w2 = load(weight_map["shift_w2"])
    b2 = load(weight_map["b2"])
    shift_b2 = load(weight_map["shift_b2"])
    shift_io2 = load(weight_map["shift_io2"])

    w3 = load(weight_map["w3"])
    shift_w3 = load(weight_map["shift_w3"])
    b3 = load(weight_map["b3"])
    shift_b3 = load(weight_map["shift_b3"])
    shift_io3 = load(weight_map["shift_io3"])

    w4 = load(weight_map["w4"])
    shift_w4 = load(weight_map["shift_w4"])
    b4 = load(weight_map["b4"])
    shift_b4 = load(weight_map["shift_b4"])
    shift_io4 = load(weight_map["shift_io4"])

    w5 = load(weight_map["w5"])
    shift_w5 = load(weight_map["shift_w5"])
    b5 = load(weight_map["b5"])
    shift_b5 = load(weight_map["shift_b5"])
    shift_io5 = load(weight_map["shift_io5"])

    w6 = load(weight_map["w6"])
    shift_w6 = load(weight_map["shift_w6"])
    b6 = load(weight_map["b6"])
    shift_b6 = load(weight_map["shift_b6"])
    shift_io6 = load(weight_map["shift_io6"])

    w7 = load(weight_map["w7"])
    shift_w7 = load(weight_map["shift_w7"])
    b7 = load(weight_map["b7"])
    shift_b7 = load(weight_map["shift_b7"])
    shift_io7 = load(weight_map["shift_io7"])

    w8 = load(weight_map["w8"])
    shift_w8 = load(weight_map["shift_w8"])
    b8 = load(weight_map["b8"])
    shift_b8 = load(weight_map["shift_b8"])
    shift_io8 = load(weight_map["shift_io8"])

    # w1按照第二维度拆分 * pow(shift_w1[0][0][0][c] + shift_io1[0][0][0][0] - shift_b1[0][0][0][c])
    shift_o1 = []
    for i in range(b1.shape[3]):
        b1[:, :, :, i] *= pow(2, shift_w1[0, 0, 0, i] + shift_io1[0, 0, 0, 0] - shift_b1[0, 0, 0, i])
        shift_o1.append(shift_w1[0, 0, 0, i] + shift_io1[0, 0, 0, 0] - shift_io1[0, 0, 0, 1])
    shift_o2 = []
    for i in range(b2.shape[3]):
        b2[:, :, :, i] *= pow(2, shift_w2[0, 0, 0, i] + shift_io2[0, 0, 0, 0] - shift_b2[0, 0, 0, i])
        shift_o2.append(shift_w2[0, 0, 0, i] + shift_io2[0, 0, 0, 0] - shift_io2[0, 0, 0, 1])
    shift_o3 = []
    for i in range(b3.shape[3]):
        b3[:, :, :, i] *= pow(2, shift_w3[0, 0, 0, i] + shift_io3[0, 0, 0, 0] - shift_b3[0, 0, 0, i])
        shift_o3.append(shift_w3[0, 0, 0, i] + shift_io3[0, 0, 0, 0] - shift_io3[0, 0, 0, 1])
    shift_o4 = []
    for i in range(b4.shape[3]):
        b4[:, :, :, i] *= pow(2, shift_w4[0, 0, 0, i] + shift_io4[0, 0, 0, 0] - shift_b4[0, 0, 0, i])
        shift_o4.append(shift_w4[0, 0, 0, i] + shift_io4[0, 0, 0, 0] - shift_io4[0, 0, 0, 1])
    shift_o5 = []
    for i in range(b5.shape[3]):
        b5[:, :, :, i] *= pow(2, shift_w5[0, 0, 0, i] + shift_io5[0, 0, 0, 0] - shift_b5[0, 0, 0, i])
        shift_o5.append(shift_w5[0, 0, 0, i] + shift_io5[0, 0, 0, 0] - shift_io5[0, 0, 0, 1])
    shift_o6 = []
    for i in range(b6.shape[3]):
        b6[:, :, :, i] *= pow(2, shift_w6[0, 0, 0, i] + shift_io6[0, 0, 0, 0] - shift_b6[0, 0, 0, i])
        shift_o6.append(shift_w6[0, 0, 0, i] + shift_io6[0, 0, 0, 0] - shift_io6[0, 0, 0, 1])
    shift_o7 = []
    for i in range(b7.shape[3]):
        b7[:, :, :, i] *= pow(2, shift_w7[0, 0, 0, i] + shift_io7[0, 0, 0, 0] - shift_b7[0, 0, 0, i])
        shift_o7.append(shift_w7[0, 0, 0, i] + shift_io7[0, 0, 0, 0] - shift_io7[0, 0, 0, 1])
    shift_o8 = []
    for i in range(b8.shape[3]):
        b8[:, :, :, i] *= pow(2, shift_w8[0, 0, 0, i] + shift_io8[0, 0, 0, 0] - shift_b8[0, 0, 0, i])
        shift_o8.append(shift_w8[0, 0, 0, i] + shift_io8[0, 0, 0, 0] - shift_io8[0, 0, 0, 1])
    
    dconv_weight_din_1 = intarray2bin(np.array(w1, dtype=np.int32), bitwidth)
    pconv_weight_din_1 = intarray2bin(np.array(w2, dtype=np.int32), bitwidth)
    dconv_bias_din_1 = intarray2bin(np.array(b1, dtype=np.int32), 32)
    pconv_bias_din_1 = intarray2bin(np.array(b2, dtype=np.int32), 32)
    dconv_shift_din_1 = intarray2bin(np.array(shift_o1, dtype=np.int32), 5)
    pconv_shift_din_1 = intarray2bin(np.array(shift_o2, dtype=np.int32), 5)

    dconv_weight_din_2 = intarray2bin(np.array(w3, dtype=np.int32), bitwidth)
    pconv_weight_din_2 = intarray2bin(np.array(w4, dtype=np.int32), bitwidth)
    dconv_bias_din_2 = intarray2bin(np.array(b3, dtype=np.int32), 32)
    pconv_bias_din_2 = intarray2bin(np.array(b4, dtype=np.int32), 32)
    dconv_shift_din_2 = intarray2bin(np.array(shift_o3, dtype=np.int32), 5)
    pconv_shift_din_2 = intarray2bin(np.array(shift_o4, dtype=np.int32), 5)

    dconv_weight_din_3 = intarray2bin(np.array(w5, dtype=np.int32), bitwidth)
    pconv_weight_din_3 = intarray2bin(np.array(w6, dtype=np.int32), bitwidth)
    dconv_bias_din_3 = intarray2bin(np.array(b5, dtype=np.int32), 32)
    pconv_bias_din_3 = intarray2bin(np.array(b6, dtype=np.int32), 32)
    dconv_shift_din_3 = intarray2bin(np.array(shift_o5, dtype=np.int32), 5)
    pconv_shift_din_3 = intarray2bin(np.array(shift_o6, dtype=np.int32), 5)

    dconv_weight_din_4 = intarray2bin(np.array(w7, dtype=np.int32), bitwidth)
    pconv_weight_din_4 = intarray2bin(np.array(w8, dtype=np.int32), bitwidth)
    dconv_bias_din_4 = intarray2bin(np.array(b7, dtype=np.int32), 32)
    pconv_bias_din_4 = intarray2bin(np.array(b8, dtype=np.int32), 32)
    dconv_shift_din_4 = intarray2bin(np.array(shift_o7, dtype=np.int32), 5)
    pconv_shift_din_4 = intarray2bin(np.array(shift_o8, dtype=np.int32), 5)
    # print(  dconv_weight_din_1, pconv_weight_din_1, dconv_bias_din_1, pconv_bias_din_1, dconv_shift_din_1, pconv_shift_din_1, \
    #         dconv_weight_din_2, pconv_weight_din_2, dconv_bias_din_2, pconv_bias_din_2, dconv_shift_din_2, pconv_shift_din_2, \
    #         dconv_weight_din_3, pconv_weight_din_3, dconv_bias_din_3, pconv_bias_din_3, dconv_shift_din_3, pconv_shift_din_3, \
    #         dconv_weight_din_4, pconv_weight_din_4, dconv_bias_din_4, pconv_bias_din_4, dconv_shift_din_4, pconv_shift_din_4
    #         )
    data =  bin2hex_low_first(dconv_weight_din_1, round_numbers(C_IN*S_KERNAL*S_KERNAL*8)) + bin2hex_low_first(pconv_weight_din_1, round_numbers(C_IN*C_INTER*8)) + \
            bin2hex_low_first(dconv_weight_din_2, round_numbers(C_INTER*S_KERNAL*S_KERNAL*8)) + bin2hex_low_first(pconv_weight_din_2, round_numbers(C_INTER*C_INTER*8)) + \
            bin2hex_low_first(dconv_weight_din_3, round_numbers(C_INTER*S_KERNAL*S_KERNAL*8)) + bin2hex_low_first(pconv_weight_din_3, round_numbers(C_INTER*C_INTER*8)) + \
            bin2hex_low_first(dconv_weight_din_4, round_numbers(C_INTER*S_KERNAL*S_KERNAL*8)) + bin2hex_low_first(pconv_weight_din_4, round_numbers(C_INTER*C_OUT*8)) + \
            bin2hex_low_first(dconv_bias_din_1, round_numbers(C_IN*32)) + bin2hex_low_first(pconv_bias_din_1, round_numbers(C_INTER*32)) + \
            bin2hex_low_first(dconv_bias_din_2, round_numbers(C_INTER*32)) + bin2hex_low_first(pconv_bias_din_2, round_numbers(C_INTER*32)) + \
            bin2hex_low_first(dconv_bias_din_3, round_numbers(C_INTER*32)) + bin2hex_low_first(pconv_bias_din_3, round_numbers(C_INTER*32)) + \
            bin2hex_low_first(dconv_bias_din_4, round_numbers(C_INTER*32)) + bin2hex_low_first(pconv_bias_din_4, round_numbers(C_OUT*32)) + \
            bin2hex_low_first(dconv_shift_din_1, round_numbers(C_IN*5)) + bin2hex_low_first(pconv_shift_din_1, round_numbers(C_INTER*5)) + \
            bin2hex_low_first(dconv_shift_din_2, round_numbers(C_INTER*5)) + bin2hex_low_first(pconv_shift_din_2, round_numbers(C_INTER*5)) + \
            bin2hex_low_first(dconv_shift_din_3, round_numbers(C_INTER*5)) + bin2hex_low_first(pconv_shift_din_3, round_numbers(C_INTER*5)) + \
            bin2hex_low_first(dconv_shift_din_4, round_numbers(C_INTER*5)) + bin2hex_low_first(pconv_shift_din_4, round_numbers(C_OUT*5))

    return data

def param2coe(coe_file):
    hex_param = param_data()
    print("")
    print("Total Bit: ", len(hex_param)*4)
    print("Total Byte: ", len(hex_param)//2)
    if len(hex_param) % 2 == 1:
        print(f"Param Error!!!")
        sys.exit()
    else:
        print(f"Parameter format detection passed.")

    with open(coe_file, "w") as f:
        f.write("memory_initialization_radix=16;\n")
        f.write("memory_initialization_vector=")
        for i in range(len(hex_param)//2):
            f.write("{} ".format(hex_param[i*2:i*2+2]))
        f.write(";")

    print("Generate COE file successfully.")

if __name__== "__main__" :
    param2coe(WEIGHT_ROM_PATH)