
module mnistv1(
    input wire clk,
    input wire rst_n,
    input wire key_0,     // 开始计算按键

    output wire led_0,  // 输出结果验证LED，显示1s
    output wire led_1   // 按键输入显示LED，显示1s
);

    // wire clk;
    // IBUFGDS clkgen(
    //     .O(clk),
    //     .I(clk_p),
    //     .IB(clk_n)
    // );

    // No Used
    wire start_flag;
    wire input_vld;
    wire [7:0] input_din;

    img u_img(
        .clk(clk),
        .rst_n(rst_n),
        .start(start_flag),
        // .start(key_0),

        .img_dout(input_din),
        .dout_vld(input_vld)
    );

    // No Used
    wire [79:0] conv_dout;
    wire conv_dout_vld;
    wire conv_dout_end;

    mnist u_mnist(
        .clk(clk),
        .rst_n(rst_n),
        .ce(1'b1),
        .input_vld(input_vld),
        .input_din(input_din),
        .conv_dout(conv_dout),
        .conv_dout_vld(conv_dout_vld),
        .conv_dout_end(conv_dout_end)
    );

    // assign led_0 = conv_dout[0];
    // 输出验证显示模块
    output_led u_output_led(
        .clk(clk),
        .rst_n(rst_n),
        .din(conv_dout),
        .dout(led_0)
    );

    start_key u_start_key(
        .clk(clk),
        .rst_n(rst_n),
        .din(key_0),
        .dout_led(led_1),
        .dout_start(start_flag)
    );

endmodule