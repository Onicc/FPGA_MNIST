import numpy as np
import binascii
import sys

INPUT_XEN_PATH = "00_Data/MNIST/xen"
IMAGE_ROM_PATH = "00_Data/ROM/img_rom.coe"

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
    complement = ""
    for i in range(bitwidth-len(bin_value)):
        complement += "0"
    bin_value = bin_value + complement
    hex_value = hex(int(bin_value, 2))[2:]
    hex_value = hex_complement(hex_value, bitwidth)
    return hex_value

def bin2hex_low_first(value, bitwidth):
    """二进制字符串转十六进制的字符串, 自动从后面补0
    """
    bin_value = value
    complement = ""
    for i in range(bitwidth-len(bin_value)):
        complement += "0"
    bin_value = bin_value + complement
    hex_value = hex(int(bin_value, 2))[2:]
    hex_value = hex_complement(hex_value, bitwidth)
    
    hex_value = hex_value[::-1]
    hex_value_low_first = ""
    for i in range(len(hex_value)//2):
        hex_value_low_first = hex_value_low_first + hex_value[i*2:i*2+2][::-1]
    return hex_value_low_first

def param_data():
    bitwidth = 8
    xen_path = INPUT_XEN_PATH
    input = load(xen_path + "/input_{}.xen".format(1))
    input = intarray2bin(np.array(input, dtype=np.int32), bitwidth)
    
    data =  bin2hex(input, 8*28*28)

    return data

def param2coe(coe_file):
    hex_param = param_data()
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
    param2coe(IMAGE_ROM_PATH)