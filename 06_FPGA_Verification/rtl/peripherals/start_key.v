// 当输出与设定值吻合时灯亮1s
module start_key #(
    parameter FREQUENCY = 50000000
    )(
    input wire clk,
    input wire rst_n,
    input wire din,
    output reg dout_led,
    output reg dout_start
);
    reg [31:0] cnt;

    // 点亮LED并在1s后关闭LED
    always@(posedge clk) begin
        if(rst_n == 1'b0) begin
            dout_led <= 1'b1;   // 低电平点亮LED
        end else begin
            if(din == 1'b0) begin   // 如果按键按下
                dout_led <= 1'b0;   // 点亮LED
            end else if(cnt >= FREQUENCY) begin
                dout_led <= 1'b1;   // 1s后关闭LED
            end else begin
                dout_led <= dout_led;
            end
        end
    end

    // 当LED亮起后计数器开始计数
    always@(posedge clk) begin
        if(rst_n == 1'b0) begin
            cnt <= 32'd0;
        end else begin
            if(dout_led == 1'b0) begin
                cnt <= cnt + 1'b1;
            end else begin
                cnt <= 32'd0;
            end
        end
    end

    // 当计数开始后dout_start信号拉高一个周期
    always@(posedge clk) begin
        if(rst_n == 1'b0) begin
            dout_start <= 1'b0;
        end else begin
            if(cnt == 32'd1) begin
                dout_start <= 1'b1;
            end else begin
                dout_start <= 1'b0;
            end
        end
    end

endmodule