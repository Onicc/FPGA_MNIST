
module mnist#(
    parameter N = 8,

    parameter INPUT_CHANNEL_1 = 1,
    parameter INPUT_SIZE_1 = 28,
    parameter OUTPUT_CHANNEL_1 = 4,
    parameter OUTPUT_SIZE_1 = 14,
    parameter KERNEL_SIZE_1 = 3,
    parameter STRIDE_1 = 2,
    parameter PADDING_1 = 1,

    parameter INPUT_CHANNEL_2 = 4,
    parameter INPUT_SIZE_2 = 14,
    parameter OUTPUT_CHANNEL_2 = 4,
    parameter OUTPUT_SIZE_2 = 5,
    parameter KERNEL_SIZE_2 = 3,
    parameter STRIDE_2 = 3,
    parameter PADDING_2 = 1,

    parameter INPUT_CHANNEL_3 = 4,
    parameter INPUT_SIZE_3 = 5,
    parameter OUTPUT_CHANNEL_3 = 4,
    parameter OUTPUT_SIZE_3 = 2,
    parameter KERNEL_SIZE_3 = 3,
    parameter STRIDE_3 = 3,
    parameter PADDING_3 = 1,

    parameter INPUT_CHANNEL_4 = 4,
    parameter INPUT_SIZE_4 = 2,
    parameter OUTPUT_CHANNEL_4 = 4,
    parameter OUTPUT_SIZE_4 = 2,
    parameter KERNEL_SIZE_4 = 1,
    parameter STRIDE_4 = 1,
    parameter PADDING_4 = 0,

    parameter INPUT_CHANNEL_5 = 8,
    parameter INPUT_SIZE_5 = 2,
    parameter OUTPUT_CHANNEL_5 = 10,
    parameter OUTPUT_SIZE_5 = 1,
    parameter KERNEL_SIZE_5 = 3,
    parameter STRIDE_5 = 2,
    parameter PADDING_5 = 1,

    parameter DILATION = 1
    )(
    input wire clk,
    input wire rst_n,
    input wire input_vld,
    input wire [INPUT_CHANNEL_1*N-1:0] input_din,

    input wire [INPUT_CHANNEL_1*(KERNEL_SIZE_1*KERNEL_SIZE_1)*N-1:0] dconv_weight_din_1,
    input wire [INPUT_CHANNEL_1*OUTPUT_CHANNEL_1*N-1:0] pconv_weight_din_1,
    input wire [INPUT_CHANNEL_1*32-1:0] dconv_bias_din_1,
    input wire [OUTPUT_CHANNEL_1*32-1:0] pconv_bias_din_1,
    input wire [INPUT_CHANNEL_1*5-1:0] dconv_shift_din_1,
    input wire [OUTPUT_CHANNEL_1*5-1:0] pconv_shift_din_1,

    input wire [INPUT_CHANNEL_2*(KERNEL_SIZE_2*KERNEL_SIZE_2)*N-1:0] dconv_weight_din_2,
    input wire [INPUT_CHANNEL_2*OUTPUT_CHANNEL_2*N-1:0] pconv_weight_din_2,
    input wire [INPUT_CHANNEL_2*32-1:0] dconv_bias_din_2,
    input wire [OUTPUT_CHANNEL_2*32-1:0] pconv_bias_din_2,
    input wire [INPUT_CHANNEL_2*5-1:0] dconv_shift_din_2,
    input wire [OUTPUT_CHANNEL_2*5-1:0] pconv_shift_din_2,

    input wire [INPUT_CHANNEL_3*(KERNEL_SIZE_3*KERNEL_SIZE_3)*N-1:0] dconv_weight_din_3,
    input wire [INPUT_CHANNEL_3*OUTPUT_CHANNEL_3*N-1:0] pconv_weight_din_3,
    input wire [INPUT_CHANNEL_3*32-1:0] dconv_bias_din_3,
    input wire [OUTPUT_CHANNEL_3*32-1:0] pconv_bias_din_3,
    input wire [INPUT_CHANNEL_3*5-1:0] dconv_shift_din_3,
    input wire [OUTPUT_CHANNEL_3*5-1:0] pconv_shift_din_3,

    input wire [INPUT_CHANNEL_4*(KERNEL_SIZE_4*KERNEL_SIZE_4)*N-1:0] dconv_weight_din_4,
    input wire [INPUT_CHANNEL_4*OUTPUT_CHANNEL_4*N-1:0] pconv_weight_din_4,
    input wire [INPUT_CHANNEL_4*32-1:0] dconv_bias_din_4,
    input wire [OUTPUT_CHANNEL_4*32-1:0] pconv_bias_din_4,
    input wire [INPUT_CHANNEL_4*5-1:0] dconv_shift_din_4,
    input wire [OUTPUT_CHANNEL_4*5-1:0] pconv_shift_din_4,

    input wire [INPUT_CHANNEL_5*(KERNEL_SIZE_5*KERNEL_SIZE_5)*N-1:0] dconv_weight_din_5,
    input wire [INPUT_CHANNEL_5*OUTPUT_CHANNEL_5*N-1:0] pconv_weight_din_5,
    input wire [INPUT_CHANNEL_5*32-1:0] dconv_bias_din_5,
    input wire [OUTPUT_CHANNEL_5*32-1:0] pconv_bias_din_5,
    input wire [INPUT_CHANNEL_5*5-1:0] dconv_shift_din_5,
    input wire [OUTPUT_CHANNEL_5*5-1:0] pconv_shift_din_5,

    output wire [OUTPUT_CHANNEL_5*N-1:0] conv_dout,
    output wire conv_dout_vld,
    output wire conv_dout_end
);

    wire [OUTPUT_CHANNEL_1*N-1:0] conv_dout_1;
    wire conv_dout_vld_1;
    wire conv_dout_end_1;
    dwconv #(.N(N), .INPUT_CHANNEL(INPUT_CHANNEL_1), .INPUT_SIZE(INPUT_SIZE_1), .OUTPUT_CHANNEL(OUTPUT_CHANNEL_1), .OUTPUT_SIZE(OUTPUT_SIZE_1), .KERNEL_SIZE(KERNEL_SIZE_1), .STRIDE(STRIDE_1), .PADDING(PADDING_1), .DILATION(DILATION)) dut_dwconv1 (
    // dwconv_c1 #(.N(N), .INPUT_CHANNEL(INPUT_CHANNEL_1), .INPUT_SIZE(INPUT_SIZE_1), .OUTPUT_CHANNEL(OUTPUT_CHANNEL_1), .OUTPUT_SIZE(OUTPUT_SIZE_1), .KERNEL_SIZE(KERNEL_SIZE_1), .STRIDE(STRIDE_1), .PADDING(PADDING_1), .DILATION(DILATION)) dut_dwconv1 (
        .clk(clk),
        .rst_n(rst_n),
        .input_vld(input_vld),
        .input_din(input_din),
        .dconv_weight_din(dconv_weight_din_1),
        .pconv_weight_din(pconv_weight_din_1),
        .dconv_bias_din(dconv_bias_din_1),
        .pconv_bias_din(pconv_bias_din_1),
        .dconv_shift_din(dconv_shift_din_1),
        .pconv_shift_din(pconv_shift_din_1),
        .conv_dout(conv_dout_1),
        .conv_dout_vld(conv_dout_vld_1),
        .conv_dout_end(conv_dout_end_1)
    );

    wire [OUTPUT_CHANNEL_2*N-1:0] conv_dout_2;
    wire conv_dout_vld_2;
    wire conv_dout_end_2;
    dwconv #(.N(N), .INPUT_CHANNEL(INPUT_CHANNEL_2), .INPUT_SIZE(INPUT_SIZE_2), .OUTPUT_CHANNEL(OUTPUT_CHANNEL_2), .OUTPUT_SIZE(OUTPUT_SIZE_2), .KERNEL_SIZE(KERNEL_SIZE_2), .STRIDE(STRIDE_2), .PADDING(PADDING_2), .DILATION(DILATION)) dut_dwconv2 (
    // dwconv_c6 #(.N(N), .INPUT_CHANNEL(INPUT_CHANNEL_2), .INPUT_SIZE(INPUT_SIZE_2), .OUTPUT_CHANNEL(OUTPUT_CHANNEL_2), .OUTPUT_SIZE(OUTPUT_SIZE_2), .KERNEL_SIZE(KERNEL_SIZE_2), .STRIDE(STRIDE_2), .PADDING(PADDING_2), .DILATION(DILATION)) dut_dwconv2 (
        .clk(clk),
        .rst_n(rst_n),
        .input_vld(conv_dout_vld_1),
        .input_din(conv_dout_1),
        .dconv_weight_din(dconv_weight_din_2),
        .pconv_weight_din(pconv_weight_din_2),
        .dconv_bias_din(dconv_bias_din_2),
        .pconv_bias_din(pconv_bias_din_2),
        .dconv_shift_din(dconv_shift_din_2),
        .pconv_shift_din(pconv_shift_din_2),
        .conv_dout(conv_dout_2),
        .conv_dout_vld(conv_dout_vld_2),
        .conv_dout_end(conv_dout_end_2)
    );


    wire [OUTPUT_CHANNEL_3*N-1:0] conv_dout_3;
    wire conv_dout_vld_3;
    wire conv_dout_end_3;
    dwconv #(.N(N), .INPUT_CHANNEL(INPUT_CHANNEL_3), .INPUT_SIZE(INPUT_SIZE_3), .OUTPUT_CHANNEL(OUTPUT_CHANNEL_3), .OUTPUT_SIZE(OUTPUT_SIZE_3), .KERNEL_SIZE(KERNEL_SIZE_3), .STRIDE(STRIDE_3), .PADDING(PADDING_3), .DILATION(DILATION)) dut_dwconv3 (
    // dwconv_c6 #(.N(N), .INPUT_CHANNEL(INPUT_CHANNEL_3), .INPUT_SIZE(INPUT_SIZE_3), .OUTPUT_CHANNEL(OUTPUT_CHANNEL_3), .OUTPUT_SIZE(OUTPUT_SIZE_3), .KERNEL_SIZE(KERNEL_SIZE_3), .STRIDE(STRIDE_3), .PADDING(PADDING_3), .DILATION(DILATION)) dut_dwconv3 (
        .clk(clk),
        .rst_n(rst_n),
        .input_vld(conv_dout_vld_2),
        .input_din(conv_dout_2),
        .dconv_weight_din(dconv_weight_din_3),
        .pconv_weight_din(pconv_weight_din_3),
        .dconv_bias_din(dconv_bias_din_3),
        .pconv_bias_din(pconv_bias_din_3),
        .dconv_shift_din(dconv_shift_din_3),
        .pconv_shift_din(pconv_shift_din_3),
        .conv_dout(conv_dout_3),
        .conv_dout_vld(conv_dout_vld_3),
        .conv_dout_end(conv_dout_end_3)
    );

    wire [OUTPUT_CHANNEL_4*N-1:0] conv_dout_4;
    wire conv_dout_vld_4;
    wire conv_dout_end_4;
    dwconv_p0 #(.N(N), .INPUT_CHANNEL(INPUT_CHANNEL_4), .INPUT_SIZE(INPUT_SIZE_4), .OUTPUT_CHANNEL(OUTPUT_CHANNEL_4), .OUTPUT_SIZE(OUTPUT_SIZE_4), .KERNEL_SIZE(KERNEL_SIZE_4), .STRIDE(STRIDE_4), .PADDING(PADDING_4), .DILATION(DILATION)) dut_dwconv4 (
    // dwconv_c6 #(.N(N), .INPUT_CHANNEL(INPUT_CHANNEL_4), .INPUT_SIZE(INPUT_SIZE_4), .OUTPUT_CHANNEL(OUTPUT_CHANNEL_4), .OUTPUT_SIZE(OUTPUT_SIZE_4), .KERNEL_SIZE(KERNEL_SIZE_4), .STRIDE(STRIDE_4), .PADDING(PADDING_4), .DILATION(DILATION)) dut_dwconv4 (
        .clk(clk),
        .rst_n(rst_n),
        .input_vld(conv_dout_vld_3),
        .input_din(conv_dout_3),
        .dconv_weight_din(dconv_weight_din_4),
        .pconv_weight_din(pconv_weight_din_4),
        .dconv_bias_din(dconv_bias_din_4),
        .pconv_bias_din(pconv_bias_din_4),
        .dconv_shift_din(dconv_shift_din_4),
        .pconv_shift_din(pconv_shift_din_4),
        .conv_dout(conv_dout_4),
        .conv_dout_vld(conv_dout_vld_4),
        .conv_dout_end(conv_dout_end_4)
    );

    wire [OUTPUT_CHANNEL_5*N-1:0] conv_dout_5;
    wire conv_dout_vld_5;
    wire conv_dout_end_5;
    dwconv #(.N(N), .INPUT_CHANNEL(INPUT_CHANNEL_5), .INPUT_SIZE(INPUT_SIZE_5), .OUTPUT_CHANNEL(OUTPUT_CHANNEL_5), .OUTPUT_SIZE(OUTPUT_SIZE_5), .KERNEL_SIZE(KERNEL_SIZE_5), .STRIDE(STRIDE_5), .PADDING(PADDING_5), .DILATION(DILATION)) dut_dwconv5 (
        .clk(clk),
        .rst_n(rst_n),
        .input_vld(conv_dout_vld_4),
        .input_din(conv_dout_4),
        .dconv_weight_din(dconv_weight_din_5),
        .pconv_weight_din(pconv_weight_din_5),
        .dconv_bias_din(dconv_bias_din_5),
        .pconv_bias_din(pconv_bias_din_5),
        .dconv_shift_din(dconv_shift_din_5),
        .pconv_shift_din(pconv_shift_din_5),
        .conv_dout(conv_dout_5),
        .conv_dout_vld(conv_dout_vld_5),
        .conv_dout_end(conv_dout_end_5)
    );


    assign conv_dout = conv_dout_5;
    assign conv_dout_vld = conv_dout_vld_5;
    assign conv_dout_end = conv_dout_end_5;

    // Dump waves
    initial begin
        $dumpfile("mnist.vcd");
        $dumpvars(1, mnist);
    end

endmodule