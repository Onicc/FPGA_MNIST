/*
 https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html#torch.nn.Conv2d

 parameter:
    N: data bit width.
    Q: fraction bit width.
    INPUT_CHANNEL: Size of the input chanel.
    INPUT_SIZE: Size of the input image.
    KERNEL_SIZE: Size of the convolving kernel.
    STRIDE: Stride of the convolution. Default: 1.
    PADDING: Padding added to all four sides of the input. Default: 0.
    DILATION: Spacing between kernel elements. Default: 1.

 input:
    clk:
    rst_n:
    ce: high level enable.
    input_vld: input valid flag, active high.
    input_din: input.
    weight_din: weight.

 output:
    conv_dout: conv output.
    conv_dout_vld: output valid flag, active high.
    conv_dout_end: operation end flag, high level end.
 */

 module pconv_unit_c1#(
    parameter N = 16,
    parameter MAX = 127
    )(
    input wire clk,
    input wire rst_n,
    input wire input_vld,
    input wire [N-1:0] input_din,
    input wire [N-1:0] weight_din,
    input wire [31:0] bias_din,
    input wire [4:0] shift_din,
    output wire [N-1:0] conv_dout,
    output reg conv_dout_vld
);
    wire [31:0] pconv_dout;
    wire pconv_dout_vld;
    wire product_end;
    wire [31:0] conv_dout_temp_1;   // 取有效信号的卷积输出数据,输出数据有效时结果有效
    wire [31:0] conv_dout_temp_2;   // 最大值限幅, 当输出数据大于127时为127，否则为conv_dout_temp_1
    wire [31:0] conv_dout_temp_1_diff;// 卷积输出数据减最大值的差值
    reg [31:0] pconv_dout_temp;

    // 由于FPGA右移动自动补0，因此高位也跟着一起移动。RELU操作
    assign conv_dout_temp_1 = conv_dout_vld? (pconv_dout_temp+bias_din)>>shift_din:0;
    assign conv_dout_temp_1_diff = conv_dout_temp_1 - MAX;
    assign conv_dout_temp_2 = (conv_dout_temp_1_diff[31-shift_din]==0)? MAX:conv_dout_temp_1;
    assign conv_dout = (conv_dout_temp_2[31-shift_din]==1)? 0:conv_dout_temp_2[N-1:0];

    qmult #(.N(N)) u_mult(
        .clk(clk),
        .rst_n(rst_n),
        .input_vld(input_vld),
        .multiplicand_din(input_din),
        .multiplier_din(weight_din),
        .product_dout(pconv_dout),
        .product_dout_vld(pconv_dout_vld),
        .product_end(product_end)
    );

    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            pconv_dout_temp <= 0;
        end else begin
            if(pconv_dout_vld == 1'b1) begin
                pconv_dout_temp <= pconv_dout;
                conv_dout_vld <= 1'b1;
            end else begin
                pconv_dout_temp <= 0;
                conv_dout_vld <= 1'b0;
            end
        end
    end

    // Dump waves
    initial begin
        $dumpfile("pconv_unit_c1.vcd");
        $dumpvars(1, pconv_unit_c1);
    end

endmodule