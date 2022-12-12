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

 module pconv_unit#(
    parameter N = 16,
    parameter INPUT_CHANNEL = 3,
    parameter MAX = 127
    )(
    input wire clk,
    input wire rst_n,
    input wire input_vld,
    input wire [INPUT_CHANNEL*N-1:0] input_din,
    input wire [INPUT_CHANNEL*N-1:0] weight_din,
    input wire [31:0] bias_din,
    input wire [4:0] shift_din,
    output wire [N-1:0] conv_dout,
    output reg conv_dout_vld
);
    wire [2*N-1:0] pconv_dout [0:INPUT_CHANNEL-1];
    wire [INPUT_CHANNEL-1:0] pconv_dout_vld;
    wire [INPUT_CHANNEL-1:0] product_end;
    wire [31:0] conv_dout_temp_1;   // 取有效信号的卷积输出数据,输出数据有效时结果有效
    wire [31:0] conv_dout_temp_2;   // 最大值限幅, 当输出数据大于127时为127，否则为conv_dout_temp_1
    wire [31:0] conv_dout_temp_1_diff;// 卷积输出数据减最大值的差值
    reg [31:0] pconv_dout_temp;

    // 由于FPGA右移动自动补0，因此高位也跟着一起移动。RELU操作
    assign conv_dout_temp_1 = conv_dout_vld? (pconv_dout_temp+bias_din)>>shift_din:0;
    assign conv_dout_temp_1_diff = conv_dout_temp_1 - MAX;
    assign conv_dout_temp_2 = (conv_dout_temp_1_diff[31-shift_din]==0)? MAX:conv_dout_temp_1;
    assign conv_dout = (conv_dout_temp_2[31-shift_din]==1)? 0:conv_dout_temp_2[N-1:0];

    generate
        genvar i;
        for(i = 0; i < INPUT_CHANNEL; i = i+1) begin: MULT
            qmult #(.N(N)) u_mult(
                .clk(clk),
                .rst_n(rst_n),
                .input_vld(input_vld),
                .multiplicand_din(input_din[(i+1)*N-1:i*N]),
                .multiplier_din(weight_din[(i+1)*N-1:i*N]),
                .product_dout(pconv_dout[i]),
                .product_dout_vld(pconv_dout_vld[i]),
                .product_end(product_end[i])
            );
        end
    endgenerate

    integer i2;
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            pconv_dout_temp = 0;
        end else begin
            if(pconv_dout_vld == {INPUT_CHANNEL{1'b1}}) begin
                for(i2 = 0; i2 < INPUT_CHANNEL; i2 = i2+1) begin
                    // 16位加到32位上
                    pconv_dout_temp = pconv_dout_temp + {{(32+1-2*N){pconv_dout[i2][2*N-1]}}, pconv_dout[i2][2*N-2:0]};
                end
                conv_dout_vld = 1'b1;
            end else begin
                pconv_dout_temp = 0;
                conv_dout_vld = 1'b0;
            end
        end
    end

    // Dump waves
    initial begin
        $dumpfile("pconv_unit.vcd");
        $dumpvars(1, pconv_unit);
    end

endmodule