/*
 kernel=1 stride=1时的深度可分离卷积
 */

 module conv_unit_k1#(
    parameter N = 8,
    parameter INPUT_SIZE = 6,
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
    output wire conv_dout_vld,
    output reg conv_dout_end
);

    wire [2*N-1:0] product_dout;
    wire product_dout_vld;
    wire product_end;

    wire [31:0] conv_dout_temp_1;   // 取有效信号的卷积输出数据,输出数据有效时结果有效
    wire [31:0] conv_dout_temp_2;   // 最大值限幅, 当输出数据大于127时为127，否则为conv_dout_temp_1
    wire [31:0] conv_dout_temp_1_diff;// 卷积输出数据减最大值的差值

    reg [$clog2(INPUT_SIZE*INPUT_SIZE+1):0] cnt;

    assign conv_dout_temp_1 = product_dout_vld? ({{(32+1-2*N){product_dout[2*N-1]}}, product_dout[2*N-2:0]}+bias_din)>>shift_din:0;
    assign conv_dout_temp_1_diff = conv_dout_temp_1 - MAX;
    assign conv_dout_temp_2 = (conv_dout_temp_1_diff[31-shift_din]==0)? MAX:conv_dout_temp_1;
    assign conv_dout = (conv_dout_temp_2[31-shift_din]==1)? 0:conv_dout_temp_2[N-1:0];    // RELU，由于FPGA右移动自动补0，因此高位也跟着一起移动。RELU操作
    assign conv_dout_vld = product_dout_vld;

    qmult #(.N(N)) u_mult(
        .clk(clk),
        .rst_n(rst_n),
        .input_vld(input_vld),
        .multiplicand_din(input_din),
        .multiplier_din(weight_din),
        .product_dout(product_dout),
        .product_dout_vld(product_dout_vld),
        .product_end(product_end)
    );

    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            cnt <= 0;
            conv_dout_end <= 1'b1;
        end else begin
            if(product_dout_vld == 1'b1) begin
                cnt <= cnt + 1'b1;
                conv_dout_end <= 1'b0;
            end else if(cnt > (INPUT_SIZE*INPUT_SIZE-1)) begin
                cnt <= 0;
                conv_dout_end <= 1'b1;
            end else begin
                cnt <= cnt;
                conv_dout_end <= conv_dout_end;
            end
        end
    end

    // Dump waves
    initial begin
        $dumpfile("conv_unit_k1.vcd");
        $dumpvars(1, conv_unit_k1);
    end

endmodule