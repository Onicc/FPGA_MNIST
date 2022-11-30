

module img_rom_send(
    input wire clk,
    input wire rst_n,
    input wire start,
    output wire uart_txd
);
    parameter SUM_BYTES = 784;

    /* Start UART *****************************************************/
    //parameter define
    parameter  CLK_FREQ = 50000000;         //定义系统时钟频率
    parameter  UART_BPS = 115200;           //定义串口波特率

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
    /* End UART *****************************************************/

    /* Start Image ROM **********************************************/
    reg [9:0] rom_addr;
    wire [7:0] rom_rdata;

    img_rom u_img_rom (
        .clka(clk),    // input wire clka
        .ena(1'b1),      // input wire ena
        .addra(rom_addr),  // input wire [9 : 0] addra
        .douta(rom_rdata)   // output wire [7 : 0] douta
    );
    /* End Image ROM ************************************************/

    // start_flag为开始信号，直到发送完成后才拉低
    reg start_flag;
    always @(posedge clk) begin 
        if (!rst_n) begin 
            start_flag <= 1'b0;
        end else if(start) begin
            start_flag <= 1'b1;
        end else if(rom_addr == SUM_BYTES) begin
            start_flag <= 1'b0;
        end else begin
            start_flag <= start_flag;
        end
    end

    // 串口BUSY信号检测
    reg uart_start_send;
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


    always @(posedge clk) begin 
        if (!rst_n) begin
            uart_send_en <= 1'b0;
            uart_send_data <= 8'd0;
            uart_start_send <= 1'b0;

            rom_addr <= 10'd0;
        end else begin
            if(start_flag) begin
                if(uart_busy_negedge || ~uart_start_send) begin
                    uart_start_send <= 1'b1;
                    uart_send_en <= 1'b1;
                    rom_addr <= rom_addr + 1'b1;
                end else begin
                    uart_send_en <= 1'b0;
                    uart_send_data <= rom_rdata;
                end
            end else begin
                uart_send_en <= 1'b0;
                uart_send_data <= 8'd0;
                uart_start_send <= 1'b0;
                rom_addr <= 10'd0;
            end
        end
    end

endmodule
