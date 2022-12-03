
module variable_shift_reg #(
    parameter width = 8, 
    parameter depth = 3
    )(
    input wire clk,
    input wire rst,
    input wire ce,
    input wire input_vld,
    input wire [width-1:0] din,
    output wire [width-1:0] dout,
    output wire dout_vld
);
    reg [width*(depth+1)-1:0] sr;   // 比2022.10.28日前版本多了一位，因为在questa仿真的时候sr进来时钟要快一些
    reg [32:0] cnt;

    assign dout_vld = (cnt > depth)? input_vld:0;
    assign dout = (dout_vld)? sr[width-1:0]:dout;

    always@(posedge input_vld) begin
        // sr <= sr >> width;
        // sr[(width*(depth+1)-1):width*depth] <= din;
        sr <= {din, sr[width*(depth+1)-1:width]};
    end

    always@(posedge input_vld or negedge rst) begin
        if(rst == 1'b0) begin
            cnt <= 0;
        end else begin
            if(input_vld == 1'b1 && cnt <= depth) begin
                cnt <= cnt + 1'b1;
            end
        end
    end

    // Dump waves
    initial begin
        $dumpfile("variable_shift_reg.vcd");
        $dumpvars(1, variable_shift_reg);
    end

endmodule