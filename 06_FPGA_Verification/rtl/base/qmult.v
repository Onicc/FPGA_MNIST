module qmult#(
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
    reg [2*N-1:0] multiplicand_temp;    // 需要左移动，因此需要大一点
    reg [2*N-1:0] inv_multiplicand_temp;    // 需要左移动，因此需要大一点
    reg [N:0] multiplier_temp;
    reg [2*N-1:0] product_working;
    reg [5:0] multiplier_cnt;    // 最长为64位=2^6
    wire [1:0] booth_code; 
    wire product_stop;

    assign booth_code = multiplier_temp[1:0];
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
            inv_multiplicand_temp <= ~{{N{multiplicand_din[N-1]}}, multiplicand_din} + 1'b1;
            multiplier_temp <= {multiplier_din, 1'b0};
            product_working <= 0;
            multiplier_cnt <= 0;
        end else if(!product_end) begin
            if(~product_stop) begin 
                case(booth_code)
                   2'b01 : product_working <= product_working + multiplicand_temp;
                   2'b10 : product_working <= product_working + inv_multiplicand_temp;
                   default: product_working <= product_working;
               endcase 
               multiplicand_temp <= {multiplicand_temp[N*2-2:0],1'b0};          // 左移补0
               inv_multiplicand_temp <=  {inv_multiplicand_temp[N*2-2:0],1'b0}; // 左移补0
               multiplier_temp <= {multiplier_temp[N], multiplier_temp[N:1]};   // 右移补符号位
            end
            multiplier_cnt <= multiplier_cnt + 1;
            if(multiplier_cnt == N)  begin
                product_end <= 1'b1;
                product_dout_vld <= 1'b1;
                product_dout <= product_working;
            end
        end else if (product_dout_vld) begin
            product_dout_vld <= 1'b0;
        end
    end

    // // Dump waves
    // initial begin
    //     $dumpfile("qmult.vcd");
    //     $dumpvars(1, qmult);
    // end

endmodule