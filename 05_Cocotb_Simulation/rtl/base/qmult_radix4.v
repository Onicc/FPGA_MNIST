module qmult_radix4#(
    parameter N = 8
    )(
    input wire clk,
    input wire rst_n,
    input wire input_vld,
    input wire [N-1:0] multiplicand_din,
    input wire [N-1:0] multiplier_din,
    output reg [N*2-1:0] product_dout,
    output reg product_dout_vld,
    output reg product_end
);

    // reg [1:0] product_state;
    reg [2*N-1:0] multiplicand_temp;        // 需要左移动，因此需要大一点
    reg [2*N-1:0] inv_multiplicand_temp;    // 需要左移动，因此需要大一点
    reg [2*N-1:0] multiplicand_temp_x2;     // 需要左移动，因此需要大一点
    reg [2*N-1:0] inv_multiplicand_temp_x2; // 需要左移动，因此需要大一点
    reg [N:0] multiplier_temp;
    reg [2*N-1:0] product_working;
    reg [5:0] multiplier_cnt;    // 最长为64位=2^6
    wire [2:0] booth_code; 
    wire product_stop;

    assign booth_code = multiplier_temp[2:0];
    assign product_stop = (~|multiplier_temp)||(&multiplier_temp);

    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            // product_state <= 1'b0;
            multiplicand_temp <= 0;
            inv_multiplicand_temp <= 0;
            multiplier_temp <= 0;
            product_working <= 0;
            multiplier_cnt <= 0;

            product_dout <= 0;
            product_dout_vld <= 1'b0;
            product_end <= 1'b1;
        end else if(product_end && input_vld) begin
            product_dout_vld <= 1'b0;
            product_end <= 1'b0;

            multiplicand_temp <= {{N{multiplicand_din[N-1]}}, multiplicand_din}; 
            multiplicand_temp_x2 <= {{(N-1){multiplicand_din[N-1]}}, multiplicand_din, 1'b0};
            inv_multiplicand_temp <= ~{{N{multiplicand_din[N-1]}}, multiplicand_din} + 1'b1;
            inv_multiplicand_temp_x2 <= ~{{(N-1){multiplicand_din[N-1]}}, multiplicand_din, 1'b0} + 1'b1;
            multiplier_temp <= {multiplier_din, 1'b0};
            product_working <= 0;
            multiplier_cnt <= 0;
        end else if(!product_end) begin
            if(~product_stop) begin 
                case(booth_code)
                    3'b001 : product_working <= product_working + multiplicand_temp;    // +A
                    3'b010 : product_working <= product_working + multiplicand_temp;    // +A
                    3'b011 : product_working <= product_working + multiplicand_temp_x2;     // +2A
                    3'b100 : product_working <= product_working + inv_multiplicand_temp_x2; // -2A
                    3'b101 : product_working <= product_working + inv_multiplicand_temp;    // -A
                    3'b110 : product_working <= product_working + inv_multiplicand_temp;    // -A
                   default: product_working <= product_working;
               endcase 
               multiplicand_temp <= {multiplicand_temp[N*2-3:0],2'b00};          // 左移2位补0
               multiplicand_temp_x2 <= {multiplicand_temp[N*2-4:0],3'b000};
               inv_multiplicand_temp <= {inv_multiplicand_temp[N*2-3:0],2'b00}; // 左移2位补0
               inv_multiplicand_temp_x2 <= {inv_multiplicand_temp[N*2-4:0],3'b000};;
               multiplier_temp <= {{2{multiplier_temp[N]}}, multiplier_temp[N:2]};   // 右移2位补符号位
            end
            multiplier_cnt <= multiplier_cnt + 1;
            if(multiplier_cnt == 4)  begin
                product_end <= 1'b1;
                product_dout_vld <= 1'b1;
                product_dout <= product_working;
            end
        end else if (product_dout_vld) begin
            product_dout_vld <= 1'b0;
        end
    end

    // Dump waves
    initial begin
        $dumpfile("qmult_radix4.vcd");
        $dumpvars(1, qmult_radix4);
    end

endmodule