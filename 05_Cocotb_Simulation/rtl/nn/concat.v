// 1. 由于串形结构导致分支数据到来时与layer数据只隔几个周期，并且中间不回跳跃数据，因此可不用RAM
// 2. 更具有效信号获取需要合并的数据和读取数据
// 3. 合并数据
// 结构
//     |
//   layer ---
//     |      | branch
//   concat --
//     |

module concat#(
    parameter N = 8,
    parameter INPUT_CHANNEL = 1,
    parameter INPUT_SIZE = 1
    )(
    input wire clk,
    input wire rst_n,

    // 主干输入，用于存入RAM
    input wire layer_vld,
    input wire [INPUT_CHANNEL*N-1:0] layer_din,

    // 分支输入，当输入有效时从RAM取数据进行合并
    input wire branch_vld,
    input wire [INPUT_CHANNEL*N-1:0] branch_din,

    // concat输出及有效位
    output reg concat_dout_vld,
    output reg [INPUT_CHANNEL*N*2-1:0] concat_dout
);
    // concat
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            concat_dout <= 0;
        end else begin
            if(layer_vld == 1'b1) begin
                concat_dout <= {{INPUT_CHANNEL*N{1'b0}}, layer_din};
            end else if(branch_vld == 1'b1) begin
                concat_dout <= {concat_dout | {branch_din, {INPUT_CHANNEL*N{1'b0}}}};
            end else begin
                concat_dout <= concat_dout;
            end
        end
    end

    // 输出有效位
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            concat_dout_vld <= 1'b0;
        end else begin
            if(branch_vld == 1'b1) begin
                concat_dout_vld <= 1'b1;
            end else begin
                concat_dout_vld <= 1'b0;
            end
        end
    end

    // Dump waves
    initial begin
        $dumpfile("concat.vcd");
        $dumpvars(1, concat);
    end

endmodule