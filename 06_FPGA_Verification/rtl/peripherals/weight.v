
module weight # (
    parameter TOTAL_BYTES = 715
    )(
    input wire clk,
    input wire rst_n,

    output reg [72-1:0] dconv_weight_din_1,
    output reg [48-1:0] pconv_weight_din_1,
    output reg [432-1:0] dconv_weight_din_2,
    output reg [288-1:0] pconv_weight_din_2,
    output reg [432-1:0] dconv_weight_din_3,
    output reg [288-1:0] pconv_weight_din_3,
    output reg [432-1:0] dconv_weight_din_4,
    output reg [480-1:0] pconv_weight_din_4,
    output reg [32-1:0] dconv_bias_din_1,
    output reg [192-1:0] pconv_bias_din_1,
    output reg [192-1:0] dconv_bias_din_2,
    output reg [192-1:0] pconv_bias_din_2,
    output reg [192-1:0] dconv_bias_din_3,
    output reg [192-1:0] pconv_bias_din_3,
    output reg [192-1:0] dconv_bias_din_4,
    output reg [320-1:0] pconv_bias_din_4,
    output reg [8-1:0] dconv_shift_din_1,
    output reg [32-1:0] pconv_shift_din_1,
    output reg [32-1:0] dconv_shift_din_2,
    output reg [32-1:0] pconv_shift_din_2,
    output reg [32-1:0] dconv_shift_din_3,
    output reg [32-1:0] pconv_shift_din_3,
    output reg [32-1:0] dconv_shift_din_4,
    output reg [56-1:0] pconv_shift_din_4,

    output reg done
);
    // kegai
    reg [9:0] rom_addr;
    wire [7:0] rom_douta;

    weight_rom u_weight_rom (
        .clka(clk),         // input wire clka
        .ena(1'b1),         // input wire ena
        .addra(rom_addr),   // input wire [9 : 0] addra
        .douta(rom_douta)   // output wire [7 : 0] douta
    );

    // addr
    always @ (posedge clk) begin
        if(!rst_n) begin
            rom_addr <= 0;
        end else begin
            if(rom_addr < TOTAL_BYTES) begin
                rom_addr <= rom_addr + 1'b1;
            end else begin
                rom_addr <= rom_addr;
            end
        end
    end

    // done信号
    always @ (posedge clk) begin
        if(!rst_n) begin
            done <= 1'b0;
        end else begin
            if(rom_addr < TOTAL_BYTES) begin
                done <= 1'b0;
            end else begin
                done <= 1'b1;
            end
        end
    end

    // ROM的latency为2个clk，将rom_addr延时同步rom_douta
    reg [9:0] rom_addr_d0;
    reg [9:0] rom_addr_d1;
    always @ (posedge clk) begin
        if(!rst_n) begin
            rom_addr_d0 <= 0;
            rom_addr_d1 <= 0;
        end else begin
            rom_addr_d0 <= rom_addr;
            rom_addr_d1 <= rom_addr_d0;
        end
    end

    // auto genaration
    always @ (posedge clk) begin
        if (!rst_n) begin
            dconv_weight_din_1 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd0 && rom_addr_d1 < 10'd9) begin
                dconv_weight_din_1[(rom_addr_d1-10'd0)*8 +: 8] <= rom_douta;
            end else begin
                dconv_weight_din_1 <= dconv_weight_din_1;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            pconv_weight_din_1 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd9 && rom_addr_d1 < 10'd15) begin
                pconv_weight_din_1[(rom_addr_d1-10'd9)*8 +: 8] <= rom_douta;
            end else begin
                pconv_weight_din_1 <= pconv_weight_din_1;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            dconv_weight_din_2 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd15 && rom_addr_d1 < 10'd69) begin
                dconv_weight_din_2[(rom_addr_d1-10'd15)*8 +: 8] <= rom_douta;
            end else begin
                dconv_weight_din_2 <= dconv_weight_din_2;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            pconv_weight_din_2 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd69 && rom_addr_d1 < 10'd105) begin
                pconv_weight_din_2[(rom_addr_d1-10'd69)*8 +: 8] <= rom_douta;
            end else begin
                pconv_weight_din_2 <= pconv_weight_din_2;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            dconv_weight_din_3 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd105 && rom_addr_d1 < 10'd159) begin
                dconv_weight_din_3[(rom_addr_d1-10'd105)*8 +: 8] <= rom_douta;
            end else begin
                dconv_weight_din_3 <= dconv_weight_din_3;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            pconv_weight_din_3 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd159 && rom_addr_d1 < 10'd195) begin
                pconv_weight_din_3[(rom_addr_d1-10'd159)*8 +: 8] <= rom_douta;
            end else begin
                pconv_weight_din_3 <= pconv_weight_din_3;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            dconv_weight_din_4 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd195 && rom_addr_d1 < 10'd249) begin
                dconv_weight_din_4[(rom_addr_d1-10'd195)*8 +: 8] <= rom_douta;
            end else begin
                dconv_weight_din_4 <= dconv_weight_din_4;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            pconv_weight_din_4 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd249 && rom_addr_d1 < 10'd309) begin
                pconv_weight_din_4[(rom_addr_d1-10'd249)*8 +: 8] <= rom_douta;
            end else begin
                pconv_weight_din_4 <= pconv_weight_din_4;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            dconv_bias_din_1 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd309 && rom_addr_d1 < 10'd313) begin
                dconv_bias_din_1[(rom_addr_d1-10'd309)*8 +: 8] <= rom_douta;
            end else begin
                dconv_bias_din_1 <= dconv_bias_din_1;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            pconv_bias_din_1 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd313 && rom_addr_d1 < 10'd337) begin
                pconv_bias_din_1[(rom_addr_d1-10'd313)*8 +: 8] <= rom_douta;
            end else begin
                pconv_bias_din_1 <= pconv_bias_din_1;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            dconv_bias_din_2 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd337 && rom_addr_d1 < 10'd361) begin
                dconv_bias_din_2[(rom_addr_d1-10'd337)*8 +: 8] <= rom_douta;
            end else begin
                dconv_bias_din_2 <= dconv_bias_din_2;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            pconv_bias_din_2 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd361 && rom_addr_d1 < 10'd385) begin
                pconv_bias_din_2[(rom_addr_d1-10'd361)*8 +: 8] <= rom_douta;
            end else begin
                pconv_bias_din_2 <= pconv_bias_din_2;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            dconv_bias_din_3 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd385 && rom_addr_d1 < 10'd409) begin
                dconv_bias_din_3[(rom_addr_d1-10'd385)*8 +: 8] <= rom_douta;
            end else begin
                dconv_bias_din_3 <= dconv_bias_din_3;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            pconv_bias_din_3 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd409 && rom_addr_d1 < 10'd433) begin
                pconv_bias_din_3[(rom_addr_d1-10'd409)*8 +: 8] <= rom_douta;
            end else begin
                pconv_bias_din_3 <= pconv_bias_din_3;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            dconv_bias_din_4 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd433 && rom_addr_d1 < 10'd457) begin
                dconv_bias_din_4[(rom_addr_d1-10'd433)*8 +: 8] <= rom_douta;
            end else begin
                dconv_bias_din_4 <= dconv_bias_din_4;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            pconv_bias_din_4 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd457 && rom_addr_d1 < 10'd497) begin
                pconv_bias_din_4[(rom_addr_d1-10'd457)*8 +: 8] <= rom_douta;
            end else begin
                pconv_bias_din_4 <= pconv_bias_din_4;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            dconv_shift_din_1 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd497 && rom_addr_d1 < 10'd498) begin
                dconv_shift_din_1[(rom_addr_d1-10'd497)*8 +: 8] <= rom_douta;
            end else begin
                dconv_shift_din_1 <= dconv_shift_din_1;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            pconv_shift_din_1 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd498 && rom_addr_d1 < 10'd502) begin
                pconv_shift_din_1[(rom_addr_d1-10'd498)*8 +: 8] <= rom_douta;
            end else begin
                pconv_shift_din_1 <= pconv_shift_din_1;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            dconv_shift_din_2 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd502 && rom_addr_d1 < 10'd506) begin
                dconv_shift_din_2[(rom_addr_d1-10'd502)*8 +: 8] <= rom_douta;
            end else begin
                dconv_shift_din_2 <= dconv_shift_din_2;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            pconv_shift_din_2 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd506 && rom_addr_d1 < 10'd510) begin
                pconv_shift_din_2[(rom_addr_d1-10'd506)*8 +: 8] <= rom_douta;
            end else begin
                pconv_shift_din_2 <= pconv_shift_din_2;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            dconv_shift_din_3 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd510 && rom_addr_d1 < 10'd514) begin
                dconv_shift_din_3[(rom_addr_d1-10'd510)*8 +: 8] <= rom_douta;
            end else begin
                dconv_shift_din_3 <= dconv_shift_din_3;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            pconv_shift_din_3 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd514 && rom_addr_d1 < 10'd518) begin
                pconv_shift_din_3[(rom_addr_d1-10'd514)*8 +: 8] <= rom_douta;
            end else begin
                pconv_shift_din_3 <= pconv_shift_din_3;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            dconv_shift_din_4 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd518 && rom_addr_d1 < 10'd522) begin
                dconv_shift_din_4[(rom_addr_d1-10'd518)*8 +: 8] <= rom_douta;
            end else begin
                dconv_shift_din_4 <= dconv_shift_din_4;
            end
        end
    end
    always @ (posedge clk) begin
        if (!rst_n) begin
            pconv_shift_din_4 <= 0;
        end else begin
            if(rom_addr_d1 >= 10'd522 && rom_addr_d1 < 10'd529) begin
                pconv_shift_din_4[(rom_addr_d1-10'd522)*8 +: 8] <= rom_douta;
            end else begin
                pconv_shift_din_4 <= pconv_shift_din_4;
            end
        end
    end


endmodule
