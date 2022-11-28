
module mnist#(
    parameter N = 8,

    parameter INPUT_CHANNEL_1 = 1,
    parameter INPUT_SIZE_1 = 28,
    parameter OUTPUT_CHANNEL_1 = 6,
    parameter OUTPUT_SIZE_1 = 14,
    parameter KERNEL_SIZE_1 = 3,
    parameter STRIDE_1 = 2,
    parameter PADDING_1 = 1,

    parameter INPUT_CHANNEL_2 = 6,
    parameter INPUT_SIZE_2 = 14,
    parameter OUTPUT_CHANNEL_2 = 6,
    parameter OUTPUT_SIZE_2 = 5,
    parameter KERNEL_SIZE_2 = 3,
    parameter STRIDE_2 = 3,
    parameter PADDING_2 = 1,

    parameter INPUT_CHANNEL_3 = 6,
    parameter INPUT_SIZE_3 = 5,
    parameter OUTPUT_CHANNEL_3 = 6,
    parameter OUTPUT_SIZE_3 = 2,
    parameter KERNEL_SIZE_3 = 3,
    parameter STRIDE_3 = 3,
    parameter PADDING_3 = 1,

    parameter INPUT_CHANNEL_4 = 6,
    parameter INPUT_SIZE_4 = 2,
    parameter OUTPUT_CHANNEL_4 = 10,
    parameter OUTPUT_SIZE_4 = 1,
    parameter KERNEL_SIZE_4 = 3,
    parameter STRIDE_4 = 2,
    parameter PADDING_4 = 1,

    parameter DILATION = 1
    )(
    input wire clk,
    input wire rst_n,
    input wire ce,
    input wire input_vld,
    input wire [INPUT_CHANNEL_1*N-1:0] input_din,

    output wire [OUTPUT_CHANNEL_4*N-1:0] conv_dout,
    output wire conv_dout_vld,
    output wire conv_dout_end
);

    wire [72-1:0] dconv_weight_din_1;
    wire [48-1:0] pconv_weight_din_1;
    wire [432-1:0] dconv_weight_din_2;
    wire [288-1:0] pconv_weight_din_2;
    wire [432-1:0] dconv_weight_din_3;
    wire [288-1:0] pconv_weight_din_3;
    wire [432-1:0] dconv_weight_din_4;
    wire [480-1:0] pconv_weight_din_4;
    wire [32-1:0] dconv_bias_din_1;
    wire [192-1:0] pconv_bias_din_1;
    wire [192-1:0] dconv_bias_din_2;
    wire [192-1:0] pconv_bias_din_2;
    wire [192-1:0] dconv_bias_din_3;
    wire [192-1:0] pconv_bias_din_3;
    wire [192-1:0] dconv_bias_din_4;
    wire [320-1:0] pconv_bias_din_4;
    wire [8-1:0] dconv_shift_din_1;
    wire [32-1:0] pconv_shift_din_1;
    wire [32-1:0] dconv_shift_din_2;
    wire [32-1:0] pconv_shift_din_2;
    wire [32-1:0] dconv_shift_din_3;
    wire [32-1:0] pconv_shift_din_3;
    wire [32-1:0] dconv_shift_din_4;
    wire [56-1:0] pconv_shift_din_4;
    wire weight_load_done;
    
    weight u_weight (
        .clk(clk),
        .rst_n(rst_n),
        .dconv_weight_din_1(dconv_weight_din_1),
        .pconv_weight_din_1(pconv_weight_din_1),
        .dconv_weight_din_2(dconv_weight_din_2),
        .pconv_weight_din_2(pconv_weight_din_2),
        .dconv_weight_din_3(dconv_weight_din_3),
        .pconv_weight_din_3(pconv_weight_din_3),
        .dconv_weight_din_4(dconv_weight_din_4),
        .pconv_weight_din_4(pconv_weight_din_4),
        .dconv_bias_din_1(dconv_bias_din_1),
        .pconv_bias_din_1(pconv_bias_din_1),
        .dconv_bias_din_2(dconv_bias_din_2),
        .pconv_bias_din_2(pconv_bias_din_2),
        .dconv_bias_din_3(dconv_bias_din_3),
        .pconv_bias_din_3(pconv_bias_din_3),
        .dconv_bias_din_4(dconv_bias_din_4),
        .pconv_bias_din_4(pconv_bias_din_4),
        .dconv_shift_din_1(dconv_shift_din_1),
        .pconv_shift_din_1(pconv_shift_din_1),
        .dconv_shift_din_2(dconv_shift_din_2),
        .pconv_shift_din_2(pconv_shift_din_2),
        .dconv_shift_din_3(dconv_shift_din_3),
        .pconv_shift_din_3(pconv_shift_din_3),
        .dconv_shift_din_4(dconv_shift_din_4),
        .pconv_shift_din_4(pconv_shift_din_4),
        .done(weight_load_done)
    );

    wire [OUTPUT_CHANNEL_1*N-1:0] conv_dout_1;
    wire conv_dout_vld_1;
    wire conv_dout_end_1;
    dwconv #(.N(N), .INPUT_CHANNEL(INPUT_CHANNEL_1), .INPUT_SIZE(INPUT_SIZE_1), .OUTPUT_CHANNEL(OUTPUT_CHANNEL_1), .OUTPUT_SIZE(OUTPUT_SIZE_1), .KERNEL_SIZE(KERNEL_SIZE_1), .STRIDE(STRIDE_1), .PADDING(PADDING_1), .DILATION(DILATION)) dut_dwconv1 (
        .clk(clk),
        .rst_n(rst_n),
        .ce(ce),
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
        .clk(clk),
        .rst_n(rst_n),
        .ce(ce),
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
        .clk(clk),
        .rst_n(rst_n),
        .ce(ce),
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
    dwconv #(.N(N), .INPUT_CHANNEL(INPUT_CHANNEL_4), .INPUT_SIZE(INPUT_SIZE_4), .OUTPUT_CHANNEL(OUTPUT_CHANNEL_4), .OUTPUT_SIZE(OUTPUT_SIZE_4), .KERNEL_SIZE(KERNEL_SIZE_4), .STRIDE(STRIDE_4), .PADDING(PADDING_4), .DILATION(DILATION)) dut_dwconv4 (
        .clk(clk),
        .rst_n(rst_n),
        .ce(ce),
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


    assign conv_dout = conv_dout_4;
    assign conv_dout_vld = conv_dout_vld_4;
    assign conv_dout_end = conv_dout_end_4;

    // // Dump waves
    // initial begin
    //     $dumpfile("mnist.vcd");
    //     $dumpvars(1, mnist);
    // end

endmodule