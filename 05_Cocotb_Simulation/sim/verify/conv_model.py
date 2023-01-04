from enum import EnumMeta
import torch
import torch.nn.functional as F
import numpy as np

def hex_complement(value, bitwidth):
    """十六进制补0

    notes: hex must no prefix
    """
    hex_value = value
    complement = ""
    if(len(hex_value) != round(bitwidth/4)):
        for i in range(round(bitwidth/4)-len(hex_value)):
            complement += "0"
        hex_value = complement + hex_value
    return hex_value

# 十进制整数转二进制补码
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

def intarray2binline(intarray, bitwidth):
    function_vector = np.vectorize(integer2bin)
    bin_array = function_vector(intarray, bitwidth)
    bin_line = np.reshape(bin_array, -1)
    return bin_line

def intarray2binunit(intarray, bitwidth):
    function_vector = np.vectorize(integer2bin)
    bin_array = function_vector(intarray, bitwidth)
    input_reshape = bin_array.reshape((bin_array.shape[1], -1))
    input = []
    for i in range(input_reshape.shape[1]):
        str_adder = ""
        for j in range(input_reshape.shape[0]):
            str_adder = str_adder + input_reshape[j, i]
        input.append(str_adder)
    return input

def conv_unit_model(input_size, kernel_size, stride, padding = None, bitwidth = 8):
    # 顺序生成数组，当前仅支持channel为1
    input = np.arange(input_size*input_size, dtype=np.float32).reshape(1, 1, input_size, input_size) % 16 - 8
    kernel = np.arange(kernel_size*kernel_size, dtype=np.float32).reshape(1, 1, kernel_size, kernel_size) % 2

    input = np.array(input, dtype=np.float32)
    kernel = np.array(kernel, dtype=np.float32)

    input = torch.from_numpy(input)
    kernel = torch.from_numpy(kernel)
    bias = torch.tensor([1437.0])
    shift_n = 4

    if padding == None:
        padding = (kernel_size - 1) // 2
    output = F.conv2d(
        input=input,
        weight=kernel,
        bias=bias,
        stride=stride,
        padding=padding
    )

    output = output.numpy()

    print(output)

    print("{} x {} = {}".format(input.shape, kernel.shape, output.shape))
    # conv2d_precess(input, kernel, bitwidth, quantification)
    
    input_bin = intarray2binline(np.array(input, dtype=np.int32), bitwidth)
    kernel_bin = intarray2bin(np.array(kernel, dtype=np.int32), bitwidth)
    bias_bin = integer2bin(int(bias), 32)
    shift_bin = integer2bin(shift_n, 6)
    # output_bin = intarray2binline(np.array(output, dtype=np.int32), bitwidth)
    output_bin = intarray2binline(np.array(output/pow(2, shift_n), dtype=np.int32), bitwidth)

    return input_bin, kernel_bin, bias_bin, shift_bin, output_bin


def dconv_model(input_channel, input_size, kernel_size, stride, padding = None, bitwidth = 8):
    # 顺序生成数组，当前仅支持channel为1
    input = np.arange(input_size*input_size*input_channel, dtype=np.float32).reshape(1, input_channel, input_size, input_size) % 8 - 4
    kernel = np.arange(kernel_size*kernel_size*input_channel, dtype=np.float32).reshape(input_channel, 1, kernel_size, kernel_size) % 4 - 2
    kernel = np.ones((input_channel, 1, kernel_size, kernel_size), dtype=np.float32)

    input = np.array(input, dtype=np.float32)
    kernel = np.array(kernel, dtype=np.float32)

    input = torch.from_numpy(input)
    kernel = torch.from_numpy(kernel)
    bias = 24
    shift_n = 1

    if padding == None:
        padding = (kernel_size - 1) // 2
    output = F.conv2d(
        input=input,
        weight=kernel,
        bias=None,
        stride=stride,
        padding=padding,
        groups=input_channel
    )

    output = output.numpy() + bias

    # print(output)

    print("{} x {} = {}".format(input.shape, kernel.shape, output.shape))
    # conv2d_precess(input, kernel, bitwidth, quantification)
    
    input_bin = intarray2binunit(np.array(input, dtype=np.int32), bitwidth)
    kernel_bin = intarray2bin(np.array(kernel, dtype=np.int32), bitwidth)
    bias_bin = integer2bin(int(bias), 32)
    shift_bin = integer2bin(shift_n, 6)
    # output_bin = intarray2binline(np.array(output, dtype=np.int32), bitwidth)
    output_bin = intarray2binunit(np.array(output/pow(2, shift_n), dtype=np.int32), bitwidth)

    # print(input_bin)
    # print(input)

    return input_bin, kernel_bin, bias_bin, shift_bin, output_bin

from nio import load

PARAM_PATH = "/home/caixc/Documents/Work/Project/NNA/FPGA_MNIST/00_Data/Param/xen"
INPUT_PATH = "/home/caixc/Documents/Work/Project/NNA/FPGA_MNIST/00_Data/MNIST/xen"

def mnist(n, bitwidth):
    weight_map = {}
    weight_map["b1"] = PARAM_PATH + "/b1.xen"
    weight_map["b2"] = PARAM_PATH + "/b2.xen"
    weight_map["b3"] = PARAM_PATH + "/b3.xen"
    weight_map["b4"] = PARAM_PATH + "/b4.xen"
    weight_map["b5"] = PARAM_PATH + "/b5.xen"
    weight_map["b6"] = PARAM_PATH + "/b6.xen"
    weight_map["b7"] = PARAM_PATH + "/b7.xen"
    weight_map["b8"] = PARAM_PATH + "/b8.xen"
    weight_map["b9"] = PARAM_PATH + "/b9.xen"
    weight_map["b10"] = PARAM_PATH + "/b10.xen"
    weight_map["shift_b1"] = PARAM_PATH + "/shift_b1.xen"
    weight_map["shift_b2"] = PARAM_PATH + "/shift_b2.xen"
    weight_map["shift_b3"] = PARAM_PATH + "/shift_b3.xen"
    weight_map["shift_b4"] = PARAM_PATH + "/shift_b4.xen"
    weight_map["shift_b5"] = PARAM_PATH + "/shift_b5.xen"
    weight_map["shift_b6"] = PARAM_PATH + "/shift_b6.xen"
    weight_map["shift_b7"] = PARAM_PATH + "/shift_b7.xen"
    weight_map["shift_b8"] = PARAM_PATH + "/shift_b8.xen"
    weight_map["shift_b9"] = PARAM_PATH + "/shift_b9.xen"
    weight_map["shift_b10"] = PARAM_PATH + "/shift_b10.xen"
    weight_map["shift_input1"] = PARAM_PATH + "/shift_input1.xen"
    weight_map["shift_input2"] = PARAM_PATH + "/shift_input2.xen"
    weight_map["shift_input3"] = PARAM_PATH + "/shift_input3.xen"
    weight_map["shift_input4"] = PARAM_PATH + "/shift_input4.xen"
    weight_map["shift_input5"] = PARAM_PATH + "/shift_input5.xen"
    weight_map["shift_input6"] = PARAM_PATH + "/shift_input6.xen"
    weight_map["shift_input7"] = PARAM_PATH + "/shift_input7.xen"
    weight_map["shift_input8"] = PARAM_PATH + "/shift_input8.xen"
    weight_map["shift_input9"] = PARAM_PATH + "/shift_input9.xen"
    weight_map["shift_input10"] = PARAM_PATH + "/shift_input10.xen"
    weight_map["shift_io1"] = PARAM_PATH + "/shift_io1.xen"
    weight_map["shift_io2"] = PARAM_PATH + "/shift_io2.xen"
    weight_map["shift_io3"] = PARAM_PATH + "/shift_io3.xen"
    weight_map["shift_io4"] = PARAM_PATH + "/shift_io4.xen"
    weight_map["shift_io5"] = PARAM_PATH + "/shift_io5.xen"
    weight_map["shift_io6"] = PARAM_PATH + "/shift_io6.xen"
    weight_map["shift_io7"] = PARAM_PATH + "/shift_io7.xen"
    weight_map["shift_io8"] = PARAM_PATH + "/shift_io8.xen"
    weight_map["shift_io9"] = PARAM_PATH + "/shift_io9.xen"
    weight_map["shift_io10"] = PARAM_PATH + "/shift_io10.xen"
    weight_map["shift_w1"] = PARAM_PATH + "/shift_w1.xen"
    weight_map["shift_w2"] = PARAM_PATH + "/shift_w2.xen"
    weight_map["shift_w3"] = PARAM_PATH + "/shift_w3.xen"
    weight_map["shift_w4"] = PARAM_PATH + "/shift_w4.xen"
    weight_map["shift_w5"] = PARAM_PATH + "/shift_w5.xen"
    weight_map["shift_w6"] = PARAM_PATH + "/shift_w6.xen"
    weight_map["shift_w7"] = PARAM_PATH + "/shift_w7.xen"
    weight_map["shift_w8"] = PARAM_PATH + "/shift_w8.xen"
    weight_map["shift_w9"] = PARAM_PATH + "/shift_w9.xen"
    weight_map["shift_w10"] = PARAM_PATH + "/shift_w10.xen"
    weight_map["w1"] = PARAM_PATH + "/w1.xen"
    weight_map["w2"] = PARAM_PATH + "/w2.xen"
    weight_map["w3"] = PARAM_PATH + "/w3.xen"
    weight_map["w4"] = PARAM_PATH + "/w4.xen"
    weight_map["w5"] = PARAM_PATH + "/w5.xen"
    weight_map["w6"] = PARAM_PATH + "/w6.xen"
    weight_map["w7"] = PARAM_PATH + "/w7.xen"
    weight_map["w8"] = PARAM_PATH + "/w8.xen"
    weight_map["w9"] = PARAM_PATH + "/w9.xen"
    weight_map["w10"] = PARAM_PATH + "/w10.xen"

    weight_map["inout_root"] = INPUT_PATH

    input1 = load(weight_map["inout_root"] + "/input_{}.xen".format(n))
    output1 = load(weight_map["inout_root"] + "/output_{}.xen".format(n))

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

    w9 = load(weight_map["w9"])
    shift_w9 = load(weight_map["shift_w9"])
    b9 = load(weight_map["b9"])
    shift_b9 = load(weight_map["shift_b9"])
    shift_io9 = load(weight_map["shift_io9"])

    w10 = load(weight_map["w10"])
    shift_w10 = load(weight_map["shift_w10"])
    b10 = load(weight_map["b10"])
    shift_b10 = load(weight_map["shift_b10"])
    shift_io10 = load(weight_map["shift_io10"])

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
    shift_o9 = []
    for i in range(b9.shape[3]):
        b9[:, :, :, i] *= pow(2, shift_w9[0, 0, 0, i] + shift_io9[0, 0, 0, 0] - shift_b9[0, 0, 0, i])
        shift_o9.append(shift_w9[0, 0, 0, i] + shift_io9[0, 0, 0, 0] - shift_io9[0, 0, 0, 1])
    shift_o10 = []
    for i in range(b10.shape[3]):
        b10[:, :, :, i] *= pow(2, shift_w10[0, 0, 0, i] + shift_io10[0, 0, 0, 0] - shift_b10[0, 0, 0, i])
        shift_o10.append(shift_w10[0, 0, 0, i] + shift_io10[0, 0, 0, 0] - shift_io10[0, 0, 0, 1])

    input_din = intarray2binunit(np.array(input1, dtype=np.int32), bitwidth)

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

    dconv_weight_din_5 = intarray2bin(np.array(w9, dtype=np.int32), bitwidth)
    pconv_weight_din_5 = intarray2bin(np.array(w10, dtype=np.int32), bitwidth)
    dconv_bias_din_5 = intarray2bin(np.array(b9, dtype=np.int32), 32)
    pconv_bias_din_5 = intarray2bin(np.array(b10, dtype=np.int32), 32)
    dconv_shift_din_5 = intarray2bin(np.array(shift_o9, dtype=np.int32), 5)
    pconv_shift_din_5 = intarray2bin(np.array(shift_o10, dtype=np.int32), 5)

    # print(input1.shape)

    # print(w1.shape)
    # print(shift_w1.shape)
    # print(b1.shape)
    # print(shift_b1.shape)
    # print(shift_io1.shape)

    # print(w2.shape)
    # print(shift_w2.shape)
    # print(b2.shape)
    # print(shift_b2.shape)
    # print(shift_io2.shape)

    return input_din, output1[0][0][0][0], \
           dconv_weight_din_1, pconv_weight_din_1, dconv_bias_din_1, pconv_bias_din_1, dconv_shift_din_1, pconv_shift_din_1, \
           dconv_weight_din_2, pconv_weight_din_2, dconv_bias_din_2, pconv_bias_din_2, dconv_shift_din_2, pconv_shift_din_2, \
           dconv_weight_din_3, pconv_weight_din_3, dconv_bias_din_3, pconv_bias_din_3, dconv_shift_din_3, pconv_shift_din_3, \
           dconv_weight_din_4, pconv_weight_din_4, dconv_bias_din_4, pconv_bias_din_4, dconv_shift_din_4, pconv_shift_din_4, \
           dconv_weight_din_5, pconv_weight_din_5, dconv_bias_din_5, pconv_bias_din_5, dconv_shift_din_5, pconv_shift_din_5


def simulation_conv():
    input_1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, \
                0,11,6,6,6,6,6,6,6,6,6,6,6,6,6,0, \
                0,8,1,1,1,1,3,8,12,7,1,1,1,1,1,0, \
                0,8,1,1,1,7,29,33,30,24,5,1,1,1,1,0, \
                0,8,1,1,3,24,26,8,14,30,7,1,1,1,1,0, \
                0,8,1,1,3,9,3,2,23,28,3,1,1,1,1,0, \
                0,8,1,1,1,1,1,11,34,15,1,1,1,1,1,0, \
                0,8,1,1,1,1,5,30,23,3,1,1,1,1,1,0, \
                0,8,1,1,1,2,20,32,6,1,1,1,1,1,1,0, \
                0,8,1,1,1,9,33,18,1,1,1,1,1,1,1,0, \
                0,8,1,1,1,21,30,4,2,2,1,2,5,8,6,0, \
                0,8,1,1,1,21,32,28,28,24,23,28,31,27,14,0, \
                0,8,1,1,1,9,17,17,23,23,17,13,8,6,3,0, \
                0,8,1,1,1,1,1,1,1,1,1,1,1,1,1,0, \
                0,8,1,1,1,1,1,1,1,1,1,1,1,1,1,0, \
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    kernel_1 = [-18,30,22, \
                52,25,70, \
                21,0,48]

    input_1 = np.array(input_1, dtype=np.int32)
    kernel_1 = np.array(kernel_1, dtype=np.int32)

    output_step_1 = []
    for i in range(len(input_1)):
        output_step_1.append(kernel_1*input_1[i])

    output_step_1 = np.array(output_step_1, dtype=np.int32)
    output_step_1 = output_step_1.T

    reg = []
    size = 16
    stride = size-3
    for y_th in range(9):
        reg_ = []
        mappp = [0, 1, 2, 3+stride, 4+stride, 5+stride, 6+2*stride, 7+2*stride, 8+2*stride]
        for m in range(mappp[y_th]):
            reg_.append(0)
        for j in range(output_step_1.shape[1]-(3+stride)*3):
            i1 = 0
            i2 = 0
            y = 0
            reg_sum = 0
            for i in range(output_step_1.shape[1]):
                x = i+j
                i1 += 1
                i2 += 1
                if i1%(3+stride) == 0:
                    i2 = 0
                if(0 < i2 <= 3):
                    # print(y, x, end=", ")
                    reg_sum += output_step_1[y, x]
                    y += 1
                # if(i1 >= (3+stride)*3):
                if(y > y_th):
                    reg_.append(reg_sum)
                    break
        reg.append(reg_[:size*size])

    # output_step_1: 为每一层的乘积
    # reg: 为行的乘加后值

    product = []
    for d in output_step_1:
        temp_ = []
        for d1 in d:
            temp_.append(d1)
        product.append(temp_)
    
    x1 = []
    for i in range(9):
        x1.append(list(input_1))

    x2 = []
    for d in kernel_1:
        x2_ = []
        for i in range(len(input_1)):
            x2_.append(d)
        x2.append(x2_)

    x3 = []
    reg = np.array(reg, dtype=np.int32)
    for i in range(9):
        x3_ = []
        if(i == 0):
            for i in range(len(reg[0])):
                x3_.append(0)
        else:
            x3_.append(0)
            for d in reg[i-1]:
                x3_.append(d)
        x3.append(x3_)

    for i, r in enumerate(reg):
        def bin2hex(binx):
            return hex_complement(hex(int(binx, 2)).split("x")[1], 16)
        function_vector = np.vectorize(bin2hex)

        r_bin = intarray2binline(np.array(r, dtype=np.int32), 16)
        r_hex = function_vector(r_bin)

        x1_bin = intarray2binline(np.array(x1[i], dtype=np.int32), 16)
        x1_hex = function_vector(x1_bin)

        x2_bin = intarray2binline(np.array(x2[i], dtype=np.int32), 16)
        x2_hex = function_vector(x2_bin)

        x3_bin = intarray2binline(np.array(x3[i], dtype=np.int32), 16)
        x3_hex = function_vector(x3_bin)

        product_bin = intarray2binline(np.array(product[i], dtype=np.int32), 16)
        product_hex = function_vector(product_bin)

        print("x1,", x1[i])
        print("x1_hex,", list(x1_hex))
        print("x2,", x2[i])
        # print("x2_bin,", x2_bin[i])
        print("x2_hex,", list(x2_hex))
        print("x3,", list(x3[i]))
        print("x3_hex,", list(x3_hex))
        print("product,", product[i])
        print("product_hex,", list(product_hex))
        print("product add,", list(r))
        print("product add hex,", list(r_hex))
        # print(list(r_hex))

    # print(output_step_1[:, :30])

    # print(input_1)
    # print(kernel_1)

# simulation_conv()
# dwconv(8)

# input_bin, kernel_bin, bias_bin, shift_bin, output_bin = dconv_model(input_channel=3, input_size = 10, kernel_size = 3, stride = 1, padding = 0, bitwidth = 8)
# print(input_bin, kernel_bin, bias_bin, shift_bin, output_bin)

# print(integer2bin(-5, 8))

def checkweight(n, bitwidth):
    weight_map = {}
    weight_map["b1"] = PARAM_PATH + "/b1.xen"
    weight_map["b2"] = PARAM_PATH + "/b2.xen"
    weight_map["b3"] = PARAM_PATH + "/b3.xen"
    weight_map["b4"] = PARAM_PATH + "/b4.xen"
    weight_map["b5"] = PARAM_PATH + "/b5.xen"
    weight_map["b6"] = PARAM_PATH + "/b6.xen"
    weight_map["b7"] = PARAM_PATH + "/b7.xen"
    weight_map["b8"] = PARAM_PATH + "/b8.xen"
    weight_map["input"] = PARAM_PATH + "/input.xen"
    weight_map["shift_b1"] = PARAM_PATH + "/shift_b1.xen"
    weight_map["shift_b2"] = PARAM_PATH + "/shift_b2.xen"
    weight_map["shift_b3"] = PARAM_PATH + "/shift_b3.xen"
    weight_map["shift_b4"] = PARAM_PATH + "/shift_b4.xen"
    weight_map["shift_b5"] = PARAM_PATH + "/shift_b5.xen"
    weight_map["shift_b6"] = PARAM_PATH + "/shift_b6.xen"
    weight_map["shift_b7"] = PARAM_PATH + "/shift_b7.xen"
    weight_map["shift_b8"] = PARAM_PATH + "/shift_b8.xen"
    weight_map["shift_input1"] = PARAM_PATH + "/shift_input1.xen"
    weight_map["shift_input2"] = PARAM_PATH + "/shift_input2.xen"
    weight_map["shift_input3"] = PARAM_PATH + "/shift_input3.xen"
    weight_map["shift_input4"] = PARAM_PATH + "/shift_input4.xen"
    weight_map["shift_input5"] = PARAM_PATH + "/shift_input5.xen"
    weight_map["shift_input6"] = PARAM_PATH + "/shift_input6.xen"
    weight_map["shift_input7"] = PARAM_PATH + "/shift_input7.xen"
    weight_map["shift_input8"] = PARAM_PATH + "/shift_input8.xen"
    weight_map["shift_io1"] = PARAM_PATH + "/shift_io1.xen"
    weight_map["shift_io2"] = PARAM_PATH + "/shift_io2.xen"
    weight_map["shift_io3"] = PARAM_PATH + "/shift_io3.xen"
    weight_map["shift_io4"] = PARAM_PATH + "/shift_io4.xen"
    weight_map["shift_io5"] = PARAM_PATH + "/shift_io5.xen"
    weight_map["shift_io6"] = PARAM_PATH + "/shift_io6.xen"
    weight_map["shift_io7"] = PARAM_PATH + "/shift_io7.xen"
    weight_map["shift_io8"] = PARAM_PATH + "/shift_io8.xen"
    weight_map["shift_w1"] = PARAM_PATH + "/shift_w1.xen"
    weight_map["shift_w2"] = PARAM_PATH + "/shift_w2.xen"
    weight_map["shift_w3"] = PARAM_PATH + "/shift_w3.xen"
    weight_map["shift_w4"] = PARAM_PATH + "/shift_w4.xen"
    weight_map["shift_w5"] = PARAM_PATH + "/shift_w5.xen"
    weight_map["shift_w6"] = PARAM_PATH + "/shift_w6.xen"
    weight_map["shift_w7"] = PARAM_PATH + "/shift_w7.xen"
    weight_map["shift_w8"] = PARAM_PATH + "/shift_w8.xen"
    weight_map["w1"] = PARAM_PATH + "/w1.xen"
    weight_map["w2"] = PARAM_PATH + "/w2.xen"
    weight_map["w3"] = PARAM_PATH + "/w3.xen"
    weight_map["w4"] = PARAM_PATH + "/w4.xen"
    weight_map["w5"] = PARAM_PATH + "/w5.xen"
    weight_map["w6"] = PARAM_PATH + "/w6.xen"
    weight_map["w7"] = PARAM_PATH + "/w7.xen"
    weight_map["w8"] = PARAM_PATH + "/w8.xen"

    weight_map["inout_root"] = PARAM_PATH + "/MNIST/test_inout"

    input1 = load(weight_map["inout_root"] + "/input_{}.xen".format(n))
    output1 = load(weight_map["inout_root"] + "/output_{}.xen".format(n))

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

    w1_bin = intarray2binline(np.array(w1, dtype=np.int32), bitwidth)
    w2_bin = intarray2binline(np.array(w2, dtype=np.int32), bitwidth)
    b1_bin = intarray2binline(np.array(b1, dtype=np.int32), 32)
    b2_bin = intarray2binline(np.array(b2, dtype=np.int32), 32)

    w3_bin = intarray2binline(np.array(w3, dtype=np.int32), bitwidth)
    w4_bin = intarray2binline(np.array(w4, dtype=np.int32), bitwidth)
    b3_bin = intarray2binline(np.array(b3, dtype=np.int32), 32)
    b4_bin = intarray2binline(np.array(b4, dtype=np.int32), 32)

    w5_bin = intarray2binline(np.array(w5, dtype=np.int32), bitwidth)
    w6_bin = intarray2binline(np.array(w6, dtype=np.int32), bitwidth)
    b5_bin = intarray2binline(np.array(b5, dtype=np.int32), 32)
    b6_bin = intarray2binline(np.array(b6, dtype=np.int32), 32)

    w7_bin = intarray2binline(np.array(w7, dtype=np.int32), bitwidth)
    w8_bin = intarray2binline(np.array(w8, dtype=np.int32), bitwidth)
    b7_bin = intarray2binline(np.array(b7, dtype=np.int32), 32)
    b8_bin = intarray2binline(np.array(b8, dtype=np.int32), 32)


    shift_o1_bin = intarray2bin(np.array(shift_o1, dtype=np.int32), 5)
    shift_o2_bin = intarray2bin(np.array(shift_o2, dtype=np.int32), 5)
    shift_o3_bin = intarray2bin(np.array(shift_o3, dtype=np.int32), 5)
    shift_o4_bin = intarray2bin(np.array(shift_o4, dtype=np.int32), 5)
    shift_o5_bin = intarray2bin(np.array(shift_o5, dtype=np.int32), 5)
    shift_o6_bin = intarray2bin(np.array(shift_o6, dtype=np.int32), 5)
    shift_o7_bin = intarray2bin(np.array(shift_o7, dtype=np.int32), 5)
    shift_o8_bin = intarray2bin(np.array(shift_o8, dtype=np.int32), 5)

    def bin2dec(bin_data, bitwidth):
        dec = 0
        if(bin_data[0] == "1"):
            dec =  -int(bin(int(bin_data, 2)^0xffffffff)[-bitwidth:], 2)-1
        else:
            dec = int(bin_data, 2)
        return dec

    def bin2decline(bin_data, bitwidth):
        function_vector = np.vectorize(bin2dec)
        bin_array = function_vector(bin_data, bitwidth)
        return bin_array
    
    dec_list = []
    dec_cov_list = []

    dec_cov_list.append(bin2decline(w1_bin, bitwidth))
    dec_list.append(np.array(w1.flatten(), np.int64))
    dec_cov_list.append(bin2decline(w2_bin, bitwidth))
    dec_list.append(np.array(w2.flatten(), np.int64))
    dec_cov_list.append(bin2decline(w3_bin, bitwidth))
    dec_list.append(np.array(w3.flatten(), np.int64))
    dec_cov_list.append(bin2decline(w4_bin, bitwidth))
    dec_list.append(np.array(w4.flatten(), np.int64))
    dec_cov_list.append(bin2decline(w5_bin, bitwidth))
    dec_list.append(np.array(w5.flatten(), np.int64))
    dec_cov_list.append(bin2decline(w6_bin, bitwidth))
    dec_list.append(np.array(w6.flatten(), np.int64))
    dec_cov_list.append(bin2decline(w7_bin, bitwidth))
    dec_list.append(np.array(w7.flatten(), np.int64))
    dec_cov_list.append(bin2decline(w8_bin, bitwidth))
    dec_list.append(np.array(w8.flatten(), np.int64))

    dec_cov_list.append(bin2decline(b1_bin, 32))
    dec_list.append(np.array(b1.flatten(), np.int64))
    dec_cov_list.append(bin2decline(b2_bin, 32))
    dec_list.append(np.array(b2.flatten(), np.int64))
    dec_cov_list.append(bin2decline(b3_bin, 32))
    dec_list.append(np.array(b3.flatten(), np.int64))
    dec_cov_list.append(bin2decline(b4_bin, 32))
    dec_list.append(np.array(b4.flatten(), np.int64))
    dec_cov_list.append(bin2decline(b5_bin, 32))
    dec_list.append(np.array(b5.flatten(), np.int64))
    dec_cov_list.append(bin2decline(b6_bin, 32))
    dec_list.append(np.array(b6.flatten(), np.int64))
    dec_cov_list.append(bin2decline(b7_bin, 32))
    dec_list.append(np.array(b7.flatten(), np.int64))
    dec_cov_list.append(bin2decline(b8_bin, 32))
    dec_list.append(np.array(b8.flatten(), np.int64))

    def bin2decline2(bin_data, bitwidth):
        # print(bin_data)
        # print(int(len(bin_data)/5))
        decline = []
        for i in range(int(len(bin_data)/5)):
            # print(bin_data[i*5:(i+1)*5])
            decline.append(bin2dec(bin_data[i*5:(i+1)*5], bitwidth))
        return decline

    dec_cov_list.append(bin2decline2(shift_o1_bin, 5))
    dec_list.append(np.array(shift_o1, np.int64))
    dec_cov_list.append(bin2decline2(shift_o2_bin, 5))
    dec_list.append(np.array(shift_o2, np.int64))
    dec_cov_list.append(bin2decline2(shift_o3_bin, 5))
    dec_list.append(np.array(shift_o3, np.int64))
    dec_cov_list.append(bin2decline2(shift_o4_bin, 5))
    dec_list.append(np.array(shift_o4, np.int64))
    dec_cov_list.append(bin2decline2(shift_o5_bin, 5))
    dec_list.append(np.array(shift_o5, np.int64))
    dec_cov_list.append(bin2decline2(shift_o6_bin, 5))
    dec_list.append(np.array(shift_o6, np.int64))
    dec_cov_list.append(bin2decline2(shift_o7_bin, 5))
    dec_list.append(np.array(shift_o7, np.int64))
    dec_cov_list.append(bin2decline2(shift_o8_bin, 5))
    dec_list.append(np.array(shift_o8, np.int64))

    for i in range(len(dec_list)):
        if((dec_list[i] == dec_cov_list[i]).all()):
            print("{} Pass!".format(i%8))
        else:
            print("{} Fail!".format(i%8))
            print(dec_list[i])
            print(dec_cov_list[i])

    # print(b1_bin)
    # print("----------------------------")
    # print(b1)
    # print("----------------------------")
    # print(b2_bin)
    # print("----------------------------")
    # print(b2)
    # print("----------------------------")

    # print(shift_o1)
    # print(shift_o2)
    # print(shift_o3)
    # print(shift_o4)
    # print(shift_o5)
    # print(shift_o6)
    # print(shift_o7)
    # print(shift_o8)

# checkweight(1, 8)

# print(bin(-127 & 0xffffffff)[-8:])
# print(bin(-127 & 0xffffffff)[-8:])
# print(-int(bin(218^0xffff)[-8:], 2)-1)
