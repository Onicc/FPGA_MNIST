
module variable_shift_reg #(
    parameter width = 8, 
    parameter depth = 3
    )(
    input wire clk,
    input wire rst,
    input wire input_vld,
    input wire [width-1:0] din,
    output reg [width-1:0] dout,
    output reg dout_vld
);
    reg [width*(depth+1)-1:0] sr;   // /rtl/base/variable_shift_reg.v(25): (vopt-3373) Range of part-select [-1:32] into 'sr' [31:0] is reversed.
    reg [32:0] cnt;

    // assign dout_vld = (cnt > depth)? input_vld:0;
    // assign dout = (dout_vld)? sr[width-1:0]:dout;

    always@(posedge clk) begin
        if(rst == 1'b0) begin
            sr <= 0;
        end else begin
            if(input_vld == 1'b1) begin
                sr <= {din, sr[width*(depth+1)-1:width]};
            end else begin
                sr <= sr;
            end
        end
    end

    always@(posedge clk) begin
        if(rst == 1'b0) begin
            cnt <= 0;
        end else begin
            if(input_vld == 1'b1 && cnt <= depth) begin
                cnt <= cnt + 1'b1;
            end else begin
                cnt <= cnt;
            end
        end
    end

    always@(posedge clk) begin
        if(rst == 1'b0) begin
            dout_vld <= 0;
        end else begin
            if(cnt >= depth && input_vld == 1'b1) begin
                dout_vld <= 1'b1;
            end else begin
                dout_vld <= 1'b0;
            end
        end
    end

    always@(posedge clk) begin
        if(rst == 1'b0) begin
            dout <= 0;
        end else begin
            if(cnt >= depth && input_vld == 1'b1) begin
                dout <= sr[width*2-1:width];
            end else begin
                dout <= dout;
            end
        end
    end

    // // Dump waves
    // initial begin
    //     $dumpfile("variable_shift_reg.vcd");
    //     $dumpvars(1, variable_shift_reg);
    // end

endmodule