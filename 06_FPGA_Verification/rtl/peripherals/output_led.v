// 当输出与设定值吻合时灯亮1s
module output_led #(
    parameter OUTPUT = 80'h271D7E0C000000001300,
    parameter FREQUENCY = 50000000
    )(
    input wire clk,
    input wire rst_n,
    input wire [79:0] din,

    output reg dout
);
    reg [31:0] cnt;

    always@(posedge clk) begin
        if(rst_n == 1'b0) begin
            dout <= 1'b1;
        end else begin
            if(din == OUTPUT) begin
                dout <= 1'b0;
            end else if(cnt >= FREQUENCY) begin
                dout <= 1'b1;
            end else begin
                dout <= dout;
            end
        end
    end

    always@(posedge clk) begin
        if(rst_n == 1'b0) begin
            cnt <= 32'd0;
        end else begin
            if(dout == 1'b1) begin
                cnt <= cnt + 1'b1;
            end else begin
                cnt <= 32'd0;
            end
        end
    end

endmodule