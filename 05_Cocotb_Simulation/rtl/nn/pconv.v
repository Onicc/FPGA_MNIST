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

 module pconv#(
    parameter N = 16,
    parameter INPUT_CHANNEL = 3,
    parameter INPUT_SIZE = 6,
    parameter OUTPUT_CHANNEL = 32
    )(
    input wire clk,
    input wire rst_n,
    input wire ce,
    input wire input_vld,
    input wire [INPUT_CHANNEL*N-1:0] input_din,
    input wire [INPUT_CHANNEL*OUTPUT_CHANNEL*N-1:0] weight_din,
    input wire [OUTPUT_CHANNEL*32-1:0] bias_din,
    input wire [OUTPUT_CHANNEL*5-1:0] shift_din,
    output wire [OUTPUT_CHANNEL*N-1:0] conv_dout,
    output wire conv_dout_vld,
    output reg conv_dout_end
);
    // conv_dout[0][i] = input_din[i]*weight_din[0][i]
    wire [OUTPUT_CHANNEL-1:0] pwconv_dout_vld;
    reg [31:0] cnt;

    assign conv_dout_vld = (pwconv_dout_vld == {OUTPUT_CHANNEL{1'b1}})? 1'b1:1'b0;

    generate
        genvar i;
        for(i = 0; i < OUTPUT_CHANNEL; i = i+1) begin: PWCONVCELL
            pconv_unit #(.N(N), .INPUT_CHANNEL(INPUT_CHANNEL)) u_pconv_unit(
                .clk(clk),
                .rst_n(rst_n),
                .ce(ce),
                .input_vld(input_vld),
                .input_din(input_din),
                .bias_din(bias_din[(i+1)*32-1:i*32]),
                .shift_din(shift_din[(i+1)*5-1:i*5]),
                .weight_din(weight_din[(i+1)*INPUT_CHANNEL*N-1:i*INPUT_CHANNEL*N]),
                .conv_dout(conv_dout[(i+1)*N-1:i*N]),
                .conv_dout_vld(pwconv_dout_vld[i])
            );
        end
    endgenerate

    always @(posedge clk) begin
        if(rst_n == 1'b0 || ce == 1'b0) begin
            conv_dout_end <= 1'b1;
            cnt <= 1'b0;
        end else if(ce == 1'b1) begin
            if(input_vld == 1'b1) begin
                conv_dout_end <= 1'b0;
            end
            if(conv_dout_vld == 1'd1) begin
                cnt <= cnt + 1;
            end
            if(cnt >= INPUT_SIZE*INPUT_SIZE) begin
                cnt <= 1'b0;
                conv_dout_end <= 1'b1;
            end
        end
    end

    // // Dump waves
    // initial begin
    //     $dumpfile("pconv.vcd");
    //     $dumpvars(1, pconv);
    // end

endmodule