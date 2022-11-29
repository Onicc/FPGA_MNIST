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
    reg din_flag;

    always@(posedge clk) begin
        if(rst_n == 1'b0) begin
            din_flag <= 1'b0;
        end else begin
            if(din == 1'b0) begin   // 如果按键按下
                din_flag <= 1'b1;
            end else begin
                din_flag <= 1'b0;
            end
        end
    end

    // 输出正确时开始计数
    always@(posedge clk) begin
        if(rst_n == 1'b0) begin
            cnt <= 32'hffffffff;
        end else begin
            if(din_flag == 1'b1) begin
                cnt <= 32'd0;
            end else if(cnt < FREQUENCY) begin
                cnt <= cnt + 1'b1;
            end else begin
                cnt <= cnt;
            end
        end
    end

    // 计数期间亮灯，计数完后灭灯
    always@(posedge clk) begin
        if(rst_n == 1'b0) begin
            dout_led <= 1'b1;
        end else begin
            if(cnt < FREQUENCY) begin
                dout_led <= 1'b0;
            end else begin
                dout_led <= 1'b1;
            end
        end
    end

    // 按下按键后的1000个时钟后发送开始信号
    always@(posedge clk) begin
        if(rst_n == 1'b0) begin
            dout_start <= 1'b0;
        end else begin
            if(cnt == 1000) begin
                dout_start <= 1'b1;
            end else begin
                dout_start <= 1'b0;
            end
        end
    end

endmodule