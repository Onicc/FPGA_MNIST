// 当输出与设定值吻合时灯亮1s
module output_led #(
    parameter MODEL_OUTPUT = 80'h1D471500200000B00037,
    parameter COUNT = 75000
    )(
    input wire clk,
    input wire rst_n,
    input wire [79:0] din,

    output reg dout
);
    reg [31:0] cnt;
    reg output_flag;

    // 检测输出是否匹配，若匹配output_flag拉高一个周期
    always@(posedge clk) begin
        if(rst_n == 1'b0) begin
            output_flag <= 1'b0;
        end else begin
            if(din == MODEL_OUTPUT) begin
                output_flag <= 1'b1;
            end else begin
                output_flag <= 1'b0;
            end
        end
    end

    // 输出正确时开始计数
    always@(posedge clk) begin
        if(rst_n == 1'b0) begin
            cnt <= 32'hffffffff;
        end else begin
            if(output_flag == 1'b1) begin
                cnt <= 32'd0;
            end else if(cnt < COUNT) begin
                cnt <= cnt + 1'b1;
            end else begin
                cnt <= cnt;
            end
        end
    end

    // 计数期间亮灯，计数完后灭灯
    always@(posedge clk) begin
        if(rst_n == 1'b0) begin
            dout <= 1'b1;
        end else begin
            if(cnt < COUNT) begin
                dout <= 1'b0;
            end else begin
                dout <= 1'b1;
            end
        end
    end

endmodule