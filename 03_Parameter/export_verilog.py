
width = [9, 6, 54, 36, 54, 36, 54, 60, 4, 24, 24, 24, 24, 24, 24, 40, 1, 4, 4, 4, 4, 4, 4, 7]
name = ["dconv_weight_din_1", "pconv_weight_din_1", 
        "dconv_weight_din_2", "pconv_weight_din_2", 
        "dconv_weight_din_3", "pconv_weight_din_3", 
        "dconv_weight_din_4", "pconv_weight_din_4", 

        "dconv_bias_din_1", "pconv_bias_din_1", 
        "dconv_bias_din_2", "pconv_bias_din_2", 
        "dconv_bias_din_3", "pconv_bias_din_3", 
        "dconv_bias_din_4", "pconv_bias_din_4", 

        "dconv_shift_din_1", "pconv_shift_din_1", 
        "dconv_shift_din_2", "pconv_shift_din_2", 
        "dconv_shift_din_3", "pconv_shift_din_3", 
        "dconv_shift_din_4", "pconv_shift_din_4"]

print("[weight.v]")
for i in range(len(name)):
    print("output reg [{}-1:0] {},".format(width[i]*8, name[i]))

print("[mnist.v]")
for i in range(len(name)):
    print("wire [{}-1:0] {};".format(width[i]*8, name[i]))


print("Use")
for n in name:
    print(".{}({}),".format(n, n))

print("[weight.v]")
template = "    always @ (posedge clk or negedge rst_n) begin\n        if (!rst_n) begin\n            {name} <= 0;\n        end else begin\n            if(rom_addr_d1 >= 10'd{begin} && rom_addr_d1 < 10'd{end}) begin\n                {name}[(rom_addr_d1-10'd{offset})*8 +: 8] <= rom_douta;\n            end else begin\n                {name} <= {name};\n            end\n        end\n    end"
begin = 0
for i in range(len(name)):
    end = begin + width[i]
    offset = begin
    print(template.format(begin = begin, end = end, offset = begin, name = name[i]))
    begin = end