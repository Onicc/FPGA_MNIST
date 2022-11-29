module output_send(
    input wire clk,
    input wire rst_n,
    input wire [79:0] model_ouput,

    output wire uart_txd
);

    //parameter define
    parameter  CLK_FREQ = 50000000;         //定义系统时钟频率
    parameter  UART_BPS = 115200;           //定义串口波特率

    // 模型输出暂存
    reg [79:0] model_ouput_temp;
    reg model_ouput_vld;

    // uart
    reg uart_send_en;
    reg [7:0] uart_send_data;
    wire uart_send_busy;

    //串口发送模块    
    uart_send #(                          
        .CLK_FREQ       (CLK_FREQ),     //设置系统时钟频率
        .UART_BPS       (UART_BPS)      //设置串口发送波特率
    ) u_uart_send (                 
        .sys_clk        (clk),
        .sys_rst_n      (rst_n),
        
        .uart_en        (uart_send_en),
        .uart_din       (uart_send_data),
        .uart_tx_busy   (uart_send_busy),
        .uart_txd       (uart_txd)
    );

    // 锁存model_ouput
    always@(posedge clk) begin
        if(rst_n == 1'b0) begin
            model_ouput_temp <= 80'd0;
        end else begin
            if(model_ouput != 80'd0) begin
                model_ouput_temp <= model_ouput;
            end else begin
                model_ouput_temp <= model_ouput_temp;
            end
        end
    end

    // 模型结果输出有效位
    always@(posedge clk) begin
        if(rst_n == 1'b0) begin
            model_ouput_vld <= 1'b0;
        end else begin
            if(model_ouput != 80'd0) begin
                model_ouput_vld <= 1'b1;
            end else begin
                model_ouput_vld <= 1'b0;
            end
        end
    end

    reg uart_send_busy_d0;
    reg uart_send_busy_d1;
    wire uart_busy_negedge;
    assign uart_busy_negedge = ~uart_send_busy_d0&uart_send_busy_d1;
    always @(posedge clk) begin         
        if (!rst_n) begin
            uart_send_busy_d0 <= 1'b0;
            uart_send_busy_d1 <= 1'b0;
        end else begin                                               
            uart_send_busy_d0 <= uart_send_busy;                               
            uart_send_busy_d1 <= uart_send_busy_d0;                            
        end
    end

    reg [3:0] cnt;
    always @(posedge clk) begin         
        if (!rst_n) begin
            cnt <= 4'b1111;
            uart_send_en <= 1'b0;
            uart_send_data <= 8'd0;
        end else begin            
            if(model_ouput_vld) begin
                cnt <= 4'd1;
            end else if(cnt <= 10) begin
                if(uart_busy_negedge || cnt == 4'd1) begin
                    cnt <= cnt + 1'b1;
                    uart_send_en <= 1'b1;
                    uart_send_data <= model_ouput_temp[(cnt*8-1) -: 8];
                end else begin
                    cnt <= cnt;
                    uart_send_en <= 1'b0;
                end
            end else begin
                cnt <= cnt;
                uart_send_en <= 1'b0;
            end
        end
    end

endmodule