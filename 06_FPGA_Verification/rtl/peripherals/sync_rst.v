module sync_rst(
    input wire clk,
    input wire rst_n,

    output reg rst_sync
);
    reg rst_s0;

    always@(posedge clk or negedge rst_n) begin
        if(!rst_n)begin
            rst_s0 <= 1'b0;
        end else begin
            rst_s0 <= 1'b1;
        end
    end

    always@(posedge clk or negedge rst_n) begin
        if(!rst_n)begin
            rst_sync <= 1'b0;
        end else begin
            rst_sync <= rst_s0;
        end
    end

endmodule