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

 module dconv_k1#(
    parameter N = 8,
    parameter INPUT_CHANNEL = 3,
    parameter INPUT_SIZE = 6
    )(
    input wire clk,
    input wire rst_n,
    input wire input_vld,
    input wire [INPUT_CHANNEL*N-1:0] input_din,
    input wire [INPUT_CHANNEL*N-1:0] weight_din,
    input wire [INPUT_CHANNEL*32-1:0] bias_din,
    input wire [INPUT_CHANNEL*5-1:0] shift_din,
    output wire [INPUT_CHANNEL*N-1:0] conv_dout,
    output wire conv_dout_vld,
    output wire conv_dout_end
);

    wire [INPUT_CHANNEL-1:0] conv_cell_dout_vld;
    wire [INPUT_CHANNEL-1:0] conv_cell_dout_end;

    assign conv_dout_vld = (conv_cell_dout_vld == {INPUT_CHANNEL{1'b1}})? 1'b1:1'b0;
    assign conv_dout_end = (conv_cell_dout_end == {INPUT_CHANNEL{1'b1}})? 1'b1:1'b0;

    generate
        genvar i;
        for(i = 0; i < INPUT_CHANNEL; i = i+1) begin
            conv_unit_k1 #(.N(N), .INPUT_SIZE(INPUT_SIZE)) dut_conv_unit_k1(
                .clk(clk), 
                .rst_n(rst_n),
                .input_vld(input_vld),
                .input_din(input_din[N*(i+1)-1:N*i]), 
                .weight_din(weight_din[N*(i+1)-1:N*i]), 
                .bias_din(bias_din[32*(i+1)-1:32*i]),
                .shift_din(shift_din[5*(i+1)-1:5*i]),
                .conv_dout(conv_dout[N*(i+1)-1:N*i]), 
                .conv_dout_vld(conv_cell_dout_vld[i]),
                .conv_dout_end(conv_cell_dout_end[i])
            );
        end
    endgenerate

    // Dump waves
    initial begin
        $dumpfile("dconv_k1.vcd");
        $dumpvars(1, dconv_k1);
    end

endmodule