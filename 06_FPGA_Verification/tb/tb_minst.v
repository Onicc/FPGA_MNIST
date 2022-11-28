`timescale 1ns / 1ps

module tb_minst();

    //输入
    reg sys_clk;
    reg sys_rst_n;
    reg key_0;
    wire led_0;
    wire led_1;

    //信号初始化
    initial begin
        sys_clk = 1'b0;
        sys_rst_n = 1'b0;
        key_0 = 1'b1;
        #20
        sys_rst_n = 1'b1;

        #100000
        key_0 = 1'b0;
        #20
        key_0 = 1'b1;
    end

    //生成时钟
    always #10 sys_clk = ~sys_clk;

    mnistv1 u_mnistv1(
        .clk(sys_clk),
        .rst_n(sys_rst_n),
        .key_0(key_0),
        .led_0(led_0),
        .led_1(led_1)
    );

endmodule
