import sys

def bin2dec(hex_data):
    dec = 0
    if(int(hex_data[0], 16) >= 8):
        dec =  -int(bin(int(hex_data, 16)^0xffffffff)[2:], 2)-1
    else:
        dec = int(hex_data, 16)
    return dec

print(bin2dec(sys.argv[1]))