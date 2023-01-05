
/*
 * 介绍: 用于branch数据的存储的双端口RAM
 * 
 * parameter:
 *     RAM_WIDTH: 数据宽度
 *     RAM_DEPTH: 数据深度
 *     ADDR_WIDTH: 地址线位宽
 */

module bram #(
    parameter RAM_WIDTH = 8,
    parameter RAM_DEPTH = 16,
    parameter ADDR_WIDTH = 4
    )(
    input wire clk,
    input wire wr_en,
    input wire rd_en,
    input wire [ADDR_WIDTH-1:0]wr_addr,
    input wire [RAM_WIDTH-1:0]wr_data,
    input wire [ADDR_WIDTH-1:0]rd_addr,
    output reg [RAM_WIDTH-1:0]rd_data
);
    reg [RAM_WIDTH-1:0] memory[RAM_DEPTH-1:0]; 

    //写
    always@(posedge clk) begin
        if(wr_en) begin
            memory[wr_addr] <= wr_data;
        end else begin
            memory[wr_addr] <= memory[wr_addr];
        end
    end

    //读
    always@(posedge clk) begin
        if(rd_en) begin
            rd_data <= memory[rd_addr];
        end else begin
            rd_data <= rd_data;
        end
    end

    // Dump waves
    initial begin
        $dumpfile("bram.vcd");
        $dumpvars(1, bram);
    end

endmodule

