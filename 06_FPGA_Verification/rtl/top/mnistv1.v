
module mnistv1(
    input wire clk,
    input wire rst_n,
    input wire key_0,     // 开始计算按键

    output wire uart_txd,   //UART发送端口
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

    wire rst_sync;

    // 异步复位，同步释放
    sync_rst u_sync_rst(
        .clk(clk),
        .rst_n(rst_n),
        
        .rst_sync(rst_sync)
    );

    img u_img(
        .clk(clk),
        .rst_n(rst_sync),
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
        .rst_n(rst_sync),
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
        .rst_n(rst_sync),
        .din(conv_dout),
        .dout(led_0)
    );

    start_key u_start_key(
        .clk(clk),
        .rst_n(rst_sync),
        .din(key_0),
        .dout_led(led_1),
        .dout_start(start_flag)
    );

    output_send u_output_send(
        .clk(clk),
        .rst_n(rst_sync),
        .model_ouput(conv_dout),

        .uart_txd(uart_txd)
    );

    // ila_0 u_ila_0 (
    //     .clk(clk), // input wire clk


    //     .probe0(u_mnist.dut_dwconv1.input_vld), // input wire [0:0]  probe0  
    //     .probe1(u_mnist.dut_dwconv1.input_din), // input wire [7:0]  probe1 
    //     .probe2(u_mnist.dut_dwconv1.padding_dout_vld), // input wire [0:0]  probe2 
    //     .probe3(u_mnist.dut_dwconv1.padding_dout), // input wire [7:0]  probe3 
    //     .probe4(u_mnist.dut_dwconv1.dconv_dout_vld), // input wire [0:0]  probe4 
    //     .probe5(u_mnist.dut_dwconv1.dconv_dout), // input wire [7:0]  probe5 
    //     .probe6(u_mnist.dut_dwconv1.pconv_dout_vld), // input wire [0:0]  probe6 
    //     .probe7(u_mnist.dut_dwconv1.pconv_dout) // input wire [47:0]  probe7
    // );

    ila_1 u_ila_1 (
        .clk(clk), // input wire clk


        .probe0(u_mnist.dut_dwconv2.input_vld), // input wire [0:0]  probe0  
        .probe1(u_mnist.dut_dwconv2.input_din), // input wire [47:0]  probe1 
        .probe2(u_mnist.dut_dwconv2.padding_dout_vld), // input wire [0:0]  probe2 
        .probe3(u_mnist.dut_dwconv2.padding_dout), // input wire [47:0]  probe3 
        .probe4(u_mnist.dut_dwconv2.dconv_dout_vld), // input wire [0:0]  probe4 
        .probe5(u_mnist.dut_dwconv2.dconv_dout) // input wire [47:0]  probe5
    );

    // ila_1 u_ila_1 (
    //     .clk(clk), // input wire clk


    //     .probe0(u_mnist.dut_dwconv3.input_vld), // input wire [0:0]  probe0  
    //     .probe1(u_mnist.dut_dwconv3.input_din), // input wire [47:0]  probe1 
    //     .probe2(u_mnist.dut_dwconv3.padding_dout_vld), // input wire [0:0]  probe2 
    //     .probe3(u_mnist.dut_dwconv3.padding_dout), // input wire [47:0]  probe3 
    //     .probe4(u_mnist.dut_dwconv3.dconv_dout_vld), // input wire [0:0]  probe4 
    //     .probe5(u_mnist.dut_dwconv3.dconv_dout) // input wire [47:0]  probe5
    // );

    // ila_param_3 u_ila_param_3 (
    //     .clk(clk), // input wire clk


    //     .probe0(u_mnist.dconv_weight_din_3), // input wire [431:0]  probe0  
    //     .probe1(u_mnist.dconv_bias_din_3), // input wire [191:0]  probe1 
    //     .probe2(u_mnist.dconv_shift_din_3) // input wire [29:0]  probe2
    // );

endmodule