module img # (
    parameter TOTAL_BYTES = 28*28,
    parameter CLK_INTERVAL = 12 // 13(真正的周期) - 1
    )(
    input wire clk,
    input wire rst_n,
    input wire start,

    output reg [8-1:0] img_dout,
    output reg dout_vld
);
    reg working;
    // reg rom_done;
    reg [9:0] rom_addr;
    wire [7:0] rom_dout;

    img_rom u_img_rom (
        .clka(clk),    // input wire clka
        .ena(1'b1),      // input wire ena
        .addra(rom_addr),  // input wire [9 : 0] addra
        .douta(rom_dout)   // output wire [7 : 0] douta
    );

    // start信号检测
    always @ (posedge clk) begin
        if(!rst_n) begin
            working <= 1'b0;
        end else if(start == 1'b1) begin
            working <= 1'b1;
        end else if(rom_addr == TOTAL_BYTES)  begin
            working <= 1'b0;
        end else begin
            working <= working;
        end
    end

    // 计数9轮
    reg [3:0] cnt;
    always @ (posedge clk) begin
        if(!rst_n) begin
            cnt <= 0;
        end else begin
            if(cnt < CLK_INTERVAL && working == 1'b1) begin
                cnt <= cnt + 1'b1;
            end else begin
                cnt <= 1'b0;
            end
        end
    end

    // addr
    always @ (posedge clk) begin
        if(!rst_n) begin
            rom_addr <= 0;
        end else begin
            if(rom_addr < TOTAL_BYTES && working == 1'b1 && cnt == CLK_INTERVAL) begin
                rom_addr <= rom_addr + 1'b1;
            end else if(rom_addr == TOTAL_BYTES) begin
                rom_addr <= 0;
            end else begin
                rom_addr <= rom_addr;
            end
        end
    end

    // // done信号
    // always @ (posedge clk) begin
    //     if(!rst_n) begin
    //         rom_done <= 1'b0;
    //     end else begin
    //         if(rom_addr < TOTAL_BYTES) begin
    //             rom_done <= 1'b0;
    //         end else begin
    //             rom_done <= 1'b1;
    //         end
    //     end
    // end

    // val信号
    always @ (posedge clk) begin
        if(!rst_n) begin
            dout_vld <= 0;
        end else begin
            if(cnt == 4'd2) begin
                dout_vld <= 1'b1;
            end else begin
                dout_vld <= 1'b0;
            end
        end
    end

    // shuchu1
    always @ (posedge clk) begin
        if(!rst_n) begin
            img_dout <= 0;
        end else begin
            if(cnt == 4'd2) begin
                img_dout <= rom_dout;
            end else begin
                img_dout <= img_dout;
            end
        end
    end

endmodule