/*
 https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html#torch.nn.Conv2d

 parameter:
    N: data bit width.
    Q: fraction bit width.
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

 module conv_unit#(
    parameter N = 8,
    parameter INPUT_SIZE = 6,
    parameter KERNEL_SIZE = 3,
    parameter STRIDE = 1,
    parameter PADDING = 0,
    parameter DILATION = 1
    )(
    input wire clk,
    input wire rst_n,
    input wire ce,
    input wire input_vld,
    input wire [N-1:0] input_din,
    input wire [(KERNEL_SIZE*KERNEL_SIZE)*N-1:0] weight_din,
    input wire [31:0] bias_din,
    input wire [4:0] shift_din,
    output wire [N-1:0] conv_dout,
    output wire conv_dout_vld,
    output reg conv_dout_end
);

    wire [31:0] tmp [KERNEL_SIZE*KERNEL_SIZE+1:0];
    wire tmp_vld [KERNEL_SIZE*KERNEL_SIZE+1:0];
    wire [N-1:0] weight_mat [0:KERNEL_SIZE*KERNEL_SIZE-1];
    wire [31:0] conv_output;
    wire conv_output_vld;
    wire [31:0] conv_dout_temp;

    // cnt1计第三行第三个(第kernelsize个)位置开始计数，从1开始，计到行底停止输出等待下s(步长)行的第三个再继续输出
    // cnt2计行从1开始
    reg [31:0] cnt1, cnt2, in_cnt;

    assign tmp[0] = 1'b0;
    assign tmp_vld[0] = input_vld;
    assign conv_dout_temp = conv_dout_vld? (conv_output+bias_din)>>shift_din:0;
    assign conv_dout = (conv_dout_temp[31-shift_din]==1)? 0:conv_dout_temp[N-1:0];    // RELU，由于FPGA右移动自动补0，因此高位也跟着一起移动。RELU操作
    assign conv_dout_vld = ( (cnt1-1)%STRIDE==0 && (cnt1%INPUT_SIZE)>0 && (cnt1%INPUT_SIZE)<=(INPUT_SIZE-KERNEL_SIZE+1) && (cnt2-1)%STRIDE==0 )? conv_output_vld:1'b0;

    generate
        genvar l;
        for(l = 0;l < KERNEL_SIZE*KERNEL_SIZE;l = l+1) begin
            assign weight_mat[KERNEL_SIZE*KERNEL_SIZE-1-l][N-1:0] = weight_din[N*l +: N]; 		
        end
    endgenerate


    generate
        genvar i;
        for(i = 0; i < KERNEL_SIZE*KERNEL_SIZE; i = i+1) begin: MAC
            if((i+1)%KERNEL_SIZE == 0) begin
                if(i==KERNEL_SIZE*KERNEL_SIZE-1) begin
                    mac_unit #(.N(N)) mac1(
                        .clk(clk),
                        .rst_n(rst_n),
                        .ce(ce),
                        .multiplicand_vld(input_vld),
                        .addend_vld(tmp_vld[i]),
                        .multiplicand_din(input_din),
                        .multiplier_din(weight_mat[i]),
                        .addend_din(tmp[i]),
                        .mac_dout(conv_output),
                        .mac_dout_vld(conv_output_vld)
                    );
                end else begin
                    wire [31:0] tmp2;
                    wire tmp2_vld;
                    mac_unit #(.N(N)) mac2(                    
                        .clk(clk), 
                        .rst_n(rst_n),
                        .ce(ce),
                        .multiplicand_vld(input_vld),
                        .addend_vld(tmp_vld[i]),
                        .multiplicand_din(input_din),
                        .multiplier_din(weight_mat[i]),
                        .addend_din(tmp[i]),
                        .mac_dout(tmp2),
                        .mac_dout_vld(tmp2_vld)
                    );

                    variable_shift_reg #(.width(32),.depth((INPUT_SIZE-KERNEL_SIZE))) SR (
                        .clk(clk),
                        .rst(rst_n),
                        .ce(ce),
                        .input_vld(tmp2_vld),
                        .din(tmp2),
                        .dout(tmp[i+1]),
                        .dout_vld(tmp_vld[i+1])
                    );
                end
            end else begin
                mac_unit #(.N(N)) mac3(                    
                    .clk(clk), 
                    .rst_n(rst_n),
                    .ce(ce),
                    .multiplicand_vld(input_vld),
                    .addend_vld(tmp_vld[i]),
                    .multiplicand_din(input_din),
                    .multiplier_din(weight_mat[i]),
                    .addend_din(tmp[i]),
                    .mac_dout(tmp[i+1]),
                    .mac_dout_vld(tmp_vld[i+1])
                );
            end 
        end
    endgenerate

    always @(posedge input_vld) begin
        if(rst_n == 1'b0) begin
            in_cnt <= 0;
        end else begin
            in_cnt <= in_cnt + 1;
            if(conv_dout_end == 1'b1) begin
                in_cnt <= 0;
            end
        end
    end

    always @(posedge conv_output_vld or negedge rst_n or posedge conv_dout_end) begin
        if(rst_n == 1'b0) begin
            cnt1 <= 0;
            cnt2 <= 0;
        end else begin
            if(in_cnt > (INPUT_SIZE*2 + 1)) begin
                cnt1 <= cnt1 + 1'b1;
                if(cnt1%INPUT_SIZE == 0) begin
                    cnt2 <= cnt2 + 1'b1;
                end
            end

            if(conv_dout_end == 1'b1) begin
                cnt1 <= 0;
                cnt2 <= 0;
            end
        end
    end

    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            conv_dout_end <= 1'b1;
        end else begin
            if(cnt1 > (INPUT_SIZE*(INPUT_SIZE-KERNEL_SIZE+1)-KERNEL_SIZE)) begin
                conv_dout_end <= 1'b1;
            end else begin
                if(input_vld == 1'b1 && conv_dout_end == 1'b1) begin
                    conv_dout_end <= 1'b0;
                end
            end
        end
    end

    // // Dump waves
    // initial begin
    //     $dumpfile("conv_unit.vcd");
    //     $dumpvars(1, conv_unit);
    // end

endmodule