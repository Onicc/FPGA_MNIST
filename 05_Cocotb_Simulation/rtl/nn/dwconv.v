
module dwconv#(
    parameter N = 16,
    parameter INPUT_CHANNEL = 3,
    parameter INPUT_SIZE = 6,
    parameter OUTPUT_CHANNEL = 3,
    parameter OUTPUT_SIZE = 6,
    parameter KERNEL_SIZE = 3,
    parameter STRIDE = 1,
    parameter PADDING = 0,
    parameter DILATION = 1
    )(
    input wire clk,
    input wire rst_n,
    input wire input_vld,
    input wire [INPUT_CHANNEL*N-1:0] input_din,
    input wire [INPUT_CHANNEL*(KERNEL_SIZE*KERNEL_SIZE)*N-1:0] dconv_weight_din,
    input wire [INPUT_CHANNEL*OUTPUT_CHANNEL*N-1:0] pconv_weight_din,
    input wire [INPUT_CHANNEL*32-1:0] dconv_bias_din,
    input wire [OUTPUT_CHANNEL*32-1:0] pconv_bias_din,
    input wire [INPUT_CHANNEL*5-1:0] dconv_shift_din,
    input wire [OUTPUT_CHANNEL*5-1:0] pconv_shift_din,
    output wire [OUTPUT_CHANNEL*N-1:0] conv_dout,
    output wire conv_dout_vld,
    output wire conv_dout_end
);

    wire [INPUT_CHANNEL*N-1:0] padding_dout;
    wire [INPUT_CHANNEL*N-1:0] padding_temp;
    wire padding_dout_vld;
    wire padding_dout_end;

    // 让他在修正的时候改变 不修正的时候保留原始值
    // assign padding_temp = (padding_dout_vld == 1'b1)? padding_dout:padding_temp;

    padding #(.N(N), .CHANNEL(INPUT_CHANNEL), .SIZE(INPUT_SIZE), .PADDING(PADDING)) dut_padding(
        .clk(clk),
        .rst_n(rst_n),
        .input_vld(input_vld),
        .input_din(input_din),
        .padding_dout(padding_dout),
        .padding_dout_vld(padding_dout_vld),
        .padding_dout_end(padding_dout_end)
    );


    wire [INPUT_CHANNEL*N-1:0] dconv_dout;
    wire dconv_dout_vld;
    wire dconv_dout_end;
    dconv #(.N(N), .INPUT_CHANNEL(INPUT_CHANNEL), .INPUT_SIZE(INPUT_SIZE+2*PADDING), .KERNEL_SIZE(KERNEL_SIZE), .STRIDE(STRIDE), .PADDING(PADDING), .DILATION(DILATION)) dut_dconv(
        .clk(clk),
        .rst_n(rst_n),
        .input_vld(padding_dout_vld),
        .input_din(padding_dout),
        .weight_din(dconv_weight_din),
        .bias_din(dconv_bias_din),
        .shift_din(dconv_shift_din),
        .conv_dout(dconv_dout),
        .conv_dout_vld(dconv_dout_vld),
        .conv_dout_end(dconv_dout_end)
    );

    wire [OUTPUT_CHANNEL*N-1:0] pconv_dout;
    wire pconv_dout_vld;
    wire pconv_dout_end;

    pconv #(.N(N), .INPUT_CHANNEL(INPUT_CHANNEL), .INPUT_SIZE(OUTPUT_SIZE), .OUTPUT_CHANNEL(OUTPUT_CHANNEL)) dut_pwconv(
        .clk(clk),
        .rst_n(rst_n),
        .input_vld(dconv_dout_vld),
        .input_din(dconv_dout),
        .weight_din(pconv_weight_din),
        .bias_din(pconv_bias_din),
        .shift_din(pconv_shift_din),
        .conv_dout(pconv_dout),
        .conv_dout_vld(pconv_dout_vld),
        .conv_dout_end(pconv_dout_end)
    );

    assign conv_dout = pconv_dout;
    assign conv_dout_vld = pconv_dout_vld;
    assign conv_dout_end = pconv_dout_end;

    // Dump waves
    initial begin
        $dumpfile("dwconv.vcd");
        $dumpvars(1, dwconv);
    end

endmodule